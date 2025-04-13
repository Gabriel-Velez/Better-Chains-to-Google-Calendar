from bs4 import BeautifulSoup # type: ignore
from datetime import datetime, timedelta
import re
import os, json

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

#import config
try:
    from config_private import *
except ImportError:
    from config_public import *

SCOPES = ['https://www.googleapis.com/auth/calendar']
GOOGLE_TOKEN = os.environ["GOOGLE_TOKEN"]
creds = Credentials.from_authorized_user_info(json.loads(GOOGLE_TOKEN), SCOPES)
service = build("calendar", "v3", credentials=creds)

# Convert string times in config into uniform 24hr format for fallback use
SHIFT_RULES = {
    day: {
        "default_start": datetime.strptime(DEFAULT_SHIFT_START[day], "%I:%M %p").strftime("%H:%M"),
        "default_end": datetime.strptime(DEFAULT_SHIFT_END[day], "%I:%M %p").strftime("%H:%M"),
    }
    for day in DEFAULT_SHIFT_START
}

TRAVEL_TIME_MINUTES = TRAVEL_TIME_DURATION.total_seconds() / 60

# Open the HTML file
with open("Better Chains - My Schedule.html", "r", encoding="utf-8") as f:
    html = f.read()

# Parse it with BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Find all day containers
day_blocks = soup.find_all("div")
shift_blocks = soup.find_all("div", class_="foh-schedule-shifts")

parsed_schedule = []

for block in shift_blocks:
    # Get the day label (e.g., "Friday (4/11)")
    day_head = block.find("div", class_="day-head")
    if not day_head:
        continue

    # Remove anything like "Today" and extract just "Friday (4/11)"
    clean_text = re.sub(r"Today.*", "", day_head.get_text()).strip()

    # Match the date inside parentheses
    match = re.match(r"(.+)\((\d+/\d+)\)", clean_text)
    if not match:
        continue

    weekday = match.group(1).strip()
    date_str = match.group(2).strip()
    weekday = weekday.strip()
    date_str = date_str.strip(")")

    # Convert MM/DD to full YYYY-MM-DD (using 2025 as the year)
    try:
        month, day = date_str.split("/")
        date_iso = f"2025-{int(month):02}-{int(day):02}"
    except ValueError:
        continue  # skip if malformed

    # Check if there's a <bdo> tag with the time
    time_bdo = block.find("bdo")
    if time_bdo:
        start_time = time_bdo.text.strip()
        parsed_schedule.append({"date": date_iso, "start_time": start_time})
    else:
        parsed_schedule.append({"date": date_iso, "off": True})


def get_shift_times(shift):
    date_obj = datetime.strptime(shift["date"], "%Y-%m-%d")
    day_name = date_obj.strftime("%A")
    fallback = SHIFT_RULES[day_name]

    start_str = shift.get("start_time", fallback["default_start"])
    end_str = fallback["default_end"]

    shift_start = datetime.strptime(f"{shift['date']} {start_str}", "%Y-%m-%d %I:%M %p")
    shift_end = datetime.strptime(f"{shift['date']} {end_str}", "%Y-%m-%d %H:%M")

    events = [
        {
            "title": CALENDAR_SUMMARY,
            "start": shift_start,
            "end": shift_end,
            "color": SHIFT_EVENT_COLOR
        }
    ]

    if ADD_TRAVEL_TIME:
        travel_minutes = TRAVEL_TIME_DURATION.total_seconds() / 60
        events.insert(0, {
            "title": TRAVEL_TIME_DEPARTURE_SUMMARY,
            "start": shift_start - timedelta(minutes=travel_minutes),
            "end": shift_start,
            "color": TRAVEL_EVENT_COLOR
        })
        events.append({
            "title": TRAVEL_TIME_ARIVAL_SUMMARY,
            "start": shift_end,
            "end": shift_end + timedelta(minutes=travel_minutes),
            "color": TRAVEL_EVENT_COLOR
        })

    return events


# Main loop that adds events to Google Calendar
for shift in parsed_schedule:
    if shift.get("off"):
        continue

    for event in get_shift_times(shift):
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

        # 🧹 Remove duplicates first
        existing_events = service.events().list(
            calendarId="primary",
            timeMin=event["start"].isoformat(),
            timeMax=event["end"].isoformat(),
            q=event["title"],
            singleEvents=True
        ).execute().get("items", [])
        
        print("🕵️ Checking for duplicates:",
            f"title={event['title']}",
            f"timeMin={event['start'].isoformat()}",
            f"timeMax={event['end'].isoformat()}")

        for existing_event in existing_events:
            service.events().delete(calendarId="primary", eventId=existing_event["id"]).execute()

        # ✅ Then insert new event
        added_event = service.events().insert(calendarId="primary", body=calendar_event).execute()
        print("✅ Created:", added_event.get("summary"), added_event.get("start").get("dateTime"))