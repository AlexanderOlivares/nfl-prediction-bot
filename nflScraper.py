from selenium import webdriver
import time

driver = webdriver.Chrome(
    '/Users/alexolivares/Desktop/items/automate/chromedriver')

driver.get('https://www.dratings.com/predictor/nfl-football-predictions/')

game_table = driver.find_element_by_class_name('table-body')
# print(game_table.text.split('\n')[:-1])

team_names = game_table.find_elements_by_class_name('ta--left.tf--body')

matchup = []
for i in team_names:
    matchup.append([i.text])
    # print(i.text)
print(matchup)

percentages_and_points = game_table.find_elements_by_class_name(
    'table-division')
for i in percentages_and_points:
    print(i.text)
