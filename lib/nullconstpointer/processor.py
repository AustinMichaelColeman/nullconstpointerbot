class Processor:
    def __init__(self):
        self.users = []

    def user_count(self):
        return len(self.users)

    def add_user(self, user):
        self.users.append(user)
        return (
            "Thank you "
            + user.name
            + ", your level "
            + user.levels[0]
            + " has been added."
        )
