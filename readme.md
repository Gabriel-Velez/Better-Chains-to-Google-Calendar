# BetterChains Scraper 🧠

This repo automates scraping your BetterChains schedule and syncing it to Google Calendar. Designed for Portland Pie, but easily adjustable for other employers on BetterChains.

# 🚀 Getting Started

1. Clone or fork this repo.
2. Add your secrets to GitHub.
3. Customize `config_public.py` to fit your shift structure.
4. (Optional) Run locally with `python main.py` to test.
5. GitHub Actions will take care of the rest.

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

# 🍴 Forking

To use this project with your own BetterChains account:

1.  Fork the repo to your own GitHub account.

2.  Go to your fork’s Settings > Secrets and variables > Actions and add these secrets:

- `BETTERCHAINS_USER`
- `BETTERCHAINS_PASS`
- `GOOGLE_TOKEN`

# 🔑 Generate Your Google Token

Run locally:

<pre lang = "nginx">
python generate_google_token.py
</pre>

Then paste the contents of `token.json` into your GitHub secret named `GOOGLE_TOKEN`.

# ⚙️ Customization

Customize shift settings in config_public.py:

- Default shift times
- Travel time
- Event colors
- Timezone
- Week Scraped
- Betterchanins Organizaton

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

# 🙋 FAQ

**Q:** What if my schedule isn’t posted yet?

**A:** You’ll see a message `🕙 All shifts are marked as 'off'. No events to process.`

---

**Q:** Will it detect duplicate events?

**A:** No. The script does not currently detect or remove existing events. If the same schedule is processed multiple times (e.g., from repeated manual runs or automation), duplicate events will be added to your calendar.
To avoid this, make sure your schedule only runs once per week — or manually delete duplicates if needed.

# 📜 License

MIT License — open source and yours to build on.

# ❤️ Credit

Created by @Gabe for fun and to avoid manually copying shifts like a caveman.
