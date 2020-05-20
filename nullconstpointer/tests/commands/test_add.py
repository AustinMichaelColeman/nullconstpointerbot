import unittest
from nullconstpointer.bot.user import User, MOD_LEVEL_OWNER
from nullconstpointer.bot.processor import Processor
from nullconstpointer.commands.add import AddCommand
from nullconstpointer.commands.remove import RemoveCommand

TEST_USER_A = "userA"
TEST_USER_B = "userB"
TEST_USER_C = "userC"

LEVEL_INPUT_A = "aaa-aaa-aaa"
LEVEL_EXPECTED_A = "AAA-AAA-AAA"

LEVEL_INPUT_B = "bbb-bbb-bbb"
LEVEL_EXPECTED_B = "BBB-BBB-BBB"

LEVEL_INPUT_C = "ccc ccc ccc"
LEVEL_EXPECTED_C = "CCC-CCC-CCC"

LEVEL_INPUT_D = "ddd ddd ddd"
LEVEL_EXPECTED_D = "DDD-DDD-DDD"

LEVEL_INPUT_MULTIPLE_AB = "aaa aaa aaa bbb bbb bbb"
LEVEL_INPUT_MULTIPLE_AB_EXPECTED = ["AAA-AAA-AAA", "BBB-BBB-BBB"]

LEVEL_INPUT_MULTIPLE_BC = "bbb bbb bbb ccc ccc ccc"
LEVEL_INPUT_MULTIPLE_BC_EXPECTED = ["BBB-BBB-BBB", "CCC-CCC-CCC"]

LEVEL_INPUT_MULTIPLE_ABC = "aaa aaa aaa bbb bbb bbb ccc ccc ccc"
LEVEL_INPUT_MULTIPLE_ABC_EXPECTED = ["AAA-AAA-AAA", "BBB-BBB-BBB", "CCC-CCC-CCC"]

LEVEL_INPUT_MULTIPLE_BCD = "bbb bbb bbb ccc ccc ccc ddd ddd ddd"
LEVEL_INPUT_MULTIPLE_BCD_EXPECTED = ["BBB-BBB-BBB", "CCC-CCC-CCC", "DDD-DDD-DDD"]

LEVEL_INPUT_MULTIPLE_ABCD = "aaa aaa aaa bbb bbb bbb ccc ccc ccc ddd ddd ddd"

LEVEL_INVALID_ONE = "abc-def-gh"
LEVEL_INVALID_TWO = "aaa-aaa-aaa aaa aaa aai"
LEVEL_INVALID_THREE_MIDDLE = "aaa-aaa-aaa bbb bbb bbi ccc ccc ccc"
LEVEL_INVALID_THREE_MIDDLE_END = "aaa aaa aaa bbb bbb bbi ccc ccc cci"


