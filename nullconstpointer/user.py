MOD_LEVEL_OWNER = 0
MOD_LEVEL_MOD = 1
MOD_LEVEL_USER = 2


class User:
    def __init__(self, name, modlevel=MOD_LEVEL_USER):
        self.username = name
        self.levels = []
        self.modlevel = modlevel
        assert (
            modlevel == MOD_LEVEL_OWNER
            or modlevel == MOD_LEVEL_MOD
            or modlevel == MOD_LEVEL_USER
        )

    def __eq__(self, other):
        if other == None:
            return False
        if isinstance(other, str):
            return self.username == other
        return self.username == other.username

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)

    def __bool__(self):
        return self.username != ""

    def levelCount(self):
        return len(self.levels)

    def next_level(self):
        if len(self.levels) > 0:
            return self.levels[0]
        return None

    def last_level(self):
        if len(self.levels) > 0:
            return self.levels[len(self.levels) - 1]
        return None

    def remove_level(self):
        self.levels.pop(0)

    def add_level(self, level):
        self.levels.append(level)

    def mod_level(self):
        return self.modlevel

    def make_mod(self):
        self.modlevel = MOD_LEVEL_MOD

    def make_owner(self):
        self.modlevel = MOD_LEVEL_OWNER

    def make_user(self):
        self.modlevel = MOD_LEVEL_USER

    def has_level(self, levelcode):
        for level in self.levels:
            if level == levelcode:
                return True
        return False

    def is_mod_or_owner(self):
        return (self.modlevel == MOD_LEVEL_MOD) or (self.modlevel == MOD_LEVEL_OWNER)

    def __str__(self):
        return self.username
