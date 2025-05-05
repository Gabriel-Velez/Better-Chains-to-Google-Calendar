import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import platform
from datetime import date, timedelta

#import config
try:
    from config_private import *
except ImportError:
    from config_public import *

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 1. Go to login page
driver.get(LOGIN_URL)
time.sleep(3)

# 2. Fill in login form~
wait = WebDriverWait(driver, 15)
email_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
password_input = driver.find_element(By.NAME, "password")

print("✅ USERNAME loaded:", bool(BETTERCHAINS_USER))

email_input.send_keys(BETTERCHAINS_USER)
password_input.send_keys(BETTERCHAINS_PASS + Keys.RETURN)
time.sleep(20)

if "login" in driver.current_url:
    print("❌ Login failed. Please check your credentials.")
    driver.quit()
    exit(1)

# 3. Calculate target week's Tuesday
today = date.today()

if SCRAPE_WEEK == "current":
    days_until_tuesday = (1 - today.weekday() + 7) % 7
    target_tuesday = today + timedelta(days=days_until_tuesday if today.weekday() > 1 else 0)
else:
    days_until_next_tuesday = (1 - today.weekday() + 7) % 7
    days_until_next_tuesday = days_until_next_tuesday or 7
    target_tuesday = today + timedelta(days=days_until_next_tuesday)

formatted_date = target_tuesday.strftime("%Y-%m-%d")

# 4. Append ?date=YYYY-MM-DD to the base SCHEDULE_URL
full_schedule_url = f"{SCHEDULE_URL}?date={formatted_date}"

# 5. Go to schedule page
driver.get(full_schedule_url)

# 6. Wait for schedule to load
try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "foh-schedule-shifts"))
    )
except Exception as e:
    print("❌ Failed to load schedule page:", str(e))
    driver.quit()
    exit(1)

# 7. Save HTML
html = driver.page_source
with open("next_week_schedule.html", "w", encoding="utf-8") as f:
    f.write(html)
