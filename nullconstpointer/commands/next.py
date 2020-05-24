from nullconstpointer.commands.icommand import ICommand


class NextCommand(ICommand):
    def __init__(self, processor, invoker_user, next_user):
        self.processor = processor
        self.invoker_user = invoker_user
        self.next_user = next_user

    def success_next_level(self, next_level, username):
        return f"The next level has been selected: {next_level} submitted by {username}"

    def fail_next_level_no_more_levels(self):
        return "There are no more levels to select."

    def fail_next_level_not_mod(self):
        return f"Next can only be called by mods."

    def fail_user_no_levels(self, user):
        return f"{user} has no levels. Usernames are case sensitive."

    def find_invoker_user(self):
        for user in self.processor.users:
            if user == self.invoker_user:
                return user

    def execute(self):
        invoker = self.find_invoker_user()
        if not invoker:
            return self.fail_next_level_not_mod()
        if invoker.is_mod_or_owner():
            found_user = None
            if self.next_user:
                found_user = self.processor.find_user_with_level(self.next_user)
            else:
                found_user = self.processor.find_first_user_with_level()
            if found_user:
                self.processor.current_user = found_user
                return self.success_next_level(self.processor.next_level(), found_user)
            if not found_user and self.next_user:
                return self.fail_user_no_levels(self.next_user)
            return self.fail_next_level_no_more_levels()
        return self.fail_next_level_not_mod()
