import unittest

from nullconstpointer.user import User, MOD_LEVEL_OWNER
from nullconstpointer.processor import Processor
from nullconstpointer.commands.add import AddCommand
from nullconstpointer.commands.current import CurrentCommand
from nullconstpointer.commands.next import NextCommand


class TestCommandCurrent(unittest.TestCase):
    def setUp(self):
        self.test_owner = User("test_owner", MOD_LEVEL_OWNER)
        self.test_processor = Processor(self.test_owner)

    def test_current_level_is_none(self):
        command = CurrentCommand(self.test_processor)
        response = self.test_processor.process_command(command)
        self.assertEqual(response, command.fail_current_level_not_selected())

    def test_current_level_success_with_next_level_owner(self):
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-gha")
        self.test_processor.process_command(command)
        command = NextCommand(self.test_processor, self.test_owner)
        self.test_processor.process_command(command)

        command = CurrentCommand(self.test_processor)
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.success_current_level())

    def test_current_changes_after_level_removed(self):
        command = AddCommand(self.test_processor, "userA", "userA", "123-123-123")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userB", "userB", "123-123-124")
        self.test_processor.process_command(command)
        command = NextCommand(self.test_processor, self.test_owner)
        self.test_processor.process_command(command)
        self.test_processor.remove_current(self.test_owner)
        command = NextCommand(self.test_processor, self.test_owner)
        self.test_processor.process_command(command)
        command = CurrentCommand(self.test_processor)
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.success_current_level())
