import re


class Level:
    def __init__(self, level):
        self.level_code = self.validate(level)

    def __str__(self):
        return self.level_code

    def __eq__(self, other):
        return self.level_code == other.level_code

    def validate(self, level):
        # Text allowed in level codes: 0-9 A-Z a-z except I O Z
        # ignore anything but 0-9, A-Z, a-z, except IiOoZz
        # remove everything but 0-9, A-Z, a-z except IiOoZz
        non_alpha_numberic_removed = re.sub("[\\W_IiOoZz]+", "", level)
        if len(non_alpha_numberic_removed) != 9:
            return ""
        non_alpha_numberic_removed = non_alpha_numberic_removed.upper()

        validated_level = (
            non_alpha_numberic_removed[0:3]
            + "-"
            + non_alpha_numberic_removed[3:6]
            + "-"
            + non_alpha_numberic_removed[6:9]
        )

        return validated_level
