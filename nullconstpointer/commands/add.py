from nullconstpointer.commands.icommand import ICommand
from nullconstpointer.bot.level import Level, create_levels
from nullconstpointer.bot.user import User


class AddCommand(ICommand):
    def __init__(self, processor, invoker_name, level_submitter, levelcode):
        self.processor = processor
        self.invoker_name = invoker_name
        self.level_submitter = level_submitter
        self.levelcode = levelcode

    def success_add_user_level(self, level_submitter, levelcode):
        if isinstance(levelcode, list):
            singular = "level has"
            plural = "levels have"
            level_grammar = plural if len(levelcode) > 1 else singular
            response = f"Thank you {level_submitter}, your {level_grammar} been added: "

            level_index = 0
            for level in levelcode:
                response += f"{level}"
                if level_index != (len(levelcode) - 1):
                    response += " "
                level_index += 1
            return response
        else:
            return (
                f"Thank you {level_submitter}, your level has been added: {levelcode}"
            )

    def fail_add_user_level_invalid_code(self, invoker_name, levelcode):
        return f"{invoker_name}, addition rejected, only submit valid level codes: {levelcode}"

    def fail_add_user_level_duplicate_code(
        self, invoker_name, levelcode, level_submitter
    ):
        return (
            f"{invoker_name}, addition rejected, {levelcode}"
            f" already submitted by {level_submitter}"
        )

    def fail_add_user_level_level_limit(self, invoker_name):
        return f"{invoker_name}, !add is limited to {self.processor.level_limit} levels at a time. Check !list and !remove some levels first."

    def levels_would_make_us_exceed_limit(self, levels, processed_user):
        level_count = len(levels) + processed_user.levelCount()
        return level_count > self.processor.level_limit

    def execute(self):
        levels = create_levels(self.levelcode)

        if not levels:
            return self.fail_add_user_level_invalid_code(
                self.invoker_name, self.levelcode
            )

        for level in levels:
            for processed_user in self.processor.users:
                if processed_user.has_level(level):
                    return self.fail_add_user_level_duplicate_code(
                        self.invoker_name, level, processed_user
                    )

        foundUser = False
        for processed_user in self.processor.users:
            if processed_user == self.level_submitter:
                foundUser = True

                if self.levels_would_make_us_exceed_limit(levels, processed_user):
                    return self.fail_add_user_level_level_limit(self.invoker_name)

                for level in levels:
                    processed_user.add_level(level)

                return self.success_add_user_level(processed_user, levels)

        if not foundUser:
            foundUser = User(self.level_submitter)
            if self.levels_would_make_us_exceed_limit(levels, foundUser):
                return self.fail_add_user_level_level_limit(self.invoker_name)
            for level in levels:
                foundUser.add_level(level)
            self.processor.users.append(foundUser)
            return self.success_add_user_level(foundUser, levels)
