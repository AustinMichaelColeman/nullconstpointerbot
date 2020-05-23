import unittest

from nullconstpointer.tests.helper import TestHelper


class TestCommandMod(unittest.TestCase):
    def setUp(self):
        self.test_helper = TestHelper()

    def test_mod_success(self):
        command, response = self.test_helper.owner_calls_mod_user_a()

        self.assertEqual(response, command.success_mod(self.test_helper.TEST_USER_A))

    def test_mod_fail_none_specified(self):
        command, response = self.test_helper.owner_calls_mod_empty()

        self.assertEqual(response, command.fail_mod_none_specified())

    def test_mod_fail_when_user_to_mod_none_as_owner(self):
        command, response = self.test_helper.owner_calls_mod_empty()

        self.assertEqual(response, command.fail_mod_none_specified())

    def test_mod_fail_when_user_to_mod_none_as_mod(self):
        self.test_helper.owner_calls_mod_user_a()
        command, response = self.test_helper.user_a_calls_mod_none()

        self.assertEqual(response, command.fail_mod_not_owner())

    def test_mod_fail_when_user_to_mod_none_as_user(self):
        self.test_helper.owner_calls_mod_user_a()
        self.test_helper.owner_calls_unmod_user_a()
        command, response = self.test_helper.user_a_calls_mod_none()

        self.assertEqual(response, command.fail_mod_not_owner())
