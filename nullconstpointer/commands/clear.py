from nullconstpointer.commands.icommand import ICommand


class ClearCommand(ICommand):
    def __init__(self, processor, invoker_name, user_to_clear):
        self.processor = processor
        self.invoker_name = invoker_name
        self.user_to_clear = user_to_clear

    def success_clear_owner(self):
        return "Successfully cleared all levels."

    def success_clear_user(self, caller_name):
        return f"Cleared all levels submitted by {caller_name}"

    def fail_clear_user_no_levels(self, caller_name):
        return f"{caller_name} does not have any levels added."

    def fail_clear_no_permission(self, invoker_name):
        return f"{invoker_name} does not have permission to clear other user's levels."

    def find_user_to_clear(self):
        for user in self.processor.users:
            if user == self.user_to_clear:
                return user
        return None

    def find_invoker_user(self):
        for user in self.processor.users:
            if user == self.invoker_name:
                return user
        return None

    def find_and_clear_user(self):
        user = self.find_user_to_clear()
        if user:
            if user.has_levels():
                if user == self.processor.current_user:
                    self.processor.current_user = None
                user.levels.clear()
                return self.success_clear_user(user)
            else:
                return self.fail_clear_user_no_levels(user)
        else:
            return self.fail_clear_user_no_levels(self.user_to_clear)

    def execute(self):
        if self.invoker_name == self.processor.current_owner:
            if self.user_to_clear:
                return self.find_and_clear_user()
            else:
                for user in self.processor.users:
                    user.levels.clear()
                self.processor.current_user = None
                return self.success_clear_owner()

        invoker_user = self.find_invoker_user()
        if self.user_to_clear:
            if invoker_user:
                if invoker_user == self.user_to_clear:
                    if invoker_user == self.processor.current_user:
                        self.processor.current_user = None
                    invoker_user.levels.clear()
                    return self.success_clear_user(invoker_user)
                else:
                    if invoker_user.is_mod_or_owner():
                        return self.find_and_clear_user()
                    return self.fail_clear_no_permission(self.invoker_name)
            else:
                if self.invoker_name == self.user_to_clear:
                    return self.fail_clear_user_no_levels(self.user_to_clear)
                return self.fail_clear_no_permission(self.invoker_name)

        for user in self.processor.users:
            if user != self.invoker_name:
                continue

            if user.levels:
                user.levels.clear()
                return self.success_clear_user(self.invoker_name)
            return self.fail_clear_user_no_levels(self.invoker_name)
        return self.fail_clear_user_no_levels(self.invoker_name)
