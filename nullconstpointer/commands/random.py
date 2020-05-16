from datetime import datetime
import random

from nullconstpointer.commands.icommand import ICommand


class RandomCommand(ICommand):
    def __init__(self, processor, caller_user):
        self.processor = processor
        self.caller_user = caller_user
        random.seed(datetime.now())

    def success_random_level(self, level_submitter_name, level_code):
        return f"{level_submitter_name}, your level {level_code} has been randomly selected!"

    def fail_random_no_permission(self, caller_name):
        return f"{caller_name}, only the owner {self.processor.current_owner} can call !random"

    def fail_random_no_levels(self):
        return "There are no levels to select at random."

    def execute(self):
        if self.caller_user != self.processor.current_owner:
            return self.fail_random_no_permission(self.caller_user)

        users_with_levels = []
        for user in self.processor.users:
            if user.has_levels():
                users_with_levels += user

        if len(users_with_levels) == 0:
            return self.fail_random_no_levels()

        random_user_index = random.randrange(0, len(users_with_levels))
        selected_user = users_with_levels[random_user_index]

        self.processor.current_user = selected_user
        return self.success_random_level(selected_user, self.processor.next_level())
