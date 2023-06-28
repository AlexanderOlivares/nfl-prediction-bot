import os
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import psycopg2

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")


driver = webdriver.Chrome(options=chrome_options)
sentry_dsn = os.environ.get("SENTRY_DSN")
db_url = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(db_url)
cursor = conn.cursor()

config = {
    "connection": conn,
    "cursor": cursor,
    "driver": driver,
    "sentry_dsn": sentry_dsn,
}
