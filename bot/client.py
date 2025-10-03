import requests
import time
import hmac
import hashlib
from urllib.parse import urlencode
from bot.config import TESTNET_BASE, ORDER_ENDPOINT, SERVER_TIME_ENDPOINT, RECV_WINDOW
from bot.logger import logger


def now_ms():
    return int(time.time() * 1000)


class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

    def _sign(self, params: dict) -> str:
        query_string = urlencode(params, doseq=True)
        return hmac.new(self.api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

    def get_server_time(self):
        url = TESTNET_BASE + SERVER_TIME_ENDPOINT
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            return resp.json().get("serverTime", now_ms())
        except Exception as e:
            logger.warning("Falling back to local time: %s", e)
            return now_ms()

    def place_order(self, params: dict):
        url = TESTNET_BASE + ORDER_ENDPOINT
        params = dict(params)
        params.setdefault("recvWindow", RECV_WINDOW)
        params.setdefault("timestamp", self.get_server_time())
        params["signature"] = self._sign(params)

        headers = {"X-MBX-APIKEY": self.api_key}

        try:
            logger.info("Placing order: %s", params)
            resp = requests.post(url, headers=headers, data=params, timeout=15)
            resp.raise_for_status()
            result = resp.json()
            logger.info("Order successful: %s", result)
            return result
        except requests.exceptions.HTTPError as http_err:
            try:
                return {"error": resp.json()}
            except Exception:
                return {"error": str(http_err)}
        except Exception as e:
            logger.error("Error placing order: %s", e)
            return {"error": str(e)}

