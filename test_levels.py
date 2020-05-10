import unittest
from lib.nullconstpointer import level


class TestLevels(unittest.TestCase):
    def test_level_code_empty(self):
        levelinst = level.Level()

        self.assertEqual(levelinst.code(), "")


if __name__ == "__main__":
    unittest.main()
