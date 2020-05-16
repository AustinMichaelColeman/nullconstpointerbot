import re


def remove_invalid_characters(code):
    return re.sub("([^ -~]|[\\W_IiOoZz])+", "", code)


def validate_levels(levels):
    # Text allowed in level codes: 0-9 A-Z a-z except I O Z
    # ignore anything but 0-9, A-Z, a-z, except IiOoZz
    # remove everything but 0-9, A-Z, a-z except IiOoZz

    valid_characters = remove_invalid_characters(levels)
    empty = len(valid_characters) == 0
    divisible_by_nine = len(valid_characters) % 9 != 0
    if empty or divisible_by_nine:
        return None
    valid_characters = valid_characters.upper()

    level_count = len(valid_characters) / 9

    validated_levels = []

    level_index = 0
    while level_index < level_count:
        offset = 9 * level_index
        left_begin = 0 + offset
        left_end = 3 + offset
        mid_begin = 3 + offset
        mid_end = 6 + offset
        right_begin = 6 + offset
        right_end = 9 + offset
        validated_level = (
            valid_characters[left_begin:left_end]
            + "-"
            + valid_characters[mid_begin:mid_end]
            + "-"
            + valid_characters[right_begin:right_end]
        )
        validated_levels.append(validated_level)
        level_index += 1

    return validated_levels


def create_levels(levels):
    level_codes = validate_levels(levels)
    if level_codes is None:
        return None

    levels = []
    for level in level_codes:
        levels.append(Level(level))
    return levels


class Level:
    def __init__(self, level):
        if isinstance(level, Level):
            self.level_code = level.level_code
        else:
            code = validate_levels(level)
            if code is None:
                self.level_code = None
            else:
                assert len(code) == 1
                self.level_code = code[0]

    def __str__(self):
        return self.level_code

    def __eq__(self, other):
        if other == None:
            return False
        if isinstance(other, str):
            code = validate_levels(other)
            assert len(code) == 1
            return self.level_code == code[0]
        return self.level_code == other.level_code

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)

    def __bool__(self):
        return self.level_code != None
