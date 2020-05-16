from nullconstpointer.commands.icommand import ICommand
from nullconstpointer.bot.level import Level


class RemoveCommand(ICommand):
    def __init__(self, processor, caller_user, level):
        self.processor = processor
        self.caller_user = caller_user
        self.level = level

    def fail_remove_no_level_specified(self):
        return "Remove failed: no level specified."

    def fail_remove_invalid_level_code(self, invalid_level_code):
        return f"Remove failed: invalid level code: {invalid_level_code}"

    def success_remove_user_level(self, user_submitted_by, level_removed):
        return f"Successfully removed level {level_removed} submitted by {user_submitted_by}"

    def fail_remove_level_not_found(self, level_not_found):
        return f"Remove failed: could not find level {level_not_found}"

    def fail_remove_no_permission_no_level_specified(self, caller_name):
        return f"{caller_name} does not have permission to remove levels."

    def fail_remove_no_permission(self, caller_name, level_submitter_name, level_code):
        return (
            f"{caller_name} does not have permission "
            f"to remove {level_code} submitted by {level_submitter_name}"
        )

    def has_permission_to_remove(self, user):
        return (
            self.processor.is_mod_or_owner(self.caller_user) or self.caller_user == user
        )

    def execute(self):
        if not self.level:
            return self.fail_remove_no_level_specified()

        level_fmt = Level(self.level)
        if not level_fmt:
            return self.fail_remove_invalid_level_code(self.level)

        for user in self.processor.users:
            for user_level in user.levels:
                if user_level != self.level:
                    continue

                if not self.has_permission_to_remove(user):
                    return self.fail_remove_no_permission(
                        self.caller_user, user, user_level
                    )

                if user_level == self.processor.next_level():
                    self.processor.current_user = None

                user.levels.remove(user_level)

                return self.success_remove_user_level(user, user_level)

        return self.fail_remove_level_not_found(level_fmt)
