import unittest

from nullconstpointer.bot.level import Level


class TestLevels(unittest.TestCase):
    def test_level_code_empty(self):
        level = Level("")

        self.assertFalse(level)

    def test_invalid_level_is_empty(self):
        # Text allowed in level codes: 0-9 A-Z a-z except I O Z
        # ignore anything but 0-9, A-Z, a-z, except IiOoZz
        # ensure level length
        level = Level("invalid_LEVEL_code0123456789-=}||test")

        self.assertFalse(level)

        # cannot contain iIOoZz
        level = Level("iIo-OzZ-abc")
        self.assertFalse(level)

        # must match correct length
        level = Level("abc-def-gh")
        self.assertFalse(level)

        level = Level("abc-def-ghhh")
        self.assertFalse(level)

    def test_valid_level_is_capitalized(self):
        valid_level = "abc-def-ghd"
        level = Level(valid_level)
        self.assertEqual(level, "ABC-DEF-GHD")

    def test_valid_level_ignores_whitespace(self):
        valid_level = " abc ---_ def     ghd -]{}/"
        level = Level(valid_level)
        self.assertEqual(level, "ABC-DEF-GHD")


if __name__ == "__main__":
    unittest.main()
