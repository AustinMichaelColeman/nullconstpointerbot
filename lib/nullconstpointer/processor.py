from . import level, user


class Processor:
    def __init__(self):
        self.users = []

    def user_count(self):
        return len(self.users)

    def success(self, username, levelcode):
        return (
            "Thank you " + username + ", your level " + levelcode + " has been added."
        )

    def fail(self, username, levelcode):
        return username + " has entered an invalid level code: " + levelcode

    def add_user_level(self, username, levelcode):
        userlevel = level.Level(levelcode)
        if str(userlevel) == "":
            return self.fail(username, levelcode)

        foundUser = False
        for processed_user in self.users:
            if processed_user.username == username:
                foundUser = True
                processed_user.add_level(userlevel)
                return self.success(
                    processed_user.username, str(processed_user.last_level())
                )

        if not foundUser:
            foundUser = user.User(username, userlevel)
            self.users.append(foundUser)
            return self.success(foundUser.username, str(foundUser.last_level()))
