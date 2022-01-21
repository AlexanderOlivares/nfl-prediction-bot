# NFL Prediction Bot

##### A web scraper that gets NFL predicted scores for each team and averages them to determine which team is a better pick against the Vegas points spread

#### How to run this script

To run on your computer clone the "scraper_only" branch

```
git clone -b scraper_only --single-branch https://github.com/AlexanderOlivares/nfl-prediction-bot.git
```

Install dependencies
`pip install -r requirements.txt`

Download the [Chromedriver](https://chromedriver.chromium.org/downloads) version corresponding to your currnet version of Google Chrome

Run the script
`python3 nflScraper.py`

#### Sites Scraped

For Predictions

- [OddShark](https://www.oddsshark.com/)
- [dRatings](https://www.dratings.com/)

For Schedule and Vegas Lines

- [NFL](https://www.nfl.com/)
- [ESPN](https://www.espn.com/)

#### Format of Raw Data Output

Raw data is formatted as an list of dictionaries. Each list item contains a current week NFL matchup. The favored team will have the additional properties of "favoredBy" and "avgMinusSpread" to provide betting odds context.

```
[
 	{
		awayTeam: {
			"dRatings": score,
			"oddShark": score,
			"average": avg of three predicted scores
			"favoredBy": -vegasLine,
			avgMinusSpread": avg - favoredBy
		}
 	},
 	{
		homeTeam: {
			"dRatings": score,
			"oddShark": score,
			"average": avg of three predicted scores
		}
 	}
]
```

#### Pick Format

Final picks will display the team name of the predicted winner against the spread.

Example:

```
Picks
-----------
Cowboys -10
Panthers +3
```

Above the Cowboys are predicted to win by more than 10 and the Panthers are predicted to win or lose by less than 3

#### Technologies Used

- Selenium
- Chromedriver
- PostgreSQL (psycopg2)

##### Disclaimer

**_This is not gambling advice this is for entertainment purposes only_**