class TestCommandAdd(unittest.TestCase):
    def setUp(self):
        self.test_owner = User("test_owner", MOD_LEVEL_OWNER)
        self.test_processor = Processor(self.test_owner)

    def owner_add_level(self, levelcode):
        command = AddCommand(
            self.test_processor, self.test_owner, self.test_owner, LEVEL_INPUT_A
        )
        response = self.test_processor.process_command(command)
        return (command, response)

    def owner_add_level_a(self):
        return self.owner_add_level(LEVEL_INPUT_A)

    def owner_add_level_b(self):
        return self.owner_add_level(LEVEL_INPUT_B)

    def user_add_level(self, user, levelcode):
        command = AddCommand(self.test_processor, user, user, levelcode)
        response = self.test_processor.process_command(command)
        return (command, response)

    def user_a_add_level(self, levelcode):
        return self.user_add_level(TEST_USER_A, levelcode)

    def user_a_add_level_a(self):
        return self.user_a_add_level(LEVEL_INPUT_A)

    def user_a_add_level_b(self):
        return self.user_a_add_level(LEVEL_INPUT_B)

    def user_a_add_level_c(self):
        return self.user_a_add_level(LEVEL_INPUT_C)

    def user_a_add_level_d(self):
        return self.user_a_add_level(LEVEL_INPUT_D)

    def user_a_add_invalid_code_one(self):
        return self.user_a_add_level(LEVEL_INVALID_ONE)

    def user_a_add_invalid_code_two(self):
        return self.user_a_add_level(LEVEL_INVALID_TWO)

    def user_a_add_invalid_code_three_middle(self):
        return self.user_a_add_level(LEVEL_INVALID_THREE_MIDDLE)

    def user_a_add_invalid_code_three_middle_end(self):
        return self.user_a_add_level(LEVEL_INVALID_THREE_MIDDLE_END)

    def user_a_add_multiple_ab(self):
        return self.user_a_add_level(LEVEL_INPUT_MULTIPLE_AB)

    def user_a_add_multiple_bc(self):
        return self.user_a_add_level(LEVEL_INPUT_MULTIPLE_BC)

    def user_a_add_multiple_abc(self):
        return self.user_a_add_level(LEVEL_INPUT_MULTIPLE_ABC)

    def user_a_add_multiple_bcd(self):
        return self.user_a_add_level(LEVEL_INPUT_MULTIPLE_BCD)

    def user_a_add_multiple_abcd(self):
        return self.user_a_add_level(LEVEL_INPUT_MULTIPLE_ABCD)

    def user_b_add_level(self, levelcode):
        return self.user_add_level(TEST_USER_B, levelcode)

    def user_b_add_level_a(self):
        return self.user_b_add_level(LEVEL_INPUT_A)

    def user_b_add_level_b(self):
        return self.user_b_add_level(LEVEL_INPUT_B)

    def user_b_add_level_c(self):
        return self.user_b_add_level(LEVEL_INPUT_C)

    def user_b_add_level_d(self):
        return self.user_b_add_level(LEVEL_INPUT_D)

    def user_a_remove_level(self, levelcode):
        command = RemoveCommand(self.test_processor, TEST_USER_A, levelcode)
        response = self.test_processor.process_command(command)
        return (command, response)

    def user_a_remove_level_b(self):
        return self.user_a_remove_level(LEVEL_INPUT_B)

    def user_c_add_level(self, levelcode):
        return self.user_add_level(TEST_USER_C, levelcode)

    def user_c_add_multiple_abc(self):
        return self.user_c_add_level(LEVEL_INPUT_MULTIPLE_ABC)

    def test_add_user_level_response_valid(self):
        command, response = self.user_a_add_level_a()

        self.assertEqual(
            response, command.success_add_user_level(TEST_USER_A, LEVEL_EXPECTED_A)
        )

    def test_add_user_level_multiple_duplicate_levels_fails(self):
        self.user_a_add_level_a()
        (command, response) = self.user_a_add_level_a()

        self.assertEqual(
            response,
            command.fail_add_user_level_duplicate_code(
                TEST_USER_A, LEVEL_EXPECTED_A, TEST_USER_A
            ),
        )

    def test_add_user_level_multiple_different_levels_succeeds(self):
        self.user_a_add_level_a()
        command, response = self.user_a_add_level_b()

        self.assertEqual(
            response, command.success_add_user_level(TEST_USER_A, LEVEL_EXPECTED_B),
        )

    def test_add_user_level_response_invalid(self):
        (command, response) = self.user_a_add_invalid_code_one()
        self.assertEqual(
            response,
            command.fail_add_user_level_invalid_code(TEST_USER_A, LEVEL_INVALID_ONE),
        )

    def test_two_levels_simultaneous_valid(self):
        (command, response) = self.user_a_add_multiple_ab()

        self.assertEqual(
            response,
            command.success_add_user_level(
                TEST_USER_A, LEVEL_INPUT_MULTIPLE_AB_EXPECTED
            ),
        )

    def test_one_valid_and_one_invalid_level_fails(self):
        (command, response) = self.user_a_add_invalid_code_two()

        self.assertEqual(
            response,
            command.fail_add_user_level_invalid_code(TEST_USER_A, LEVEL_INVALID_TWO),
        )

    def test_middle_invalid(self):
        (command, response) = self.user_a_add_invalid_code_three_middle()

        self.assertEqual(
            response,
            command.fail_add_user_level_invalid_code(
                TEST_USER_A, LEVEL_INVALID_THREE_MIDDLE
            ),
        )

    def test_end_and_middle_invalid(self):
        (command, response) = self.user_a_add_invalid_code_three_middle_end()
        self.assertEqual(
            response,
            command.fail_add_user_level_invalid_code(
                TEST_USER_A, LEVEL_INVALID_THREE_MIDDLE_END
            ),
        )

    def test_level_limit(self):
        (command, response) = self.user_a_add_multiple_abcd()

        self.assertEqual(response, command.fail_add_user_level_level_limit(TEST_USER_A))

    def test_limit_one_at_a_time_fails_past_limit(self):
        self.user_a_add_level_a()
        self.user_a_add_level_b()
        self.user_a_add_level_c()
        (command, response) = self.user_a_add_level_d()

        self.assertEqual(response, command.fail_add_user_level_level_limit(TEST_USER_A))

    def test_limit_one_at_a_time_succeeds_at_limit(self):
        self.user_a_add_level_a()
        self.user_a_add_level_b()
        (command, response) = self.user_a_add_level_c()

        self.assertEqual(
            response, command.success_add_user_level(TEST_USER_A, LEVEL_EXPECTED_C)
        )

    def test_limit_after_removal(self):
        self.user_a_add_level_a()
        self.user_a_add_level_b()
        self.user_a_add_level_c()

        self.user_a_remove_level_b()

        (command, response) = self.user_a_add_level_b()

        self.assertEqual(
            response, command.success_add_user_level(TEST_USER_A, LEVEL_EXPECTED_B)
        )

    def test_limit_one_then_multi(self):
        self.user_a_add_level_a()
        (command, response) = self.user_a_add_multiple_bcd()

        self.assertEqual(
            response, command.fail_add_user_level_level_limit(TEST_USER_A),
        )

    def test_limit_duplicate_multi(self):
        self.user_a_add_multiple_bc()
        (command, response) = self.user_a_add_multiple_abc()

        self.assertEqual(
            response,
            command.fail_add_user_level_duplicate_code(
                TEST_USER_A, LEVEL_EXPECTED_B, TEST_USER_A
            ),
        )

    def test_limit_duplicate_multi_user(self):
        self.user_b_add_level_b()
        self.user_a_add_level_a()
        (command, response) = self.user_c_add_multiple_abc()

        self.assertEqual(
            response,
            command.fail_add_user_level_duplicate_code(
                TEST_USER_C, LEVEL_EXPECTED_A, TEST_USER_A
            ),
        )
