# Simulated Trading Bot

This is a simple Python simulation of a stock trading bot that buys a target number of shares based on price constraints and market availability. It includes retry logic for failed orders and handles temporary market disconnections gracefully.

---

## Project Overview

The bot aims to buy **10,000 shares** at prices within **1% of a target price ($100)**. It simulates:

- A **fake market feed** that updates prices and available shares.
- A **buy order execution API** with an 85% success rate.
- Handling of **connection errors** (simulated 5% disconnect chance).
- **Retries on order failure** (up to 3 times per order).
- Real-time logging of each market tick and order attempt.

---

## How It Works

### 1. Market Feed Simulation

The `FakeMarketSocket` class provides:
- Randomized price between $98.5–$101.5
- Random available shares between 100–2000
- 5% chance of simulated disconnection

### 2. Buy Logic

- Accepts price updates every 1 second.
- Buys shares only if the price is between **$99.00 and $101.00**.
- Attempts to buy up to the available or remaining shares.
- If an order fails (15% chance), it retries up to 3 times.

### 3. Error Handling

- If the market feed "disconnects", the bot reconnects and resumes.
- Any unexpected errors are caught and logged.

---

## Example Output

```bash
[MARKET] Price: 100.84, Available Shares: 1845
Bought 1845 shares at $100.84
[STATUS] Remaining shares to buy: 8155
[MARKET] Price: 98.74, Available Shares: 1290
Price is outside the acceptable range. Skipping.
[ERROR] Market socket disconnected!
[INFO] Reconnecting to market feed...
[INFO] Reconnected successfully.
