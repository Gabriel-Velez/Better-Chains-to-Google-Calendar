BetterChains Scraper 🧠
This repo automates scraping your BetterChains schedule and syncing it to Google Calendar. Designed for Portland Pie, but easily adjustable for other employers on BetterChains.

🧩 Features
Logs into BetterChains using provided credentials

Fetches the upcoming or current week's schedule

Converts shifts into Google Calendar events

Adds optional travel time before and after shifts

Automatically runs weekly via GitHub Actions

📁 Folder Structure
.
├── .github/
│ └── workflows/
│ └── betterchains.yml # GitHub Actions workflow
├── auth_google.py # Google token handling
├── config_public.py # Public configuration (defaults, colors, labels)
├── fetch_schedule.py # Fetches schedule from BetterChains
├── main.py # Orchestrates the full process
├── requirements.txt # Dependencies
└── .gitignore

⚙️ Setup

1.  🔐 Environment Secrets (GitHub Actions)
    In your repo settings, set the following repository secrets:
    BETTERCHAINS_USER
    BETTERCHAINS_PASS
    GOOGLE_TOKEN

2.  🔑 Generate Your Google Token
    Run locally:
    nginx
    Copy
    Edit
    python generate_google_token.py
    Follow the instructions and paste the output into your GitHub secret GOOGLE_TOKEN.

🔧 Configuration
Open config_public.py to configure:
Default shift times
Travel time settings
Calendar event color
Timezone and event summary format

Example:
python:
DEFAULT_SHIFT_START = {
"Monday": "3:00 PM",
"Tuesday": "3:00 PM",
...
}

SCRAPE_WEEK = "next" # Options: "next", "current", or "both"

🤖 Automation
The GitHub Actions workflow runs every Sunday at 11 AM (UTC) to fetch and sync next week's schedule.

You can also trigger it manually via the Actions tab.

🧪 Debug Mode (Dry Run)
Enable DRY_RUN mode by setting the environment variable:
yaml:
DRY_RUN: true
This will simulate calendar creation without actually syncing events — useful for testing.

🙋 FAQ
Q: What if my schedule isn’t posted yet?
A: You’ll see a message like 🔴 All shifts are marked as 'off'. No events to process.

Q: Will it detect duplicate events?
A: Yes, events with matching titles and timestamps are skipped or removed before adding new ones.

📜 License
MIT License — open source and yours to build on.

❤️ Credit
Created by @Gabe for fun and to avoid manually copying shifts like a caveman.
