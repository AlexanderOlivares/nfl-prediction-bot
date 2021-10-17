from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import re

driver = webdriver.Chrome(
    '/Users/alexolivares/Desktop/items/automate/chromedriver')

driver.get('https://www.dratings.com/predictor/nfl-football-predictions/')

dRatings_game_table = driver.find_element_by_class_name('table-body')

dRating_team_names = dRatings_game_table.find_elements_by_class_name(
    'ta--left.tf--body')

dRating_machup = []
for i in dRating_team_names:
    teams = i.text.split('\n')
    dRating_machup.append(teams)

dRatings_percentages_and_points = dRatings_game_table.find_elements_by_class_name(
    'table-division')

dRatings_percentages = []
dRatings_predicted_scores = []
for i in dRatings_percentages_and_points:
    data_list = i.text.split('\n')
    if len(data_list) > 1:
        if data_list[0].endswith('%'):
            dRatings_percentages.append(data_list)
        else:
            dRatings_predicted_scores.append(data_list)

dRatings_formatted_data = []
dRatings_zip = (zip(dRating_machup, dRatings_percentages,
                dRatings_predicted_scores))
for i in dRatings_zip:
    dRatings_formatted_data.append(tuple(i))

# UNCOMMENT FOR FINAL DRATINGS DATA
# for i in dRatings_formatted_data:
#     print(i)


#################### PREDICTEM BELOW ################################################
# OPEN NEW TAB
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])
driver.get('https://www.predictem.com/nfl/nfl-football-computer-picks-simulated-predictions-for-each-pro-football-game-every-week/')

predictEm_predictions = driver.find_element_by_class_name('et_pb_text_inner')
predictEm_all_text = predictEm_predictions.text

predictEm_individual_team_prediction = re.findall(
    '(?<=\d{3}: ).+', predictEm_all_text)

predictEm_formatted_data = []
for i in range(0, len(predictEm_individual_team_prediction)):
    predictEm_formatted_data.append(predictEm_individual_team_prediction[i])

# UNCOMMENT FOR FINAL PREDICTEM DATA
print(predictEm_formatted_data)

####################### ODD SHARK BELOW ###############################################
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[2])
driver.get('https://www.oddsshark.com/nfl/scores')


time.sleep(3)
oddShark_scoreboard = driver.find_element_by_class_name('scoreboard')
oddShark_all_text = oddShark_scoreboard.text.split('\n')

reg_exp_oddShark = re.compile("^(\d{1,2}[\.]?[\d]?)$")
oddShark_regex_match_score_with_over_under = list(
    filter(reg_exp_oddShark.match, oddShark_all_text))
oddShark_regex_match_score_with_over_under.insert(0, '0 index place filler')

oddShark_predcted_scores_only = []

for i in range(0, len(oddShark_regex_match_score_with_over_under)):
    if i % 3 != 0:
        oddShark_predcted_scores_only.append(
            oddShark_regex_match_score_with_over_under[i])


nfl_team_lookup = ["Cardinals", "Falcons", "Ravens", "Bills", "Panthers", "Bears", "Bengals", "Browns", "Cowboys", "Broncos", "Lions", "Packers", "Texans", "Colts", "Jaguars", "Chiefs",
                   "Raiders", "Chargers", "Rams", "Dolphins", "Vikings", "Patriots", "Saints", "Giants", "Jets", "Eagles", "Steelers", "49ers", "Seahawks", "Buccaneers", "Titans", "Football Team"]

oddShark_active_team_names = []

for i in oddShark_all_text:
    if i in nfl_team_lookup:
        oddShark_active_team_names.append(i)

oddShark_formatted_data = []

for i in range(0, len(oddShark_predcted_scores_only)):
    team_name = oddShark_active_team_names[i]
    predicted_score = oddShark_predcted_scores_only[i]
    oddShark_formatted_data.append([team_name, predicted_score])

print(oddShark_formatted_data)

time.sleep(7)
driver.quit()
