import unittest

from nullconstpointer.tests.helper import TestHelper


class TestCommandFinish(unittest.TestCase):
    def setUp(self):
        self.test_helper = TestHelper()

    def test_finish_called_by_owner_no_levels(self):
        command, response = self.test_helper.owner_calls_finish()

        self.assertEqual(response, command.fail_finish_no_levels())

    def test_finish_called_by_owner_with_levels(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.owner_calls_random()
        command, response = self.test_helper.owner_calls_finish()

        self.assertEqual(
            response,
            command.success_remove_user_level(
                self.test_helper.TEST_USER_A, self.test_helper.LEVEL_EXPECTED_A
            ),
        )

    def test_finish_called_by_user_with_levels(self):
        self.test_helper.user_a_add_level_a()
        command, response = self.test_helper.user_a_calls_finish()

        self.assertEqual(
            response, command.fail_finish_no_permission(self.test_helper.TEST_USER_A)
        )

    def test_finish_called_by_user_without_levels(self):
        command, response = self.test_helper.user_a_calls_finish()

        self.assertEqual(
            response, command.fail_finish_no_permission(self.test_helper.TEST_USER_A)
        )

    def test_finish_called_by_mod_with_levels(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.owner_calls_mod_user_a()
        self.test_helper.owner_calls_next_no_args()
        command, response = self.test_helper.user_a_calls_finish()

        self.assertEqual(
            response,
            command.success_remove_user_level(
                self.test_helper.TEST_USER_A, self.test_helper.LEVEL_EXPECTED_A
            ),
        )

    def test_finish_called_by_mod_without_levels(self):
        self.test_helper.owner_calls_mod_user_a()
        command, response = self.test_helper.user_a_calls_finish()

        self.assertEqual(response, command.fail_finish_no_levels())

    def test_current_has_correct_output_after_finish_same_user(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.user_a_add_level_b()
        self.test_helper.owner_calls_next_no_args()
        self.test_helper.owner_calls_finish()
        command, response = self.test_helper.current_called()

        self.assertEqual(response, command.fail_current_level_not_selected())

    def test_current_has_correct_output_after_finish_different_user(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.user_b_add_level_b()
        self.test_helper.owner_calls_next_no_args()
        self.test_helper.owner_calls_finish()
        command, response = self.test_helper.current_called()

        self.assertEqual(response, command.fail_current_level_not_selected())
