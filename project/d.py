from werkzeug.security import generate_password_hash

print(generate_password_hash("qwerty12345", method='pbkdf2:sha256'))

import os
import reprlib
from sqlalchemy.engine.url import URL


def show_bytes(label, value):
    print(f"{label}: {value!r} | Bytes: {reprlib.repr(value.encode('utf-8'))}")

user = os.getenv("POSTGRESQL_USER", "").strip()
password = os.getenv("POSTGRESQL_PASSWORD", "").strip()
host = os.getenv("DATABASE_HOST", "").strip()
database = os.getenv("POSTGRESQL_DATABASE", "").strip()

show_bytes("User", user)
show_bytes("Password", password)
show_bytes("Host", host)
show_bytes("Database", database)

db_url = URL.create(
    drivername="postgresql",
    username=user,
    password=password,
    host=host,
    port=5432,
    database=database,
)

print(db_url)