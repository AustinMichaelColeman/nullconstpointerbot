import unittest

from nullconstpointer.tests.helper import TestHelper


class TestCommandRemove(unittest.TestCase):
    def setUp(self):
        self.test_helper = TestHelper()

    def test_remove_called_without_args(self):
        command, response = self.test_helper.user_a_remove_level_empty()

        self.assertEqual(response, command.fail_remove_no_level_specified())

    def test_remove_called_with_invalid_level_format(self):
        command, response = self.test_helper.user_a_remove_level_invalid_one()

        self.assertEqual(
            response,
            command.fail_remove_invalid_level_code(self.test_helper.LEVEL_INVALID_ONE),
        )

    def test_remove_level_not_found(self):
        command, response = self.test_helper.user_a_remove_level_b()

        self.assertEqual(
            response,
            command.fail_remove_level_not_found(self.test_helper.LEVEL_EXPECTED_B),
        )

    def test_remove_called_by_user_with_one_level(self):
        self.test_helper.user_a_add_level_b()
        command, response = self.test_helper.user_a_remove_level_b()

        self.assertEqual(
            response,
            command.success_remove_user_level(
                self.test_helper.TEST_USER_A, self.test_helper.LEVEL_EXPECTED_B
            ),
        )

    def test_remove_called_by_user_with_two_levels(self):
        self.test_helper.user_a_add_level_b()
        self.test_helper.user_a_add_level_a()
        command, response = self.test_helper.user_a_remove_level_b()

        self.assertEqual(
            response,
            command.success_remove_user_level(
                self.test_helper.TEST_USER_A, self.test_helper.LEVEL_EXPECTED_B
            ),
        )

    def test_remove_called_by_mod(self):
        self.test_helper.owner_calls_mod_user_a()
        self.test_helper.user_b_add_level_b()
        command, response = self.test_helper.user_a_remove_level_b()

        self.assertEqual(
            response,
            command.success_remove_user_level(
                self.test_helper.TEST_USER_B, self.test_helper.LEVEL_EXPECTED_B
            ),
        )

    def test_remove_called_by_owner(self):
        self.test_helper.user_a_add_level_a()
        command, response = self.test_helper.owner_calls_remove_level_a()

        self.assertEqual(
            response,
            command.success_remove_user_level(
                self.test_helper.TEST_USER_A, self.test_helper.LEVEL_EXPECTED_A
            ),
        )

    def test_remove_called_by_user_fails(self):
        self.test_helper.user_b_add_level_b()
        command, response = self.test_helper.user_a_remove_level_b()

        self.assertEqual(
            response,
            command.fail_remove_no_permission(
                self.test_helper.TEST_USER_A,
                self.test_helper.TEST_USER_B,
                self.test_helper.LEVEL_EXPECTED_B,
            ),
        )

    def test_remove_level_none_fails_owner(self):
        command, response = self.test_helper.owner_calls_remove_none()

        self.assertEqual(response, command.fail_remove_no_level_specified())

    def test_remove_level_none_fails_mod(self):
        self.test_helper.owner_calls_mod_user_a()
        command, response = self.test_helper.user_a_remove_level_none()

        self.assertEqual(response, command.fail_remove_no_level_specified())

    def test_remove_level_none_fails_user(self):
        self.test_helper.owner_calls_mod_user_a()
        self.test_helper.owner_calls_unmod_user_a()
        command, response = self.test_helper.user_a_remove_level_none()

        self.assertEqual(
            response, command.fail_remove_no_level_specified(),
        )
