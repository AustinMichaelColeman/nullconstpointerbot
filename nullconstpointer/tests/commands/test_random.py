import unittest

from nullconstpointer.tests.helper import TestHelper


class TestCommandRandom(unittest.TestCase):
    def setUp(self):
        self.test_helper = TestHelper()

    def test_random_called_by_owner_with_no_levels(self):
        command, response = self.test_helper.owner_calls_random()

        self.assertEqual(response, command.fail_random_no_levels())

    def test_random_called_by_owner_with_levels(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.user_b_add_level_b()
        command, response = self.test_helper.owner_calls_random()

        possible_responses = [
            command.success_random_level(
                self.test_helper.TEST_USER_A, self.test_helper.LEVEL_EXPECTED_A
            ),
            command.success_random_level(
                self.test_helper.TEST_USER_B, self.test_helper.LEVEL_EXPECTED_B
            ),
        ]

        self.assertIn(response, possible_responses)

    def test_random_called_by_owner_first_level_submitted_selected(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.user_a_add_level_b()
        self.test_helper.user_a_add_level_c()
        command, response = self.test_helper.owner_calls_random()

        self.assertEqual(
            response,
            command.success_random_level(
                self.test_helper.TEST_USER_A, self.test_helper.LEVEL_EXPECTED_A
            ),
        )

        self.test_helper.owner_calls_remove_level_a()
        command, response = self.test_helper.owner_calls_random()

        self.assertEqual(
            response,
            command.success_random_level(
                self.test_helper.TEST_USER_A, self.test_helper.LEVEL_EXPECTED_B
            ),
        )

    def test_random_called_by_owner_first_level_submitted_selected_multi_user(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.user_b_add_level_b()
        self.test_helper.user_a_add_level_c()
        self.test_helper.user_b_add_level_d()
        command, response = self.test_helper.owner_calls_random()

        possible_responses = [
            command.success_random_level(
                self.test_helper.TEST_USER_A, self.test_helper.LEVEL_EXPECTED_A
            ),
            command.success_random_level(
                self.test_helper.TEST_USER_B, self.test_helper.LEVEL_EXPECTED_B
            ),
        ]

        self.assertIn(response, possible_responses)

    def test_random_called_by_mod(self):
        self.test_helper.owner_calls_mod_user_a()
        command, response = self.test_helper.user_a_calls_random()

        self.assertEqual(
            response, command.fail_random_no_permission(self.test_helper.TEST_USER_A)
        )

    def test_random_called_by_user(self):
        command, response = self.test_helper.user_a_calls_random()

        self.assertEqual(
            response, command.fail_random_no_permission(self.test_helper.TEST_USER_A)
        )
