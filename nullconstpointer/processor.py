import random
from datetime import datetime

from nullconstpointer.commands.remove import RemoveCommand
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

    def fail_leave_no_levels(self, caller):
        return f"{caller} has no levels to remove."

    def success_leave(self, caller):
        return f"Removed all levels submitted by {caller}"

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

    def find_first_user_with_level(self):
        for user in self.users:
            if len(user.levels) > 0:
                return user
        return None

    def is_mod_or_owner(self, username):
        for user in self.users:
            if user == username:
                return user.is_mod_or_owner()
        return False

    def leave(self, caller_name):
        for user in self.users:
            if user == caller_name:
                if user.levels:
                    user.levels.clear()
                    return self.success_leave(caller_name)
                else:
                    return self.fail_leave_no_levels(caller_name)
        return self.fail_leave_no_levels(caller_name)

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

        command = RemoveCommand(self, caller_name, self.current_level)
        return self.process_command(command)

    def process_command(self, command):
        return command.execute()
