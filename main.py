from bs4 import BeautifulSoup  # type: ignore
from datetime import date, datetime, timedelta
import re
import os, json
from dateutil import parser
from auth_google import authenticate_google

# Import config
try:
    from config_private import *
except ImportError:
    from config_public import *

service = authenticate_google()

# 🔧 Grab DRY_RUN from environment variable
DRY_RUN = os.environ.get("DRY_RUN", "false").lower() == "true"
if DRY_RUN:
    print(f"🧪 DRY_RUN mode")

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
if not os.path.exists("Better Chains - My Schedule.html"):
    print("❌ Schedule HTML file not found.")
    exit(1)

with open("Better Chains - My Schedule.html", "r", encoding="utf-8") as f:
    html = f.read()

# Parse it with BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Find all day containers
day_blocks = soup.find_all("div")
shift_blocks = soup.find_all("div", class_="day-body assigned")

print(f"Found {len(shift_blocks)} shift blocks")

if not shift_blocks:
    # fallback to older structure if needed
    shift_blocks = soup.find_all("div", class_="foh-schedule-shifts")

parsed_schedule = []

if not parsed_schedule:
    print("❌ No shift data found in the schedule.")
    exit(1)

for block in shift_blocks:
    # Get the day label (e.g., "Friday (4/11)")
    day_head = block.find_previous("div", class_="day-head")
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

    # Convert MM/DD to full YYYY-MM-DD 
    today = date.today()
    try:
        month, day = date_str.split("/")
        date_iso = f"{today.year}-{int(month):02}-{int(day):02}"
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


if all(shift.get("off") for shift in parsed_schedule):
    print("🕙 All shifts are marked as 'off'. No events to process.")
else:
    print(f"📅 Loaded {len(parsed_schedule)} shifts to process")

# 🟢 Main loop that adds events to Google Calendar
for shift in parsed_schedule:
    if shift.get("off"):
        continue

    if "start_time" not in shift:
        print(f"⏭️  Skipping: no start_time on {shift.get('date')}")
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

        if not DRY_RUN:
            try:
                added_event = service.events().insert(
                    calendarId="primary",
                    body=calendar_event
                ).execute()
                print("✅ Created:", added_event.get("summary"), added_event["start"].get("dateTime"))
            except Exception as e:
                print("❌ Failed to create event:", calendar_event["summary"], "-", str(e))
            else:
                print("🧪 DRY RUN: Would create event", calendar_event["summary"], calendar_event["start"]["dateTime"])
