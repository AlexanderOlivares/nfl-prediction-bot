import re
from datetime import date


class DateFormatter():
    @staticmethod
    def remove_leading_zero(str):
        return str[1:] if str.startswith("0") else str

    def get_todays_date():
        today = date.today()
        month = today.strftime("%B")
        day = DateFormatter.remove_leading_zero(today.strftime("%d")).lower()
        return (f"{month} {day}")

    def get_current_year():
        today = date.today()
        return today.year


def seventysixers_to_sixers(teamname_string):
    return "sixers" if teamname_string == "76ers" else teamname_string


def normal_round(number):
    return int(number + 0.5)


def get_and_format_vegas_line(espn_vegas_lines, predictions, format_outlier_teamname, normal_round):
    for i in espn_vegas_lines:
        team_name_and_data = i.text.split('\n')
        print(team_name_and_data)
        if len(team_name_and_data) == 2:
            full_team_name, data = team_name_and_data
            regex_line_finder = '(?<=\) )\-\d+\.\d{1}'
            line_list = re.findall(regex_line_finder, data)
            if (len(line_list) == 1):
                line = float(line_list[0])
                fav = format_outlier_teamname(full_team_name.split(' ')[-1])
                predictions[fav]["favoredBy"] = line
                predictions[fav]["avgMinusSpread"] = normal_round(
                    predictions[fav]["average"] + line)
    return predictions
