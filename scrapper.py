from datetime import timedelta
from config_private import *
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from dateutil import parser
import os
import json

# Read HTML file
with open("Better Chains - My Schedule.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
events = []

for div in soup.find_all("div", class_="fc-event-time"): 
    parent = div.find_parent("a")
    text = parent.text.strip()
    day = parent["data-date"]
    parts = text.split(" - ")
    if len(parts) != 2:
        continue
    start_time = parts[0].strip()
    end_time = parts[1].strip()

    if "off" in text.lower():
        events.append({"off": True})
        continue

    if "am" not in start_time.lower() and "pm" not in start_time.lower():
        start_time += "am"
    if "am" not in end_time.lower() and "pm" not in end_time.lower():
        end_time += "pm"

    start = parser.parse(f"{day} {start_time}")
    end = parser.parse(f"{day} {end_time}")
    title = "Work Shift"

    events.append({
        "title": title,
        "start": start,
        "end": end,
        "color": SHIFT_EVENT_COLOR,
    })

    if ADD_TRAVEL_TIME:
        travel_start = start - TRAVEL_TIME_DURATION
        travel_end = start
        events.append({
            "title": TRAVEL_TIME_DEPARTURE_SUMMARY,
            "start": travel_start,
            "end": travel_end,
            "color": TRAVEL_EVENT_COLOR,
        })

        travel_start_back = end
        travel_end_back = end + TRAVEL_TIME_DURATION
        events.append({
            "title": TRAVEL_TIME_ARIVAL_SUMMARY,
            "start": travel_start_back,
            "end": travel_end_back,
            "color": TRAVEL_EVENT_COLOR,
        })

# Auth
print("🔐 GOOGLE_TOKEN loaded?", bool(GOOGLE_TOKEN))
with open("token.json", "w") as f:
    f.write(GOOGLE_TOKEN)
    print("✅ Token saved to token.json")

creds = Credentials.from_authorized_user_file("token.json", SCOPES)
service = build("calendar", "v3", credentials=creds)
os.remove("token.json")

# Main loop that adds events to Google Calendar
for event in events:
    calendar_event = {
        "summary": event["title"],
        "start": {
            "dateTime": event["start"].isoformat(),
            "timeZone": TIMEZONE,
        },
        "end": {
            "dateTime": event["end"].isoformat(),
            "timeZone": TIMEZONE,
        },
        "description": "Auto-synced from BetterChains schedule",
        "colorId": event["color"]
    }

    # 🧹 Remove any existing event with the same time and title (±5 minutes)
    print("🔍 Checking for duplicates within ±5 minutes:")
    print(f"  ⤷ title = {event['title']}")
    window_start = (event["start"] - timedelta(minutes=5)).isoformat()
    window_end = (event["end"] + timedelta(minutes=5)).isoformat()
    print(f"  ⤷ window = {window_start} to {window_end}")

    existing_events = service.events().list(
        calendarId="primary",
        timeMin=window_start,
        timeMax=window_end,
        singleEvents=True
    ).execute().get("items", [])

    for existing_event in existing_events:
        if existing_event.get("summary") == event["title"]:
            print(f"  🗑️ Deleting duplicate: {existing_event['summary']}")
            service.events().delete(
                calendarId="primary",
                eventId=existing_event["id"]
            ).execute()

    added_event = service.events().insert(
        calendarId="primary",
        body=calendar_event
    ).execute()

    print("✅ Created:", added_event.get("summary"), added_event.get("start").get("dateTime"))