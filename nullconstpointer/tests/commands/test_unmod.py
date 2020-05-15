import unittest

from nullconstpointer.user import User, MOD_LEVEL_OWNER
from nullconstpointer.processor import Processor
from nullconstpointer.commands.add import AddCommand
from nullconstpointer.commands.next import NextCommand
from nullconstpointer.commands.mod import ModCommand
from nullconstpointer.commands.unmod import UnmodCommand


class TestCommandUnmod(unittest.TestCase):
    def setUp(self):
        self.test_owner = User("test_owner", MOD_LEVEL_OWNER)
        self.test_processor = Processor(self.test_owner)

    def test_unmod_success(self):
        command = ModCommand(self.test_processor, self.test_owner, "userB")
        self.test_processor.process_command(command)

        command = UnmodCommand(self.test_processor, self.test_owner, "userB")
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.success_unmod("userB"))

    def test_unmod_fail(self):
        command = UnmodCommand(self.test_processor, "userB", "userA")
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_unmod_not_owner())

    def test_unmod_fail_when_user_to_unmod_none_as_owner(self):
        command = UnmodCommand(self.test_processor, self.test_owner, None)
        response = self.test_processor.process_command(command)
        self.assertEqual(response, command.fail_unmod_none_specified())

    def test_unmod_fail_when_user_to_unmod_none_as_mod(self):
        command = ModCommand(self.test_processor, self.test_owner, "userA")
        self.test_processor.process_command(command)
        command = UnmodCommand(self.test_processor, "userA", None)
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_unmod_not_owner())

    def test_unmod_fail_when_user_to_unmod_none_as_user(self):
        command = ModCommand(self.test_processor, self.test_owner, "userA")
        self.test_processor.process_command(command)
        command = UnmodCommand(self.test_processor, self.test_owner, "userA")
        self.test_processor.process_command(command)

        command = UnmodCommand(self.test_processor, "userA", None)
        response = self.test_processor.process_command(command)
        self.assertEqual(response, command.fail_unmod_not_owner())
