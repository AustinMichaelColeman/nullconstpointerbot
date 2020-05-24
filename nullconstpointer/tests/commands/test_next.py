import unittest

from nullconstpointer.tests.helper import TestHelper


class TestCommandNext(unittest.TestCase):
    def setUp(self):
        self.test_helper = TestHelper()

    def test_next_level_fails_if_no_more_levels(self):
        command, response = self.test_helper.owner_calls_next_no_args()

        self.assertEqual(response, command.fail_next_level_no_more_levels())

    def test_next_level_fails_if_not_mod(self):
        self.test_helper.user_a_add_level_a()
        command, response = self.test_helper.user_a_calls_next_no_args()

        self.assertEqual(response, command.fail_next_level_not_mod())

    def test_next_level_success(self):
        self.test_helper.user_a_add_level_a()
        command, response = self.test_helper.owner_calls_next_no_args()

        self.assertEqual(
            response,
            command.success_next_level(
                self.test_helper.LEVEL_EXPECTED_A, self.test_helper.TEST_USER_A
            ),
        )

    def test_next_usable_by_mods(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.owner_calls_mod_user_a()
        command, response = self.test_helper.user_a_calls_next_no_args()

        self.assertEqual(
            response,
            command.success_next_level(
                self.test_helper.LEVEL_EXPECTED_A, self.test_helper.TEST_USER_A
            ),
        )

    def test_user_calls_next_user_fails_no_permission_no_levels(self):
        command, response = self.test_helper.user_a_calls_next_user_b()

        self.assertEqual(response, command.fail_next_level_not_mod())

    def test_user_calls_next_user_fails_no_permission_with_levels(self):
        self.test_helper.user_b_add_level_a()
        command, response = self.test_helper.user_a_calls_next_user_b()

        self.assertEqual(response, command.fail_next_level_not_mod())

    def test_mod_calls_next_user_succeeds(self):
        self.test_helper.owner_calls_mod_user_a()
        self.test_helper.user_b_add_level_a()
        command, response = self.test_helper.user_a_calls_next_user_b()

        self.assertEqual(
            response,
            command.success_next_level(
                self.test_helper.LEVEL_EXPECTED_A, self.test_helper.TEST_USER_B
            ),
        )

    def test_mod_calls_next_user_fails_no_levels(self):
        self.test_helper.owner_calls_mod_user_a()
        command, response = self.test_helper.user_a_calls_next_user_b()

        self.assertEqual(
            response, command.fail_user_no_levels(self.test_helper.TEST_USER_B),
        )

    def test_next_user_does_not_exist_owner(self):
        command, response = self.test_helper.owner_calls_next_user_a()

        self.assertEqual(
            response, command.fail_user_no_levels(self.test_helper.TEST_USER_A)
        )
