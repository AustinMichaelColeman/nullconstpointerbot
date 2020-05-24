from nullconstpointer.commands.icommand import ICommand

from nullconstpointer.commands.remove import RemoveCommand


class FinishCommand(ICommand):
    def __init__(self, processor, caller_name):
        self.processor = processor
        self.caller_name = caller_name
        self.remove_command = RemoveCommand(
            self.processor, self.caller_name, self.processor.next_level()
        )

    def success_remove_user_level(self, user, level):
        return self.remove_command.success_remove_user_level(user, level)

    def fail_finish_no_levels(self):
        return "There are no levels currently selected."

    def fail_finish_no_permission(self, caller_name):
        return f"{caller_name}, only the owner and mods can use !finish"

    def execute(self):
        found_user = self.processor.find_user(self.caller_name)
        if not found_user:
            return self.fail_finish_no_permission(self.caller_name)

        if not found_user.is_mod_or_owner():
            return self.fail_finish_no_permission(self.caller_name)

        if self.processor.next_level() is None:
            return self.fail_finish_no_levels()

        command = RemoveCommand(
            self.processor, self.caller_name, self.processor.next_level()
        )
        return self.processor.process_command(command)
