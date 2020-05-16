from nullconstpointer.commands.remove import RemoveCommand
from nullconstpointer.bot.user import (
    User,
    MOD_LEVEL_OWNER,
    MOD_LEVEL_MOD,
    MOD_LEVEL_USER,
)


class Processor:
    def __init__(self, owner):
        self.current_owner = owner
        self.users = [self.current_owner]
        self.current_user = None

    def user_count(self):
        return len(self.users)

    def level_count(self):
        level_count = 0
        for user in self.users:
            level_count += len(user.levels)
        return level_count

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

    def next_level(self):
        if not self.current_user:
            return None

        return self.current_user.next_level()

    def process_command(self, command):
        return command.execute()
