import os

from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0"))
API_URL = os.getenv("API_URL", "http://127.0.0.1:5000/api/scores/typegg/daily")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN is missing from .env")

if not DISCORD_CHANNEL_ID:
    raise ValueError("DISCORD_CHANNEL_ID is missing from .env")
