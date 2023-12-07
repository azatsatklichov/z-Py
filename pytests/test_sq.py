import unittest
import math


class MyTestCase(unittest.TestCase):

    def test_something(self):
        self.assertEqual(True, True)


    def test_sqrt(self):
        num = 25
        assert math.sqrt(num) == 5

    def testsquare(self):
        num = 7
        assert 7*7 == 49

    def tesequality(self):
        assert 10 == 10


if __name__ == '__main__':
    unittest.main()
