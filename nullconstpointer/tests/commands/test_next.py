import unittest

from nullconstpointer.user import User, MOD_LEVEL_OWNER
from nullconstpointer.processor import Processor
from nullconstpointer.commands.add import AddCommand
from nullconstpointer.commands.next import NextCommand


class TestCommandNext(unittest.TestCase):
    def setUp(self):
        self.test_owner = User("test_owner", MOD_LEVEL_OWNER)
        self.test_processor = Processor(self.test_owner)

    def test_next_level_fails_if_no_more_levels(self):
        command = NextCommand(self.test_processor, self.test_owner)
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_next_level_no_more_levels())

    def test_next_level_fails_if_not_owner(self):
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-gha")
        self.test_processor.process_command(command)
        test_user = User("userA")
        command = NextCommand(self.test_processor, test_user)
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_next_level_not_owner())

    def test_next_level_success(self):
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-gha")
        self.test_processor.process_command(command)
        command = NextCommand(self.test_processor, self.test_owner)
        response = self.test_processor.process_command(command)
        self.assertEqual(response, command.success_next_level("ABC-DEF-GHA", "userA"))

    def test_next_not_usable_by_mods(self):
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-gha")
        self.test_processor.process_command(command)
        self.test_processor.mod(self.test_owner, "userA")
        command = NextCommand(self.test_processor, "userA")
        response = self.test_processor.process_command(command)
        self.assertEqual(response, command.fail_next_level_not_owner())
