import unittest

from nullconstpointer.processor import Processor
from nullconstpointer.user import User, MOD_LEVEL_OWNER, MOD_LEVEL_MOD, MOD_LEVEL_USER
from nullconstpointer.level import Level
from nullconstpointer.commands.add import AddCommand
from nullconstpointer.commands.mod import ModCommand
from nullconstpointer.commands.unmod import UnmodCommand
from nullconstpointer.commands.remove import RemoveCommand
from nullconstpointer.commands.random import RandomCommand


class TestProcessor(unittest.TestCase):
    def setUp(self):
        self.test_owner = User("test_owner", MOD_LEVEL_OWNER)
        self.test_processor = Processor(self.test_owner)

    def test_processor_users_equal_to_one(self):
        self.assertEqual(self.test_processor.user_count(), 1)

    def test_remove_current_called_by_owner_no_levels(self):
        response = self.test_processor.remove_current(self.test_owner)

        self.assertEqual(response, self.test_processor.fail_remove_current_no_levels())

    def test_remove_current_called_by_owner_with_levels(self):
        command = AddCommand(self.test_processor, "userA", "userA", "123-123-123")
        self.test_processor.process_command(command)
        command = RandomCommand(self.test_processor, self.test_owner)
        self.test_processor.process_command(command)
        response = self.test_processor.remove_current(self.test_owner)

        # hack for now, make success_remove_user_level not require an object to call it
        # in the future
        removeCommand = RemoveCommand(self.test_processor, "userA", "123-123-123")
        self.assertEqual(
            response, removeCommand.success_remove_user_level("userA", "123-123-123"),
        )

    def test_remove_current_called_by_user_with_levels(self):
        command = AddCommand(self.test_processor, "userA", "userA", "123-123-123")
        self.test_processor.process_command(command)
        response = self.test_processor.remove_current("userA")

        self.assertEqual(
            response, self.test_processor.fail_remove_current_no_permission("userA")
        )

    def test_remove_current_called_by_user_without_levels(self):
        response = self.test_processor.remove_current("userA")

        self.assertEqual(
            response, self.test_processor.fail_remove_current_no_permission("userA")
        )

    def test_remove_current_called_by_mod_with_levels(self):
        command = AddCommand(self.test_processor, "userA", "userA", "123-123-123")
        self.test_processor.process_command(command)
        command = ModCommand(self.test_processor, self.test_owner, "userA")
        self.test_processor.process_command(command)
        response = self.test_processor.remove_current("userA")

        self.assertEqual(
            response, self.test_processor.fail_remove_current_no_permission("userA")
        )

    def test_remove_current_called_by_mod_without_levels(self):
        command = ModCommand(self.test_processor, self.test_owner, "userA")
        self.test_processor.process_command(command)
        response = self.test_processor.remove_current("userA")

        self.assertEqual(
            response, self.test_processor.fail_remove_current_no_permission("userA")
        )


if __name__ == "__main__":
    unittest.main()
