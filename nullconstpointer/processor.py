import random
from datetime import datetime

from nullconstpointer.level import Level
from nullconstpointer.user import User, MOD_LEVEL_OWNER, MOD_LEVEL_MOD, MOD_LEVEL_USER


class Processor:
    def __init__(self, owner):
        self.current_owner = owner
        self.users = [self.current_owner]
        self.current_user = None
        self.current_level = None
        random.seed(datetime.now())

    def user_count(self):
        return len(self.users)

    def level_count(self):
        level_count = 0
        for user in self.users:
            level_count += len(user.levels)
        return level_count

    def fail_current_level_not_selected(self):
        return "No level has been selected yet."

    def success_current_level(self, current_level, user):
        return f"The current level is {current_level} submitted by {user}"

    def success_next_level(self, next_level, username):
        return f"The next level has been selected: {next_level} submitted by {username}"

    def fail_next_level_no_more_levels(self):
        return "There are no more levels to select."

    def fail_next_level_not_owner(self):
        return f"Next can only be called by the owner: {self.current_owner}"

    def success_mod(self, user_to_mod):
        return f"{user_to_mod} is now a mod!"

    def fail_mod(self, user_to_mod):
        return f"Unable to mod: Could not find {user_to_mod}"

    def fail_mod_not_owner(self):
        return f"Only the owner {self.current_owner} can call !mod"

    def fail_mod_none_specified(self):
        return "Unable to mod, please specify a user."

    def success_unmod(self, user_to_unmod):
        return f"{user_to_unmod} is no longer a mod."

    def fail_unmod_cannot_find_user(self, user_to_unmod):
        return f"Unable to unmod: Could not find {user_to_unmod}"

    def fail_unmod_none_specified(self):
        return "Unable to unmod, please specify a user."

    def fail_unmod_not_owner(self):
        return f"Only the owner {self.current_owner} can call !mod"

    def fail_remove_no_level_specified(self):
        return "Remove failed: no level specified."

    def fail_remove_invalid_level_code(self, invalid_level_code):
        return f"Remove failed: invalid level code: {invalid_level_code}"

    def success_remove_user_level(self, user_submitted_by, level_removed):
        return f"Successfully removed level {level_removed} submitted by {user_submitted_by}"

    def fail_remove_level_not_found(self, level_not_found):
        return f"Remove failed: could not find level {level_not_found}"

    def fail_remove_no_permission_no_level_specified(self, caller_name):
        return f"{caller_name} does not have permission to remove levels."

    def fail_remove_no_permission(self, caller_name, level_submitter_name, level_code):
        return (
            f"{caller_name} does not have permission "
            f"to remove {level_code} submitted by {level_submitter_name}"
        )

    def fail_leave_no_levels(self, caller):
        return f"{caller} has no levels to remove."

    def success_leave(self, caller):
        return f"Removed all levels submitted by {caller}"

    def success_clear_owner(self):
        return "Successfully cleared all levels."

    def success_clear_user(self, caller_name):
        return f"Cleared all levels submitted by {caller_name}"

    def fail_clear_user_no_levels(self, caller_name):
        return f"{caller_name} does not have any levels added."

    def success_random_level(self, level_submitter_name, level_code):
        return f"{level_submitter_name}, your level {level_code} has been randomly selected!"

    def fail_random_no_permission(self, caller_name):
        return f"{caller_name}, only the owner {self.current_owner} can call !random"

    def fail_random_no_levels(self):
        return "There are no levels to select at random."

    def fail_remove_current_no_levels(self):
        return "There are no levels currently selected."

    def fail_remove_current_no_permission(self, caller_name):
        return f"{caller_name}, only the owner {self.current_owner} can use !finish"

    def get_current_level(self):
        if self.current_level == None:
            return self.fail_current_level_not_selected()
        else:
            return self.success_current_level(self.current_level, self.current_user)

    def find_first_user_with_level(self):
        for user in self.users:
            if len(user.levels) > 0:
                return user
        return None

    def next_level(self, caller_user):
        if caller_user == self.current_owner:
            found_user = self.find_first_user_with_level()
            if found_user:
                self.current_level = found_user.next_level()
                self.current_user = found_user
                return self.success_next_level(self.current_level, found_user)
            return self.fail_next_level_no_more_levels()
        else:
            return self.fail_next_level_not_owner()

    def mod(self, caller_name, user_to_mod):
        if caller_name != self.current_owner:
            return self.fail_mod_not_owner()
        if not user_to_mod:
            return self.fail_mod_none_specified()

        for user in self.users:
            if user == user_to_mod:
                user.make_mod()
                return self.success_mod(user)
        modded_user = User(user_to_mod, MOD_LEVEL_MOD)
        self.users.append(modded_user)
        return self.success_mod(modded_user)

    def unmod(self, caller_name, user_to_unmod):
        if caller_name != self.current_owner:
            return self.fail_unmod_not_owner()

        if not user_to_unmod:
            return self.fail_unmod_none_specified()

        for user in self.users:
            if user == user_to_unmod:
                user.make_user()
                return self.success_unmod(user)
        return self.fail_unmod_cannot_find_user(user_to_unmod)

    def is_mod_or_owner(self, username):
        for user in self.users:
            if user == username:
                return user.is_mod_or_owner()
        return False

    def remove(self, caller_name, level):
        if not level:
            return self.fail_remove_no_level_specified()

        level_fmt = Level(level)
        if not level_fmt:
            return self.fail_remove_invalid_level_code(level)

        for user in self.users:
            for user_level in user.levels:
                if user_level != level:
                    continue

                if self.is_mod_or_owner(caller_name) or caller_name == user:
                    user.levels.remove(user_level)

                    if user_level == self.current_level:
                        self.current_level = None
                        self.current_user = None

                    return self.success_remove_user_level(user, user_level)

                return self.fail_remove_no_permission(caller_name, user, user_level)
        return self.fail_remove_level_not_found(level_fmt)

    def leave(self, caller_name):
        for user in self.users:
            if user == caller_name:
                if user.levels:
                    user.levels.clear()
                    return self.success_leave(caller_name)
                else:
                    return self.fail_leave_no_levels(caller_name)
        return self.fail_leave_no_levels(caller_name)

    def clear(self, caller_name):
        if caller_name == self.current_owner:
            for user in self.users:
                user.levels.clear()
            return self.success_clear_owner()

        for user in self.users:
            if user != caller_name:
                continue

            if user.levels:
                user.levels.clear()
                return self.success_clear_user(caller_name)
            return self.fail_clear_user_no_levels(caller_name)
        return self.fail_clear_user_no_levels(caller_name)

    def random_level(self, caller_name):
        if caller_name != self.current_owner:
            return self.fail_random_no_permission(caller_name)

        users_with_levels = []
        for user in self.users:
            if user.has_levels():
                users_with_levels += user

        if len(users_with_levels) == 0:
            return self.fail_random_no_levels()

        random_user_index = random.randrange(0, len(users_with_levels))
        selected_user = users_with_levels[random_user_index]

        self.current_level = selected_user.next_level()
        self.current_user = selected_user
        return self.success_random_level(selected_user, self.current_level)

    def remove_current(self, caller_name):
        if caller_name != self.current_owner:
            return self.fail_remove_current_no_permission(caller_name)

        if self.current_level is None:
            return self.fail_remove_current_no_levels()

        return self.remove(caller_name, self.current_level)

    def process_command(self, command):
        return command.execute()
