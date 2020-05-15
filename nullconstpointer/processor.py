from nullconstpointer.commands.remove import RemoveCommand
from nullconstpointer.user import User, MOD_LEVEL_OWNER, MOD_LEVEL_MOD, MOD_LEVEL_USER


class Processor:
    def __init__(self, owner):
        self.current_owner = owner
        self.users = [self.current_owner]
        self.current_user = None
        self.current_level = None

    def user_count(self):
        return len(self.users)

    def level_count(self):
        level_count = 0
        for user in self.users:
            level_count += len(user.levels)
        return level_count

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

    def remove_current(self, caller_name):
        if caller_name != self.current_owner:
            return self.fail_remove_current_no_permission(caller_name)

        if self.current_level is None:
            return self.fail_remove_current_no_levels()

        command = RemoveCommand(self, caller_name, self.current_level)
        return self.process_command(command)

    def process_command(self, command):
        return command.execute()
