import unittest

from nullconstpointer.tests.helper import TestHelper


class TestCommandUnmod(unittest.TestCase):
    def setUp(self):
        self.test_helper = TestHelper()

    def test_unmod_success(self):
        self.test_helper.owner_calls_mod_user_a()
        command, response = self.test_helper.owner_calls_unmod_user_a()

        self.assertEqual(response, command.success_unmod(self.test_helper.TEST_USER_A))

    def test_user_calls_unmod_fails(self):
        command, response = self.test_helper.user_a_calls_unmod_user_a()

        self.assertEqual(response, command.fail_unmod_not_owner())

    def test_unmod_fail_when_user_to_unmod_none_as_owner(self):
        command, response = self.test_helper.owner_calls_unmod_none()

        self.assertEqual(response, command.fail_unmod_none_specified())

    def test_unmod_fail_when_user_to_unmod_none_as_mod(self):
        self.test_helper.owner_calls_mod_user_a()
        command, response = self.test_helper.user_a_calls_unmod_none()

        self.assertEqual(response, command.fail_unmod_not_owner())

    def test_unmod_fail_when_user_to_unmod_none_as_user(self):
        self.test_helper.owner_calls_mod_user_a()
        self.test_helper.owner_calls_unmod_user_a()
        command, response = self.test_helper.user_a_calls_unmod_none()

        self.assertEqual(response, command.fail_unmod_not_owner())
