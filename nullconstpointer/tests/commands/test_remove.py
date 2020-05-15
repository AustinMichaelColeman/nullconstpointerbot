import unittest

from nullconstpointer.user import User, MOD_LEVEL_OWNER
from nullconstpointer.processor import Processor
from nullconstpointer.commands.add import AddCommand
from nullconstpointer.commands.next import NextCommand
from nullconstpointer.commands.mod import ModCommand
from nullconstpointer.commands.unmod import UnmodCommand
from nullconstpointer.commands.remove import RemoveCommand


class TestCommandRemove(unittest.TestCase):
    def setUp(self):
        self.test_owner = User("test_owner", MOD_LEVEL_OWNER)
        self.test_processor = Processor(self.test_owner)

    def test_remove_called_without_args(self):
        command = RemoveCommand(self.test_processor, "userA", "")
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_remove_no_level_specified())

    def test_remove_called_with_invalid_level_format(self):
        command = RemoveCommand(self.test_processor, "userA", "abc-def-ghi")
        response = self.test_processor.process_command(command)

        self.assertEqual(
            response, command.fail_remove_invalid_level_code("abc-def-ghi")
        )

    def test_remove_level_not_found(self):
        command = RemoveCommand(self.test_processor, "userA", "abc-def-ghd")
        response = self.test_processor.process_command(command)

        self.assertEqual(
            response, command.fail_remove_level_not_found("ABC-DEF-GHD"),
        )

    def test_remove_called_by_user_with_one_level(self):
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-ghd")
        self.test_processor.process_command(command)
        command = RemoveCommand(self.test_processor, "userA", "abc-def-ghd")
        response = self.test_processor.process_command(command)

        self.assertEqual(
            response, command.success_remove_user_level("userA", "ABC-DEF-GHD"),
        )

    def test_remove_called_by_user_with_two_levels(self):
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-ghd")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-gha")
        self.test_processor.process_command(command)
        command = RemoveCommand(self.test_processor, "userA", "abc-def-ghd")
        response = self.test_processor.process_command(command)

        self.assertEqual(
            response, command.success_remove_user_level("userA", "ABC-DEF-GHD"),
        )

    def test_remove_called_by_mod(self):
        command = ModCommand(self.test_processor, self.test_owner, "userA")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userB", "userB", "abc-def-ghd")
        self.test_processor.process_command(command)
        command = RemoveCommand(self.test_processor, "userA", "abc-def-ghd")
        response = self.test_processor.process_command(command)

        self.assertEqual(
            response, command.success_remove_user_level("userB", "ABC-DEF-GHD"),
        )

    def test_remove_called_by_owner(self):
        command = AddCommand(self.test_processor, "userB", "userB", "abc-def-ghd")
        self.test_processor.process_command(command)
        command = RemoveCommand(self.test_processor, self.test_owner, "abc-def-ghd")
        response = self.test_processor.process_command(command)

        self.assertEqual(
            response, command.success_remove_user_level("userB", "ABC-DEF-GHD"),
        )

    def test_remove_called_by_user_fails(self):
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-ghd")
        self.test_processor.process_command(command)
        command = RemoveCommand(self.test_processor, "userB", "abc-def-ghd")
        response = self.test_processor.process_command(command)

        self.assertEqual(
            response,
            command.fail_remove_no_permission("userB", "userA", "ABC-DEF-GHD"),
        )

    def test_remove_level_none_fails_owner(self):
        command = RemoveCommand(self.test_processor, self.test_owner, None)
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_remove_no_level_specified())

    def test_remove_level_none_fails_mod(self):
        command = ModCommand(self.test_processor, self.test_owner, "userA")
        self.test_processor.process_command(command)
        command = RemoveCommand(self.test_processor, "userA", None)
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_remove_no_level_specified())

    def test_remove_level_none_fails_user(self):
        command = ModCommand(self.test_processor, self.test_owner, "userA")
        self.test_processor.process_command(command)
        command = UnmodCommand(self.test_processor, self.test_owner, "userA")
        self.test_processor.process_command(command)

        command = RemoveCommand(self.test_processor, "userA", None)
        response = self.test_processor.process_command(command)

        self.assertEqual(
            response, command.fail_remove_no_level_specified(),
        )
