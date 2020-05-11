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
            response, "Thank you userA, your level ABC-DEF-GHD has been added."
        )

    def test_add_user_level_response_invalid(self):
        test_processor = processor.Processor()

        response = test_processor.add_user_level("userA", "abc-def-gh")
        self.assertEqual(response, "Invalid level code: abc-def-gh")


if __name__ == "__main__":
    unittest.main()
