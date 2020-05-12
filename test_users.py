import unittest
from lib.nullconstpointer import user, level


class TestUsers(unittest.TestCase):
    def test_user_mod_level_is_user_by_default(self):
        theuser = user.User("userA", "xxx-xxx-xxx")
        self.assertEqual(theuser.modlevel, user.MOD_LEVEL_USER)

    def test_user_level_count_is_one_by_default(self):
        theuser = user.User("userA", "xxx-xxx-xxx")
        self.assertEqual(theuser.levelCount(), 1)

    def test_user_level_is_formatted(self):
        thelevel = level.Level("xxx-xxx-xxx")
        theuser = user.User("userA", thelevel)
        self.assertEqual(str(theuser.next_level()), "XXX-XXX-XXX")

    def test_user_can_remove_level(self):
        thelevel = level.Level("xxx-xxx-xxx")
        theuser = user.User("userA", thelevel)
        theuser.remove_level()
        self.assertEqual(theuser.next_level(), None)

    def test_users_can_have_multiple_levels(self):
        levelOne = level.Level("abc-def-ghd")
        theuser = user.User("userA", levelOne)
        levelTwo = level.Level("aaa-bbb-ccc")
        theuser.add_level(levelTwo)

        self.assertEqual(str(theuser.next_level()), str(levelOne))
        theuser.remove_level()
        self.assertEqual(str(theuser.next_level()), str(levelTwo))
        theuser.remove_level()
        self.assertEqual(theuser.next_level(), None)

    def test_user_can_be_mod_level_mod(self):
        theuser = user.User("moderator", level.Level("abc-abc-abc"), user.MOD_LEVEL_MOD)
        self.assertEqual(theuser.mod_level(), user.MOD_LEVEL_MOD)

    def test_user_can_be_mod_level_owner(self):
        thelevel = level.Level("abc-abc-abc")
        theuser = user.User("moderator", thelevel, user.MOD_LEVEL_OWNER)
        self.assertEqual(theuser.mod_level(), user.MOD_LEVEL_OWNER)

    def test_user_can_be_mod_level_user(self):
        thelevel = level.Level("abc-abc-abc")
        theuser = user.User("moderator", thelevel, user.MOD_LEVEL_USER)
        self.assertEqual(theuser.mod_level(), user.MOD_LEVEL_USER)

    def test_user_has_user_name(self):
        thelevel = level.Level("abc-def-ghd")
        theuser = user.User("userA", thelevel)
        self.assertEqual(theuser.username, "userA")

    def test_user_has_level_works(self):
        thelevel = level.Level("abc-def-ghd")
        theuser = user.User("userA", thelevel)
        does_not_have_level = level.Level("abc-def-ghh")
        self.assertEqual(theuser.has_level(thelevel), True)
        self.assertEqual(theuser.has_level(does_not_have_level), False)


if __name__ == "__main__":
    unittest.main()
