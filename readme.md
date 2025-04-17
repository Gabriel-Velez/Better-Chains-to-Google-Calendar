# BetterChains Scraper 🧠

This repo automates scraping your BetterChains schedule and syncing it to Google Calendar. Designed for Portland Pie, but easily adjustable for other employers on BetterChains.

# 🧩 Features

Logs into BetterChains using provided credentials

Fetches the upcoming or current week's schedule

Converts shifts into Google Calendar events

Adds optional travel time before and after shifts

Automatically runs weekly via GitHub Actions

# 📁 Folder Structure

<pre lang="md">  
├── .github/  
│   └── workflows/  
│       └── betterchains.yml   # GitHub Actions workflow  
├── auth_google.py             # Google token handling  
├── config_public.py           # Public configuration (defaults, colors, labels)  
├── fetch_schedule.py          # Fetches schedule from BetterChains  
├── main.py                    # Orchestrates the full process  
├── requirements.txt           # Dependencies  
└── .gitignore
 </pre>

# 🍴 Forking & Customization

To use this project with your own BetterChains account:

1.  Fork the repo to your own GitHub account.

2.  Go to your fork’s Settings > Secrets and variables > Actions and add these secrets:

   <pre lang="md">
   BETTERCHAINS_USER
   BETTERCHAINS_PASS
   GOOGLE_TOKEN
   </pre>

Customize shift settings in config_public.py:

   <pre lang="md">
   Default shift times
   Travel time
   Event colors and timezone
   Week Scraped
   Betterchanins Organizaton
   <pre lang="md">


# 🤖 Automation

The GitHub Actions workflow runs every Sunday at 11 AM (UTC) to fetch and sync next week's schedule. 

You can change the time by editing GitHub workflow schedule in .github/workflows/betterchains.yml. 
   <pre lang="yml">
   on:
      schedule:
         - cron: "0 15 * * 0" # <--HERE
      workflow_dispatch:
   <pre>

How to edit the CRON expression
   <pre lang="md">
   0 15 * * 0
   ┬ ┬ ┬ ┬ ┬
   │ │ │ │ └──── Day of week (0 = Sunday)
   │ │ │ └────── Month (1 - 12)
   │ │ └──────── Day of month (1 - 31)
   │ └────────── Hour (0 - 23)
   └──────────── Minute (0 - 59)
   <pre lang="md">

You can also trigger it manually via the Actions tab.

# 🧪 Debug Mode (Dry Run)
**Enable DRY_RUN mode by setting the environment variable:**
`DRY_RUN: "true"`

This will simulate calendar creation without actually syncing events — useful for testing._

# 🙋 FAQ

**Q:** What if my schedule isn’t posted yet?

**A:** You’ll see a message `🕙 All shifts are marked as 'off'. No events to process.`

---

**Q:** Will it detect duplicate events?

**A:** Yes, events with matching titles and timestamps are skipped or removed before adding new ones.

# 📜 License

MIT License — open source and yours to build on.

# ❤️ Credit

Created by @Gabe for fun and to avoid manually copying shifts like a caveman.
