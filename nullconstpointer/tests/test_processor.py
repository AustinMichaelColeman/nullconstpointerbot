import unittest

from nullconstpointer.processor import Processor
from nullconstpointer.user import User, MOD_LEVEL_OWNER, MOD_LEVEL_MOD, MOD_LEVEL_USER
from nullconstpointer.level import Level
from nullconstpointer.commands.add import AddCommand
from nullconstpointer.commands.mod import ModCommand
from nullconstpointer.commands.unmod import UnmodCommand
from nullconstpointer.commands.remove import RemoveCommand
from nullconstpointer.commands.random import RandomCommand


class TestProcessor(unittest.TestCase):
    def setUp(self):
        self.test_owner = User("test_owner", MOD_LEVEL_OWNER)
        self.test_processor = Processor(self.test_owner)

    def test_processor_users_equal_to_one(self):
        self.assertEqual(self.test_processor.user_count(), 1)


if __name__ == "__main__":
    unittest.main()
