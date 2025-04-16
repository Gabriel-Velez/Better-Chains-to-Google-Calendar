import json
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

try:
    from config_private import *
except ImportError:
    from config_public import *

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google():
    if not GOOGLE_TOKEN:
        raise ValueError("❌ GOOGLE_TOKEN is missing from environment or config")

    # Write token to a temporary file
    with open("token.json", "w") as f:
        f.write(GOOGLE_TOKEN)
        print("✅ Token saved to token.json")

    # Load credentials and build service
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    service = build("calendar", "v3", credentials=creds)

    # Clean up token file
    os.remove("token.json")
    return service

def generate_token():
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)

    # Save and print token
    with open("token.json", "w") as token_file:
        token_file.write(creds.to_json())
    print("✅ Token saved to token.json")
    print("\n---- COPY BELOW FOR GITHUB SECRET ----")
    print(creds.to_json())
    print("---- END ----")

if __name__ == "__main__":
    generate_token()