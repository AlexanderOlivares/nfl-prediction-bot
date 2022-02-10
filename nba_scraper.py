from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from nba_team_list import nba_team_list
from utils import DateFormatter, get_and_format_vegas_line, normal_round, seventysixers_to_sixers
import os
import re
import json
import time

if "PRODUCTION" in os.environ:
    from env_configs import prod_config as config
else:
    from env_configs import dev_config as config

try:
    driver = config.driver
    predictions = {}

    ###############################################################################
    # ODD SHARK BELOW
    ###############################################################################
    driver.get('https://www.oddsshark.com/nba/scores')

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "oslive-scoreboard")))
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "header-text")))

    time.sleep(5)

    get_oddshark_date = driver.find_element_by_class_name('header-text').text
    match_date_regex = '[A-Z]\w+\s\d{1,2}'
    oddshark_game_date = re.findall(
        rf"{match_date_regex}", get_oddshark_date)[0]

    todays_date = DateFormatter.get_todays_date()
    if oddshark_game_date != todays_date:
        raise Exception("Game dates do not match")

    scoreboard = driver.find_element_by_id("oslive-scoreboard")
    oddshark_game_data = scoreboard.text.split('\n')

    team_and_score = []
    score_count = 0
    for i in oddshark_game_data:
        for team in nba_team_list:
            team_name = i.split(' ')[-1]
            if team_name == team["simpleName"]:
                team_and_score.append(team_name)
        predicted_score = re.findall("^\d{2,3}\.?\d*$", i)
        if predicted_score:
            if score_count < 2:
                team_and_score.append(predicted_score[0])
                score_count += 1
            else:
                score_count = 0

    for i in range(len(team_and_score) - 2):
        is_team_name = re.findall("[^0-9\.]", team_and_score[i])
        if is_team_name:
            team_name = seventysixers_to_sixers(team_and_score[i])
            predictions[team_name] = {
                "oddshark": float(team_and_score[i + 2])
            }

    ###############################################################################
    # DRATINGS BELOW
    ###############################################################################
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('https://www.dratings.com/predictor/nba-basketball-predictions/')

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "table-division")))
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ta--left.tf--body")))
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "heading-3")))
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "scroll-upcoming")))

    time.sleep(5)

    get_dratings_date = driver.find_element_by_class_name('heading-3').text
    dratings_date = re.findall(rf"{match_date_regex}", get_dratings_date)[0]
    if dratings_date != todays_date:
        raise Exception("Game dates do not match")

    get_game_table = driver.find_element_by_id("scroll-upcoming")

    scrape_teams = get_game_table.find_elements_by_class_name(
        "ta--left.tf--body")
    scrape_scores = get_game_table.find_elements_by_class_name(
        "table-division")

    dratings_teams = []
    for i in scrape_teams:
        matchup_list = i.text.split('\n')
        for team in matchup_list:
            is_team_name = re.findall("\w+(?=\s\(\d{1,2}\-\d{1,2}\))", team)
            if is_team_name:
                team_name = seventysixers_to_sixers(is_team_name[0])
                dratings_teams.append(team_name)

    dratings_scores = []
    for i in scrape_scores:
        split_mulitline_scores = i.text.split('\n')
        if (len(split_mulitline_scores) > 1):
            score_one, score_two = split_mulitline_scores
            for score in split_mulitline_scores:
                if not score.endswith('%'):
                    dratings_scores.append(score)

    dratings_teams_and_scores = zip(dratings_teams, dratings_scores)
    for team, score in dratings_teams_and_scores:
        if team in predictions:
            predictions[team]['dratings'] = float(score)
            predictions[team]['average'] = normal_round((float(
                score) + predictions[team]['oddshark']) / 2)
        else:
            print('Team is not in predictions')
            driver.quit()

    ###############################################################################
    # ESPN BELOW
    ###############################################################################
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[2])
    driver.get('https://www.espn.com/nba/lines')

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "Table__TR")))
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "Table__Title.margin-subtitle")))

    time.sleep(5)

    get_espn_date = driver.find_element_by_class_name(
        'Table__Title.margin-subtitle').text
    espn_date = re.findall(rf"{match_date_regex}", get_espn_date)[0]
    if espn_date != todays_date:
        raise Exception("Game dates do not match")

    espn_vegas_lines = driver.find_elements_by_class_name('Table__TR')

    spread_predictions = get_and_format_vegas_line(
        espn_vegas_lines, predictions, seventysixers_to_sixers, normal_round)

    print(json.dumps(spread_predictions, indent=4))

    matchups = []
    matchup_cache = {}
    db_row = {}
    teams_in_current_matchup = 1
    for team in spread_predictions:
        if "favoredBy" in spread_predictions[team]:
            db_row["favored_team"] = team
        if "avgMinusSpread" in spread_predictions[team]:
            db_row["favored_team"] = team
            db_row["vegas_line"] = spread_predictions[team]["favoredBy"]
            matchup_cache["avg_minus_spread"] = spread_predictions[team]["avgMinusSpread"]
            matchup_cache["dog_pick"] = team
        if teams_in_current_matchup == 1:
            db_row["away_team"] = team
            db_row["away_predicted"] = spread_predictions[team]["average"]
        if teams_in_current_matchup == 2:
            db_row["home_team"] = team
            db_row["home_predicted"] = spread_predictions[team]["average"]
            spread = abs(db_row["vegas_line"])
            pick = ""
            if db_row["favored_team"] == team:
                # home team is favorite
                if spread_predictions[team]["avgMinusSpread"]:
                    if spread_predictions[team]["avgMinusSpread"] - db_row["away_predicted"] > 0:
                        pick = f"{team} -{spread}"
                    elif spread_predictions[team]["avgMinusSpread"] - db_row["away_predicted"] < 0:
                        dog = db_row["away_team"]
                        pick = f"{dog} +{spread}"
                    else:
                        pick = "PUSH"
                    db_row["pick"] = pick
            else:
                # away team is favorite
                away_team = db_row["away_team"]
                if matchup_cache["avg_minus_spread"] - spread_predictions[team]["average"] < 0:
                    pick = f"{team} +{spread}"
                elif matchup_cache["avg_minus_spread"] - spread_predictions[team]["average"] > 0:
                    pick = f"{away_team} -{spread}"
                else:
                    pick = "PUSH"
                db_row["pick"] = pick
        if teams_in_current_matchup == 2:
            db_row["game_date"] = todays_date
            matchups.append(db_row)
            db_row = {}
            matchup_cache = {}
            teams_in_current_matchup = 1
        else:
            teams_in_current_matchup += 1

    print(json.dumps(matchups, indent=4))

    ############################################
    # ADD TO DB
    ############################################
    cur = config.cursor
    conn = config.conn

    year = DateFormatter.get_current_year()
    create_table = (
        f"""
        CREATE TABLE IF NOT EXISTS nba_{year}(
        game_date VARCHAR(255),
        away_team VARCHAR(255),
        away_predicted decimal,
        home_team VARCHAR(255),
        home_predicted decimal,
        vegas_line decimal,
        favored_team VARCHAR(255),
        pick VARCHAR(255)
        )
        """
    )

    cur.execute(create_table)
    conn.commit()

    for column in matchups:
        insert_command = f"""INSERT INTO nba_{year} (away_team, away_predicted, favored_team, vegas_line, home_team, home_predicted, pick, game_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        insert_values = (column["away_team"], column["away_predicted"], column["favored_team"],
                         column["vegas_line"], column["home_team"], column["home_predicted"], column["pick"], column["game_date"])
        cur.execute(insert_command, insert_values)

    conn.commit()
    print('Row Inserted')

except TimeoutException:
    print(str(TimeoutException))
    driver.quit()

finally:
    driver.quit()
