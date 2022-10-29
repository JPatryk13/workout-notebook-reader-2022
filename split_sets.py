from math import floor
import re


class SplitSets:
    def __init__(self, sets) -> None:
        self.sets = sets

    def var_reps(self) -> list[tuple[int, float]]:
        """
        Convert following strings:
            1. 72x5+5+12
            2. 10+20x5+5+8
            3. 81.6x5+5+8
            4. 72x5+5+12.5
            5. 72x5
            6. 72x
            7. 72
        To lists:
            1. [(5, 72.0), (5, 72.0), (12, 72.0)]
            2. [(5, 30.0), (5, 30.0), (8, 30.0)]
            3. [(5, 81.6), (5, 81.6), (8, 81.6)]
            4. [(5, 72.0), (5, 72.0), (12, 72.0)]
            5. [(5, 72.0)]
            6-7. [(0, 72.0)]
        The left side (to the 'x') of the string is weight. The right side is number of reps.
        """
        # consider the case #7
        if 'x' in self.sets:
            str_weight, str_reps = self.sets.split('x')
        else:
            str_weight = self.sets
            str_reps = ''

        # sort out weights-side of the string
        if '+' in str_weight:
            float_weight = sum([float(w) for w in str_weight.split('+')])
        else:
            float_weight = float(str_weight)

        # split and convert reps
        if '+' in str_reps:
            int_reps_list = [int(floor(float(r))) for r in str_reps.split('+')]
        elif ',' in str_reps:
            int_reps_list = [int(floor(float(r))) for r in str_reps.split(',')]
        elif str_reps == '':
            int_reps_list = [0]
        else:
            int_reps_list = [int(floor(float(str_reps)))]

        # couple up weights and reps
        sets_list = []
        for reps in int_reps_list:
            sets_list.append((reps, float_weight))

        return sets_list

    def var_weight(self) -> list[tuple[int, float]]:
        """
        Convert following strings:
            1. 5x40,60,70,80
            2. 5x7+10,27,47,57
            3. 5x7+10,7+20,7+40,7+50
            4. 5x17.5,27.5,47.5,57.5
            5. 5x40
            6. 5x
            7. 5
        To lists:
            1. [(5, 40.0), (5, 60.0), (5, 70.0), (5, 80.0)]
            2-3. [(5, 17.0), (5, 27.0), (5, 47.0), (5, 57.0)]
            4. [(5, 17.5), (5, 27.5), (5, 47.5), (5, 57.5)]
            5. [(5, 40.0)]
            6-7. [(5, 0.0)]
        The right side (to the 'x') of the string is weight. The left side is number of reps.
        """
        # consider the case #7
        if 'x' in self.sets:
            str_reps, str_weight = self.sets.split('x')
        else:
            str_weight = ''
            str_reps = self.sets

        # split and convert weights - take into account composite weights for some cases
        if ',' in str_weight:
            float_weight_list = []
            for w in str_weight.split(','):
                float_weight_list.append(sum(list(map(lambda x: float(x), w.split('+')))) if '+' in w else float(w))
        elif str_weight == '':
            float_weight_list = [0.0]
        else:
            float_weight_list = [float(str_weight)]

        # couple up weights and reps
        sets_list = []
        for w in float_weight_list:
            sets_list.append((int(str_reps), w))

        return sets_list

    def var_both(self) -> list[tuple[int, float]]:
        """
        Convert following strings:
            1. 8x60+8x70+6x70
            2. 8x60,8x70,6x70
            3. 8x60kg,8x70kg,6x70kg
            4. 5x40,60,70,80+2x90
            5. 5x40,60,70,80,2x90
            6. 8x67.5+8x77.5+6x77.5
            7. 8.5x60+8x70+6.5x70
        To lists:
            1-3. [(8, 60.0), (8, 70.0), (6, 70.0)]
            4-5. [(5, 40.0), (5, 60.0), (5, 70.0), (5, 80.0), (2, 90.0)]
            6. [(8, 67.5), (8, 77.5), (6, 77.5)]
            7. [(8, 60), (8, 70), (6, 70)]
        Here reps are always on the LHS of the 'x'.
        """
        # split sets ang remove mass units if there are any
        str_sets_list = [s.strip('kg') for s in re.split(r"\+|,", self.sets)]

        # separate reps from weights and fill up missing reps
        str_rep_list, str_weight_list = [], []
        last_rep_temp = '0'
        for s in str_sets_list:
            if 'x' in s:
                # update the control variable that stores the last explicit rep number
                last_rep_temp = s.split('x')[0]
                str_rep_list.append(s.split('x')[0])
                str_weight_list.append(s.split('x')[1])
            else:
                str_rep_list.append(last_rep_temp)
                str_weight_list.append(s)

        # convert from strings to appropriate units
        int_rep_list = list(map(lambda x: int(float(x)), str_rep_list))
        float_weight_list = list(map(lambda x: float(x), str_weight_list))

        # couple sets and reps
        sets_list = []
        for i, r in enumerate(int_rep_list):
            sets_list.append((r, float_weight_list[i]))

        return sets_list


if __name__ == "__main__":
    sets_list_1 = ["72x5+5+12", "10+20x5+5+8", "81.6x5+5+8", "72x5+5+12.5", "72x5", "72x", "72"]
    for sets in sets_list_1:
        split_sets = SplitSets(sets).var_reps()

    sets_list_3 = ["8x60+8x70+6x70", "8x60,8x70,6x70", "8x60kg,8x70kg,6x70kg", "5x40,60,70,80+2x90",
                   "5x40,60,70,80,2x90", "8x67.5+8x77.5+6x77.5", "8.5x60+8x70+6.5x70"]
    for sets in sets_list_3:
        split_sets = SplitSets(sets).var_both()
