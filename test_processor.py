import unittest
from lib.nullconstpointer import processor, user, level


class TestProcessor(unittest.TestCase):
    def test_processor_users_empty(self):
        test_processor = processor.Processor()

        self.assertEqual(test_processor.user_count(), 0)

    def test_add_user_level_response_valid(self):
        test_processor = processor.Processor()

        response = test_processor.add_user_level("userA", "abc-def-ghd")

        self.assertEqual(
            response, test_processor.success_add_user_level("userA", "ABC-DEF-GHD")
        )

    def test_add_user_level_multiple_duplicate_levels_fails(self):
        test_processor = processor.Processor()

        test_processor.add_user_level("userA", "abc-def-ghd")
        response = test_processor.add_user_level("userA", "abc-def-ghd")
        self.assertEqual(
            response,
            test_processor.fail_duplicate_code("userA", "ABC-DEF-GHD", "userA"),
        )

    def test_add_user_level_multiple_different_levels_succeeds(self):
        test_processor = processor.Processor()

        test_processor.add_user_level("userA", "abc-def-ghd")
        response = test_processor.add_user_level("userA", "abc-def-gha")
        self.assertEqual(
            response, test_processor.success_add_user_level("userA", "ABC-DEF-GHA"),
        )

    def test_add_user_level_response_invalid(self):
        test_processor = processor.Processor()

        response = test_processor.add_user_level("userA", "abc-def-gh")
        self.assertEqual(
            response,
            test_processor.fail_add_user_level_invalid_code("userA", "abc-def-gh"),
        )

    def test_list_levels_empty(self):
        test_processor = processor.Processor()

        response = test_processor.list_levels()
        self.assertEqual(response, test_processor.success_list_empty())

    def test_list_levels_one_user_one_level(self):
        test_processor = processor.Processor()

        test_processor.add_user_level("userA", "abc-def-gha")
        test_processor.add_user_level("userA", "abc-def-ghb")
        response = test_processor.list_levels()
        self.assertEqual(response, test_processor.success_list(test_processor.users))

    def test_current_level_is_none(self):
        test_processor = processor.Processor()

        response = test_processor.get_current_level()
        self.assertEqual(response, test_processor.fail_current_level_not_selected())

    def test_current_level_success_with_next_level(self):
        test_processor = processor.Processor()

        test_processor.add_user_level("userA", "abc-def-gha")
        test_processor.next_level()
        response = test_processor.get_current_level()

        self.assertEqual(
            response, test_processor.success_current_level("ABC-DEF-GHA", "userA")
        )

    def test_next_level_fails_if_no_more_levels(self):
        test_processor = processor.Processor()

        response = test_processor.next_level()

        self.assertEqual(response, test_processor.fail_next_level_no_more_levels())

    def test_next_level_success(self):
        test_processor = processor.Processor()

        test_processor.add_user_level("userA", "abc-def-gha")
        response = test_processor.next_level()
        self.assertEqual(
            response, test_processor.success_next_level("ABC-DEF-GHA", "userA")
        )


if __name__ == "__main__":
    unittest.main()
