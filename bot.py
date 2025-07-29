import os import time import math import logging from dotenv import load_dotenv from pybit.unified_trading import HTTP from utils.indicators import get_signal from utils.telegram import send_telegram_message

load_dotenv()

logging.basicConfig(level=logging.INFO)

API_KEY = os.getenv("BYBIT_API_KEY") API_SECRET = os.getenv("BYBIT_API_SECRET") TELEGRAM = os.getenv("TELEGRAM") == "true"

session = HTTP( api_key=API_KEY, api_secret=API_SECRET, testnet=True )

SYMBOLS = ["SOLUSDT", "MOONDENGUSDT", "SPXUSDT"] RISK_PER_TRADE = 0.2  # 20% SL_PERCENT = 0.20  # 20%

open_positions = {}

def get_balance(): res = session.get_wallet_balance(accountType="UNIFIED") balance = float(res['result']['list'][0]['totalEquity']) return balance

def cancel_open_orders(symbol): session.cancel_all_orders(category="linear", symbol=symbol)

def close_existing_position(symbol): try: position = session.get_positions(category="linear", symbol=symbol)["result"]["list"][0] size = float(position["size"]) side = position["side"] if size > 0: session.place_order( category="linear", symbol=symbol, side="Buy" if side == "Sell" else "Sell", order_type="Market", qty=size, timeInForce="GTC" ) logging.info(f"Closed existing position on {symbol}") except Exception as e: logging.error(f"Error closing position for {symbol}: {e}")

def place_trade(symbol, side, confidence): balance = get_balance() allocation = balance * RISK_PER_TRADE price_info = session.get_ticker(category="linear", symbol=symbol)["result"][0] last_price = float(price_info["lastPrice"])

qty = allocation / last_price
qty = round(qty, 3)
if qty <= 0:
    logging.warning(f"Invalid qty calculated for {symbol}: {qty}")
    return

cancel_open_orders(symbol)
close_existing_position(symbol)

try:
    order = session.place_order(
        category="linear",
        symbol=symbol,
        side=side,
        order_type="Market",
        qty=qty,
        timeInForce="GTC"
    )
    logging.info(f"Placed {side} order on {symbol}, Qty: {qty}")
    open_positions[symbol] = side
    if TELEGRAM:
        send_telegram_message(f"🟢 {side} Entry: {symbol}\nQty: {qty}\nPrice: {last_price}")
except Exception as e:
    logging.error(f"Trade failed for {symbol}: {e}")

def monitor(): while True: for symbol in SYMBOLS: try: signal = get_signal(symbol) if not signal: continue

side = "Buy" if signal == "long" else "Sell"

            if open_positions.get(symbol) == side:
                logging.info(f"Already in {side} position for {symbol}, skipping.")
                continue

            place_trade(symbol, side, confidence=True)

        except Exception as e:
            logging.error(f"Error monitoring {symbol}: {e}")
    time.sleep(30)  # Wait before re-checking

if name == "main": monitor()


