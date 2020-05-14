import unittest

from nullconstpointer.user import User, MOD_LEVEL_OWNER
from nullconstpointer.processor import Processor
from nullconstpointer.commands.list import ListCommand
from nullconstpointer.commands.add import AddCommand


class TestCommandList(unittest.TestCase):
    def setUp(self):
        self.test_owner = User("test_owner", MOD_LEVEL_OWNER)
        self.test_processor = Processor(self.test_owner)

    def test_list_levels_empty(self):
        command = ListCommand(self.test_processor)
        response = self.test_processor.process_command(command)
        self.assertEqual(response, command.success_list_empty())

    def test_list_levels_one_user_one_level(self):
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-gha")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-gha")
        self.test_processor.process_command(command)
        command = ListCommand(self.test_processor)
        response = self.test_processor.process_command(command)
        self.assertEqual(response, command.success_list())
