import os
from dotenv import load_dotenv

load_dotenv()

class DB_route():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    DB_PATH = os.path.join(BASE_DIR, "data", "database.db")

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    SQLALCHEMY_DATABASE_URI = rf"sqlite:///{DB_PATH}"


class Secret_Key():
    SECRET_KEY = os.environ.get("SECRET_KEY") or "fallback-key"
