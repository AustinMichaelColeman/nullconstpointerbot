import unittest

from nullconstpointer.tests.helper import TestHelper


class TestCommandList(unittest.TestCase):
    def setUp(self):
        self.test_helper = TestHelper()

    def test_list_levels_empty(self):
        command, response = self.test_helper.list_called()

        self.assertEqual(response, command.success_list_empty())

    def test_list_levels_one_user_one_level(self):
        self.test_helper.user_a_add_level_a()
        self.test_helper.user_a_add_level_b()
        command, response = self.test_helper.list_called()
        self.assertEqual(response, command.success_list())
