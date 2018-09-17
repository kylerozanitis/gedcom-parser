from app import create_table_individual, read_data_file, data_parser
from classes import individualPerson, familyClass
import unittest

class TestTable(unittest.TestCase):

    def test_create_table_individual(self):
        y = create_table_individual([])
        x = create_table_individual([])
        self.assertEqual(x, y, True)


if __name__ == '__main__':
    print('Running unit tests')
    unittest.main()
