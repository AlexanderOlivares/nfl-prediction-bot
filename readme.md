# NFL Prediction Bot

View the [live site](https://sports-prediction-bot.herokuapp.com/)

##### A web scraper that gets NBA and NFL predicted scores for each team and averages them to determine which team is a better pick against the Vegas points spread

#### How to run this script

To run on your computer clone the "scraper_only" branch

```
git clone -b scraper_only --single-branch https://github.com/AlexanderOlivares/nfl-prediction-bot.git
```

Install dependencies
`pip install -r requirements.txt`

Download the [Chromedriver](https://chromedriver.chromium.org/downloads) version corresponding to your currnet version of Google Chrome

Run the script
`python3 nba_scraper.py`
or
`python3 nflScraper.py`

#### Sites Scraped

For Predictions

- [OddShark](https://www.oddsshark.com/)
- [dRatings](https://www.dratings.com/)

For Schedule and Vegas Lines

- [NFL](https://www.nfl.com/)
- [ESPN](https://www.espn.com/)

#### Format of Raw Data Output

###### NFL

Raw NFL data is formatted as a list of dictionaries. Each list item contains a matchup. The favored team will have the additional properties of "favoredBy" and "avgMinusSpread" to provide betting odds context.

```
[
    {
        awayTeam: {
            "oddShark": score,
            "dRatings": score,
            "average": avg of the predicted scores
            "favoredBy": Vegas line,
            avgMinusSpread": avg - Vegas line
        }
        homeTeam: {
            "oddShark": score,
            "dRatings": score,
            "average": avg of the predicted scores
        }
    }
]
```

###### Pick Format

Final NFL picks will display the team name of the predicted winner against the spread.

Example:

```
Picks
-----------
Cowboys -10
Panthers +3
```

Above the Cowboys are predicted to win by more than 10 and the Panthers are predicted to win or lose by less than 3

###### NBA

Below is a preview of the raw NBA data format that will print to the console.

```
{
    "favored_team": "Hawks",
    "vegas_line": 5.5,
    "away_team": "Hawks",
    "away_predicted": 114,
    "home_team": "Magic",
    "home_predicted": 106,
    "pick": "Hawks -5.5",
    "game_date": "February 16"
}
    `
```

#### Technologies Used

- Selenium
- Chromedriver
- PostgreSQL (psycopg2)

######**_This is not gambling advice this is for entertainment purposes only_**
