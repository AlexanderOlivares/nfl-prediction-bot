from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import re
import teamDict
import json
from pyfiglet import Figlet

f = Figlet(font='smslant')
# f = Figlet(fonts)
# print(f)
print(f.renderText("Loading..."))

team_lookup = teamDict.lookup

driver = webdriver.Chrome(
    '/Users/alexolivares/Desktop/items/automate/chromedriver')

driver.get('https://www.dratings.com/predictor/nfl-football-predictions/')

dRatings_game_table = driver.find_element_by_class_name('table-body')

dRating_team_names = dRatings_game_table.find_elements_by_class_name(
    'ta--left.tf--body')

# washington football team is going to labled just by "Team"
dRating_team_name_list = []
for i in dRating_team_names:
    teams = re.findall('\w+(?= \(\d+-\d+\))', i.text)
    for i in teams:
        dRating_team_name_list.append(i)

dRatings_percentages_and_points = dRatings_game_table.find_elements_by_class_name(
    'table-division')

dRatings_predicted_scores = []
for i in dRatings_percentages_and_points:
    data_list = i.text.split('\n')
    if len(data_list) > 1:
        for i in data_list:
            if not i.endswith('%'):
                dRatings_predicted_scores.append(float(i))

dRatings_formatted_data = []

for i in range(0, len(dRating_team_name_list)):
    dRatings_formatted_data.append(
        [dRating_team_name_list[i], dRatings_predicted_scores[i]])

# UNCOMMENT FOR FINAL DRATINGS DATA
print(f.renderText("dRatings Scores"))
print(dRatings_formatted_data)
print('---------------------------')

predictions = {}

for i in dRatings_formatted_data:
    predictions[i[0]] = {
        "dRatings": i[1]
    }


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
    predictEm_regex_split = "\s(?=\d+)"
    predictEm_formatted_data.append(
        re.split(predictEm_regex_split, predictEm_individual_team_prediction[i]))


def make_lowercase_and_number(two_dim_list):
    formatted = []
    for i in two_dim_list:
        lower_case_team_and_number_score = []
        lower_case_team_and_number_score.append(i[0][0] + i[0][1:].lower())
        lower_case_team_and_number_score.append(float(i[1]))
        formatted.append(lower_case_team_and_number_score)
    return formatted


predictEm_formatted_data = make_lowercase_and_number(predictEm_formatted_data)
# UNCOMMENT FOR FINAL PREDICTEM DATA
print(f.renderText("predictEm Scores"))
print(predictEm_formatted_data)
print('---------------------------')


for i in predictEm_formatted_data:
    location_regex = r'(?i){0}'.format(i[0])
    for j in team_lookup:
        full_name_found = re.findall(location_regex, j["full_name"])
        if full_name_found:
            if j["name"] in predictions:
                predictions[j["name"]]["predictEm"] = i[1]
            else:
                predictions[j["name"]] = {
                    "predictEm": i[1]
                }
        elif "alt" in j:
            if j["name"] in predictions:
                predictions[j["name"]]["predictEm"] = i[1]
            else:
                predictions[j["name"]] = {
                    "predictEm": i[1]
                }


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
    predicted_score = float(oddShark_predcted_scores_only[i])
    if team_name == "Football Team":
        team_name = "Team"
    oddShark_formatted_data.append([team_name, predicted_score])

print(f.renderText("oddShark Scores"))
print(oddShark_formatted_data)


for i in oddShark_formatted_data:
    if i[0] in predictions:
        predictions[i[0]]["oddShark"] = i[1]
    else:
        predictions[i[0]] = {
            "oddShark": i[1]
        }


for key in predictions:
    dict = predictions[key]
    total = 0
    total_predictions = 0
    for i in dict:
        total += dict[i]
        total_predictions += 1
    average = round(total / total_predictions, 1)
    predictions[key]["average"] = average


driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[3])
driver.get('https://www.espn.com/nfl/lines')

espn_com = driver.find_elements_by_class_name('Table__TR')

for i in espn_com:
    team_name_and_data = i.text.split('\n')
    if len(team_name_and_data) == 2:
        full_team_name, data = team_name_and_data
        regex_line_finder = '(?<=\) )\-\d+[.]?\d'
        line_list = re.findall(regex_line_finder, data)
        if (len(line_list) == 1):
            line = float(line_list[0])
            fav = full_team_name.split(' ')[-1]
            if line < 0:
                predictions[fav]["favoredBy"] = line
                predictions[fav]["avgMinusSpread"] = round(
                    predictions[fav]["average"] + line, 1)


# THIS WILL ORDER PREDICTIONS BY MATCHUP
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[4])
driver.get('https://www.nfl.com/schedules/')

time.sleep(3)

nfl_com_schedule = driver.find_element_by_id("main-content")
nfl_com_sched = nfl_com_schedule.text.split('\n')

matchups = []
head_to_head = []
for i in nfl_com_sched:
    if i in predictions:
        head_to_head.append({i: predictions[i]})
    if i == "Washington":
        head_to_head.append({"Team": predictions["Team"]})
    if len(head_to_head) == 2:
        matchups.append(head_to_head)
        head_to_head = []

print(f.renderText("Predictions"))
print(json.dumps(matchups, indent=4))
print(f.renderText("good luck!"))


time.sleep(7)
driver.quit()
