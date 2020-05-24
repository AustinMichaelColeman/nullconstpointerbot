import unittest

from nullconstpointer.tests.helper import TestHelper


class TestCommandTimer(unittest.TestCase):
    def setUp(self):
        self.test_helper = TestHelper()

    def test_non_owner_with_timer_set(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.owner_calls_next_no_args()
        self.test_helper.owner_calls_timer()
        command, response = self.test_helper.owner_calls_timer_no_args()

        self.assertEqual(
            response, self.test_helper.success_time_remaining_user_a_level_a(command),
        )

    def test_non_owner_with_timer_not_set(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.owner_calls_next_no_args()
        command, response = self.test_helper.user_a_calls_timer_no_args()

        self.assertEqual(response, command.fail_timer_not_set())

    def test_owner_with_timer_set(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.owner_calls_next_no_args()
        self.test_helper.owner_calls_timer()
        command, response = self.test_helper.owner_calls_timer()

        self.assertEqual(
            response, command.success_starting_new_timer_stopping_previous()
        )

    def test_owner_with_timer_not_set(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.owner_calls_next_no_args()
        command, response = self.test_helper.owner_calls_timer()

        self.assertEqual(response, command.success_starting_new_timer())

    def test_owner_without_current_level(self):
        command, response = self.test_helper.owner_calls_timer()

        self.assertEqual(response, command.fail_no_current_level())

    def test_owner_calls_timer_no_args_with_level_set(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.owner_calls_next_no_args()
        command, response = self.test_helper.owner_calls_timer_no_args()
        self.assertEqual(response, command.fail_enter_a_timer_value())

    def test_timer_finish_calls_success_time_expired(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.owner_calls_next_no_args()
        self.test_helper.owner_calls_timer()
        self.test_helper.test_processor.time_remaining = 0
        command, response = self.test_helper.owner_calls_timer_no_args()
        self.assertEqual(
            response,
            command.success_time_expired(
                self.test_helper.test_processor.next_level(),
                self.test_helper.test_processor.current_user,
            ),
        )
