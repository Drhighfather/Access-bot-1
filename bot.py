
import os
import time
import logging
import requests
import datetime
import math
import csv
from pybit.unified_trading import HTTP
from dotenv import load_dotenv

load_dotenv()

# === CONFIGURATION ===
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
TESTNET = True
SYMBOLS = [
    "MOODENGUSDT", "SPXUSDT", "SOLUSDT", "DOGEUSDT", "XRPUSDT", "ADAUSDT",
    "AVAXUSDT", "MATICUSDT", "DOTUSDT", "LTCUSDT", "LINKUSDT", "ATOMUSDT",
    "NEARUSDT", "FILUSDT", "SUIUSDT", "RNDRUSDT", "INJUSDT", "GRTUSDT",
    "AAVEUSDT",
]
RISK_PERCENT = 0.5
STOP_LOSS_PERCENT = 0.2
TAKE_PROFIT_PERCENT = 0.4
TRADE_TIMEOUT_MINUTES = 60
TRAILING_SETTINGS = {
    "MOODENGUSDT": {"trigger": 0.02, "lock": 0.01},
    "SPXUSDT": {"trigger": 0.025, "lock": 0.012},
    "SOLUSDT": {"trigger": 0.015, "lock": 0.008},
}
USE_LIMIT_ORDER = True
LIMIT_OFFSET = 0.001
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
MAX_OPEN_TRADES = 2

TP_SL_SETTINGS = {
    "MOODENGUSDT": {"tp": 0.5, "sl": 0.2},
    "SPXUSDT": {"tp": 0.6, "sl": 0.25},
    "SOLUSDT": {"tp": 0.45, "sl": 0.18},
}

MIN_QTY = {
    "XRPUSDT": 20,
    "DOGEUSDT": 100,
    "FILUSDT": 1,
    "SOLUSDT": 0.1,
    "SPXUSDT": 0.1,
    "MOODENGUSDT": 10,
    "ADAUSDT": 20
}

QTY_STEP = {
    "DOTUSDT": 1,
    "XRPUSDT": 1,
    "SOLUSDT": 0.1,
    "MOODENGUSDT": 1,
    "SPXUSDT": 0.1,
    "ADAUSDT": 1,
    "FILUSDT": 1,
    "DOGEUSDT": 1,
    "MATICUSDT": 1,
    "AVAXUSDT": 1,
    "LTCUSDT": 1,
    "ATOMUSDT": 1,
    "NEARUSDT": 1,
    "SUIUSDT": 1,
    "RNDRUSDT": 1,
    "INJUSDT": 1,
    "GRTUSDT": 1,
    "AAVEUSDT": 1,
}

# truncated for brevity...
