from nullconstpointer.commands.icommand import ICommand
from nullconstpointer.level import Level
from nullconstpointer.user import User


class AddCommand(ICommand):
    def __init__(self, processor, invoker_name, level_submitter, levelcode):
        self.processor = processor
        self.invoker_name = invoker_name
        self.level_submitter = level_submitter
        self.levelcode = levelcode

    def success_add_user_level(self):
        return f"Thank you {self.level_submitter}, your level {self.levelcode} has been added."

    def fail_add_user_level_invalid_code(self):
        return (
            f"{self.invoker_name} has entered an invalid level code: {self.levelcode}"
        )

    def fail_add_user_level_duplicate_code(self):
        return (
            f"{self.invoker_name}, that level code {self.levelcode} "
            f"has already been entered by {self.level_submitter}"
        )

    def execute(self):
        userlevel = Level(self.levelcode)
        if not userlevel:
            return self.fail_add_user_level_invalid_code()

        foundUser = False
        for processed_user in self.processor.users:
            if processed_user == self.level_submitter:
                foundUser = True
                if not processed_user.has_level(userlevel):
                    processed_user.add_level(userlevel)
                    self.level_submitter = processed_user
                    self.levelcode = processed_user.last_level()
                    return self.success_add_user_level()
                else:
                    self.level_submitter = userlevel
                    self.levelcode = processed_user
                    return self.fail_add_user_level_duplicate_code()

        if not foundUser:
            foundUser = User(self.level_submitter)
            foundUser.add_level(userlevel)
            self.processor.users.append(foundUser)
            return self.success_add_user_level()
