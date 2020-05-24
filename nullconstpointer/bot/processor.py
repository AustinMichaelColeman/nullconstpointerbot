from datetime import datetime

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
        self.level_limit = 3
        self.time_remaining = -1
        self.time_started = 0

    def timer_has_been_set(self):
        return self.time_remaining != -1

    def start_timer(self, time):
        self.time_remaining = time
        self.time_started = datetime.now()

    def get_time_remaining(self):
        delta_seconds = (datetime.now() - self.time_started).seconds
        return self.time_remaining - delta_seconds

    def user_count(self):
        return len(self.users)

    def level_count(self):
        level_count = 0
        for user in self.users:
            level_count += len(user.levels)
        return level_count

    def find_user(self, user_to_find):
        for user in self.users:
            if user == user_to_find:
                return user
        return None

    def find_user_with_level(self, user_to_find):
        user = self.find_user(user_to_find)
        if user:
            if user == user_to_find and user.has_levels():
                return user
        return None

    def find_first_user_with_level(self):
        for user in self.users:
            if user.has_levels():
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
