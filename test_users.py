import unittest
from lib.nullconstpointer import user


class TestUsers(unittest.TestCase):
    def test_user_level_count_empty(self):
        theuser = user.User()

        self.assertEqual(theuser.levelCount(), 0)


if __name__ == "__main__":
    unittest.main()
