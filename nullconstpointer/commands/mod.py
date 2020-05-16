from nullconstpointer.commands.icommand import ICommand
from nullconstpointer.bot.user import User, MOD_LEVEL_MOD


class ModCommand(ICommand):
    def __init__(self, processor, caller_user, user_to_mod):
        self.processor = processor
        self.caller_user = caller_user
        self.user_to_mod = user_to_mod

    def success_mod(self, user_to_mod):
        return f"{user_to_mod} is now a mod!"

    def fail_mod(self, user_to_mod):
        return f"Unable to mod: Could not find {user_to_mod}"

    def fail_mod_not_owner(self):
        return f"Only the owner {self.processor.current_owner} can call !mod"

    def fail_mod_none_specified(self):
        return "Unable to mod, please specify a user."

    def execute(self):
        if self.caller_user != self.processor.current_owner:
            return self.fail_mod_not_owner()
        if not self.user_to_mod:
            return self.fail_mod_none_specified()

        for user in self.processor.users:
            if user == self.user_to_mod:
                user.make_mod()
                return self.success_mod(user)
        modded_user = User(self.user_to_mod, MOD_LEVEL_MOD)
        self.processor.users.append(modded_user)
        return self.success_mod(modded_user)
