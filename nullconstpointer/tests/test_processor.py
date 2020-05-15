import unittest

from nullconstpointer.processor import Processor
from nullconstpointer.user import User, MOD_LEVEL_OWNER, MOD_LEVEL_MOD, MOD_LEVEL_USER


class TestProcessor(unittest.TestCase):
    def setUp(self):
        self.test_owner = User("test_owner", MOD_LEVEL_OWNER)
        self.test_processor = Processor(self.test_owner)

    def test_processor_users_equal_to_one(self):
        self.assertEqual(self.test_processor.user_count(), 1)


if __name__ == "__main__":
    unittest.main()
