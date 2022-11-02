from math import floor
import re
from typing import Callable, Optional, Union


class SplitSets:
    def __init__(self, sets) -> None:
        self.sets = sets

    def _which_varies(self) -> Optional[Callable]:
        """
        Determines which side of the sets string varies. Following cases are considered:
            1.  single 'x', no ','; e.g. "10+20x5+5+8" -> var_reps()
            2.  single 'x', ',' present; e.g. "5x7+10,7+20,7+40,7+50" -> var_weight()
            3.  multiple 'x'; e.g. "5x40,60,70,80,2x90" -> var_both()
            4.  multiple 'x', groups such '2x[0-9]+x[0-9]' are present; convert to '[0-9]+[+][0-9]+x[0-9]' and run
                through the function again
        :return: one of the three functions for splitting sets
        """
        if 'x' in self.sets:
            if self.sets.count('x') > 1:
                product_weight_group = re.search(r"2x[\d.]+x\d", self.sets)
                if product_weight_group:
                    start, end = product_weight_group.span()
                    end -= 2  # exclude 'x\d' from the string
                    weight = self.sets[start:end].split('x')[1]
                    # swap product with sum
                    self.sets = re.sub(self.sets[start:end], weight + '+' + weight, self.sets)
                    return self._which_varies()
                return self.var_both
            else:
                if ',' in self.sets.split('x')[1]:
                    return self.var_weight
                elif self.sets.split('x')[1] == '':
                    return None
                else:
                    return self.var_reps
        else:
            if '+' in self.sets:
                # body-weight exercise with no added weight
                self.sets = '0.0x' + self.sets
                return self._which_varies()
            else:
                return None

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

    def get_list(self) -> Optional[list]:
        method = self._which_varies()
        if method:
            return method()
        else:
            return None


if __name__ == "__main__":
    sets_list_1 = ["72x5+5+12", "10+20x5+5+8", "81.6x5+5+8", "72x5+5+12.5", "72x5", "72x", "72"]
    for sets in sets_list_1:
        split_sets = SplitSets(sets).get_list()

    sets_list_3 = ["8x60+8x70+6x70", "8x60,8x70,6x70", "8x60kg,8x70kg,6x70kg", "5x40,60,70,80+2x90",
                   "5x40,60,70,80,2x90", "8x67.5+8x77.5+6x77.5", "8.5x60+8x70+6.5x70"]
    for sets in sets_list_3:
        split_sets = SplitSets(sets).get_list()
