import unittest

from nullconstpointer.level import Level


class TestLevels(unittest.TestCase):
    def test_level_code_empty(self):
        levelinst = Level("")

        self.assertEqual(str(levelinst), "")

    def test_invalid_level_is_empty(self):
        # Text allowed in level codes: 0-9 A-Z a-z except I O Z
        # ignore anything but 0-9, A-Z, a-z, except IiOoZz
        # ensure level length
        levelinst = Level("invalid_LEVEL_code0123456789-=}||test")
        self.assertEqual(str(levelinst), "")

        # cannot contain iIOoZz
        levelinst = Level("iIo-OzZ-abc")
        self.assertEqual(str(levelinst), "")

        # must match correct length
        levelinst = Level("abc-def-gh")
        self.assertEqual(str(levelinst), "")

        levelinst = Level("abc-def-ghhh")
        self.assertEqual(str(levelinst), "")

    def test_valid_level_is_capitalized(self):
        valid_level = "abc-def-ghd"
        levelinst = Level(valid_level)
        self.assertEqual(str(levelinst), "ABC-DEF-GHD")

    def test_valid_level_ignores_whitespace(self):
        valid_level = " abc ---_ def     ghd -]{}/"
        levelinst = Level(valid_level)
        self.assertEqual(str(levelinst), "ABC-DEF-GHD")


if __name__ == "__main__":
    unittest.main()
