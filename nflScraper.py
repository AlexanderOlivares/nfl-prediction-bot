from utils import get_and_format_vegas_line, washington_to_team
import time
import re
import teamDict
import json
from pyfiglet import Figlet
import os
if "PRODUCTION" in os.environ:
    from env_configs import prod_config as config
else:
    from env_configs import dev_config as config

driver = config.driver

figlet = Figlet(font='smslant')
print(figlet.renderText("Loading..."))

team_lookup = teamDict.lookup
week_of_season = "_"
predictions = {}

###############################################################################
# ODD SHARK BELOW
###############################################################################
driver.get('https://www.oddsshark.com/nfl/scores')

time.sleep(5)

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

nfl_team_lookup = list(map(lambda team: team["name"], team_lookup))

oddShark_active_team_names = []

for i in oddShark_all_text:
    if i in nfl_team_lookup or i == 'Fooball Team':
        oddShark_active_team_names.append(i)

oddShark_formatted_data = []

for i in range(0, len(oddShark_predcted_scores_only)):
    team_name = oddShark_active_team_names[i]
    predicted_score = float(oddShark_predcted_scores_only[i])
    if team_name == "Football Team":
        team_name = "Team"
    oddShark_formatted_data.append([team_name, predicted_score])

print(figlet.renderText("oddShark Scores"))
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

time.sleep(5)

###############################################################################
# dRatings displays games by day. So only thur games are visibible and you
# must hit the link below to view sat/sun/mon games on new pages
###############################################################################
scroll_page = 2
while len(dratings_formatted_data) < total_teams_playing_this_week:
    driver.get(
        f'https://www.dratings.com/predictor/nfl-football-predictions/upcoming/{scroll_page}#scroll-upcoming')

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

print(figlet.renderText("dRatings Scores"))
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

espn_vegas_lines = driver.find_elements_by_class_name('Table__TR')

predictions = get_and_format_vegas_line(
    espn_vegas_lines, predictions, washington_to_team)


###############################################################################
# ORDER PREDICTIONS BY CURRENT WEEKLY MATCHUP
###############################################################################
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[3])
driver.get('https://www.nfl.com/schedules/')

time.sleep(3)

nfl_com_schedule = driver.find_element_by_id("main-content")
nfl_com_sched = nfl_com_schedule.text.split('\n')

###############################################################################
# WRITE TO DB
###############################################################################

try:
    cur = config.cursor
    conn = config.conn

    create_table = (
        f"""
        CREATE TABLE nfl{week_of_season}(
        away_team VARCHAR(255),
        away_predicted decimal,
        home_team VARCHAR(255),
        home_predicted decimal,
        vegas_line numeric,
        favored_team VARCHAR(255),
        pick VARCHAR(255)
        )
        """
    )

    cur.execute(create_table)
    conn.commit()

    matchups = []
    head_to_head = []
    for i in nfl_com_sched:
        if i in predictions:
            head_to_head.append({i: predictions[i]})
        if i == "Washington":
            head_to_head.append({"Team": predictions["Team"]})
        if len(head_to_head) == 2:
            away_team = list(head_to_head[0])[0]
            home_team = list(head_to_head[1])[0]
            away_predicted = 0
            home_predicted = 0
            favored_team = ""

            if "avgMinusSpread" in predictions[away_team]:
                away_predicted = predictions[away_team]["average"]
                favored_team = away_team
            else:
                away_predicted = predictions[away_team]["average"]

            if "avgMinusSpread" in predictions[home_team]:
                home_predicted = predictions[home_team]["average"]
                favored_team = home_team
            else:
                home_predicted = predictions[home_team]["average"]

            insert_command = f'INSERT INTO nfl{week_of_season} (away_team, away_predicted, home_team, home_predicted, favored_team) VALUES (%s, %s, %s, %s, %s)'
            insert_values = (away_team, away_predicted,
                             home_team, home_predicted, favored_team)
            cur.execute(insert_command, insert_values)

            matchups.append(head_to_head)
            head_to_head = []

    print(figlet.renderText("Raw Data"))
    print(json.dumps(matchups, indent=4))
    print(figlet.renderText("Picks"))

################### PRINT OUT FINAL PICKS ###################
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
                insert_command = f'UPDATE nfl{week_of_season} SET vegas_line = (%s) WHERE home_team = (%s) OR away_team = (%s)'
                insert_value = (favored_by, fav_team, fav_team)
                cur.execute(insert_command, insert_value)
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
        insert_command = f'UPDATE nfl{week_of_season} SET pick = (%s) WHERE home_team = (%s) OR away_team = (%s)'
        insert_value = (pick, fav_team, fav_team)
        cur.execute(insert_command, insert_value)

    conn.commit()
except Exception as error:
    print(error)
finally:
    if cur is not None:
        print('cursor was open')
        cur.close()
    if conn is not None:
        print('connection was successful')
        conn.close()

driver.quit()
