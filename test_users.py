import unittest

from nullconstpointer.user import User, MOD_LEVEL_USER, MOD_LEVEL_MOD, MOD_LEVEL_OWNER
from nullconstpointer.level import Level


class TestUsers(unittest.TestCase):
    def test_user_mod_level_is_user_by_default(self):
        theuser = User("userA")
        self.assertEqual(theuser.modlevel, MOD_LEVEL_USER)

    def test_user_level_count_is_zero_by_default(self):
        theuser = User("userA")
        self.assertEqual(theuser.levelCount(), 0)

    def test_user_level_is_formatted(self):
        thelevel = Level("xxx-xxx-xxx")
        theuser = User("userA")
        theuser.add_level(thelevel)
        self.assertEqual(str(theuser.next_level()), "XXX-XXX-XXX")

    def test_user_can_remove_level(self):
        thelevel = Level("xxx-xxx-xxx")
        theuser = User("userA")
        theuser.add_level(thelevel)
        theuser.remove_level()
        self.assertEqual(theuser.next_level(), None)

    def test_users_can_have_multiple_levels(self):
        levelOne = Level("abc-def-ghd")
        theuser = User("userA")
        theuser.add_level(levelOne)
        levelTwo = Level("aaa-bbb-ccc")
        theuser.add_level(levelTwo)

        self.assertEqual(str(theuser.next_level()), str(levelOne))
        theuser.remove_level()
        self.assertEqual(str(theuser.next_level()), str(levelTwo))
        theuser.remove_level()
        self.assertEqual(theuser.next_level(), None)

    def test_user_can_be_mod_level_mod(self):
        theuser = User("moderator", MOD_LEVEL_MOD)
        self.assertEqual(theuser.mod_level(), MOD_LEVEL_MOD)

    def test_user_can_be_mod_level_owner(self):
        theuser = User("moderator", MOD_LEVEL_OWNER)
        self.assertEqual(theuser.mod_level(), MOD_LEVEL_OWNER)

    def test_user_can_be_mod_level_user(self):
        theuser = User("moderator", MOD_LEVEL_USER)
        self.assertEqual(theuser.mod_level(), MOD_LEVEL_USER)

    def test_user_has_user_name(self):
        theuser = User("userA")
        self.assertEqual(theuser.username, "userA")

    def test_user_has_level_works(self):
        thelevel = Level("abc-def-ghd")
        theuser = User("userA")
        theuser.add_level(thelevel)
        does_not_have_level = Level("abc-def-ghh")
        self.assertEqual(theuser.has_level(thelevel), True)
        self.assertEqual(theuser.has_level(does_not_have_level), False)

    def test_user_can_be_modded(self):
        theuser = User("userA", MOD_LEVEL_USER)
        theuser.make_mod()
        self.assertEqual(theuser.modlevel, MOD_LEVEL_MOD)

    def test_user_can_be_unmodded(self):
        theuser = User("userA", MOD_LEVEL_MOD)
        theuser.make_user()
        self.assertEqual(theuser.modlevel, MOD_LEVEL_USER)


if __name__ == "__main__":
    unittest.main()
