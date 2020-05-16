from nullconstpointer.commands.icommand import ICommand
from nullconstpointer.bot.user import User, MOD_LEVEL_MOD


class UnmodCommand(ICommand):
    def __init__(self, processor, caller_user, user_to_unmod):
        self.processor = processor
        self.caller_user = caller_user
        self.user_to_unmod = user_to_unmod

    def success_unmod(self, user_to_unmod):
        return f"{user_to_unmod} is no longer a mod."

    def fail_unmod_cannot_find_user(self, user_to_unmod):
        return f"Unable to unmod: Could not find {user_to_unmod}"

    def fail_unmod_none_specified(self):
        return "Unable to unmod, please specify a user."

    def fail_unmod_not_owner(self):
        return f"Only the owner {self.processor.current_owner} can call !unmod"

    def execute(self):
        if self.caller_user != self.processor.current_owner:
            return self.fail_unmod_not_owner()

        if not self.user_to_unmod:
            return self.fail_unmod_none_specified()

        for user in self.processor.users:
            if user == self.user_to_unmod:
                user.make_user()
                return self.success_unmod(user)
        return self.fail_unmod_cannot_find_user(self.user_to_unmod)
