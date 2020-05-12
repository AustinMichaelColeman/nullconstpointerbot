from . import level, user


class Processor:
    def __init__(self):
        self.users = []
        self.current_username = None
        self.current_level = None

    def user_count(self):
        return len(self.users)

    def success_list_empty(self):
        return "There are no levels to list"

    def success_list(self, users):
        output = ""
        user_index = 0
        for theuser in users:
            output += theuser.username
            output += " "
            level_index = 0
            for thelevel in theuser.levels:
                output += str(thelevel)
                if level_index < (len(theuser.levels) - 1):
                    output += ", "
                level_index += 1
            if user_index < (len(users) - 1):
                output += " | "
            user_index += 1

        return output

    def success_add_user_level(self, username, levelcode):
        return (
            "Thank you " + username + ", your level " + levelcode + " has been added."
        )

    def fail_add_user_level_invalid_code(self, username, levelcode):
        return username + " has entered an invalid level code: " + levelcode

    def fail_duplicate_code(self, username_of_command, levelcode, username_of_level):
        return (
            username_of_command
            + ", that level code "
            + levelcode
            + " has already been entered by "
            + username_of_level
        )

    def fail_current_level_not_selected(self):
        return "No level has been selected yet."

    def success_current_level(self, current_level, theuser):
        return "The current level is " + current_level + " submitted by " + theuser

    def success_next_level(self, next_level, username):
        return (
            "The next level has been selected: "
            + next_level
            + " submitted by "
            + username
        )

    def fail_next_level_no_more_levels(self):
        return "There are no more levels to select."

    def list_levels(self):
        if len(self.users) == 0:
            return self.success_list_empty()
        else:
            return self.success_list(self.users)

    def add_user_level(self, username, levelcode):
        userlevel = level.Level(levelcode)
        if str(userlevel) == "":
            return self.fail_add_user_level_invalid_code(username, levelcode)

        foundUser = False
        for processed_user in self.users:
            if processed_user.username == username:
                foundUser = True
                if not processed_user.has_level(userlevel):
                    processed_user.add_level(userlevel)
                    return self.success_add_user_level(
                        processed_user.username, str(processed_user.last_level())
                    )
                else:
                    return self.fail_duplicate_code(
                        username, str(userlevel), processed_user.username
                    )

        if not foundUser:
            foundUser = user.User(username, userlevel)
            self.users.append(foundUser)
            return self.success_add_user_level(
                foundUser.username, str(foundUser.last_level())
            )

    def get_current_level(self):
        if self.current_level == None:
            return self.fail_current_level_not_selected()
        else:
            return self.success_current_level(
                str(self.current_level), self.current_username
            )

    def next_level(self):
        if len(self.users) > 0:
            first_user = self.users[0]
            self.current_level = first_user.next_level()
            self.current_username = first_user.username
            return self.success_next_level(str(self.current_level), first_user.username)
        return self.fail_next_level_no_more_levels()
