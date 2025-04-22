# 📅 BetterChains Schedule Scraper

This repo automates scraping your BetterChains schedule and syncing it to Google Calendar. Designed for Portland Pie, but easily adjustable for other employers on BetterChains.

# 🚀 Getting Started

1. Clone or fork this repo.
2. Add your secrets to GitHub.
3. Generate Your Google Token
4. Get Your Google Client Secret
5. Customize `config_public.py` to fit your shift structure.
6. GitHub Actions will take care of the rest.

# 🧩 Features

- Logs into BetterChains using provided credentials
- Fetches the upcoming or current week's schedule
- Converts shifts into Google Calendar events
- Adds optional travel time before and after shifts
- Automatically runs weekly via GitHub Actions

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

# 🍴 Forking

To use this project with your own BetterChains account:

1.  Fork the repo to your own GitHub account.

2.  Go to your fork’s Settings > Secrets and variables > Actions and add these secrets:

- `BETTERCHAINS_USER`
- `BETTERCHAINS_PASS`
- `GOOGLE_TOKEN`

# 🔑 Generate Your Google Token

To allow this script to create events in your Google Calendar, you'll need to generate a `GOOGLE_TOKEN,` which authorizes access to your calendar on your behalf.

1. Open the terminal and cd to your project file
2. Run locally: `python auth_google.py`
3. Open the file `token.json` and copy the entire contents.
4. In your GitHub repo, go to **Settings > Secrets and variables > Actions**, and paste it into your GitHub secret named `GOOGLE_TOKEN`.

# ⚙️ Customization

Customize shift settings in config_public.py:

- Default shift times
- Travel time
- Event colors
- Timezone
- Week Scraped
- BetterChains Organization

# 🤖 Automation

The GitHub Actions workflow runs 4AM every Monday (which is 11 PM Sunday EST) to fetch and sync next week's schedule.

You can change the time by editing GitHub workflow schedule in .github/workflows/betterchains.yml.

   <pre lang="yml">
   on:
      schedule:
         - cron: "0 4 * * 1" # <--HERE
      workflow_dispatch:
   </pre>

How to edit the CRON expression

   <pre lang="md">
   0 4 * * 1
   ┬ ┬ ┬ ┬ ┬
   │ │ │ │ └──── Day of week (0 = Sunday)
   │ │ │ └────── Month (1 - 12)
   │ │ └──────── Day of month (1 - 31)
   │ └────────── Hour (0 - 23)
   └──────────── Minute (0 - 59)
   </pre>

You can also trigger it manually via the Actions tab.

# 🧪 Debug Mode (Dry Run)

**Enable DRY_RUN mode by setting the environment variable:**
`DRY_RUN: "true"`

This will simulate calendar creation without actually syncing events — useful for testing.

# 💻 Local Development (Optional)

If you'd like to run the script locally instead of GitHub Actions, create a file named `config_private.py` in your root directory. This file should contain your personal credentials and token, like so:

<pre lang="python">
# config_private.py
BETTERCHAINS_USER = "your_email@example.com"
BETTERCHAINS_PASS = "your_password"
GOOGLE_TOKEN = """{ ... }"""  # Paste your token JSON here as a multi-line string
GOOGLE_CLIENT_SECRET = """{ ... }"""  # Paste your Google client secret JSON here as a multi-line string
</pre>

- This file is already excluded via `.gitignore` and will never be uploaded to GitHub.
- The script will automatically prioritize `config_private.py` if it exists.
- Then just run `python main.py` in your terminal

## ⚠️ Error Handling

This script includes basic error handling to ensure smooth execution:

- ❌ **Login failure**: If credentials are incorrect or the login page fails to load, the script exits with a helpful message.
- ❌ **Schedule loading failure**: If the schedule page doesn’t load properly (due to a network issue or site changes), the script will stop and log the error.
- ❌ **Missing schedule file**: If the expected schedule HTML file isn’t found, the script will exit safely.
- ❌ **Google Calendar API errors**: Any issues with adding events (e.g., invalid tokens, rate limits) will be logged with clear details.

For troubleshooting, review the logs printed during each run.

# 🙋 FAQ

### **Q:** What if my schedule isn’t posted yet?

**A:** You’ll see a message `🕙 All shifts are marked as 'off'. No events to process.`

### **Q:** Will it detect duplicate events?

**A:** No. The script does not currently detect or remove existing events. If the same schedule is processed multiple times (e.g., from repeated manual runs or automation), duplicate events will be added to your calendar.
To avoid this, make sure your schedule only runs once per week — or manually delete duplicates if needed.

# 📜 License

MIT License — open source and yours to build on.

# ❤️ Credit

Created by @Gabe for fun and to avoid manually copying shifts like a caveman.
