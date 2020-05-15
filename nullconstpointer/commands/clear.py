from nullconstpointer.commands.icommand import ICommand


class ClearCommand(ICommand):
    def __init__(self, processor, invoker_name):
        self.processor = processor
        self.invoker_name = invoker_name

    def success_clear_owner(self):
        return "Successfully cleared all levels."

    def success_clear_user(self, caller_name):
        return f"Cleared all levels submitted by {caller_name}"

    def fail_clear_user_no_levels(self, caller_name):
        return f"{caller_name} does not have any levels added."

    def execute(self):
        if self.invoker_name == self.processor.current_owner:
            for user in self.processor.users:
                user.levels.clear()
            return self.success_clear_owner()

        for user in self.processor.users:
            if user != self.invoker_name:
                continue

            if user.levels:
                user.levels.clear()
                return self.success_clear_user(self.invoker_name)
            return self.fail_clear_user_no_levels(self.invoker_name)
        return self.fail_clear_user_no_levels(self.invoker_name)
