import os
import json
import requests
from dotenv import load_dotenv
from app.tests.test_file_courts import courts_url, court_credentials_1

print(courts_url)
print(court_credentials_1)

load_dotenv()

headers = {"Content-Type": "application/json"}
admin_credentials = json.loads(os.getenv("admin_credentails"))

session = requests.session()

def call_court():    

    court_post_res = session.post(courts_url, json=court_credentials_1, headers=headers)