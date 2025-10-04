# ⚙️ config.py — Madara Edition

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from telethon.sessions import StringSession

# Load .env
load_dotenv()

# Telegram credentials
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "madara_pm_security")

mongo_client = MongoClient(MONGO_URL)
db = mongo_client[MONGO_DB_NAME]

# Collections
APPROVED = db["approved_users"]
BLOCKED = db["blocked_users"]
