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
            if str(level) == str(levelcode):
                return True
        return False

    def __str__(self):
        return self.username
