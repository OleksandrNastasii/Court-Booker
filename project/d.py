from datetime import datetime
from zoneinfo import ZoneInfo

polish_tz = ZoneInfo("Europe/Warsaw")
x = datetime.now(polish_tz)

print(x)