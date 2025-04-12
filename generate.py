import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google():
    creds_data = os.environ["GOOGLE_CREDENTIALS_JSON"]
    creds = Credentials.from_authorized_user_info(json.loads(creds_data), SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    print("✅ Successfully authenticated and built the Calendar service!")

authenticate_google()