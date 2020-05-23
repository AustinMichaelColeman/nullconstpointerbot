import unittest

from nullconstpointer.tests.helper import TestHelper


class TestCommandClear(unittest.TestCase):
    def setUp(self):
        self.test_helper = TestHelper()

    def test_clear_called_by_owner(self):
        command, response = self.test_helper.owner_calls_clear()

        self.assertEqual(response, command.success_clear_owner())

    def test_clear_called_by_owner_with_levels(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.user_a_add_level_b()
        self.test_helper.user_b_add_level_c()

        command, response = self.test_helper.owner_calls_clear()

        self.assertEqual(response, command.success_clear_owner())

    def test_clear_called_by_mod_without_levels(self):
        self.test_helper.owner_calls_mod_user_a()
        command, response = self.test_helper.user_a_calls_clear()

        self.assertEqual(
            response, command.fail_clear_user_no_levels(self.test_helper.TEST_USER_A)
        )

    def test_clear_called_by_mod_with_levels(self):
        self.test_helper.owner_calls_mod_user_a()
        self.test_helper.user_a_add_level_a()
        command, response = self.test_helper.user_a_calls_clear()

        self.assertEqual(
            response, command.success_clear_user(self.test_helper.TEST_USER_A)
        )

    def test_clear_called_by_user_without_levels(self):
        command, response = self.test_helper.user_a_calls_clear()

        self.assertEqual(
            response, command.fail_clear_user_no_levels(self.test_helper.TEST_USER_A)
        )

    def test_clear_called_by_user_with_levels(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.user_a_add_level_b()
        self.test_helper.user_b_add_level_c()
        command, response = self.test_helper.user_a_calls_clear()

        self.assertEqual(
            response, command.success_clear_user(self.test_helper.TEST_USER_A)
        )
        self.assertEqual(self.test_helper.test_processor.level_count(), 1)
