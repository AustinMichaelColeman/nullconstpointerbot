from nullconstpointer.commands.icommand import ICommand


class ListCommand(ICommand):
    def __init__(self, processor):
        self.processor = processor

    def success_list_empty(self):
        return "There are no levels to list"

    def execute(self):
        if not self.processor.find_first_user_with_level():
            return self.success_list_empty()
        else:
            return self.success_list()

    def success_list(self):
        output = ""
        user_index = 0

        users_with_levels = []
        for user in self.processor.users:
            if len(user.levels) > 0:
                users_with_levels.append(user)

        for user in users_with_levels:
            output += user
            output += " "
            level_index = 0
            for thelevel in user.levels:
                output += thelevel
                if level_index < (len(user.levels) - 1):
                    output += ", "
                level_index += 1
            if user_index < (len(users_with_levels) - 1):
                output += " | "
            user_index += 1

        return output
