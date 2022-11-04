from typing import Optional
from datetime import date, time, datetime, timedelta
import re
from pathlib import Path
import os
import json


def date_string_to_list(date_str: str) -> list[int]:
    """
    Convert strings such as "01/02/2022" or "01/02/22 some notes here" to a list of integers discarding any stuff
    written at the end.
    :param str date_str: string containing date of the format d/m/y where d is day, m is month - both can be expressed
    as two decimals or one, y is year that can be expressed with two or four decimals.
    :return: list of integers [d, m, y] with full year given
    """
    error_msg = "Given string {date_str} is not correct format."

    if len(date_str.split('/')) >= 3:
        day_str, month_str, ending = date_str.split('/')[:4]
    else:
        raise Exception(error_msg)

    # check if ear is present in the ending part of the string
    if len(ending) >= 4 and ending[:4].isdigit():
        year_str = ending[:4]
    elif len(ending) >= 3 and ending[:3].isdigit():
        raise Exception(error_msg)
    elif len(ending) >= 2 and ending[:2].isdigit():
        year_str = "20" + ending[:2]
    else:
        raise Exception(error_msg)

    return [int(day_str), int(month_str), int(year_str)]


class WorkoutDictBuilder:
    def __init__(self):
        self.workout_dict = {
            "date": None,
            "exercises": {
                "main": {}
            }
        }
        self.latest_section_added = "main"
        self.latest_exercise_added = ""

    def _find_exercise_section(self, exercise_name: str) -> Optional[str]:
        """
        Check if given exercise exists in the self.workout_dict and return section name if it does or None otherwise.
        """
        for section_key, section in self.workout_dict["exercises"].items():
            if exercise_name in section.keys():
                return section_key

    def add_date(self, date_str: str) -> None:
        """
        Use the conversion provided in date_string_to_list() and save the date in the workout_dict using datetime.date.
        :param date_str: string containing date of the format d/m/y
        """
        date_list = date_string_to_list(date_str)
        # noinspection PyTypedDict
        self.workout_dict["date"] = date(date_list[2], date_list[1], date_list[0])

    def add_section(self, section_name: str) -> None:
        section_name = re.search(r"[A-Za-z]+", section_name).group()  # clean the string
        if section_name not in self.workout_dict["exercises"].keys():
            self.workout_dict["exercises"][section_name] = {}
        self.latest_section_added = section_name

    def add_exercise(self, exercise_name: str) -> None:
        if self._find_exercise_section(exercise_name):
            self.latest_section_added = self._find_exercise_section(exercise_name)
        else:
            self.workout_dict["exercises"][self.latest_section_added][exercise_name] = []

        self.latest_exercise_added = exercise_name

    def add_sets(self, sets_list: list, exercise_name: Optional[str] = None) -> None:
        if exercise_name:
            self.latest_section_added = self._find_exercise_section(exercise_name)
            self.latest_exercise_added = exercise_name

        self.workout_dict["exercises"][self.latest_section_added][self.latest_exercise_added] += sets_list

    def save_dict(self, *, filename: Optional[str] = None) -> None:
        path = Path(__file__).resolve().parent / "output" / "workouts"
        # exclude filenames that have different format
        filenames = [str(x)[:-5] for x in os.listdir(path) if '.json' in str(x) and str(x[:-5]).isdigit()]
        if not filename:
            if self.workout_dict["date"]:
                # convert date to the filename date part
                date_filename = datetime.combine(self.workout_dict["date"], time()).strftime("%Y%m%d")
                # find filenames with the same dates in it
                same_date_filenames = [f for f in filenames if date_filename in f]
                if same_date_filenames:
                    filename = str(max([int(x) for x in same_date_filenames]) + 1) + '.json'
                else:
                    filename = date_filename + '01.json'
            else:
                most_recent_workout = max([int(x) for x in filenames])  # find most recently added workout
                # extract year, month and day from the string and convert to integers
                year = int(str(most_recent_workout)[:-2][0:4])
                month = int(str(most_recent_workout)[:-2][4:6])
                day = int(str(most_recent_workout)[:-2][6:])
                # convert integers to date and add one day, then save as a valid-format filename (string)
                filename = (datetime.combine(date(year, month, day), time()) + timedelta(days=1)).strftime("%Y%m%d") + '01.json'

        with open(path / filename, 'w') as f:
            json.dump(self.workout_dict, f, default=str)
