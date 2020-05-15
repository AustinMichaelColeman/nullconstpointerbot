from nullconstpointer.commands.icommand import ICommand


class LeaveCommand(ICommand):
    def __init__(self, processor, caller_name):
        self.processor = processor
        self.caller_name = caller_name

    def fail_leave_no_levels(self, caller):
        return f"{caller} has no levels to remove."

    def success_leave(self, caller):
        return f"Removed all levels submitted by {caller}"

    def execute(self):
        for user in self.processor.users:
            if user == self.caller_name:
                if user.levels:
                    user.levels.clear()
                    return self.success_leave(self.caller_name)
                else:
                    return self.fail_leave_no_levels(self.caller_name)
        return self.fail_leave_no_levels(self.caller_name)
