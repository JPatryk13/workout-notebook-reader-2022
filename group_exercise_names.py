import json
import re
from pathlib import Path
from typing import Union


class GroupExerciseNames:
    def __init__(self, exercise_list: list, *, filename: Union[str, Path] = "input/exercise_names.json") -> None:
        self.exercise_list = exercise_list
        self.filename = filename

        with open(self.filename, 'r') as f:
            self.exercise_names_dict = json.load(f)

    def _get_exercise_name(self, exercise_name: str) -> str:
        """
        Ask user to match the given exercise_name to existing or input a new one.
        :return: dictionary key to be used later
        """
        existing_exercises_list = []
        for i, key in enumerate(self.exercise_names_dict.keys()):
            existing_exercises_list.append(f"{str(i + 1)}. '{key}' =?= '{exercise_name}'")
        no_of_existing_exercises = len(existing_exercises_list)
        existing_exercises_str = '\n'.join(existing_exercises_list)

        while True:
            option = input(
                f"Exercise '{exercise_name}' cannot be automatically assigned to any existing. Chose one of the"
                f"following options.\n0. (add new) '{exercise_name}' =?= '{exercise_name}'\n"
                f"{existing_exercises_str}\nSelect number 0 through {no_of_existing_exercises} or type a new"
                f"exercise name: "
            )

            if option.isdigit():
                # number was given
                if option == '0':
                    return exercise_name
                elif 1 <= int(option) <= no_of_existing_exercises:
                    return [*self.exercise_names_dict.keys()][int(option) - 1]
                else:
                    raise ValueError(
                        f"Wrong number was given. Expected range 0-{no_of_existing_exercises}, got {option}"
                        f"instead")
            elif re.search(r'\d+', option):
                while True:
                    keep_name = input(f"Digit(s) found in the given name {option}. Do you want to save the name?"
                                      f"(y/n): ")
                    if keep_name == 'y':
                        return option.lower()
                    elif keep_name == 'n':
                        break
                    else:
                        continue
                continue
            else:
                return option.lower()

    def update_exercise_names(self) -> None:
        """
        Check if exercises provided in the constructor exist as keys or values in the dictionary. if they don't ask user
        to choose either assigning it to the existing exercise as an alias or creating a new one.
        :return: None
        """
        all_exercises = [item for sublist in [*self.exercise_names_dict.values()] for item in sublist]
        for exercise_name in self.exercise_list:
            if exercise_name in all_exercises:
                continue
            else:
                key = self._get_exercise_name(exercise_name)
                if key in [*self.exercise_names_dict.keys()]:
                    self.exercise_names_dict[key].append(exercise_name)
                else:
                    self.exercise_names_dict[key] = [exercise_name]

