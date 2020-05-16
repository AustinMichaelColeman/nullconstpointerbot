from nullconstpointer.commands.icommand import ICommand
from nullconstpointer.bot.level import Level
from nullconstpointer.bot.user import User


class AddCommand(ICommand):
    def __init__(self, processor, invoker_name, level_submitter, levelcode):
        self.processor = processor
        self.invoker_name = invoker_name
        self.level_submitter = level_submitter
        self.levelcode = levelcode

    def success_add_user_level(self, level_submitter, levelcode):
        return f"Thank you {level_submitter}, your level {levelcode} has been added."

    def fail_add_user_level_invalid_code(self, invoker_name, levelcode):
        return f"{invoker_name} has entered an invalid level code: {levelcode}"

    def fail_add_user_level_duplicate_code(
        self, invoker_name, levelcode, level_submitter
    ):
        return (
            f"{invoker_name}, that level code {levelcode} "
            f"has already been entered by {level_submitter}"
        )

    def execute(self):
        userlevel = Level(self.levelcode)
        if not userlevel:
            return self.fail_add_user_level_invalid_code(
                self.invoker_name, self.levelcode
            )

        foundUser = False
        for processed_user in self.processor.users:
            if processed_user == self.level_submitter:
                foundUser = True

                if processed_user.has_level(userlevel):
                    return self.fail_add_user_level_duplicate_code(
                        self.invoker_name, userlevel, processed_user
                    )

                processed_user.add_level(userlevel)
                self.level_submitter = processed_user
                self.levelcode = processed_user.last_level()
                return self.success_add_user_level(self.level_submitter, self.levelcode)

        if not foundUser:
            foundUser = User(self.level_submitter)
            foundUser.add_level(userlevel)
            self.processor.users.append(foundUser)
            return self.success_add_user_level(foundUser, userlevel)
