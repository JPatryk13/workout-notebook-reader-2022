import unittest
from split_sets import SplitSets


class TestSplitSetsVarReps(unittest.TestCase):
    def test_clean_input(self) -> None:
        input_sets = "72x5+5+12"
        expected = [(5, 72.0), (5, 72.0), (12, 72.0)]
        actual = SplitSets(input_sets).var_reps()
        self.assertEqual(expected, actual)

    def test_bar_plus_weight(self) -> None:
        input_sets = "10+20x5+5+8"
        expected = [(5, 30.0), (5, 30.0), (8, 30.0)]
        actual = SplitSets(input_sets).var_reps()
        self.assertEqual(expected, actual)

    def test_fraction_weight(self) -> None:
        input_sets = "81.6x5+5+8"
        expected = [(5, 81.6), (5, 81.6), (8, 81.6)]
        actual = SplitSets(input_sets).var_reps()
        self.assertEqual(expected, actual)

    def test_fraction_rep(self) -> None:
        input_sets = "72x5+5+12.5"
        expected = [(5, 72.0), (5, 72.0), (12, 72.0)]
        actual = SplitSets(input_sets).var_reps()
        self.assertEqual(expected, actual)

    def test_one_set(self) -> None:
        input_sets = "72x5"
        expected = [(5, 72.0)]
        actual = SplitSets(input_sets).var_reps()
        self.assertEqual(expected, actual)

    def test_one_set_no_reps(self) -> None:
        input_sets = "72x"
        expected = [(0, 72.0)]
        actual = SplitSets(input_sets).var_reps()
        self.assertEqual(expected, actual)

    def test_one_set_just_weight(self) -> None:
        input_sets = "72"
        expected = [(0, 72.0)]
        actual = SplitSets(input_sets).var_reps()
        self.assertEqual(expected, actual)


class TestSplitSetsVarWeight(unittest.TestCase):
    def test_clean_input(self) -> None:
        input_sets = "5x40,60,70,80"
        expected = [(5, 40.0), (5, 60.0), (5, 70.0), (5, 80.0)]
        actual = SplitSets(input_sets).var_weight()
        self.assertEqual(expected, actual)

    def test_guess_bar_plus_weight(self) -> None:
        input_sets = "5x7+10,27,47,57"
        expected = [(5, 17.0), (5, 27.0), (5, 47.0), (5, 57.0)]
        actual = SplitSets(input_sets).var_weight()
        self.assertEqual(expected, actual)

    def test_explicit_bar_plus_weight(self) -> None:
        input_sets = "5x7+10,7+20,7+40,7+50"
        expected = [(5, 17.0), (5, 27.0), (5, 47.0), (5, 57.0)]
        actual = SplitSets(input_sets).var_weight()
        self.assertEqual(expected, actual)

    def test_fraction_weight(self) -> None:
        input_sets = "5x17.5,27.5,47.5,57.5"
        expected = [(5, 17.5), (5, 27.5), (5, 47.5), (5, 57.5)]
        actual = SplitSets(input_sets).var_weight()
        self.assertEqual(expected, actual)

    def test_one_set(self) -> None:
        input_sets = "5x40"
        expected = [(5, 40.0)]
        actual = SplitSets(input_sets).var_weight()
        self.assertEqual(expected, actual)

    def test_one_set_no_weight(self) -> None:
        input_sets = "5x"
        expected = [(5, 0.0)]
        actual = SplitSets(input_sets).var_weight()
        self.assertEqual(expected, actual)

    def test_one_set_just_reps(self) -> None:
        input_sets = "5"
        expected = [(5, 0.0)]
        actual = SplitSets(input_sets).var_weight()
        self.assertEqual(expected, actual)


class TestSplitSetsVarBoth(unittest.TestCase):
    def test_var_both_all_sets_separate_plus(self) -> None:
        input_sets = "8x60+8x70+6x70"
        expected = [(8, 60.0), (8, 70.0), (6, 70.0)]
        actual = SplitSets(input_sets).var_both()
        self.assertEqual(expected, actual)

    def test_var_both_all_sets_separate_comma(self) -> None:
        input_sets = "8x60,8x70,6x70"
        expected = [(8, 60.0), (8, 70.0), (6, 70.0)]
        actual = SplitSets(input_sets).var_both()
        self.assertEqual(expected, actual)

    def test_var_both_kg_weight(self) -> None:
        input_sets = "8x60kg,8x70kg,6x70kg"
        expected = [(8, 60.0), (8, 70.0), (6, 70.0)]
        actual = SplitSets(input_sets).var_both()
        self.assertEqual(expected, actual)

    def test_var_both_grouped_sets_with_plus(self) -> None:
        input_sets = "5x40,60,70,80+2x90"
        expected = [(5, 40.0), (5, 60.0), (5, 70.0), (5, 80.0), (2, 90.0)]
        actual = SplitSets(input_sets).var_both()
        self.assertEqual(expected, actual)

    def test_var_both_grouped_sets_with_comma(self) -> None:
        input_sets = "5x40,60,70,80,2x90"
        expected = [(5, 40.0), (5, 60.0), (5, 70.0), (5, 80.0), (2, 90.0)]
        actual = SplitSets(input_sets).var_both()
        self.assertEqual(expected, actual)

    def test_var_both_fraction_weight(self) -> None:
        input_sets = "8x67.5+8x77.5+6x77.5"
        expected = [(8, 67.5), (8, 77.5), (6, 77.5)]
        actual = SplitSets(input_sets).var_both()
        self.assertEqual(expected, actual)

    def test_var_both_fraction_reps(self) -> None:
        input_sets = "8.5x60+8x70+6.5x70"
        expected = [(8, 60), (8, 70), (6, 70)]
        actual = SplitSets(input_sets).var_both()
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
