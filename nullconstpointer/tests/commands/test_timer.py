import unittest

from nullconstpointer.bot.user import User, MOD_LEVEL_OWNER
from nullconstpointer.bot.processor import Processor
from nullconstpointer.commands.add import AddCommand
from nullconstpointer.commands.next import NextCommand
from nullconstpointer.commands.timer import TimerCommand


TEST_LEVEL = "ABC-DEF-GHD"
TEST_USER = "userA"
TEST_TIME = "1"
TEST_TIME_ENGLISH = "1 minute"


class TestCommandTimer(unittest.TestCase):
    def setUp(self):
        self.test_owner = User("test_owner", MOD_LEVEL_OWNER)
        self.test_processor = Processor(self.test_owner)

    def create_level(self):
        command = AddCommand(self.test_processor, TEST_USER, TEST_USER, TEST_LEVEL)
        self.test_processor.process_command(command)

    def next(self):
        command = NextCommand(self.test_processor, self.test_owner)
        self.test_processor.process_command(command)

    def owner_calls_timer(self):
        command = TimerCommand(self.test_processor, self.test_owner, TEST_TIME)
        result = self.test_processor.process_command(command)
        return (command, result)

    def owner_calls_timer_no_args(self):
        command = TimerCommand(self.test_processor, self.test_owner, None)
        result = self.test_processor.process_command(command)
        return (command, result)

    def user_calls_timer_no_args(self):
        command = TimerCommand(self.test_processor, TEST_USER, None)
        result = self.test_processor.process_command(command)
        return (command, result)

    def success_time_remaining(self, command):
        return command.success_time_remaining(TEST_TIME_ENGLISH, TEST_USER, TEST_LEVEL)

    def test_non_owner_with_timer_set(self):
        self.create_level()
        self.next()
        self.owner_calls_timer()
        command, result = self.user_calls_timer_no_args()

        self.assertEqual(
            result, self.success_time_remaining(command),
        )

    def test_non_owner_with_timer_not_set(self):
        self.create_level()
        self.next()
        command, result = self.user_calls_timer_no_args()

        self.assertEqual(result, command.fail_timer_not_set())

    def test_owner_with_timer_set(self):
        self.create_level()
        self.next()
        self.owner_calls_timer()
        command, result = self.owner_calls_timer()

        self.assertEqual(result, command.success_starting_new_timer_stopping_previous())

    def test_owner_with_timer_not_set(self):
        self.create_level()
        self.next()
        command, result = self.owner_calls_timer()

        self.assertEqual(result, command.success_starting_new_timer())

    def test_owner_without_current_level(self):
        command, result = self.owner_calls_timer()

        self.assertEqual(result, command.fail_no_current_level())

    def test_owner_calls_timer_no_args_with_level_set(self):
        self.create_level()
        self.next()
        command, result = self.owner_calls_timer_no_args()
        self.assertEqual(result, command.fail_enter_a_timer_value())

    def test_timer_finish_calls_success_time_expired(self):
        self.create_level()
        self.next()
        self.owner_calls_timer()
        self.test_processor.time_remaining = 0
        command, result = self.owner_calls_timer_no_args()
        self.assertEqual(
            result,
            command.success_time_expired(
                self.test_processor.next_level(), self.test_processor.current_user
            ),
        )
