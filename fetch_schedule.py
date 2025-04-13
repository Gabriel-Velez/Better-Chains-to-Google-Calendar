import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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

if platform.system() == "Linux":
    driver = webdriver.Chrome(options=options)
else:
    driver_path = "D:/WebDrivers/chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path, options=options)

# 1. Go to login page
driver.get(LOGIN_URL)
time.sleep(3)

# 2. Fill in login form
wait = WebDriverWait(driver, 15)
email_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
password_input = driver.find_element(By.NAME, "password")

print("✅ USERNAME loaded:", bool(BETTERCHAINS_USER))

email_input.send_keys(BETTERCHAINS_USER)
password_input.send_keys(BETTERCHAINS_PASS + Keys.RETURN)
time.sleep(20)


# 3. Calculate date for next week's Tuesday
today = date.today()
days_until_next_tuesday = (1 - today.weekday() + 7) % 7
days_until_next_tuesday = days_until_next_tuesday or 7
next_tuesday = today + timedelta(days=days_until_next_tuesday)
formatted_date = next_tuesday.strftime("%Y-%m-%d")

# 4. Append ?date=YYYY-MM-DD to the base SCHEDULE_URL
full_schedule_url = f"{SCHEDULE_URL}?date={formatted_date}"

# 5. Go to schedule page
driver.get(full_schedule_url)

# 6. Wait for schedule to load
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CLASS_NAME, "foh-schedule-shifts"))
)

# 7. Save HTML
html = driver.page_source
with open("next_week_schedule.html", "w", encoding="utf-8") as f:
    f.write(html)