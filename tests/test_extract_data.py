from extract_data import ExtractData
import unittest


class TestExtractData(unittest.TestCase):
    """
    The class tests exercise_name(), reps() method against cases listed in self.input_lines.
    """

    def setUp(self) -> None:
        self.input_lines = [
            "Overhead press: 43x5+5+8",
            "Overhead press 43x5+5+8",
            "Overhead press 43 x 5+5+  8",
            "Overhead press: (20+23)x5+5+8",
            "Overhead press (20+23)x5+5+8",
            "Overhead press (some notes) (20+23)x5+5+8",
            "Overhead press (some notes): (20+23)x5+5+8",
            "Overhead press 43x5+5+8 (dump it)",
            "Overhead press 43x5+5+8 dump it",
            "Overhead press (20+23)x5+5, (20+23)+8 (dump it)"
        ]

    def test_exercise_name(self) -> None:
        for i, line in enumerate(self.input_lines):
            if "(some notes)" in line:
                expected = "overhead press (some notes)"
            else:
                expected = "overhead press"
            actual = ExtractData(line).exercise_name()
            self.assertEqual(expected, actual)

    def test_reps(self) -> None:
        expected = ["43x5+5+8"] * 3 + ["20+23x5+5+8"] * 4 + ["43x5+5+8"] * 2 + ["20+23x5+5,20+23+8"]
        for i, line in enumerate(self.input_lines):
            actual = ExtractData(line).reps()
            self.assertEqual(expected[i], actual)


if __name__ == "__main__":
    unittest.main()
