import unittest

from nullconstpointer.user import User, MOD_LEVEL_OWNER
from nullconstpointer.processor import Processor
from nullconstpointer.commands.list import ListCommand


class TestCommandList(unittest.TestCase):
    def setUp(self):
        self.test_owner = User("test_owner", MOD_LEVEL_OWNER)
        self.test_processor = Processor(self.test_owner)

    def test_list_levels_empty(self):
        command = ListCommand(self.test_processor)
        response = self.test_processor.process_command(command)
        self.assertEqual(response, command.success_list_empty())

    def test_list_levels_one_user_one_level(self):
        self.test_processor.add_user_level("userA", "abc-def-gha")
        self.test_processor.add_user_level("userA", "abc-def-ghb")
        command = ListCommand(self.test_processor)
        response = self.test_processor.process_command(command)
        self.assertEqual(response, command.success_list())
