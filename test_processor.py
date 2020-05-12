import unittest
from lib.nullconstpointer import processor, user, level


class TestProcessor(unittest.TestCase):
    def test_processor_users_empty(self):
        test_processor = processor.Processor()

        self.assertEqual(test_processor.user_count(), 0)

    def test_add_user_level_response_valid(self):
        test_processor = processor.Processor()

        response = test_processor.add_user_level("userA", "abc-def-ghd")

        self.assertEqual(response, test_processor.success("userA", "ABC-DEF-GHD"))

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
            response, test_processor.success("userA", "ABC-DEF-GHA"),
        )

    def test_add_user_level_response_invalid(self):
        test_processor = processor.Processor()

        response = test_processor.add_user_level("userA", "abc-def-gh")
        self.assertEqual(
            response, test_processor.fail_invalid_code("userA", "abc-def-gh")
        )


if __name__ == "__main__":
    unittest.main()
