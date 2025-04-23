from flask import jsonify
from datetime import datetime
from zoneinfo import ZoneInfo

start_time = "2025-04-23T12:53:00"
dt_object = datetime.fromisoformat(start_time)

polish_now = datetime.now(ZoneInfo("Europe/Warsaw"))
naive_polish_now = polish_now.replace(tzinfo=None)

if dt_object < naive_polish_now:
    print({"error": "Cannot book a time in the past."}), 400



