import unittest

from nullconstpointer.user import User, MOD_LEVEL_OWNER
from nullconstpointer.processor import Processor
from nullconstpointer.commands.add import AddCommand
from nullconstpointer.commands.mod import ModCommand
from nullconstpointer.commands.leave import LeaveCommand


class TestCommandLeave(unittest.TestCase):
    def setUp(self):
        self.test_owner = User("test_owner", MOD_LEVEL_OWNER)
        self.test_processor = Processor(self.test_owner)

    def test_leave_called_by_user_with_no_levels(self):
        command = LeaveCommand(self.test_processor, "userA")
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_leave_no_levels("userA"))

    def test_leave_called_by_user_with_one_level(self):
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-gha")
        self.test_processor.process_command(command)
        command = LeaveCommand(self.test_processor, "userA")
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.success_leave("userA"))

    def test_leave_called_by_user_with_two_levels(self):
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-ghd")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-gha")
        self.test_processor.process_command(command)
        command = LeaveCommand(self.test_processor, "userA")
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.success_leave("userA"))

    def test_leave_called_by_mod_with_no_levels(self):
        command = ModCommand(self.test_processor, self.test_owner, "userA")
        self.test_processor.process_command(command)
        command = LeaveCommand(self.test_processor, "userA")
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_leave_no_levels("userA"))

    def test_leave_called_by_mod_with_levels(self):
        command = ModCommand(self.test_processor, self.test_owner, "userA")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-ghd")
        self.test_processor.process_command(command)
        command = LeaveCommand(self.test_processor, "userA")
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.success_leave("userA"))
