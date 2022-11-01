import re


class ExtractData:
    """
    Example use:
        exercise_name = ExtractData(line).exercise_name()
        str_reps = ExtractData(line).reps()
    """
    def __init__(self, line) -> None:
        self.line = line

    def exercise_name(self) -> str:
        """
        Extracts and cleans exercise name from a string. Any non-digit word followed by a space or double colon and a
        space will be extracted from the given string. The output is lower-case and stripped from any multiple
        consecutive spaces.
        """
        pattern = re.compile(r"\D+\s|(:\s)")
        exercise_name = pattern.search(self.line).group()

        # remove ':' and leading/following spaces
        exercise_name = exercise_name.replace(':', '').strip()
        # remove any double spaces
        exercise_name = re.sub(' +', ' ', exercise_name).lower()

        return exercise_name

    def reps(self) -> str:
        pattern = re.compile(r"\D(\s|(:\s))[(]?\d[\d\s+,.)(xX]+")
        reps = pattern.search(self.line).group().lower()  # lower converts any 'X' to 'x'

        # first 2 or 3 characters are redundant. It either non-digit + white-space or non-digit + ':' + white-space.
        # Either way removing first two character by slicing and using .strip() will get rid of all of them.
        # Additionally .strip will remove any redundant spaces on the right-side of the string
        reps = reps[2:].strip()

        # removing brackets
        reps = re.sub(r"[)(]", "", reps)

        # May happen that the string ends with one or more meaningless characters (\s, '+', ',' or 'x' - let's call them
        # specials). Going over all characters starting from the end of the string and finding any specials followed by
        # removing it should solve the issue. The loop should break whenever any digit is detected to avoid messing up
        # the string
        for i in range(len(reps) - 1, -1, -1):
            if re.match(r"[\s+,.x]", reps[i]):
                reps = reps[:-1]
            else:
                break

        # May happen that there is a meaningless combo of characters ("specials") within the string. That cannot be
        # solved programmatically without loosing information therefore user input is required.
        pass

        # remove all spaces
        reps = re.sub(' ', '', reps)

        return reps


if __name__ == "__main__":
    input_lines = [
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
    for _line in input_lines:
        ExtractData(_line).exercise_name()
        ExtractData(_line).reps()
