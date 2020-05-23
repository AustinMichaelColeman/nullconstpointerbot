import unittest

from nullconstpointer.tests.helper import TestHelper


class TestCommandLeave(unittest.TestCase):
    def setUp(self):
        self.test_helper = TestHelper()

    def test_leave_called_by_user_with_no_levels(self):
        command, response = self.test_helper.user_a_calls_leave()

        self.assertEqual(
            response, command.fail_leave_no_levels(self.test_helper.TEST_USER_A)
        )

    def test_leave_called_by_user_with_one_level(self):
        self.test_helper.user_a_add_level_a()
        command, response = self.test_helper.user_a_calls_leave()

        self.assertEqual(response, command.success_leave(self.test_helper.TEST_USER_A))

    def test_leave_called_by_user_with_two_levels(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.user_a_add_level_b()
        command, response = self.test_helper.user_a_calls_leave()

        self.assertEqual(response, command.success_leave(self.test_helper.TEST_USER_A))

    def test_leave_called_by_mod_with_no_levels(self):
        self.test_helper.owner_calls_mod_user_a()
        command, response = self.test_helper.user_a_calls_leave()

        self.assertEqual(
            response, command.fail_leave_no_levels(self.test_helper.TEST_USER_A)
        )

    def test_leave_called_by_mod_with_levels(self):
        self.test_helper.owner_calls_mod_user_a()
        self.test_helper.user_a_add_level_a()
        command, response = self.test_helper.user_a_calls_leave()

        self.assertEqual(response, command.success_leave(self.test_helper.TEST_USER_A))
