import os

def run_bot():
    print("Bot is starting...")
    api_key = os.getenv("BYBIT_API_KEY")
    api_secret = os.getenv("BYBIT_API_SECRET")
    print(f"Using API KEY: {api_key}")
    # Add your bot logic here
