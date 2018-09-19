import unittest
from helperFunctions import change_date_format, validate_date_format

class TestTable(unittest.TestCase):
    """Unit test will be define here"""
    pass


class TestHelperFunctions(unittest.TestCase):
    """Unit for HelperFunction File"""

    def test_validate_date_format(self):
        self.assertEqual(validate_date_format('7 MAY 2018'),True, True)
        self.assertNotEqual(validate_date_format('8/FEB/2018'), True, False)
        self.assertNotEqual(validate_date_format('8/FEB/18'), True, False)

    def test_change_date_format(self):
        self.assertEqual(change_date_format('7 MAY 2018'), '2018-05-7', True)
        self.assertNotEqual(change_date_format('7 MAY 2018'), '2018/05/7', True)
        self.assertNotEqual(change_date_format('7 MAY 2018'), '2018/05/07', True)


if __name__ == '__main__':
    unittest.main()
