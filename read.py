import re
from read_file import ReadFile
from extract_data import ExtractData
from split_sets import SplitSets
from group_exercise_names import GroupExerciseNames
from workout_dict_builder import WorkoutDictBuilder
from ask_user import yes_or_no
import pprint as pp
import argparse


def read(filename: str, *, _print: bool = False):
    workout_list = ReadFile(filename).split_content()
    workout_name_tracker = GroupExerciseNames()
    for workout in workout_list:
        workout_dict = WorkoutDictBuilder()
        workout_dict.add_date(workout[0])
        for line in workout[1:]:
            # identify if the line contains a name of the section
            potentially_section_name = re.sub(r"s", "", re.search(r"[a-z]+", line.lower()).group())
            if potentially_section_name in ['extra', 'alternative']:
                workout_dict.add_section(potentially_section_name)
            elif not re.search(r"\d+", line.lower()) and re.search(r"[a-z:]+", line.lower()).group() == line:
                # problematic lines are solved manually
                if yes_or_no(f"Is the line {line} in workout {workout} a section name?"):
                    section_name = input("Rewrite section name: ").lower()
                else:
                    continue
            else:
                # skip jogging because I didn't sort that one yet
                if 'jog' not in line.lower():
                    exercise_alias = ExtractData(line).exercise_name()  # get name as is in the file
                    exercise_name = workout_name_tracker.get_alias(exercise_alias)  # generalise/assign alias
                    workout_dict.add_exercise(exercise_name)  # add exercise to the dictionary
                    sets_list = SplitSets(ExtractData(line).reps()).get_list()
                    workout_dict.add_sets(sets_list)  # add sets to the exercise
        if _print:
            pp.pprint(workout)
            pp.pprint(workout_dict.workout_dict)
        workout_dict.save_dict()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename')  # initial_21102022.txt
    parser.add_argument('-p', '--print', default=False)
    args = parser.parse_args()

    read("input/" + args.filename, _print=args.print)
