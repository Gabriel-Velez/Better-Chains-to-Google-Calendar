from google_auth_oauthlib.flow import InstalledAppFlow
import json

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main():
    # Start the OAuth flow using your credentials.json
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)

    # Save token to token.json
    with open("token.json", "w") as token_file:
        token_file.write(creds.to_json())
        print("✅ Token saved to token.json")

    # Also print to console so you can copy it for GitHub Secrets
    print("\n--- COPY BELOW FOR GITHUB SECRET ---\n")
    print(creds.to_json())
    print("\n--- END ---")

if __name__ == "__main__":
    main()