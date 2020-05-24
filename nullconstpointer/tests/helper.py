from nullconstpointer.bot.user import User, MOD_LEVEL_OWNER
from nullconstpointer.bot.processor import Processor
from nullconstpointer.commands.add import AddCommand
from nullconstpointer.commands.remove import RemoveCommand
from nullconstpointer.commands.clear import ClearCommand
from nullconstpointer.commands.mod import ModCommand
from nullconstpointer.commands.current import CurrentCommand
from nullconstpointer.commands.next import NextCommand
from nullconstpointer.commands.finish import FinishCommand
from nullconstpointer.commands.random import RandomCommand
from nullconstpointer.commands.leave import LeaveCommand
from nullconstpointer.commands.list import ListCommand
from nullconstpointer.commands.unmod import UnmodCommand


class TestHelper:
    def __init__(self):
        self.test_owner = User("test_owner", MOD_LEVEL_OWNER)
        self.test_processor = Processor(self.test_owner)
        self.TEST_USER_A = "userA"
        self.TEST_USER_B = "userB"
        self.TEST_USER_C = "userC"

        self.LEVEL_INPUT_A = "aaa-aaa-aaa"
        self.LEVEL_EXPECTED_A = "AAA-AAA-AAA"

        self.LEVEL_INPUT_B = "bbb-bbb-bbb"
        self.LEVEL_EXPECTED_B = "BBB-BBB-BBB"

        self.LEVEL_INPUT_C = "ccc ccc ccc"
        self.LEVEL_EXPECTED_C = "CCC-CCC-CCC"

        self.LEVEL_INPUT_D = "ddd ddd ddd"
        self.LEVEL_EXPECTED_D = "DDD-DDD-DDD"

        self.LEVEL_INPUT_MULTIPLE_AB = "aaa aaa aaa bbb bbb bbb"
        self.LEVEL_INPUT_MULTIPLE_AB_EXPECTED = ["AAA-AAA-AAA", "BBB-BBB-BBB"]

        self.LEVEL_INPUT_MULTIPLE_BC = "bbb bbb bbb ccc ccc ccc"
        self.LEVEL_INPUT_MULTIPLE_BC_EXPECTED = ["BBB-BBB-BBB", "CCC-CCC-CCC"]

        self.LEVEL_INPUT_MULTIPLE_ABC = "aaa aaa aaa bbb bbb bbb ccc ccc ccc"
        self.LEVEL_INPUT_MULTIPLE_ABC_EXPECTED = [
            "AAA-AAA-AAA",
            "BBB-BBB-BBB",
            "CCC-CCC-CCC",
        ]

        self.LEVEL_INPUT_MULTIPLE_BCD = "bbb bbb bbb ccc ccc ccc ddd ddd ddd"
        self.LEVEL_INPUT_MULTIPLE_BCD_EXPECTED = [
            "BBB-BBB-BBB",
            "CCC-CCC-CCC",
            "DDD-DDD-DDD",
        ]

        self.LEVEL_INPUT_MULTIPLE_ABCD = (
            "aaa aaa aaa bbb bbb bbb ccc ccc ccc ddd ddd ddd"
        )

        self.LEVEL_INVALID_ONE = "abc-def-gh"
        self.LEVEL_INVALID_TWO = "aaa-aaa-aaa aaa aaa aai"
        self.LEVEL_INVALID_THREE_MIDDLE = "aaa-aaa-aaa bbb bbb bbi ccc ccc ccc"
        self.LEVEL_INVALID_THREE_MIDDLE_END = "aaa aaa aaa bbb bbb bbi ccc ccc cci"

    def owner_add_level(self, levelcode):
        command = AddCommand(
            self.test_processor, self.test_owner, self.test_owner, self.LEVEL_INPUT_A
        )
        response = self.test_processor.process_command(command)
        return (command, response)

    def owner_add_level_a(self):
        return self.owner_add_level(self.LEVEL_INPUT_A)

    def owner_add_level_b(self):
        return self.owner_add_level(self.LEVEL_INPUT_B)

    def user_add_level(self, user, levelcode):
        command = AddCommand(self.test_processor, user, user, levelcode)
        response = self.test_processor.process_command(command)
        return (command, response)

    def user_a_add_level(self, levelcode):
        return self.user_add_level(self.TEST_USER_A, levelcode)

    def user_a_add_level_a(self):
        return self.user_a_add_level(self.LEVEL_INPUT_A)

    def user_a_add_level_b(self):
        return self.user_a_add_level(self.LEVEL_INPUT_B)

    def user_a_add_level_c(self):
        return self.user_a_add_level(self.LEVEL_INPUT_C)

    def user_a_add_level_d(self):
        return self.user_a_add_level(self.LEVEL_INPUT_D)

    def user_a_add_invalid_code_one(self):
        return self.user_a_add_level(self.LEVEL_INVALID_ONE)

    def user_a_add_invalid_code_two(self):
        return self.user_a_add_level(self.LEVEL_INVALID_TWO)

    def user_a_add_invalid_code_three_middle(self):
        return self.user_a_add_level(self.LEVEL_INVALID_THREE_MIDDLE)

    def user_a_add_invalid_code_three_middle_end(self):
        return self.user_a_add_level(self.LEVEL_INVALID_THREE_MIDDLE_END)

    def user_a_add_multiple_ab(self):
        return self.user_a_add_level(self.LEVEL_INPUT_MULTIPLE_AB)

    def user_a_add_multiple_bc(self):
        return self.user_a_add_level(self.LEVEL_INPUT_MULTIPLE_BC)

    def user_a_add_multiple_abc(self):
        return self.user_a_add_level(self.LEVEL_INPUT_MULTIPLE_ABC)

    def user_a_add_multiple_bcd(self):
        return self.user_a_add_level(self.LEVEL_INPUT_MULTIPLE_BCD)

    def user_a_add_multiple_abcd(self):
        return self.user_a_add_level(self.LEVEL_INPUT_MULTIPLE_ABCD)

    def user_b_add_level(self, levelcode):
        return self.user_add_level(self.TEST_USER_B, levelcode)

    def user_b_add_level_a(self):
        return self.user_b_add_level(self.LEVEL_INPUT_A)

    def user_b_add_level_b(self):
        return self.user_b_add_level(self.LEVEL_INPUT_B)

    def user_b_add_level_c(self):
        return self.user_b_add_level(self.LEVEL_INPUT_C)

    def user_b_add_level_d(self):
        return self.user_b_add_level(self.LEVEL_INPUT_D)

    def user_a_remove_level(self, levelcode):
        command = RemoveCommand(self.test_processor, self.TEST_USER_A, levelcode)
        response = self.test_processor.process_command(command)
        return (command, response)

    def user_a_remove_level_empty(self):
        return self.user_a_remove_level("")

    def user_a_remove_level_invalid_one(self):
        return self.user_a_remove_level(self.LEVEL_INVALID_ONE)

    def user_a_remove_level_b(self):
        return self.user_a_remove_level(self.LEVEL_INPUT_B)
    
    def user_a_remove_level_none(self):
        return self.user_a_remove_level(None)

    def user_c_add_level(self, levelcode):
        return self.user_add_level(self.TEST_USER_C, levelcode)

    def user_c_add_multiple_abc(self):
        return self.user_c_add_level(self.LEVEL_INPUT_MULTIPLE_ABC)

    def owner_calls_clear(self):
        command = ClearCommand(self.test_processor, self.test_owner)
        response = self.test_processor.process_command(command)
        return (command, response)

    def user_calls_clear(self, username):
        command = ClearCommand(self.test_processor, username)
        response = self.test_processor.process_command(command)
        return (command, response)

    def user_a_calls_clear(self):
        return self.user_calls_clear(self.TEST_USER_A)

    def user_calls_finish(self, user):
        command = FinishCommand(self.test_processor, user)
        response = self.test_processor.process_command(command)
        return (command, response)

    def user_a_calls_finish(self):
        return self.user_calls_finish(self.TEST_USER_A)

    def user_calls_leave(self, user):
        command = LeaveCommand(self.test_processor, user)
        response = self.test_processor.process_command(command)
        return (command, response)

    def user_a_calls_leave(self):
        return self.user_calls_leave(self.TEST_USER_A)

    def user_calls_next(self, user):
        command = NextCommand(self.test_processor, user)
        response = self.test_processor.process_command(command)
        return (command, response)

    def user_a_calls_next(self):
        return self.user_calls_next(self.TEST_USER_A)

    def owner_calls_mod(self, username):
        command = ModCommand(self.test_processor, self.test_owner, username)
        response = self.test_processor.process_command(command)
        return (command, response)

    def user_calls_mod(self, invoker, user_to_mod):
        command = ModCommand(self.test_processor, invoker, user_to_mod)
        response = self.test_processor.process_command(command)
        return (command, response)

    def user_a_calls_mod_none(self):
        return self.user_calls_mod(self.TEST_USER_A, None)

    def owner_calls_unmod(self, username):
        command = UnmodCommand(self.test_processor, self.test_owner, username)
        response = self.test_processor.process_command(command)
        return (command, response)

    def owner_calls_unmod_user_a(self):
        return self.owner_calls_unmod(self.TEST_USER_A)

    def current_called(self):
        command = CurrentCommand(self.test_processor)
        response = self.test_processor.process_command(command)
        return (command, response)

    def owner_calls_mod_user_a(self):
        return self.owner_calls_mod(self.TEST_USER_A)

    def owner_calls_mod_empty(self):
        return self.owner_calls_mod("")

    def owner_calls_mod_none(self):
        return self.owner_calls_mod(None)

    def owner_calls_next(self):
        command = NextCommand(self.test_processor, self.test_owner)
        response = self.test_processor.process_command(command)
        return (command, response)

    def owner_calls_finish(self):
        command = FinishCommand(self.test_processor, self.test_owner)
        response = self.test_processor.process_command(command)
        return (command, response)

    def owner_calls_remove(self, level):
        command = RemoveCommand(self.test_processor, self.test_owner, level)
        response = self.test_processor.process_command(command)
        return (command, response)

    def owner_calls_remove_level_a(self):
        return self.owner_calls_remove(self.LEVEL_INPUT_A)

    def owner_calls_remove_none(self):
        return self.owner_calls_remove(None)

    def owner_calls_random(self):
        command = RandomCommand(self.test_processor, self.test_owner)
        response = self.test_processor.process_command(command)
        return (command, response)

    def user_calls_random(self, user):
        command = RandomCommand(self.test_processor, user)
        response = self.test_processor.process_command(command)
        return (command, response)

    def user_a_calls_random(self):
        return self.user_calls_random(self.TEST_USER_A)

    def list_called(self):
        command = ListCommand(self.test_processor)
        response = self.test_processor.process_command(command)
        return (command, response)
