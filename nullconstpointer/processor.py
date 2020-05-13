from nullconstpointer.level import Level
from nullconstpointer.user import User, MOD_LEVEL_OWNER, MOD_LEVEL_MOD, MOD_LEVEL_USER


class Processor:
    def __init__(self, owner):
        self.current_owner = User(owner.username, MOD_LEVEL_OWNER)
        self.users = [self.current_owner]
        self.current_username = None
        self.current_level = None

    def user_count(self):
        return len(self.users)

    def success_list_empty(self):
        return "There are no levels to list"

    def success_list(self, users):
        output = ""
        user_index = 0

        users_with_levels = []
        for theuser in users:
            if len(theuser.levels) > 0:
                users_with_levels.append(theuser)

        for theuser in users_with_levels:
            output += theuser.username
            output += " "
            level_index = 0
            for thelevel in theuser.levels:
                output += str(thelevel)
                if level_index < (len(theuser.levels) - 1):
                    output += ", "
                level_index += 1
            if user_index < (len(users_with_levels) - 1):
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

    def fail_next_level_not_owner(self):
        return "Next can only be called by the owner: " + self.current_owner.username

    def success_mod(self, user_to_mod):
        return str(user_to_mod) + " is now a mod!"

    def fail_mod(self, user_to_mod):
        return "Unable to mod: Could not find " + user_to_mod

    def fail_mod_not_owner(self):
        return "Only the owner " + self.current_owner.username + " can call !mod"

    def fail_mod_none_specified(self):
        return "Unable to mod, please specify a user."

    def success_unmod(self, user_to_unmod):
        return user_to_unmod + " is no longer a mod."

    def fail_unmod_cannot_find_user(self, user_to_unmod):
        return "Unable to unmod: Could not find " + user_to_unmod

    def fail_unmod_none_specified(self):
        return "Unable to unmod, please specify a user."

    def fail_unmod_not_owner(self):
        return "Only the owner " + self.current_owner.username + " can call !mod"

    def fail_remove_no_level_specified(self):
        return "Remove failed: no level specified."

    def fail_remove_invalid_level_code(self, invalid_level_code):
        return "Remove failed: invalid level code: " + invalid_level_code

    def success_remove_user_level(self, user_submitted_by, level_removed):
        return (
            "Successfully removed level "
            + level_removed
            + " submitted by "
            + user_submitted_by
        )

    def fail_remove_level_not_found(self, level_not_found):
        return "Remove failed: could not find level " + level_not_found

    def fail_remove_no_permission(self, caller_name, level_submitter_name, level_code):
        return (
            caller_name
            + " does not have permission to remove "
            + level_code
            + " submitted by "
            + level_submitter_name
        )

    def list_levels(self):
        if not self.find_first_user_with_level():
            return self.success_list_empty()
        else:
            return self.success_list(self.users)

    def add_user_level(self, username, levelcode):
        userlevel = Level(levelcode)
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
            foundUser = User(username)
            foundUser.add_level(userlevel)
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

    def find_first_user_with_level(self):
        for theuser in self.users:
            if len(theuser.levels) > 0:
                return theuser
        return None

    def next_level(self, caller_user):
        if str(caller_user) == self.current_owner.username:
            found_user = self.find_first_user_with_level()
            if found_user:
                self.current_level = found_user.next_level()
                self.current_username = found_user.username
                return self.success_next_level(
                    str(self.current_level), found_user.username
                )
            return self.fail_next_level_no_more_levels()
        else:
            return self.fail_next_level_not_owner()

    def mod(self, caller_name, user_to_mod):
        if user_to_mod == "":
            return self.fail_mod_none_specified()
        if caller_name == self.current_owner.username:
            for theuser in self.users:
                if theuser.username == user_to_mod:
                    theuser.make_mod()
                    return self.success_mod(theuser.username)
            modded_user = User(user_to_mod, MOD_LEVEL_MOD)
            self.users.append(modded_user)
            return self.success_mod(modded_user)
        return self.fail_mod_not_owner()

    def unmod(self, caller_name, user_to_unmod):
        if user_to_unmod == "":
            return self.fail_unmod_none_specified()
        if caller_name == self.current_owner.username:
            for theuser in self.users:
                if theuser.username == user_to_unmod:
                    theuser.make_user()
                    return self.success_unmod(theuser.username)
            return self.fail_unmod_cannot_find_user(user_to_unmod)
        return self.fail_unmod_not_owner()

    def is_mod_or_owner(self, username):
        for theuser in self.users:
            if theuser.username == username:
                return theuser.is_mod_or_owner()
        return False

    def remove(self, caller_name, level):
        if not level:
            return self.fail_remove_no_level_specified()

        level_fmt = Level(level)
        if not str(level_fmt):
            return self.fail_remove_invalid_level_code(level)

        for user in self.users:
            for user_level in user.levels:
                if str(user_level) != str(level_fmt):
                    continue

                if self.is_mod_or_owner(caller_name) or caller_name == str(user):
                    user.levels.remove(user_level)
                    return self.success_remove_user_level(str(user), str(user_level))

                return self.fail_remove_no_permission(
                    caller_name, str(user), str(user_level)
                )
        return self.fail_remove_level_not_found(str(level_fmt))
