import unittest

from nullconstpointer.user import User, MOD_LEVEL_OWNER
from nullconstpointer.processor import Processor
from nullconstpointer.commands.add import AddCommand
from nullconstpointer.commands.mod import ModCommand
from nullconstpointer.commands.unmod import UnmodCommand
from nullconstpointer.commands.remove import RemoveCommand
from nullconstpointer.commands.random import RandomCommand


class TestCommandRandom(unittest.TestCase):
    def setUp(self):
        self.test_owner = User("test_owner", MOD_LEVEL_OWNER)
        self.test_processor = Processor(self.test_owner)

    def test_random_called_by_owner_with_no_levels(self):
        command = RandomCommand(self.test_processor, self.test_owner)
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_random_no_levels())

    def test_random_called_by_owner_with_levels(self):
        command = AddCommand(self.test_processor, "userA", "userA", "123-123-123")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userB", "userB", "123-123-124")
        self.test_processor.process_command(command)
        command = RandomCommand(self.test_processor, self.test_owner)
        response = self.test_processor.process_command(command)

        possible_responses = [
            command.success_random_level("userA", "123-123-123"),
            command.success_random_level("userB", "123-123-124"),
        ]

        self.assertIn(response, possible_responses)

    def test_random_called_by_owner_first_level_submitted_selected(self):
        command = AddCommand(self.test_processor, "userA", "userA", "123-123-123")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userA", "123-123-121")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userA", "123-123-120")
        self.test_processor.process_command(command)
        command = RandomCommand(self.test_processor, self.test_owner)
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.success_random_level("userA", "123-123-123"))

        command = RemoveCommand(self.test_processor, self.test_owner, "123-123-123")
        self.test_processor.process_command(command)

        command = RandomCommand(self.test_processor, self.test_owner)
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.success_random_level("userA", "123-123-121"))

    def test_random_called_by_owner_first_level_submitted_selected_multi_user(self):
        command = AddCommand(self.test_processor, "userA", "userA", "123-123-121")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userB", "123-123-122")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userA", "123-123-123")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userB", "123-123-124")
        self.test_processor.process_command(command)

        command = RandomCommand(self.test_processor, self.test_owner)
        response = self.test_processor.process_command(command)

        possible_responses = [
            command.success_random_level("userA", "123-123-121"),
            command.success_random_level("userB", "123-123-122"),
        ]

        self.assertIn(response, possible_responses)

    def test_random_called_by_mod(self):
        command = ModCommand(self.test_processor, self.test_owner, "userA")
        self.test_processor.process_command(command)
        command = RandomCommand(self.test_processor, "userA")
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_random_no_permission("userA"))

    def test_random_called_by_user(self):
        command = RandomCommand(self.test_processor, "userA")
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_random_no_permission("userA"))
