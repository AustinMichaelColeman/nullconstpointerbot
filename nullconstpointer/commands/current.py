from nullconstpointer.commands.icommand import ICommand


class CurrentCommand(ICommand):
    def __init__(self, processor):
        self.processor = processor

    def fail_current_level_not_selected(self):
        return "No level has been selected yet."

    def success_current_level(self):
        return f"The current level is {self.processor.next_level()} submitted by {self.processor.current_user}"

    def execute(self):
        if self.processor.next_level() == None:
            return self.fail_current_level_not_selected()
        else:
            return self.success_current_level()
