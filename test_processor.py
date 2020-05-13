import unittest
from lib.nullconstpointer import processor, user, level


class TestProcessor(unittest.TestCase):
    def setUp(self):
        self.test_owner = user.User("test_owner", user.MOD_LEVEL_OWNER)
        self.test_processor = processor.Processor(self.test_owner)

    def test_processor_users_equal_to_one(self):
        self.assertEqual(self.test_processor.user_count(), 1)

    def test_add_user_level_response_valid(self):
        response = self.test_processor.add_user_level("userA", "abc-def-ghd")

        self.assertEqual(
            response, self.test_processor.success_add_user_level("userA", "ABC-DEF-GHD")
        )

    def test_add_user_level_multiple_duplicate_levels_fails(self):
        self.test_processor.add_user_level("userA", "abc-def-ghd")
        response = self.test_processor.add_user_level("userA", "abc-def-ghd")
        self.assertEqual(
            response,
            self.test_processor.fail_duplicate_code("userA", "ABC-DEF-GHD", "userA"),
        )

    def test_add_user_level_multiple_different_levels_succeeds(self):
        self.test_processor.add_user_level("userA", "abc-def-ghd")
        response = self.test_processor.add_user_level("userA", "abc-def-gha")
        self.assertEqual(
            response,
            self.test_processor.success_add_user_level("userA", "ABC-DEF-GHA"),
        )

    def test_add_user_level_response_invalid(self):
        response = self.test_processor.add_user_level("userA", "abc-def-gh")
        self.assertEqual(
            response,
            self.test_processor.fail_add_user_level_invalid_code("userA", "abc-def-gh"),
        )

    def test_list_levels_empty(self):
        response = self.test_processor.list_levels()
        self.assertEqual(response, self.test_processor.success_list_empty())

    def test_list_levels_one_user_one_level(self):
        self.test_processor.add_user_level("userA", "abc-def-gha")
        self.test_processor.add_user_level("userA", "abc-def-ghb")
        response = self.test_processor.list_levels()
        self.assertEqual(
            response, self.test_processor.success_list(self.test_processor.users)
        )

    def test_current_level_is_none(self):
        response = self.test_processor.get_current_level()
        self.assertEqual(
            response, self.test_processor.fail_current_level_not_selected()
        )

    def test_current_level_success_with_next_level_owner(self):
        self.test_processor.add_user_level("userA", "abc-def-gha")
        self.test_processor.next_level(self.test_owner)

        response = self.test_processor.get_current_level()

        self.assertEqual(
            response, self.test_processor.success_current_level("ABC-DEF-GHA", "userA")
        )

    def test_next_level_fails_if_no_more_levels(self):
        response = self.test_processor.next_level(self.test_owner)

        self.assertEqual(response, self.test_processor.fail_next_level_no_more_levels())

    def test_next_level_fails_if_not_owner(self):
        self.test_processor.add_user_level("userA", "abc-def-gha")
        test_user = user.User("userA")
        response = self.test_processor.next_level(test_user)

        self.assertEqual(response, self.test_processor.fail_next_level_not_owner())

    def test_next_level_success(self):
        self.test_processor.add_user_level("userA", "abc-def-gha")
        response = self.test_processor.next_level(self.test_owner)
        self.assertEqual(
            response, self.test_processor.success_next_level("ABC-DEF-GHA", "userA")
        )

    def test_next_only_usable_by_mods(self):
        self.test_processor.add_user_level("userA", "abc-def-gha")


if __name__ == "__main__":
    unittest.main()
