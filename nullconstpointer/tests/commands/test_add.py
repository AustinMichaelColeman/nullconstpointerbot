import unittest
from nullconstpointer.tests.helper import TestHelper


class TestCommandAdd(unittest.TestCase):
    def setUp(self):
        self.test_helper = TestHelper()

    def test_add_user_level_response_valid(self):
        command, response = self.test_helper.user_a_add_level_a()

        self.assertEqual(
            response,
            command.success_add_user_level(
                self.test_helper.TEST_USER_A, self.test_helper.LEVEL_EXPECTED_A
            ),
        )

    def test_add_user_level_multiple_duplicate_levels_fails(self):
        self.test_helper.user_a_add_level_a()
        (command, response) = self.test_helper.user_a_add_level_a()

        self.assertEqual(
            response,
            command.fail_add_user_level_duplicate_code(
                self.test_helper.TEST_USER_A,
                self.test_helper.LEVEL_EXPECTED_A,
                self.test_helper.TEST_USER_A,
            ),
        )

    def test_add_user_level_multiple_different_levels_succeeds(self):
        self.test_helper.user_a_add_level_a()
        command, response = self.test_helper.user_a_add_level_b()

        self.assertEqual(
            response,
            command.success_add_user_level(
                self.test_helper.TEST_USER_A, self.test_helper.LEVEL_EXPECTED_B
            ),
        )

    def test_add_user_level_response_invalid(self):
        (command, response) = self.test_helper.user_a_add_invalid_code_one()
        self.assertEqual(
            response,
            command.fail_add_user_level_invalid_code(
                self.test_helper.TEST_USER_A, self.test_helper.LEVEL_INVALID_ONE
            ),
        )

    def test_two_levels_simultaneous_valid(self):
        (command, response) = self.test_helper.user_a_add_multiple_ab()

        self.assertEqual(
            response,
            command.success_add_user_level(
                self.test_helper.TEST_USER_A,
                self.test_helper.LEVEL_INPUT_MULTIPLE_AB_EXPECTED,
            ),
        )

    def test_one_valid_and_one_invalid_level_fails(self):
        (command, response) = self.test_helper.user_a_add_invalid_code_two()

        self.assertEqual(
            response,
            command.fail_add_user_level_invalid_code(
                self.test_helper.TEST_USER_A, self.test_helper.LEVEL_INVALID_TWO
            ),
        )

    def test_middle_invalid(self):
        (command, response) = self.test_helper.user_a_add_invalid_code_three_middle()

        self.assertEqual(
            response,
            command.fail_add_user_level_invalid_code(
                self.test_helper.TEST_USER_A,
                self.test_helper.LEVEL_INVALID_THREE_MIDDLE,
            ),
        )

    def test_end_and_middle_invalid(self):
        (
            command,
            response,
        ) = self.test_helper.user_a_add_invalid_code_three_middle_end()
        self.assertEqual(
            response,
            command.fail_add_user_level_invalid_code(
                self.test_helper.TEST_USER_A,
                self.test_helper.LEVEL_INVALID_THREE_MIDDLE_END,
            ),
        )

    def test_level_limit(self):
        (command, response) = self.test_helper.user_a_add_multiple_abcd()

        self.assertEqual(
            response,
            command.fail_add_user_level_level_limit(self.test_helper.TEST_USER_A),
        )

    def test_limit_one_at_a_time_fails_past_limit(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.user_a_add_level_b()
        self.test_helper.user_a_add_level_c()
        (command, response) = self.test_helper.user_a_add_level_d()

        self.assertEqual(
            response,
            command.fail_add_user_level_level_limit(self.test_helper.TEST_USER_A),
        )

    def test_limit_one_at_a_time_succeeds_at_limit(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.user_a_add_level_b()
        (command, response) = self.test_helper.user_a_add_level_c()

        self.assertEqual(
            response,
            command.success_add_user_level(
                self.test_helper.TEST_USER_A, self.test_helper.LEVEL_EXPECTED_C
            ),
        )

    def test_limit_after_removal(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.user_a_add_level_b()
        self.test_helper.user_a_add_level_c()

        self.test_helper.user_a_remove_level_b()

        (command, response) = self.test_helper.user_a_add_level_b()

        self.assertEqual(
            response,
            command.success_add_user_level(
                self.test_helper.TEST_USER_A, self.test_helper.LEVEL_EXPECTED_B
            ),
        )

    def test_limit_one_then_multi(self):
        self.test_helper.user_a_add_level_a()
        (command, response) = self.test_helper.user_a_add_multiple_bcd()

        self.assertEqual(
            response,
            command.fail_add_user_level_level_limit(self.test_helper.TEST_USER_A),
        )

    def test_limit_duplicate_multi(self):
        self.test_helper.user_a_add_multiple_bc()
        (command, response) = self.test_helper.user_a_add_multiple_abc()

        self.assertEqual(
            response,
            command.fail_add_user_level_duplicate_code(
                self.test_helper.TEST_USER_A,
                self.test_helper.LEVEL_EXPECTED_B,
                self.test_helper.TEST_USER_A,
            ),
        )

    def test_limit_duplicate_multi_user(self):
        self.test_helper.user_b_add_level_b()
        self.test_helper.user_a_add_level_a()
        (command, response) = self.test_helper.user_c_add_multiple_abc()

        self.assertEqual(
            response,
            command.fail_add_user_level_duplicate_code(
                self.test_helper.TEST_USER_C,
                self.test_helper.LEVEL_EXPECTED_A,
                self.test_helper.TEST_USER_A,
            ),
        )

    def test_duplicate_multi_AA(self):
        command, response = self.test_helper.user_a_add_code_duplicate_AA()
        self.assertEqual(
            response,
            command.success_add_user_level(
                self.test_helper.TEST_USER_A, self.test_helper.LEVEL_EXPECTED_A,
            ),
        )
        self.assertEqual(self.test_helper.test_processor.level_count(), 1)

    def test_duplicate_multi_ABB(self):
        command, response = self.test_helper.user_a_add_code_duplicate_ABB()
        self.assertEqual(
            response,
            command.success_add_user_level(
                self.test_helper.TEST_USER_A,
                self.test_helper.LEVEL_INPUT_MULTIPLE_AB_EXPECTED,
            ),
        )
        self.assertEqual(self.test_helper.test_processor.level_count(), 2)

    def test_duplicate_multi_ABA(self):
        command, response = self.test_helper.user_a_add_code_duplicate_ABA()
        self.assertEqual(
            response,
            command.success_add_user_level(
                self.test_helper.TEST_USER_A,
                self.test_helper.LEVEL_INPUT_MULTIPLE_AB_EXPECTED,
            ),
        )
        self.assertEqual(self.test_helper.test_processor.level_count(), 2)
