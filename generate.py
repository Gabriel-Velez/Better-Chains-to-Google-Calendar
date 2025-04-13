import json
import os

# import config
try:
    from config_private import *
except ImportError:
    from config_public import *

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def authenticate_google():
    print("🔑 GOOGLE_TOKEN loaded?", bool(GOOGLE_TOKEN))

    # Save token.json from the env variable
    with open("token.json", "w") as f:
        f.write(GOOGLE_TOKEN)
        print("✅ Token saved to token.json")

    # Load credentials from token.json
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    service = build("calendar", "v3", credentials=creds)

    # Clean up
    os.remove("token.json")

    return service

authenticate_google()