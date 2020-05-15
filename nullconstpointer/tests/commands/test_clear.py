import unittest

from nullconstpointer.user import User, MOD_LEVEL_OWNER
from nullconstpointer.processor import Processor
from nullconstpointer.commands.add import AddCommand
from nullconstpointer.commands.mod import ModCommand
from nullconstpointer.commands.clear import ClearCommand


class TestCommandClear(unittest.TestCase):
    def setUp(self):
        self.test_owner = User("test_owner", MOD_LEVEL_OWNER)
        self.test_processor = Processor(self.test_owner)

    def test_clear_called_by_owner_without_levels(self):
        command = ClearCommand(self.test_processor, self.test_owner)
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.success_clear_owner())

    def test_clear_called_by_owner_with_levels(self):
        command = AddCommand(self.test_processor, "userA", "userA", "123-123-123")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userA", "123-123-124")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userB", "123-123-126")
        self.test_processor.process_command(command)

        command = ClearCommand(self.test_processor, self.test_owner)
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.success_clear_owner())

    def test_clear_called_by_mod_without_levels(self):
        command = ModCommand(self.test_processor, self.test_owner, "userA")
        self.test_processor.process_command(command)
        command = ClearCommand(self.test_processor, "userA")
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_clear_user_no_levels("userA"))

    def test_clear_called_by_mod_with_levels(self):
        command = ModCommand(self.test_processor, self.test_owner, "userA")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userA", "123-123-123")
        self.test_processor.process_command(command)
        command = ClearCommand(self.test_processor, "userA")
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.success_clear_user("userA"))

    def test_clear_called_by_user_without_levels(self):
        command = ClearCommand(self.test_processor, "userA")
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_clear_user_no_levels("userA"))

    def test_clear_called_by_user_with_levels(self):
        command = AddCommand(self.test_processor, "userA", "userA", "123-123-123")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userA", "123-123-124")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userB", "123-123-125")
        self.test_processor.process_command(command)
        command = ClearCommand(self.test_processor, "userA")
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.success_clear_user("userA"))
        self.assertEqual(self.test_processor.level_count(), 1)
