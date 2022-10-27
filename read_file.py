import re
from datetime import datetime
import pprint as pp


def is_valid_year(year: str) -> bool:
    # check if the year is greater than the current one
    if len(year) == 2:
        if int(year) > int(datetime.now().strftime('%y')):
            return False
        else:
            return True
    elif len(year) == 4:
        if int(year) > int(datetime.now().strftime('%Y')):
            return False
        else:
            return True
    else:
        # the year has 3 digits = invalid
        return False


def is_valid_month(month: str) -> bool:
    # check if the month is valid
    if 0 < int(month) <= 12:
        return True
    else:
        return False


def is_valid_day(day: str, month: str) -> bool:
    # check if the day is valid
    if int(day) >= 0:
        max_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if int(day) <= max_days[int(month)]:
            return True
        else:
            return False
    else:
        return False


def is_date(_str: str) -> bool:
    """
    Check if the string _str has a date of the format d/m/y where d, m, y are integers.
    :param _str: input string
    :return: True if the input string has a date, False otherwise
    """
    date_match_obj = re.search(r"\d{1,2}/\d{1,2}/\d{2,4}", _str)
    # check if there is a date of the format d/m/y in the string
    if date_match_obj:
        d, m, y = tuple(date_match_obj.group().split('/'))

        if is_valid_year(y) and is_valid_month(m) and is_valid_day(d, m):
            return True
    else:
        return False


class ReadFile:
    """
    Example input "filename.txt" file:

        Workout
        Day A: deadlift, overhead press, lat pulldown/chinups
        Day B: squat, barbell row, bench press

        12/08/22 B
        Bench press: 8x60kg, 8x70kg, 6x70kg (stick to 70)
        Sitting row (cables, two separate handles): 8x45kg, 8x52kg, 6x59kg (stick to 52)
        Squat: 8x60kg, 8x70kg, 5x70kg (stick to 60)

        12/09/22 B
        Squat: 5x40,60,70,80
        Bench: 5x40,60,70,80 + 2x90
        Sitting low row: 5x39,49.6,59,70.6

    Output:

        workout_list = [
            [
                "12/08/22 B",
                "Bench press: 8x60kg, 8x70kg, 6x70kg (stick to 70)",
                "Sitting row (cables, two separate handles): 8x45kg, 8x52kg, 6x59kg (stick to 52)",
                "Squat: 8x60kg, 8x70kg, 5x70kg (stick to 60)"
            ],
            [
                "12/09/22 B",
                "Squat: 5x40,60,70,80",
                "Bench: 5x40,60,70,80 + 2x90",
                "Sitting low row: 5x39,49.6,59,70.6"
            ]
        ]

    Use:

        content = ReadFile("filename.txt")
        workout_list = content.split_content()

    """

    def __init__(self, filename: str) -> None:
        with open(filename, 'r') as f:
            self.workout_diary_content = f.readlines()

    def split_content(self) -> list:
        workout_diary_list = []
        single_workout = []

        for i, line in enumerate(self.workout_diary_content):
            line = line.strip('\n').rstrip(' ')
            if single_workout:
                if not (line == '' or is_date(line)):
                    # append the line if it's not an empty space or date
                    single_workout.append(line)
                if is_date(line) or line == '' or i == len(self.workout_diary_content) - 1:
                    # save previous workout day (if there is any) if the line is one of the following:
                    # 1. date
                    # 2. empty line
                    # 3. last line of the file
                    workout_diary_list.append(single_workout)
                    single_workout = []
            elif not single_workout and is_date(line):
                # start a new workout day if the line is date
                single_workout = [line]
            else:
                continue

        return workout_diary_list


if __name__ == "__main__":
    pp.pprint(ReadFile("input/initial_21102022.txt").split_content())
