from bs4 import BeautifulSoup # type: ignore
from datetime import datetime, timedelta
import re

SHIFT_RULES = {
    "Monday": {"default_start": "15:00", "default_end": "20:00"},
    "Tuesday": {"default_start": "15:00", "default_end": "20:00"},
    "Wednesday": {"default_start": "15:00", "default_end": "20:00"},
    "Thursday": {"default_start": "15:00", "default_end": "20:00"},
    "Friday": {"default_start": "15:00", "default_end": "21:00"},
    "Saturday": {"default_start": "15:00", "default_end": "21:00"},
    "Sunday": {"default_start": "15:00", "default_end": "20:00"},
}

TRAVEL_TIME_MINUTES = 30


# Open the HTML file
with open("Better Chains - My Schedule.html", "r", encoding="utf-8") as f:
    html = f.read()

# Parse it with BeautifulSoup
soup = BeautifulSoup(html, "lxml")

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

    return [
        {
            "title": "Travel Time: To Work",
            "start": shift_start - timedelta(minutes=TRAVEL_TIME_MINUTES),
            "end": shift_start,
        },
        {
            "title": "Work Shift",
            "start": shift_start,
            "end": shift_end,
        },
        {
            "title": "Travel Time: From Work",
            "start": shift_end,
            "end": shift_end + timedelta(minutes=TRAVEL_TIME_MINUTES),
        },
    ]

print("\nFinal Calendar Events:\n")

for shift in parsed_schedule:
    if shift.get("off"):
        print(f"Day Off: {shift['date']}")
        continue

    for event in get_shift_times(shift):
        print(f"{event['title']}: {event['start'].strftime('%A %Y-%m-%d %I:%M %p')} to {event['end'].strftime('%I:%M %p')}")