import unittest

from nullconstpointer.processor import Processor
from nullconstpointer.user import User, MOD_LEVEL_OWNER, MOD_LEVEL_MOD, MOD_LEVEL_USER
from nullconstpointer.level import Level


class TestProcessor(unittest.TestCase):
    def setUp(self):
        self.test_owner = User("test_owner", MOD_LEVEL_OWNER)
        self.test_processor = Processor(self.test_owner)

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
            self.test_processor.fail_add_user_level_duplicate_code(
                "userA", "ABC-DEF-GHD", "userA"
            ),
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
        test_user = User("userA")
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

    def test_mod_success(self):
        response = self.test_processor.mod(self.test_owner.username, "userB")
        self.assertEqual(response, self.test_processor.success_mod("userB"))

    def test_mod_fail_none_specified(self):
        response = self.test_processor.mod(self.test_owner.username, "")
        self.assertEqual(response, self.test_processor.fail_mod_none_specified())

    def test_mod_fail_when_user_to_mod_none_as_owner(self):
        response = self.test_processor.mod(self.test_owner, None)
        self.assertEqual(response, self.test_processor.fail_mod_none_specified())

    def test_mod_fail_when_user_to_mod_none_as_mod(self):
        self.test_processor.mod(self.test_owner, "userA")
        response = self.test_processor.mod("userA", None)

        self.assertEqual(response, self.test_processor.fail_mod_not_owner())

    def test_mod_fail_when_user_to_mod_none_as_user(self):
        self.test_processor.mod(self.test_owner, "userA")
        self.test_processor.unmod(self.test_owner, "userA")

        response = self.test_processor.mod("userA", None)
        self.assertEqual(response, self.test_processor.fail_mod_not_owner())

    def test_unmod_success(self):
        self.test_processor.mod(self.test_owner.username, "userB")
        response = self.test_processor.unmod(self.test_owner.username, "userB")

        self.assertEqual(response, self.test_processor.success_unmod("userB"))

    def test_unmod_fail(self):
        response = self.test_processor.unmod("userB", "userA")

        self.assertEqual(response, self.test_processor.fail_unmod_not_owner())

    def test_unmod_fail_when_user_to_unmod_none_as_owner(self):
        response = self.test_processor.unmod(self.test_owner, None)
        self.assertEqual(response, self.test_processor.fail_unmod_none_specified())

    def test_unmod_fail_when_user_to_unmod_none_as_mod(self):
        self.test_processor.mod(self.test_owner, "userA")
        response = self.test_processor.unmod("userA", None)

        self.assertEqual(response, self.test_processor.fail_unmod_not_owner())

    def test_unmod_fail_when_user_to_unmod_none_as_user(self):
        self.test_processor.mod(self.test_owner, "userA")
        self.test_processor.unmod(self.test_owner, "userA")

        response = self.test_processor.unmod("userA", None)
        self.assertEqual(response, self.test_processor.fail_unmod_not_owner())

    def test_remove_called_without_args(self):
        response = self.test_processor.remove("userA", "")

        self.assertEqual(response, self.test_processor.fail_remove_no_level_specified())

    def test_remove_called_with_invalid_level_format(self):
        response = self.test_processor.remove("userA", "abc-def-ghi")

        self.assertEqual(
            response, self.test_processor.fail_remove_invalid_level_code("abc-def-ghi")
        )

    def test_remove_level_not_found(self):
        response = self.test_processor.remove("userA", "abc-def-ghd")

        self.assertEqual(
            response, self.test_processor.fail_remove_level_not_found("ABC-DEF-GHD"),
        )

    def test_remove_called_by_user_with_one_level(self):
        self.test_processor.add_user_level("userA", "abc-def-ghd")
        response = self.test_processor.remove("userA", "abc-def-ghd")

        self.assertEqual(
            response,
            self.test_processor.success_remove_user_level("userA", "ABC-DEF-GHD"),
        )

    def test_remove_called_by_user_with_two_levels(self):
        self.test_processor.add_user_level("userA", "abc-def-ghd")
        self.test_processor.add_user_level("userA", "abc-def-gha")
        response = self.test_processor.remove("userA", "abc-def-ghd")

        self.assertEqual(
            response,
            self.test_processor.success_remove_user_level("userA", "ABC-DEF-GHD"),
        )

    def test_remove_called_by_mod(self):
        self.test_processor.mod(self.test_owner.username, "userA")
        self.test_processor.add_user_level("userB", "abc-def-ghd")
        response = self.test_processor.remove("userA", "abc-def-ghd")

        self.assertEqual(
            response,
            self.test_processor.success_remove_user_level("userB", "ABC-DEF-GHD"),
        )

    def test_remove_called_by_owner(self):
        self.test_processor.add_user_level("userB", "abc-def-ghd")
        response = self.test_processor.remove(str(self.test_owner), "abc-def-ghd")

        self.assertEqual(
            response,
            self.test_processor.success_remove_user_level("userB", "ABC-DEF-GHD"),
        )

    def test_remove_called_by_user_fails(self):
        self.test_processor.add_user_level("userA", "abc-def-ghd")
        response = self.test_processor.remove("userB", "abc-def-ghd")

        self.assertEqual(
            response,
            self.test_processor.fail_remove_no_permission(
                "userB", "userA", "ABC-DEF-GHD"
            ),
        )

    def test_remove_level_none_fails_owner(self):
        response = self.test_processor.remove(self.test_owner, None)

        self.assertEqual(response, self.test_processor.fail_remove_no_level_specified())

    def test_remove_level_none_fails_mod(self):
        self.test_processor.mod(self.test_owner, "userA")
        response = self.test_processor.remove("userA", None)

        self.assertEqual(response, self.test_processor.fail_remove_no_level_specified())

    def test_remove_level_none_fails_user(self):
        self.test_processor.mod(self.test_owner, "userA")
        self.test_processor.unmod(self.test_owner, "userA")

        response = self.test_processor.remove("userA", None)

        self.assertEqual(
            response, self.test_processor.fail_remove_no_level_specified(),
        )

    def test_leave_called_by_user_with_no_levels(self):
        response = self.test_processor.leave("userA")

        self.assertEqual(response, self.test_processor.fail_leave_no_levels("userA"))

    def test_leave_called_by_user_with_one_level(self):
        self.test_processor.add_user_level("userA", "abc-def-ghd")
        response = self.test_processor.leave("userA")

        self.assertEqual(response, self.test_processor.success_leave("userA"))

    def test_leave_called_by_user_with_two_levels(self):
        self.test_processor.add_user_level("userA", "abc-def-ghd")
        self.test_processor.add_user_level("userA", "abc-def-gha")
        response = self.test_processor.leave("userA")

        self.assertEqual(response, self.test_processor.success_leave("userA"))

    def test_leave_called_by_mod_with_no_levels(self):
        self.test_processor.mod(self.test_owner, "userA")
        response = self.test_processor.leave("userA")

        self.assertEqual(response, self.test_processor.fail_leave_no_levels("userA"))

    def test_leave_called_by_mod_with_levels(self):
        self.test_processor.mod(self.test_owner, "userA")
        self.test_processor.add_user_level("userA", "abc-def-ghd")
        response = self.test_processor.leave("userA")

        self.assertEqual(response, self.test_processor.success_leave("userA"))

    def test_clear_called_by_owner_without_levels(self):
        response = self.test_processor.clear(self.test_owner)

        self.assertEqual(response, self.test_processor.success_clear_owner())

    def test_clear_called_by_owner_with_levels(self):
        self.test_processor.add_user_level("userA", "123-123-123")
        self.test_processor.add_user_level("userA", "123-123-124")
        self.test_processor.add_user_level("userB", "123-123-126")
        response = self.test_processor.clear(self.test_owner)

        self.assertEqual(response, self.test_processor.success_clear_owner())

    def test_clear_called_by_mod_without_levels(self):
        self.test_processor.mod(self.test_owner, "userA")
        response = self.test_processor.clear("userA")

        self.assertEqual(
            response, self.test_processor.fail_clear_user_no_levels("userA")
        )

    def test_clear_called_by_mod_with_levels(self):
        self.test_processor.mod(self.test_owner, "userA")
        self.test_processor.add_user_level("userA", "123-123-123")
        response = self.test_processor.clear("userA")

        self.assertEqual(response, self.test_processor.success_clear_user("userA"))

    def test_clear_called_by_user_without_levels(self):
        response = self.test_processor.clear("userA")

        self.assertEqual(
            response, self.test_processor.fail_clear_user_no_levels("userA")
        )

    def test_clear_called_by_user_with_levels(self):
        self.test_processor.add_user_level("userA", "123-123-123")
        self.test_processor.add_user_level("userA", "123-123-124")
        self.test_processor.add_user_level("userB", "123-123-125")
        response = self.test_processor.clear("userA")

        self.assertEqual(response, self.test_processor.success_clear_user("userA"))
        self.assertEqual(self.test_processor.level_count(), 1)

    def test_random_called_by_owner_with_no_levels(self):
        response = self.test_processor.random_level(self.test_owner)

        self.assertEqual(response, self.test_processor.fail_random_no_levels())

    def test_random_called_by_owner_with_levels(self):
        self.test_processor.add_user_level("userA", "123-123-123")
        self.test_processor.add_user_level("userB", "123-123-124")
        response = self.test_processor.random_level(self.test_owner)

        possible_responses = [
            self.test_processor.success_random_level("userA", "123-123-123"),
            self.test_processor.success_random_level("userB", "123-123-124"),
        ]

        self.assertIn(response, possible_responses)

    def test_random_called_by_owner_first_level_submitted_selected(self):
        self.test_processor.add_user_level("userA", "123-123-123")
        self.test_processor.add_user_level("userA", "123-123-121")
        self.test_processor.add_user_level("userA", "123-123-120")
        response = self.test_processor.random_level(self.test_owner)

        self.assertEqual(
            response, self.test_processor.success_random_level("userA", "123-123-123")
        )

        self.test_processor.remove(self.test_owner, "123-123-123")
        response = self.test_processor.random_level(self.test_owner)

        self.assertEqual(
            response, self.test_processor.success_random_level("userA", "123-123-121")
        )

    def test_random_called_by_owner_first_level_submitted_selected_multi_user(self):
        self.test_processor.add_user_level("userA", "123-123-121")
        self.test_processor.add_user_level("userB", "123-123-122")
        self.test_processor.add_user_level("userB", "123-123-123")
        self.test_processor.add_user_level("userA", "123-123-124")

        response = self.test_processor.random_level(self.test_owner)

        possible_responses = [
            self.test_processor.success_random_level("userA", "123-123-121"),
            self.test_processor.success_random_level("userB", "123-123-122"),
        ]

        self.assertIn(response, possible_responses)

    def test_random_called_by_mod(self):
        self.test_processor.mod(self.test_owner, "userA")
        response = self.test_processor.random_level("userA")

        self.assertEqual(
            response, self.test_processor.fail_random_no_permission("userA")
        )

    def test_random_called_by_user(self):
        response = self.test_processor.random_level("userA")

        self.assertEqual(
            response, self.test_processor.fail_random_no_permission("userA")
        )

    def test_remove_current_called_by_owner_no_levels(self):
        response = self.test_processor.remove_current(self.test_owner)

        self.assertEqual(response, self.test_processor.fail_remove_current_no_levels())

    def test_remove_current_called_by_owner_with_levels(self):
        self.test_processor.add_user_level("userA", "123-123-123")
        self.test_processor.random_level(self.test_owner)
        response = self.test_processor.remove_current(self.test_owner)

        self.assertEqual(
            response,
            self.test_processor.success_remove_user_level("userA", "123-123-123"),
        )

    def test_remove_current_called_by_user_with_levels(self):
        self.test_processor.add_user_level("userA", "123-123-123")
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
        self.test_processor.add_user_level("userA", "123-123-123")
        self.test_processor.mod(self.test_owner, "userA")
        response = self.test_processor.remove_current("userA")

        self.assertEqual(
            response, self.test_processor.fail_remove_current_no_permission("userA")
        )

    def test_remove_current_called_by_mod_without_levels(self):
        response = self.test_processor.remove_current("userA")
        self.test_processor.mod(self.test_owner, "userA")

        self.assertEqual(
            response, self.test_processor.fail_remove_current_no_permission("userA")
        )

    def test_remove_current_changes_output_of_current(self):
        self.test_processor.add_user_level("userA", "123-123-123")
        self.test_processor.add_user_level("userB", "123-123-124")
        self.test_processor.next_level(self.test_owner)
        self.test_processor.remove_current(self.test_owner)
        self.test_processor.next_level(self.test_owner)
        response = self.test_processor.get_current_level()

        self.assertEqual(
            response, self.test_processor.success_current_level("123-123-124", "userB")
        )


if __name__ == "__main__":
    unittest.main()