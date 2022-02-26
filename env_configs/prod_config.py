import requests
import os
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import psycopg2

chromdriver_latest_release = requests.get(
    "https://chromedriver.storage.googleapis.com/LATEST_RELEASE").text
if os.environ["CHROMEDRIVER_VERSION"] != chromdriver_latest_release:
    raise Exception("chromedriver versions do not match")

print("Chromerdriver is version:")
print(os.environ.get("CHROMEDRIVER_VERSION"))

chrome_options = Options()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(executable_path=os.environ.get(
    "CHROMEDRIVER_PATH"), options=chrome_options)

db_url = os.environ.get('DATABASE_URL')
conn = psycopg2.connect(db_url)
cursor = conn.cursor()

config = {
    'connection': conn,
    'cursor': cursor,
    'driver': driver
}
