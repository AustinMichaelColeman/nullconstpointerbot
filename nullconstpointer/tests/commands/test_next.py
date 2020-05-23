import unittest

from nullconstpointer.tests.helper import TestHelper


class TestCommandNext(unittest.TestCase):
    def setUp(self):
        self.test_helper = TestHelper()

    def test_next_level_fails_if_no_more_levels(self):
        command, response = self.test_helper.owner_calls_next()

        self.assertEqual(response, command.fail_next_level_no_more_levels())

    def test_next_level_fails_if_not_owner(self):
        self.test_helper.user_a_add_level_a()
        command, response = self.test_helper.user_a_calls_next()

        self.assertEqual(response, command.fail_next_level_not_owner())

    def test_next_level_success(self):
        self.test_helper.user_a_add_level_a()
        command, response = self.test_helper.owner_calls_next()

        self.assertEqual(
            response,
            command.success_next_level(
                self.test_helper.LEVEL_EXPECTED_A, self.test_helper.TEST_USER_A
            ),
        )

    def test_next_not_usable_by_mods(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.owner_calls_mod_user_a()
        command, response = self.test_helper.user_a_calls_next()

        self.assertEqual(response, command.fail_next_level_not_owner())
