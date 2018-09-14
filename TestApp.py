from app import create_table
import unittest

class TestTable(unittest.TestCase):

    def test_create_table(self):
        y = create_table()
        x = create_table()
        self.assertEqual(x, y, True)


if __name__ == '__main__':
    print('Running unit tests')
    unittest.main(exit=False, verbosity=2)
