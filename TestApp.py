import unittest
from helperFunctions import change_date_format, validate_date_format, deceased_list
from classes import individualPerson

class TestindividualPerson(unittest.TestCase):
    """Unit test for individualPerson class"""

    individual = individualPerson('I123')
    def test_get_age(self):
        individual = individualPerson('I123')
        individual.birt = '7 MAY 2017'
        self.assertEqual(1, individual.get_age(), True)

        individual = individualPerson('I456')
        individual.birt = '10 SEP 1998'
        self.assertEqual(20, individual.get_age(), False)



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

    def test_deceased_list(self):
        ind_dict = dict()

        individual = individualPerson('I123')
        individual.alive = False
        ind_dict[individual.uid] = individual

        individual2 = individualPerson('I456')
        ind_dict[individual2.uid] = individual2

        self.assertEqual(len(deceased_list(ind_dict)), 1, True)

        individual3 = individualPerson('I789')
        ind_dict[individual2.uid] = individual3
        individual3.alive = False
        self.assertEqual(len(deceased_list(ind_dict)), 2, True)








if __name__ == '__main__':
    unittest.main()
