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
- `GOOGLE_CLIENT_SECRET`

# 🔑 Generate Your Google Token

To allow this script to create events in your Google Calendar, you'll need to generate a `GOOGLE_TOKEN,` which authorizes access to your calendar on your behalf.

1. Open the terminal and cd to your project file
2. Run locally: `python generate_google_token.py`
3. Open the file `token.json` and copy the entire contents.
4. In your GitHub repo, go to **Settings > Secrets and variables > Actions**, and paste it into your GitHub secret named `GOOGLE_TOKEN`.

# 🔐 Getting Your Google Client Secret

To allow this script to sync with your Google Calendar, you'll need to generate a `GOOGLE_CLIENT_SECRET` from the Google Cloud Console.

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Click **Create Project** and make a new project
3. Navigate to **APIs & Services > Credentials**.
4. Click **+ Create Credentials** and choose **OAuth client ID**.
5. Choose **Desktop app** as the application type.
6. Click **Create**.
7. Click **Download JSON** — this file contains your `client_id`, `client_secret`, and other OAuth details.
8. Open the file and copy the entire contents.
9. In your GitHub repo, go to **Settings > Secrets and variables > Actions**, and paste the contents into your GitHub secret named `GOOGLE_CLIENT_SECRET`.

# ⚙️ Customization

Customize shift settings in config_public.py:

- Default shift times
- Travel time
- Event colors
- Timezone
- Week Scraped
- BetterChains Organization

# 🤖 Automation

The GitHub Actions workflow runs every Sunday at 11 AM (UTC) to fetch and sync next week's schedule.

You can change the time by editing GitHub workflow schedule in .github/workflows/betterchains.yml.

   <pre lang="yml">
   on:
      schedule:
         - cron: "0 15 * * 0" # <--HERE
      workflow_dispatch:
   </pre>

How to edit the CRON expression

   <pre lang="md">
   0 15 * * 0
   ┬ ┬┬ ┬ ┬ ┬
   │ ││ │ │ └──── Day of week (0 = Sunday)
   │ ││ │ └────── Month (1 - 12)
   │ ││ └──────── Day of month (1 - 31)
   │ └└───────── Hour (0 - 23)
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
