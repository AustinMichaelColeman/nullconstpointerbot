import unittest
from nullconstpointer.bot.user import User, MOD_LEVEL_OWNER
from nullconstpointer.bot.processor import Processor
from nullconstpointer.commands.add import AddCommand


class TestCommandAdd(unittest.TestCase):
    def setUp(self):
        self.test_owner = User("test_owner", MOD_LEVEL_OWNER)
        self.test_processor = Processor(self.test_owner)

    def test_add_user_level_response_valid(self):
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-ghd")
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.success_add_user_level())

    def test_add_user_level_multiple_duplicate_levels_fails(self):
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-ghd")
        self.test_processor.process_command(command)
        response = self.test_processor.process_command(command)
        self.assertEqual(
            response, command.fail_add_user_level_duplicate_code(),
        )

    def test_add_user_level_multiple_different_levels_succeeds(self):
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-ghd")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-gha")
        response = self.test_processor.process_command(command)

        self.assertEqual(
            response, command.success_add_user_level(),
        )

    def test_add_user_level_response_invalid(self):
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-gh")
        response = self.test_processor.process_command(command)
        self.assertEqual(
            response, command.fail_add_user_level_invalid_code(),
        )
