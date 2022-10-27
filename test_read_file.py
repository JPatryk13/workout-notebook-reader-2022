import unittest
from read_file import ReadFile, is_date


class TestReadFile(unittest.TestCase):
    def test_is_date_just_date(self) -> None:
        actual = is_date("12/06/2014")
        self.assertTrue(actual)

    def test_is_date_no_date(self) -> None:
        actual = is_date("This/ is not / a date/")
        self.assertFalse(actual)

    def test_is_date_date_plus_some_text(self) -> None:
        actual = is_date("Date: 12/06/2014 B")
        self.assertTrue(actual)

    def test_is_date_invalid_date(self) -> None:
        actual = is_date("38/07/2014")
        self.assertFalse(actual)

    def test_split_content_empty_file(self) -> None:
        expected = []
        actual = ReadFile("input/test_input/empty_file.txt").split_content()
        self.assertEqual(expected, actual)

    def test_split_content_single_workout(self) -> None:
        expected = [[
            "17/09/22 B",
            "Squat: 70x5+5+9",
            "Bench: 70x5+6+12",
            "Sitting low row: 59x5+5+11"
        ]]
        actual = ReadFile("input/test_input/single_workout.txt").split_content()
        self.assertEqual(expected, actual)

    def test_split_content_workouts_and_redundant_content(self) -> None:
        expected = [
            [
                "17/09/22 B",
                "Squat: 70x5+5+9",
                "Bench: 70x5+6+12",
                "Sitting low row: 59x5+5+11"
            ],
            [
                "20/09/22 A",
                "Lat pulldown: 70.6*x5+5+8",
                "Deadlift: 70x5+5+13",
                "Overhead press: 40x5+5+6",
                "Extras:",
                "Biceps curly bar: 7.5+20x5+5+8"
            ]
        ]
        actual = ReadFile("input/test_input/workouts_and_redundant_content.txt").split_content()
        self.assertEqual(expected, actual)

    def test_split_content_just_redundant_content(self) -> None:
        expected = []
        actual = ReadFile("input/test_input/just_redundant_content.txt").split_content()
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
