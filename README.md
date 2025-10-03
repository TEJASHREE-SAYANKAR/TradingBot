# TradingBot
Building Trading bot using Binance RestApi

# Simplified Binance Futures Trading Bot (Testnet)

This project implements a simple trading bot for the **Binance Futures Testnet (USDT-M)**.
It can place **MARKET**, **LIMIT**, and **STOP-LIMIT** orders via the official REST API.

---

## Features

* Binance Futures Testnet REST API integration
* Place BUY/SELL Market and Limit orders
* Basic Stop-Limit order type supported
* Command-line interface with input validation
* Logging (console + rotating file)
* Error handling with response logging
* Unit tests for validation logic

---

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/trading-bot.git
   cd trading-bot
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure API keys:

   * Register on [Binance Futures Testnet](https://testnet.binancefuture.com)
   * Generate API keys
   * Copy `.env.example` to `.env` and fill in your keys:

     ```bash
     BINANCE_API_KEY=your_api_key
     BINANCE_API_SECRET=your_api_secret
     ```

---

## Usage

### Market Order

```bash
python binance_futures_bot.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Limit Order

```bash
python binance_futures_bot.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 30000
```

### Stop-Limit Order

```bash
python binance_futures_bot.py --symbol BTCUSDT --side BUY --type STOP --quantity 0.001 --stop-price 29500 --price 29600
```

---

## Logs

* Logs are written to:

  * Console
  * `logs/binance_bot.log`

---

## Tests

Run basic tests:

```bash
pytest tests/
```

---

## Notes

* This bot works **only on Binance Futures Testnet**.
* Never use real funds with this script.
