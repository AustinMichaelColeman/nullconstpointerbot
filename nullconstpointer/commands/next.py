from nullconstpointer.commands.icommand import ICommand


class NextCommand(ICommand):
    def __init__(self, processor, caller_user):
        self.processor = processor
        self.caller_user = caller_user

    def success_next_level(self, next_level, username):
        return f"The next level has been selected: {next_level} submitted by {username}"

    def fail_next_level_no_more_levels(self):
        return "There are no more levels to select."

    def fail_next_level_not_owner(self):
        return f"Next can only be called by the owner: {self.processor.current_owner}"

    def execute(self):
        if self.caller_user == self.processor.current_owner:
            found_user = self.processor.find_first_user_with_level()
            if found_user:
                self.processor.current_level = found_user.next_level()
                self.processor.current_user = found_user
                return self.success_next_level(self.processor.current_level, found_user)
            return self.fail_next_level_no_more_levels()
        else:
            return self.fail_next_level_not_owner()
