import unittest
import sys

class TestAll(unittest.TestCase):

    def test_python_version(self):
        self.assertTrue(sys.version_info[0] >= 3)
        self.assertTrue(sys.version_info[1] >= 6)


if __name__ in '__main__':
    unittest.main()
