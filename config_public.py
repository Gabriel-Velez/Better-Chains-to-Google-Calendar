import os
from datetime import timedelta

# -------------------------
# Account Credentials (set via GitHub Secrets)
# -------------------------
BETTERCHAINS_USER = os.environ.get("BETTERCHAINS_USER")
BETTERCHAINS_PASS = os.environ.get("BETTERCHAINS_PASS")
GOOGLE_TOKEN = os.environ.get("GOOGLE_TOKEN")

# -------------------------
# Shift Parsing Rules
# -------------------------
DEFAULT_SHIFT_START = {
    "Monday": "3:00 PM",
    "Tuesday": "3:00 PM",
    "Wednesday": "3:00 PM",
    "Thursday": "3:00 PM",
    "Friday": "3:00 PM",
    "Saturday": "3:00 PM",
    "Sunday": "3:00 PM",
}

DEFAULT_SHIFT_END = {
    "Monday": "8:00 PM",
    "Tuesday": "8:00 PM",
    "Wednesday": "8:00 PM",
    "Thursday": "8:00 PM",
    "Friday": "9:00 PM",
    "Saturday": "9:00 PM",
    "Sunday": "8:00 PM",
}

# -------------------------
# Travel Time Settings
# -------------------------
ADD_TRAVEL_TIME = True
TRAVEL_TIME_DURATION = timedelta(minutes=30)
TRAVEL_EVENT_COLOR = "8"  # Gray

# -------------------------
# Calendar Settings
# -------------------------
CALENDAR_SUMMARY = "Shift"
SHIFT_EVENT_COLOR = "1"  # Blue
TIMEZONE = "America/New_York"

# -------------------------
# URL Settings
# -------------------------
SCHEDULE_URL = "https://portlandpie.betterchains.com/schedule"
LOGIN_URL = "https://portlandpie.betterchains.com/user/login"
SCOPES = ['https://www.googleapis.com/auth/calendar']