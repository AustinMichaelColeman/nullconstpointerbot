from nullconstpointer.commands.icommand import ICommand

from nullconstpointer.commands.remove import RemoveCommand


class FinishCommand(ICommand):
    def __init__(self, processor, caller_name):
        self.processor = processor
        self.caller_name = caller_name

    def fail_finish_no_levels(self):
        return "There are no levels currently selected."

    def fail_finish_no_permission(self, caller_name):
        return f"{caller_name}, only the owner {self.processor.current_owner} can use !finish"

    def execute(self):
        if self.caller_name != self.processor.current_owner:
            return self.fail_finish_no_permission(self.caller_name)

        if self.processor.next_level() is None:
            return self.fail_finish_no_levels()

        command = RemoveCommand(
            self.processor, self.caller_name, self.processor.next_level()
        )
        return self.processor.process_command(command)
