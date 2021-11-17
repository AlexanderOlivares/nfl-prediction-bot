# NFL Prediction Bot

##### A web scraper that gets NFL predicted scores for each team and averages them to determine which team is a better pick against the Vegas points spread

#### How to run this script

To run on your computer clone the "scraper_only" branch

```
git clone -b scraper_only --single-branch https://github.com/AlexanderOlivares/nfl-prediction-bot.git
```

Additionally, install [pyfiglet](https://pypi.org/project/pyfiglet/0.7/)

```
pip install pyfiglet
```

#### Sites Scraped

For Predictions

- [OddShark](https://www.oddsshark.com/)
- [dRatings](https://www.dratings.com/)
- [PredictEm](https://www.predictem.com/)

For Schedule and Vegas Lines

- [NFL](https://www.nfl.com/)
- [ESPN](https://www.espn.com/)

#### Format of Raw Data Output

Raw data is formatted as an array of objects. Each array item contains a current week NFL matchup. The favored team will have the additional properties of "favoredBy" and "avgMinusSpread" to provide betting odds context.

```
[
 	{
		awayTeam: {
			"dRatings": score,
			"predictEm": score,
			"oddShark": score,
			"average": avg of three predicted scores
			"favoredBy": -vegasLine,
			avgMinusSpread": avg - favoredBy
		}
 	},
 	{
		homeTeam: {
			"dRatings": score,
			"predictEm": score,
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
Cowboys -10
Panthers +3
```

Cowboys are predicted to win by more than 10
Panthers predicted to win or lose by less than 3

#### Technologies Used

- Selenium
- Chromedriver
- PostgreSQL (psycopg2)

##### Disclaimer

**_This is not gambling advice this is for entertainment purposes only_**
