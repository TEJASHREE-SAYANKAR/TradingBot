import os
import sys
import argparse
from dotenv import load_dotenv 
from bot.client import BinanceFuturesClient
from bot.utils import (
    validate_symbol,
    validate_side,
    validate_type,
    validate_positive_number,
)
from bot.logger import logger

# Load .env variables automatically
load_dotenv()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Simplified Binance Futures (USDT-M) Trading Bot (Testnet)"
    )
    parser.add_argument("--api-key", required=False, help="Binance API Key (or use BINANCE_API_KEY env/.env)")
    parser.add_argument("--api-secret", required=False, help="Binance API Secret (or use BINANCE_API_SECRET env/.env)")
    parser.add_argument("--symbol", required=True, help="Trading pair symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--type", required=True, help="Order type: MARKET | LIMIT | STOP")
    parser.add_argument("--quantity", required=True, help="Quantity (contract or base asset units)")
    parser.add_argument("--price", required=False, help="Price for LIMIT orders (and STOP optional)")
    parser.add_argument("--stop-price", required=False, help="Stop price for STOP (trigger price)")
    parser.add_argument(
        "--time-in-force",
        required=False,
        default="GTC",
        choices=["GTC", "IOC", "FOK"],
        help="Time in force for LIMIT orders",
    )
    parser.add_argument("--reduce-only", action="store_true", help="Set reduceOnly flag (futures)")
    return parser.parse_args()


def main():
    args = parse_args()

    # Resolve API keys (CLI > .env/.system environment)
    api_key = args.api_key or os.getenv("BINANCE_API_KEY")
    api_secret = args.api_secret or os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        logger.error("API key/secret required. Provide via --api-key/--api-secret or .env/env vars.")
        sys.exit(2)

    # Validate input
    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        ord_type = validate_type(args.type)
        quantity = validate_positive_number("quantity", args.quantity)

        params = {
            "symbol": symbol,
            "side": side,
            "type": ord_type,
            "quantity": str(quantity),
        }

        if ord_type == "LIMIT":
            if not args.price:
                raise ValueError("LIMIT orders require --price")
            params["price"] = str(validate_positive_number("price", args.price))
            params["timeInForce"] = args.time_in_force

        if ord_type == "STOP":
            if not args.stop_price:
                raise ValueError("STOP orders require --stop-price")
            params["stopPrice"] = str(validate_positive_number("stop-price", args.stop_price))
            if not args.price:
                raise ValueError("STOP orders also require --price")
            params["price"] = str(validate_positive_number("price", args.price))
            params["timeInForce"] = args.time_in_force

        if args.reduce_only:
            params["reduceOnly"] = "true"

    except Exception as e:
        logger.error("Input validation failed: %s", e)
        sys.exit(2)

    # Place order
    client = BinanceFuturesClient(api_key, api_secret)
    print("Placing order...", client)
    result = client.place_order(params)

    if "error" in result:
        print("ORDER FAILED:", result["error"])
        sys.exit(1)

    print("\n--- Order Result ---")
    for key in ("symbol", "orderId", "price", "origQty", "status", "type", "side"):
        if key in result:
            print(f"{key}: {result[key]}")
    print("--------------------\n")


if __name__ == "__main__":
    main()