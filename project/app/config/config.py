import os
from dotenv import load_dotenv

load_dotenv()

class DB_route():
    DATABASE_URI = os.getenv("DATABASE_URI")

class Secret_Key():
    SECRET_KEY = os.getenv("SECRET_KEY") or "fallback-key"
