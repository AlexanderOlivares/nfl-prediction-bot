import os
from selenium import webdriver

path = os.environ.get('LOCAL_CHROMEDRIVER_PATH')
local_driver = driver = webdriver.Chrome(path)

config = {
    "driver": local_driver
}
