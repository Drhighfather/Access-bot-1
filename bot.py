import os
import time
import math
import logging
from dotenv import load_dotenv

from pybit.unified_trading import HTTP
from utils.indicators import get_signal
from utils.telegram import send_telegram_message

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
API_KEY = os.getenv("BYBIT_API_KEY")
API_SECRET = os.getenv("BYBIT_API_SECRET")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

SYMBOLS = os.getenv("SYMBOLS", "SOLUSDT,MOONDENGUSDT,SPXUSDT").split(",")
TIMEFRAMES = ["15", "30", "60"]  # minutes
RISK_PERCENT = float(os.getenv("RISK_PERCENT", 20)) / 100
STOP_LOSS_PERCENT = float(os.getenv("STOP_LOSS_PERCENT", 20)) / 100

# Initialize Bybit client
client = HTTP(
    api_key=API_KEY,
    api_secret=API_SECRET,
)

def calculate_position_size(balance, entry_price):
    risk_amount = balance * RISK_PERCENT
    sl_distance = entry_price * STOP_LOSS_PERCENT
    qty = risk_amount / sl_distance
    return round(qty, 2)

def get_account_balance():
    try:
        result = client.get_wallet_balance(accountType="UNIFIED")
        return float(result["result"]["list"][0]["totalEquity"])
    except Exception as e:
        logger.error(f"Balance error: {e}")
        return 0

def place_order(symbol, side, qty):
    try:
        response = client.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            orderType="Market",
            qty=qty,
            timeInForce="GoodTillCancel"
        )
        logger.info(f"{side} order placed: {response}")
        send_telegram_message(f"{side} order placed on {symbol}: {response}")
    except Exception as e:
        logger.error(f"Order error: {e}")
        send_telegram_message(f"Order error on {symbol}: {e}")

def run_bot():
    logger.info("Bot started.")
    send_telegram_message("🚀 Trading bot is now running!")

    while True:
        try:
            balance = get_account_balance()
            for symbol in SYMBOLS:
                signal = get_signal(symbol, TIMEFRAMES)

                if signal:
                    entry_price = client.get_ticker(category="linear", symbol=symbol)["result"][0]["lastPrice"]
                    entry_price = float(entry_price)
                    qty = calculate_position_size(balance, entry_price)

                    if signal == "buy":
                        place_order(symbol, "Buy", qty)
                    elif signal == "sell":
                        place_order(symbol, "Sell", qty)
                time.sleep(2)

            time.sleep(60)  # Main loop pause
        except Exception as e:
            logger.error(f"Bot error: {e}")
            send_telegram_message(f"⚠️ Bot error: {e}")
            time.sleep(60)
