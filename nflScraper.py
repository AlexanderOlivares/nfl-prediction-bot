from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import teamDict
import json
from pyfiglet import Figlet
from datetime import datetime

driver = webdriver.Chrome(
    '/Users/alexolivares/Desktop/items/automate/chromedriver')

print("Loading...")

team_lookup = teamDict.lookup
week_of_season = "_"
predictions = {}

###############################################################################
# ODD SHARK BELOW
###############################################################################
driver.get('https://www.oddsshark.com/nfl/scores')

time.sleep(3)

###############################################################################
# get the current week of the season to add data in to correct table
###############################################################################
oddShark_get_week = driver.find_element_by_class_name('button__subtitle')
week_of_season += '_'.join(oddShark_get_week.text.split(' '))

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

print("oddShark Scores")
print(oddShark_formatted_data)

total_teams_playing_this_week = len(oddShark_formatted_data)

for i in oddShark_formatted_data:
    predictions[i[0]] = {
        "oddShark": i[1]
    }

###############################################################################
# DRATINGS BELOW
###############################################################################
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])
driver.get('https://www.dratings.com/predictor/nfl-football-predictions/')

time.sleep(5)


dRatings_game_table = driver.find_element_by_class_name('table-body')

dRating_team_names = dRatings_game_table.find_elements_by_class_name(
    'ta--left.tf--body')

drating_team_name_list = []
for i in dRating_team_names:
    teams = re.findall('\w+(?= \(\d+-\d+(?:-\d+)?\))', i.text)
    for i in teams:
        drating_team_name_list.append(i)

dratings_percentages_and_points = dRatings_game_table.find_elements_by_class_name(
    'table-division')

dratings_predicted_scores = []
for i in dratings_percentages_and_points:
    data_list = i.text.split('\n')
    if len(data_list) > 1:
        for i in data_list:
            if not i.endswith('%'):
                dratings_predicted_scores.append(float(i))

dratings_formatted_data = []

for i in range(0, len(drating_team_name_list)):
    dratings_formatted_data.append(
        [drating_team_name_list[i], dratings_predicted_scores[i]])


###############################################################################
# dRatings displays games by day. So only thur games are visibible and you
# must hit the link below to view sat/sun/mon games on new pages
###############################################################################
scroll_page = 4
while len(dratings_formatted_data) < total_teams_playing_this_week:
    driver.get(
        f'https://www.dratings.com/predictor/nfl-football-predictions/upcoming/{scroll_page}#scroll-upcoming')

    time.sleep(5)

    dRatings_game_table = driver.find_element_by_class_name('table-body')

    dRating_team_names = dRatings_game_table.find_elements_by_class_name(
        'ta--left.tf--body')

    dRatings_game_table = driver.find_element_by_class_name('table-body')

    dRating_team_names = dRatings_game_table.find_elements_by_class_name(
        'ta--left.tf--body')

    drating_team_name_list = []
    for i in dRating_team_names:
        teams = re.findall('\w+(?= \(\d+-\d+(?:-\d+)?\))', i.text)
        for i in teams:
            drating_team_name_list.append(i)

    dratings_percentages_and_points = dRatings_game_table.find_elements_by_class_name(
        'table-division')

    dratings_predicted_scores = []
    for i in dratings_percentages_and_points:
        data_list = i.text.split('\n')
        if len(data_list) > 1:
            for i in data_list:
                if not i.endswith('%'):
                    dratings_predicted_scores.append(float(i))

    for i in range(0, len(drating_team_name_list)):
        dratings_formatted_data.append(
            [drating_team_name_list[i], dratings_predicted_scores[i]])

    scroll_page += 1

for i in dratings_formatted_data:
    if i[0] in predictions:
        predictions[i[0]]["dRatings"] = i[1]
    else:
        predictions[i[0]] = {
            "dRatings": i[1]
        }

print("dRatings Scores")
print(dratings_formatted_data)

for key in predictions:
    dict = predictions[key]
    total = 0
    total_predictions = 0
    for i in dict:
        total += dict[i]
        total_predictions += 1
    average = round(total / total_predictions)
    predictions[key]["average"] = average

###############################################################################
# GET VEGAS LINES FROM ESPN
###############################################################################
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[2])
driver.get('https://www.espn.com/nfl/lines')

espn_com = driver.find_elements_by_class_name('Table__TR')

for i in espn_com:
    team_name_and_data = i.text.split('\n')
    if len(team_name_and_data) == 2:
        full_team_name, data = team_name_and_data
        regex_line_finder = '(?<=\) )\-\d+\.\d{1}'
        line_list = re.findall(regex_line_finder, data)
        if (len(line_list) == 1):
            line = float(line_list[0])
            fav = full_team_name.split(' ')[-1]
            if fav == "Washington":
                fav = "Team"
            if line < 0:
                predictions[fav]["favoredBy"] = line
                predictions[fav]["avgMinusSpread"] = round(
                    predictions[fav]["average"] + line, 1)

###############################################################################
# ORDER PREDICTIONS BY CURRENT WEEKLY MATCHUP
###############################################################################
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[3])
driver.get('https://www.nfl.com/schedules/')

time.sleep(6)

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

print("Raw Data")
print(json.dumps(matchups, indent=4))
print("Picks")

###############################################################################
# PRINT OUT PICKS
###############################################################################
for matchup in matchups:
    fav_team = ""
    avg_minus_spread = 0
    favored_by = 0
    dog_team = ""
    dog_avg = 0
    for team in matchup:
        team_name = list(team)[0]
        if "avgMinusSpread" in predictions[team_name]:
            fav_team = team_name
            avg_minus_spread = predictions[team_name]["avgMinusSpread"]
            favored_by = abs(predictions[team_name]["favoredBy"])
        else:
            dog_team = team_name
            dog_avg = predictions[team_name]["average"]
    pick = ""
    if avg_minus_spread == dog_avg:
        pick = f"PUSH {fav_team} vs {dog_team}"
    elif avg_minus_spread > dog_avg:
        pick = f"{fav_team} -{str(favored_by)}"
    else:
        pick = f"{dog_team} +{str(favored_by)}"
    print(pick)

driver.quit()
