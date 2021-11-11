CREATE TABLE 2021_nfl_week_9(
	away_team VARCHAR(255) NOT NULL,
	away_predicted VARCHAR(255) NOT NULL,
	home_team VARCHAR(255) NOT NULL,
	home_predicted VARCHAR(255) NOT NULL,
	vegas_line VARCHAR(255) NOT NULL,
	favored_team VARCHAR(255) NOT NULL,
	pick VARCHAR(255) NOT NULL,
	away_actual,
	home_actual,
	ats_result,
	su_result,
);

    # insert_test = """ INSERT INTO test (name, team) VALUES (%s, %s) """
    # insert_vals = ('jaxxy', 'jets')
    # cur.execute(insert_test, insert_vals)
    # conn.commit()
    # print('values added')
