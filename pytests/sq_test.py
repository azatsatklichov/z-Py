import unittest


class MyTestCase2(unittest.TestCase):

    def test_greater(self):
        num = 100
        assert num == 100

    def test_greater_equal(self):
        num = 100
        assert num >= 100

    def test_less(self):
        num = 100
        assert num < 200

if __name__ == '__main__':
    unittest.main()
