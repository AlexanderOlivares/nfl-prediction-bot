import os
from selenium import webdriver
import psycopg2

path = os.environ.get('LOCAL_CHROMEDRIVER_PATH')
local_driver = driver = webdriver.Chrome(path)

host = os.environ.get('scraper_hostname')
database = os.environ.get('nfl_scraper_database')
user = os.environ.get('scraper_username')
password = os.environ.get('scraper_password')
port = os.environ.get('scraper_port')

conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password,
    port=port
)

cursor = conn.cursor()

config = {
    'user': user,
    'password': password,
    'host': host,
    'port': port,
    'database': database,
    'connection': conn,
    'cursor': cursor,
    "driver": local_driver
}
