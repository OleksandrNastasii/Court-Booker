import os
from dotenv import load_dotenv

#Loads data from .env
load_dotenv()

#Retrieves Secret Key from .env
class Secret_Key():
    SECRET_KEY = os.getenv("SECRET_KEY") or "fallback-key"
