MOD_LEVEL_OWNER = 0
MOD_LEVEL_MOD = 1
MOD_LEVEL_USER = 2


class User:
    def __init__(self, name, level, modlevel=MOD_LEVEL_USER):
        self.name = name
        self.levels = [level]
        self.modlevel = modlevel

    def levelCount(self):
        return len(self.levels)

    def next_level(self):
        if len(self.levels) > 0:
            return self.levels[0]
        return None

    def remove_level(self):
        self.levels.pop(0)

    def add_level(self, level):
        self.levels.append(level)

    def mod_level(self):
        return self.modlevel
