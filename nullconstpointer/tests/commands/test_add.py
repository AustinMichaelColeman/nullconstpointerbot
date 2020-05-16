import unittest
from nullconstpointer.bot.user import User, MOD_LEVEL_OWNER
from nullconstpointer.bot.processor import Processor
from nullconstpointer.commands.add import AddCommand
from nullconstpointer.commands.remove import RemoveCommand


class TestCommandAdd(unittest.TestCase):
    def setUp(self):
        self.test_owner = User("test_owner", MOD_LEVEL_OWNER)
        self.test_processor = Processor(self.test_owner)

    def test_add_user_level_response_valid(self):
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-ghd")
        response = self.test_processor.process_command(command)

        self.assertEqual(
            response, command.success_add_user_level("userA", "ABC-DEF-GHD")
        )

    def test_add_user_level_multiple_duplicate_levels_fails(self):
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-ghd")
        self.test_processor.process_command(command)
        response = self.test_processor.process_command(command)
        self.assertEqual(
            response,
            command.fail_add_user_level_duplicate_code("userA", "ABC-DEF-GHD", "userA"),
        )

    def test_add_user_level_multiple_different_levels_succeeds(self):
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-ghd")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-gha")
        response = self.test_processor.process_command(command)

        self.assertEqual(
            response, command.success_add_user_level("userA", "ABC-DEF-GHA"),
        )

    def test_add_user_level_response_invalid(self):
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-gh")
        response = self.test_processor.process_command(command)
        self.assertEqual(
            response, command.fail_add_user_level_invalid_code("userA", "abc-def-gh"),
        )

    def test_two_levels_valid(self):
        command = AddCommand(
            self.test_processor, "userA", "userA", "abc def-ghd abc   ---def-gha"
        )
        response = self.test_processor.process_command(command)

        levels_added = ["ABC-DEF-GHD", "ABC-DEF-GHA"]
        self.assertEqual(
            response, command.success_add_user_level("userA", levels_added)
        )

    def test_valid_with_invalid(self):
        command = AddCommand(self.test_processor, "userA", "userA", "abc-def-ghd asdf")
        response = self.test_processor.process_command(command)

        self.assertEqual(
            response,
            command.fail_add_user_level_invalid_code("userA", "abc-def-ghd asdf"),
        )

    def test_middle_invalid(self):
        command = AddCommand(
            self.test_processor, "userA", "userA", "123-123-123 asdf 321-321-321"
        )
        response = self.test_processor.process_command(command)

        self.assertEqual(
            response,
            command.fail_add_user_level_invalid_code(
                "userA", "123-123-123 asdf 321-321-321"
            ),
        )

    def test_end_and_middle_invalid(self):
        command = AddCommand(
            self.test_processor, "userA", "userA", "123-123-123 asdf 321-321-32I"
        )
        response = self.test_processor.process_command(command)
        self.assertEqual(
            response,
            command.fail_add_user_level_invalid_code(
                "userA", "123-123-123 asdf 321-321-32I"
            ),
        )

    def test_spaces_in_level_code(self):
        command = AddCommand(self.test_processor, "userA", "userA", "123 123 123")
        response = self.test_processor.process_command(command)

        self.assertEqual(
            response, command.success_add_user_level("userA", "123-123-123")
        )

    def test_spaces_in_level_code_multiple(self):
        command = AddCommand(
            self.test_processor, "userA", "userA", "123 123 123 abcdefghd"
        )
        response = self.test_processor.process_command(command)

        valid_levels = ["123-123-123", "ABC-DEF-GHD"]

        self.assertEqual(
            response, command.success_add_user_level("userA", valid_levels)
        )

    def test_extra_character_in_level_codes(self):
        command = AddCommand(
            self.test_processor,
            "userA",
            "userA",
            "123-123--123 ----32--1 123 _--...123",
        )
        response = self.test_processor.process_command(command)

        valid_levels = ["123-123-123", "321-123-123"]

        self.assertEqual(
            response, command.success_add_user_level("userA", valid_levels)
        )

    def test_level_limit(self):
        command = AddCommand(
            self.test_processor,
            "userA",
            "userA",
            "111-111-111 222-222-222 333-333-333 444-444-444",
        )
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_add_user_level_level_limit("userA"))

    def test_limit_one_at_a_time_fails_past_limit(self):
        command = AddCommand(self.test_processor, "userA", "userA", "123 123 121")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userA", "123 123 122")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userA", "123 123 123")
        response = self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userA", "123 123 124")
        response = self.test_processor.process_command(command)

        self.assertEqual(response, command.fail_add_user_level_level_limit("userA"))

    def test_limit_one_at_a_time_succeeds_at_limit(self):
        command = AddCommand(self.test_processor, "userA", "userA", "123 123 121")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userA", "123 123 122")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userA", "123 123 123")
        response = self.test_processor.process_command(command)

        self.assertEqual(
            response, command.success_add_user_level("userA", "123-123-123")
        )

    def test_limit_one_at_a_time_succeeds_at_limit_owner(self):
        command = AddCommand(
            self.test_processor, self.test_owner, self.test_owner, "123 123 121"
        )
        self.test_processor.process_command(command)
        command = AddCommand(
            self.test_processor, self.test_owner, self.test_owner, "123 123 122"
        )
        self.test_processor.process_command(command)
        command = AddCommand(
            self.test_processor, self.test_owner, self.test_owner, "123 123 123"
        )
        response = self.test_processor.process_command(command)

        self.assertEqual(
            response, command.success_add_user_level(self.test_owner, "123-123-123")
        )

    def test_limit_after_removal(self):
        command = AddCommand(self.test_processor, "userA", "userA", "123 123 121")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userA", "123 123 122")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userA", "123 123 123")
        self.test_processor.process_command(command)
        command = RemoveCommand(self.test_processor, "userA", "123 123 122")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userA", "123 123 122")
        response = self.test_processor.process_command(command)

        valid_levels = ["123-123-122"]
        self.assertEqual(
            response, command.success_add_user_level("userA", valid_levels)
        )

    def test_limit_one_then_multi(self):
        command = AddCommand(self.test_processor, "userA", "userA", "123 123 121")
        self.test_processor.process_command(command)
        command = AddCommand(
            self.test_processor, "userA", "userA", "111-111-111 111-111-112 111-111-113"
        )
        response = self.test_processor.process_command(command)

        self.assertEqual(
            response, command.fail_add_user_level_level_limit("userA"),
        )

    def test_limit_duplicate_multi(self):
        command = AddCommand(
            self.test_processor, "userA", "userA", "123-123-123 333-333-333"
        )
        self.test_processor.process_command(command)
        command = AddCommand(
            self.test_processor, "userA", "userA", "111-111-111 333-333-333 222-222-222"
        )
        response = self.test_processor.process_command(command)

        self.assertEqual(
            response,
            command.fail_add_user_level_duplicate_code("userA", "333-333-333", "userA"),
        )

    def test_limit_duplicate_multi_user(self):
        command = AddCommand(self.test_processor, "userB", "userB", "222-222-222")
        self.test_processor.process_command(command)
        command = AddCommand(self.test_processor, "userA", "userA", "111-111-111")
        self.test_processor.process_command(command)
        command = AddCommand(
            self.test_processor, "userC", "userC", "111-111-111 222-222-222 333-333-333"
        )
        response = self.test_processor.process_command(command)

        self.assertEqual(
            response,
            command.fail_add_user_level_duplicate_code("userC", "111-111-111", "userA"),
        )

    def test_partial_submission(self):
        command = AddCommand(
            self.test_processor, "userA", "userA", "111-111-111 222-222-22 abc-def-ghd"
        )
        response = self.test_processor.process_command(command)

        self.assertEqual(
            response,
            command.fail_add_user_level_invalid_code(
                "userA", "111-111-111 222-222-22 abc-def-ghd"
            ),
        )
