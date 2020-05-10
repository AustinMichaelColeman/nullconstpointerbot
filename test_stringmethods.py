import unittest
from lib.levels import levels


class TestUserLevelQueue(unittest.TestCase):
    def test_level_queue_empty(self):
        levels_instance = levels.Levels()

        self.assertEqual(levels_instance.empty(), True)


if __name__ == "__main__":
    unittest.main()
