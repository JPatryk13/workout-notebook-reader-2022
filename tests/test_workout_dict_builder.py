import os
import unittest
from workout_dict_builder import WorkoutDictBuilder, date_string_to_list
from datetime import date
from pathlib import Path


class TestWorkoutDictBuilder(unittest.TestCase):
    def setUp(self) -> None:
        self.output_dir_path = Path(__file__).resolve().parent.parent / "output/"
        self.files_to_be_removed = []
        self.workout = WorkoutDictBuilder()

    def tearDown(self) -> None:
        for path in self.files_to_be_removed:
            os.remove(path)

    def test_init_workout_dict(self) -> None:
        expected = {
            "date": None,
            "exercises": {
                "main": {}
            }
        }
        actual = self.workout.workout_dict
        self.assertEqual(expected, actual)

    def test_date_string_to_list_just_date(self) -> None:
        test_input = "01/02/2022"
        expected = [1, 2, 2022]
        actual = date_string_to_list(test_input)
        self.assertEqual(expected, actual)

    def test_date_string_to_list_date_with_letter(self) -> None:
        test_input = "01/02/2022 A"
        expected = [1, 2, 2022]
        actual = date_string_to_list(test_input)
        self.assertEqual(expected, actual)

    def test_date_string_to_list_date_with_letter_no_space(self) -> None:
        test_input = "01/02/2022A"
        expected = [1, 2, 2022]
        actual = date_string_to_list(test_input)
        self.assertEqual(expected, actual)

    def test_date_string_to_list_date_with_some_notes(self) -> None:
        test_input = "01/02/2022 some notes here"
        expected = [1, 2, 2022]
        actual = date_string_to_list(test_input)
        self.assertEqual(expected, actual)

    def test_date_string_to_list_just_year_ending(self) -> None:
        test_input = "01/02/22"
        expected = [1, 2, 2022]
        actual = date_string_to_list(test_input)
        self.assertEqual(expected, actual)

    def test_date_string_to_list_day_no_zero(self) -> None:
        test_input = "1/02/22"
        expected = [1, 2, 2022]
        actual = date_string_to_list(test_input)
        self.assertEqual(expected, actual)

    def test_date_string_to_list_month_no_zero(self) -> None:
        test_input = "01/2/22"
        expected = [1, 2, 2022]
        actual = date_string_to_list(test_input)
        self.assertEqual(expected, actual)

    def test_date_string_to_list_day_and_month_no_zero(self) -> None:
        test_input = "1/2/22"
        expected = [1, 2, 2022]
        actual = date_string_to_list(test_input)
        self.assertEqual(expected, actual)

    def test_add_date(self) -> None:
        test_input = "01/02/2022"
        self.workout.add_date(test_input)
        expected = {
            "date": date(2022, 2, 1),
            "exercises": {
                "main": {}
            }
        }
        actual = self.workout.workout_dict
        self.assertEqual(expected, actual)

    def test_add_section_just_section_name(self) -> None:
        test_input = "extras"
        self.workout.add_section(test_input)
        expected = {
            "date": None,
            "exercises": {
                "main": {},
                "extras": {}
            }
        }
        actual = self.workout.workout_dict
        self.assertEqual(expected, actual)

    def test_add_section_double_colon(self) -> None:
        test_input = "extras:"
        self.workout.add_section(test_input)
        expected = {
            "date": None,
            "exercises": {
                "main": {},
                "extras": {}
            }
        }
        actual = self.workout.workout_dict
        self.assertEqual(expected, actual)

    def test_add_section_that_already_exists(self) -> None:
        test_input = "main"
        self.workout.add_section(test_input)
        expected = {
            "date": None,
            "exercises": {
                "main": {}
            }
        }
        actual = self.workout.workout_dict
        self.assertEqual(expected, actual)

    def test__find_exercise_section_main_section(self):
        test_input = "bench press"
        self.workout.add_exercise(test_input)
        expected = "main"
        actual = self.workout._find_exercise_section(test_input)
        self.assertEqual(expected, actual)

    def test__find_exercise_section_added_section(self):
        test_input = "bench press"
        self.workout.add_section("extras")
        self.workout.add_exercise(test_input)
        expected = "extras"
        actual = self.workout._find_exercise_section(test_input)
        self.assertEqual(expected, actual)

    def test__find_exercise_section_no_section(self):
        expected = None
        actual = self.workout._find_exercise_section("extras")
        self.assertEqual(expected, actual)

    def test_add_exercise_no_section_defined(self) -> None:
        test_input = "bench press"
        self.workout.add_exercise(test_input)
        expected = {
            "date": None,
            "exercises": {
                "main": {
                    "bench press": []
                }
            }
        }
        actual = self.workout.workout_dict
        self.assertEqual(expected, actual)

    def test_add_exercise_after_defining_section(self) -> None:
        test_input = "lat pulldown (biceps undergrip)"
        self.workout.add_section("extras")
        self.workout.add_exercise(test_input)
        expected = {
            "date": None,
            "exercises": {
                "main": {},
                "extras": {
                    "lat pulldown (biceps undergrip)": []
                }
            }
        }
        actual = self.workout.workout_dict
        self.assertEqual(expected, actual)

    def test_add_sets(self) -> None:
        test_input = [(5, 80.0), (5, 80.0), (12, 80.0)]
        self.workout.add_exercise("bench press")
        self.workout.add_sets(test_input)
        expected = {
            "date": None,
            "exercises": {
                "main": {
                    "bench press": [(5, 80.0), (5, 80.0), (12, 80.0)]
                }
            }
        }
        actual = self.workout.workout_dict
        self.assertEqual(expected, actual)

    def test_add_date_again(self) -> None:
        self.workout.add_date("01/02/2022")
        self.workout.add_date("20/05/2021")
        expected = {
            "date": date(2021, 5, 20),
            "exercises": {
                "main": {}
            }
        }
        actual = self.workout.workout_dict
        self.assertEqual(expected, actual)

    def test_add_exercise_to_different_section(self) -> None:
        self.workout.add_section("extras")
        self.workout.add_section("main")
        self.workout.add_exercise("bench press")
        expected = {
            "date": None,
            "exercises": {
                "main": {
                    "bench press": []
                },
                "extras": {}
            }
        }
        actual = self.workout.workout_dict
        self.assertEqual(expected, actual)

    def test_add_exercise_doubled_name_same_section(self) -> None:
        self.workout.add_exercise("bench press")
        self.workout.add_exercise("bench press")
        expected = {
            "date": None,
            "exercises": {
                "main": {
                    "bench press": []
                }
            }
        }
        actual = self.workout.workout_dict
        self.assertEqual(expected, actual)

    def test_add_exercise_doubled_name_different_section(self) -> None:
        self.workout.add_exercise("bench press")
        self.workout.add_section("extras")
        self.workout.add_exercise("bench press")
        expected = {
            "date": None,
            "exercises": {
                "main": {
                    "bench press": []
                },
                "extras": {}
            }
        }
        actual = self.workout.workout_dict
        self.assertEqual(expected, actual)

    def test_add_sets_doubled_exercise_same_section(self) -> None:
        self.workout.add_exercise("bench press")
        self.workout.add_sets([(5, 80.0), (5, 80.0), (12, 80.0)])
        self.workout.add_exercise("bench press")
        self.workout.add_sets([(5, 75.0), (5, 75.0)])
        expected = {
            "date": None,
            "exercises": {
                "main": {
                    "bench press": [(5, 80.0), (5, 80.0), (12, 80.0), (5, 75.0), (5, 75.0)]
                }
            }
        }
        actual = self.workout.workout_dict
        self.assertEqual(expected, actual)

    def test_add_sets_doubled_exercise_different_section(self) -> None:
        self.workout.add_exercise("bench press")
        self.workout.add_sets([(5, 80.0), (5, 80.0), (12, 80.0)])
        self.workout.add_section("extras")
        self.workout.add_exercise("bench press")
        self.workout.add_sets([(5, 70.0), (5, 70.0)])
        expected = {
            "date": None,
            "exercises": {
                "main": {
                    "bench press": [(5, 80.0), (5, 80.0), (12, 80.0), (5, 70.0), (5, 70.0)]
                },
                "extras": {}
            }
        }
        actual = self.workout.workout_dict
        self.assertEqual(expected, actual)

    def test_add_sets_different_exercise_same_section(self) -> None:
        self.workout.add_exercise("bench press")
        self.workout.add_sets([(5, 80.0), (5, 80.0), (12, 80.0)])
        self.workout.add_exercise("biceps curls")
        self.workout.add_sets([(10, 25.5)])
        self.workout.add_sets([(5, 70.0), (5, 70.0)], "bench press")
        expected = {
            "date": None,
            "exercises": {
                "main": {
                    "bench press": [(5, 80.0), (5, 80.0), (12, 80.0), (5, 70.0), (5, 70.0)],
                    "biceps curls": [(10, 25.5)]
                }
            }
        }
        actual = self.workout.workout_dict
        self.assertEqual(expected, actual)

    def test_add_sets_different_exercise_different_section(self) -> None:
        self.workout.add_exercise("bench press")
        self.workout.add_sets([(5, 80.0), (5, 80.0), (12, 80.0)])
        self.workout.add_section("extras")
        self.workout.add_exercise("biceps curls")
        self.workout.add_sets([(10, 25.5)])
        self.workout.add_sets([(5, 70.0), (5, 70.0)], "bench press")
        expected = {
            "date": None,
            "exercises": {
                "main": {
                    "bench press": [(5, 80.0), (5, 80.0), (12, 80.0), (5, 70.0), (5, 70.0)]
                },
                "extras": {
                    "biceps curls": [(10, 25.5)]
                }
            }
        }
        actual = self.workout.workout_dict
        self.assertEqual(expected, actual)

    def test_save_dict_default_name_file_not_exit(self) -> None:
        input_date = "20/05/2022"
        self.workout.add_date(input_date)
        self.workout.save_dict()  # save dictionary to a default-named json file
        path = self.output_dir_path / "workouts" / "2022052001.json"  # generate path to the file
        self.files_to_be_removed.append(path)  # add the path to to-remove list
        path_obj = Path(path)  # create path object
        self.assertTrue(path_obj.is_file())  # verify if the file exists

    def test_save_dict_default_name_file_already_exists(self) -> None:
        input_date = "20/05/2022"
        self.workout.add_date(input_date)
        self.workout.save_dict()  # save first dictionary to a default-named json file
        second_workout_dict = WorkoutDictBuilder()
        second_workout_dict.add_date(input_date)
        second_workout_dict.save_dict()  # save second dictionary with the same date
        # generate path for each file
        path1 = self.output_dir_path / "workouts" / "2022052001.json"
        path2 = self.output_dir_path / "workouts" / "2022052002.json"
        # add both paths to the to-remove list
        self.files_to_be_removed.append(path1)
        self.files_to_be_removed.append(path2)
        # create path objects for each file
        path_obj1 = Path(path1)
        path_obj2 = Path(path2)
        # verify existence of each file
        self.assertTrue(path_obj1.is_file())
        self.assertTrue(path_obj2.is_file())

    def test_save_dict_custom_name(self) -> None:
        input_date = "20/05/2022"
        input_name = "some_custom_name.json"
        self.workout.add_date(input_date)
        self.workout.save_dict(filename=input_name)  # save the dictionary to a custom-named json file
        path = self.output_dir_path / "workouts" / input_name  # generate path to the file
        self.files_to_be_removed.append(path)  # add the path to to-remove list
        path_obj = Path(path)  # create path object
        self.assertTrue(path_obj.is_file())  # verify if the file exists

    def test_save_dict_no_date_specified(self) -> None:
        workout_dict_1 = WorkoutDictBuilder()
        workout_dict_1.add_date("29/10/2022")
        workout_dict_1.save_dict()  # save first workout as 2022112901.json
        workout_dict_2 = WorkoutDictBuilder()
        workout_dict_2.add_date("31/10/2022")
        workout_dict_2.save_dict()  # save first workout as 2022113101.json
        self.workout.save_dict()  # save the third workout without given date 2022120101.json
        path = self.output_dir_path / "workouts" / "2022110101.json"  # generate path to the file
        self.files_to_be_removed.append(path)  # add the path to to-remove list
        path_obj = Path(path)  # create path object
        self.assertTrue(path_obj.is_file())  # verify if the file exists


if __name__ == "__main__":
    unittest.main()
