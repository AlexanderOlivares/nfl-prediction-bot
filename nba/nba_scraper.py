from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from nba_team_list import nba_team_list
# import time
# import re
# import json

try:
    print(nba_team_list)

    driver = webdriver.Chrome(
        '/Users/alexolivares/Desktop/items/automate/chromedriver')

    ###############################################################################
    # ODD SHARK BELOW
    ###############################################################################
    driver.get('https://www.oddsshark.com/nba/scores')

    wait_for_oddshark_pageload = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "oslive-scoreboard")))

    ###############################################################################
    # DRATINGS BELOW
    ###############################################################################
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('https://www.dratings.com/predictor/nba-basketball-predictions/')

    wait_for_dratings_pageload = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "table-division")))

except TimeoutException:
    print(str(TimeoutException))
    driver.quit()

except:
    print("Error occurred")
    driver.quit()

finally:
    driver.quit()
