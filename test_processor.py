import unittest
from lib.nullconstpointer import processor


class TestProcessor(unittest.TestCase):
    def test_processor_users_empty(self):
        reqProcessor = processor.Processor()

        self.assertEqual(reqProcessor.user_count(), 0)


if __name__ == "__main__":
    unittest.main()
