import time
import random

TARGET_PRICE = 100
DELTA = 0.01 * TARGET_PRICE
MIN_PRICE = TARGET_PRICE - DELTA
MAX_PRICE = TARGET_PRICE + DELTA
TOTAL_SHARES_TO_BUY = 10000

class FakeMarketSocket:
    def __init__(self):
        self.connected = True

    def receive_price_update(self):
        if random.random() < 0.05:
            self.connected = False
            raise ConnectionError("Market socket disconnected!")

        time.sleep(1)

        # Generate a random price update
        current_price = round(random.uniform(98.5, 101.5), 2)
        available_shares = random.randint(100, 2000)

        return {"price": current_price, "shares": available_shares}

    def reconnect(self):
        print("[INFO] Reconnecting to market feed...")
        time.sleep(1)
        self.connected = True
        print("[INFO] Reconnected successfully.")

def place_buy_order(price, quantity, retries=3):
    attempt = 0
    while attempt < retries:
        attempt += 1
        if random.random() < 0.85:  # 85% chance of success
            print(f"Bought {quantity} shares at ${price:.2f}")
            return True
        else:
            print(f"Order failed at ${price:.2f}, retrying... ({attempt}/{retries})")
            time.sleep(1)
    print(f"Could not buy {quantity} shares at ${price:.2f} after {retries} retries.")
    return False

def is_price_within_range(price):
    return MIN_PRICE <= price <= MAX_PRICE

def run_trading_bot():
    market_feed = FakeMarketSocket()
    remaining_shares = TOTAL_SHARES_TO_BUY

    try:
        price_update = market_feed.receive_price_update()
        price = price_update["price"]
        shares_available = price_update["shares"]
        print(f"[MARKET] Price: {price}, Available Shares: {shares_available}")

        while remaining_shares > 0:
            while is_price_within_range(price) and remaining_shares > 0:
                # The minimum will handle the case for when shares_available > remaining_shares
                shares_to_buy = min(shares_available, remaining_shares)
                success = place_buy_order(price, shares_to_buy)
                if success:
                    remaining_shares -= shares_to_buy
                    print(f"[STATUS] Remaining shares to buy: {remaining_shares}")
                else:
                    print(f"[ERROR] Order at ${price} failed after retries.")

                # Get the next price
                if remaining_shares > 0:
                    price_update = market_feed.receive_price_update()
                    price = price_update["price"]
                    shares_available = price_update["shares"]
                    print(f"[MARKET] Price: {price}, Available Shares: {shares_available}")

            if remaining_shares > 0:
                print("Price went out of range. Waiting for next valid price...")
                while not is_price_within_range(price): # Exit this loop whenever a valid price is found
                    price_update = market_feed.receive_price_update()
                    price = price_update["price"]
                    shares_available = price_update["shares"]
                    print(f"[MARKET] Price: {price}, Available Shares: {shares_available}")

    except ConnectionError as err:
        print(f"[ERROR] {err}")
        market_feed.reconnect()

    except Exception as e:
        print(f"[UNEXPECTED ERROR] {e}")
        time.sleep(1)

    print("All shares successfully purchased!")

if __name__ == "__main__":
    run_trading_bot()
