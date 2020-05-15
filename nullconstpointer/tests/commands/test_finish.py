import unittest

from nullconstpointer.user import User, MOD_LEVEL_OWNER
from nullconstpointer.processor import Processor
from nullconstpointer.commands.add import AddCommand
from nullconstpointer.commands.mod import ModCommand
from nullconstpointer.commands.random import RandomCommand
from nullconstpointer.commands.remove import RemoveCommand
from nullconstpointer.commands.finish import FinishCommand


class TestCommandFinish(unittest.TestCase):
    def setUp(self):
        self.test_owner = User("test_owner", MOD_LEVEL_OWNER)
        self.test_processor = Processor(self.test_owner)

    def test_finish_called_by_owner_no_levels(self):
        command = FinishCommand(self.test_processor, self.test_owner)
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_finish_no_levels())

    def test_finish_called_by_owner_with_levels(self):
        command = AddCommand(self.test_processor, "userA", "userA", "123-123-123")
        self.test_processor.process_command(command)
        command = RandomCommand(self.test_processor, self.test_owner)
        self.test_processor.process_command(command)
        command = FinishCommand(self.test_processor, self.test_owner)
        response = self.test_processor.process_command(command)

        # hack for now, make success_remove_user_level not require an object to call it
        # in the future
        removeCommand = RemoveCommand(self.test_processor, "userA", "123-123-123")
        self.assertEqual(
            response, removeCommand.success_remove_user_level("userA", "123-123-123"),
        )

    def test_finish_called_by_user_with_levels(self):
        command = AddCommand(self.test_processor, "userA", "userA", "123-123-123")
        self.test_processor.process_command(command)
        command = FinishCommand(self.test_processor, "userA")
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_finish_no_permission("userA"))

    def test_finish_called_by_user_without_levels(self):
        command = FinishCommand(self.test_processor, "userA")
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_finish_no_permission("userA"))

    def test_finish_called_by_mod_with_levels(self):
        command = AddCommand(self.test_processor, "userA", "userA", "123-123-123")
        self.test_processor.process_command(command)
        command = ModCommand(self.test_processor, self.test_owner, "userA")
        self.test_processor.process_command(command)
        command = FinishCommand(self.test_processor, "userA")
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_finish_no_permission("userA"))

    def test_finish_called_by_mod_without_levels(self):
        command = ModCommand(self.test_processor, self.test_owner, "userA")
        self.test_processor.process_command(command)
        command = FinishCommand(self.test_processor, "userA")
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_finish_no_permission("userA"))
