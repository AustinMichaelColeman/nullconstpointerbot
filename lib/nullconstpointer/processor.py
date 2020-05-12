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

    def fail_invalid_code(self, username, levelcode):
        return username + " has entered an invalid level code: " + levelcode

    def fail_duplicate_code(self, username_of_command, levelcode, username_of_level):
        return (
            username_of_command
            + ", that level code "
            + levelcode
            + " has already been entered by "
            + username_of_level
        )

    def add_user_level(self, username, levelcode):
        userlevel = level.Level(levelcode)
        if str(userlevel) == "":
            return self.fail_invalid_code(username, levelcode)

        foundUser = False
        for processed_user in self.users:
            if processed_user.username == username:
                foundUser = True
                if not processed_user.has_level(userlevel):
                    processed_user.add_level(userlevel)
                    return self.success(
                        processed_user.username, str(processed_user.last_level())
                    )
                else:
                    return self.fail_duplicate_code(
                        username, str(userlevel), processed_user.username
                    )

        if not foundUser:
            foundUser = user.User(username, userlevel)
            self.users.append(foundUser)
            return self.success(foundUser.username, str(foundUser.last_level()))
