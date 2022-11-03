import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch, Mock
from group_exercise_names import GroupExerciseNames


class TestGroupExerciseNames(unittest.TestCase):
    def setUp(self) -> None:
        self.filepath = Path(__file__).resolve().parent.parent / "input/test_input/exercise_names_test.json"
        self.data = {
            "bench press": ["bench press", "bench"],
            "sitting low row": ["sitting low row", "sitting row", "low row", "low rows"],
            "squat": ["squat", "barbell squat"]
        }
        with open(self.filepath, 'w') as f:
            json.dump(self.data, f)

        self.exercise_list = ["deadlift", "sitting row (cables)", "kettle bell not-swing swings"]
        self.group_names = GroupExerciseNames(self.exercise_list, filename=self.filepath)

    def tearDown(self) -> None:
        os.remove(self.filepath)

    def test__read_file(self) -> None:
        expected = self.data
        actual = self.group_names.exercise_names_dict
        self.assertEqual(expected, actual)

    @patch('builtins.input', lambda *args: "0")
    def test__ask_user_new_exercise_with_same_name(self) -> None:
        expected = self.exercise_list[0]
        actual = self.group_names._get_exercise_name(self.exercise_list[0])
        self.assertEqual(expected, actual)

    @patch('builtins.input', lambda *args: "2")
    def test__ask_user_existing_exercise_new_alias(self) -> None:
        expected = "sitting low row"
        actual = self.group_names._get_exercise_name(self.exercise_list[1])
        self.assertEqual(expected, actual)

    @patch('builtins.input', lambda *args: "kettlebell front raise")
    def test__ask_user_alias_for_new_exercise(self) -> None:
        expected = "kettlebell front raise"
        actual = self.group_names._get_exercise_name(self.exercise_list[2])
        self.assertEqual(expected, actual)

    def test_update_exercise_names(self) -> None:
        input_mock = Mock()
        input_mock.side_effect = ["0", "2", "kettlebell front raise"]

        with patch('builtins.input', input_mock) as mf:
            self.group_names.update_exercise_names()

        expected = {
            "bench press": ["bench press", "bench"],
            "sitting low row": ["sitting low row", "sitting row", "low row", "low rows", "sitting row (cables)"],
            "squat": ["squat", "barbell squat"], "deadlift": ["deadlift"],
            "kettlebell front raise": ["kettle bell not-swing swings"]
        }
        actual = self.group_names.exercise_names_dict
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
