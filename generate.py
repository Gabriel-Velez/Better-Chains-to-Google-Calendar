import json

def authenticate_google():
    with open("token.json", "w") as f:
        f.write(os.environ["GOOGLE_TOKEN"])
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    service = build("calendar", "v3", credentials=creds)
    return service