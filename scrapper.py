import os
import json
from datetime import timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from config_public import *

# Read and parse the schedule HTML
with open("Better Chains - My Schedule.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

# Authenticate with Google
with open("token.json", "w") as f:
    f.write(GOOGLE_TOKEN)
creds = Credentials.from_authorized_user_file("token.json")
service = build("calendar", "v3", credentials=creds)
os.remove("token.json")

# Parse schedule from HTML (placeholder example logic)
parsed_schedule = []
for entry in soup.find_all("div", class_="shift"):
    title = entry.get("data-title", CALENDAR_SUMMARY)
    start = entry.get("data-start")
    end = entry.get("data-end")
    if not start or not end:
        continue
    parsed_schedule.append({
        "title": title,
        "start": start,
        "end": end,
        "color": SHIFT_EVENT_COLOR
    })

# Create travel events
full_schedule = []
for shift in parsed_schedule:
    start_time = shift["start"]
    end_time = shift["end"]

    full_schedule.append(shift)
    if ADD_TRAVEL_TIME:
        full_schedule.append({
            "title": TRAVEL_TIME_DEPARTURE_SUMMARY,
            "start": start_time - TRAVEL_TIME_DURATION,
            "end": start_time,
            "color": TRAVEL_EVENT_COLOR
        })
        full_schedule.append({
            "title": TRAVEL_TIME_ARIVAL_SUMMARY,
            "start": end_time,
            "end": end_time + TRAVEL_TIME_DURATION,
            "color": TRAVEL_EVENT_COLOR
        })

# Push to Google Calendar
for event in full_schedule:
    calendar_event = {
        "summary": event["title"],
        "start": {"dateTime": event["start"].isoformat(), "timeZone": TIMEZONE},
        "end": {"dateTime": event["end"].isoformat(), "timeZone": TIMEZONE},
        "description": "Auto-synced from BetterChains schedule",
        "colorId": event["color"]
    }

    print("\n🔍 Checking for duplicates within 5 minutes:")
    print(f"  ↪ title = {event['title']}")
    print(f"  ↪ window = {event['start']} to {event['end']}")

    # Find existing event with same title & time window
    existing_events = service.events().list(
        calendarId="primary",
        timeMin=event["start"].isoformat(),
        timeMax=event["end"].isoformat(),
        singleEvents=True
    ).execute().get("items", [])

    for existing_event in existing_events:
        if existing_event.get("summary") == event["title"]:
            print(f"  🗑️ Deleting duplicate: {existing_event['summary']}")
            service.events().delete(calendarId="primary", eventId=existing_event["id"]).execute()

    added_event = service.events().insert(
        calendarId="primary",
        body=calendar_event
    ).execute()

    print(f"✅ Created: {added_event.get('summary')} @ {added_event.get('start').get('dateTime')}")
