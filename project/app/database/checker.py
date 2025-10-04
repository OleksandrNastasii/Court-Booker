# import os
# import requests
# import time
# from datetime import datetime, timezone
# from dotenv import load_dotenv

# from ..models.user_model import BookingModel

# load_dotenv()
# ip = os.getenv("my_ip")
# port = os.getenv("flask_port")

# def update_booking_status():
#     while True:
#         now = datetime.now(timezone.utc)
#         bookings = BookingModel.query.all()

#         for booking in bookings:
#             booking_id = booking.id
#             BASE_URL = f"http://{ip}:{port}/bookings/{booking_id}"


#             if booking.start_time < now < booking.end_time:
#                 requests.put(BASE_URL, json={"status": True})
#             else:
#                 requests.put(BASE_URL, json={"status": False})

#         time.sleep(60)

# update_booking_status()