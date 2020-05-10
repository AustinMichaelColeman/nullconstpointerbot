import unittest
from lib.nullconstpointer import bot


class TestBot(unittest.TestCase):
    def test_bot_users_empty(self):
        nullconstpointerbot = bot.Bot()

        self.assertEqual(nullconstpointerbot.user_count(), 0)


if __name__ == "__main__":
    unittest.main()
