import unittest

from nullconstpointer.tests.helper import TestHelper


class TestCommandCurrent(unittest.TestCase):
    def setUp(self):
        self.test_helper = TestHelper()

    def test_current_level_is_none(self):
        command, response = self.test_helper.current_called()
        self.assertEqual(response, command.fail_current_level_not_selected())

    def test_current_level_success_with_next_level_owner(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.owner_calls_next_no_args()
        command, response = self.test_helper.current_called()

        self.assertEqual(response, command.success_current_level())

    def test_current_changes_after_level_removed(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.user_b_add_level_b()
        self.test_helper.owner_calls_next_no_args()
        self.test_helper.owner_calls_finish()
        self.test_helper.owner_calls_next_no_args()
        command, response = self.test_helper.current_called()

        self.assertEqual(response, command.success_current_level())

    def test_remove_clears_current(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.owner_calls_next_no_args()
        self.test_helper.owner_calls_remove_level_a()
        command, response = self.test_helper.current_called()

        self.assertEqual(response, command.fail_current_level_not_selected())

    def test_finish_clears_current(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.owner_calls_next_no_args()
        self.test_helper.owner_calls_finish()
        command, response = self.test_helper.current_called()

        self.assertEqual(response, command.fail_current_level_not_selected())

    def test_next_user_updates_current(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.owner_calls_next_user_a()
        command, response = self.test_helper.current_called()

        self.assertEqual(response, command.success_current_level())
