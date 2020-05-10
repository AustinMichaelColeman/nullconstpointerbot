class User:
    def __init__(self, name, level):
        self.name = name
        self.levels = [level]

    def levelCount(self):
        return len(self.levels)
