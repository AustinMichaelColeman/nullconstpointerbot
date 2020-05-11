from . import level, user


class Processor:
    def __init__(self):
        self.users = []

    def user_count(self):
        return len(self.users)

    def add_user_level(self, username, levelcode):
        userlevel = level.Level(levelcode)
        if userlevel.code() == "":
            return "Invalid level code: " + levelcode

        foundUser = None
        for processed_user in self.users:
            if processed_user.username == username:
                processed_user.add_level(userlevel)
                return (
                    "Thank you "
                    + processed_user.username
                    + ", your level "
                    + processed_user.last_level().code()
                    + " has been added."
                )

        if foundUser is None:
            foundUser = user.User(username, userlevel)
            self.users.append(foundUser)

            return (
                "Thank you "
                + foundUser.username
                + ", your level "
                + foundUser.last_level().code()
                + " has been added."
            )
