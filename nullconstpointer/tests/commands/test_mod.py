import unittest

from nullconstpointer.user import User, MOD_LEVEL_OWNER
from nullconstpointer.processor import Processor
from nullconstpointer.commands.add import AddCommand
from nullconstpointer.commands.next import NextCommand
from nullconstpointer.commands.mod import ModCommand


class TestCommandNext(unittest.TestCase):
    def setUp(self):
        self.test_owner = User("test_owner", MOD_LEVEL_OWNER)
        self.test_processor = Processor(self.test_owner)

    def test_mod_success(self):
        command = ModCommand(self.test_processor, self.test_owner, "userB")
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.success_mod("userB"))

    def test_mod_fail_none_specified(self):
        command = ModCommand(self.test_processor, self.test_owner, "")
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_mod_none_specified())

    def test_mod_fail_when_user_to_mod_none_as_owner(self):
        command = ModCommand(self.test_processor, self.test_owner, None)
        response = self.test_processor.process_command(command)
        self.assertEqual(response, command.fail_mod_none_specified())

    def test_mod_fail_when_user_to_mod_none_as_mod(self):
        command = ModCommand(self.test_processor, self.test_owner, "userA")
        self.test_processor.process_command(command)
        command = ModCommand(self.test_processor, "userA", None)
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_mod_not_owner())

    def test_mod_fail_when_user_to_mod_none_as_user(self):
        command = ModCommand(self.test_processor, self.test_owner, "userA")
        self.test_processor.process_command(command)

        self.test_processor.unmod(self.test_owner, "userA")

        command = ModCommand(self.test_processor, "userA", None)
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_mod_not_owner())
