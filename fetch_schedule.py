from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
import platform

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

if platform.system() == "Linux":
    driver = webdriver.Chrome(options=options)
else:
    driver_path = "D:/WebDrivers/chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path, options=options)


# Replace with the path to your ChromeDriver
CHROMEDRIVER_PATH = "D:/WebDrivers/chromedriver.exe"

# Replace with your actual login credentials
USERNAME = "gabriel.dan.velez@gmail.com"
PASSWORD = "881967"

# Setup
service = Service(CHROMEDRIVER_PATH)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# 1. Go to login page
driver.get("https://portlandpie.betterchains.com/user/login")
time.sleep(3)

# 2. Fill in login form
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 15)
email_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
password_input = driver.find_element(By.NAME, "password")

email_input.send_keys(USERNAME)
password_input.send_keys(PASSWORD + Keys.RETURN)
time.sleep(20)


# 3. Go to schedule page
driver.get("https://portlandpie.betterchains.com/schedule")
time.sleep(3)

# 4. Click the “Next Week” arrow
arrows = WebDriverWait(driver, 15).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.btn.btn-primary"))
)

# Click the SECOND one (next week)
arrows[1].click()
time.sleep(20)

# 5. Save HTML
html = driver.page_source
with open("next_week_schedule.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Schedule saved to next_week_schedule.html")

driver.quit()
