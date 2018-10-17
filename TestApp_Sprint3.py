import unittest
from classes import individualPerson, familyClass
from helperFunctions_Sprint3 import single_over_30, multiple_births

class TestHelperFunctions(unittest.TestCase):
    """Unit for HelperFunction File"""
    def test_single_over_30(self):
        fam_dict = {}
        ind_dict = {}

        individual = individualPerson("I1")
        individual.uid = "I1"
        individual.age = 27
        ind_dict[individual.uid] = individual

        individual2 = individualPerson("I2")
        individual2.uid = "I2"
        individual2.age = 35
        ind_dict[individual2.uid] = individual2

        individual3 = individualPerson("I3")
        individual3.uid = "I3"
        individual3.age = 45
        ind_dict[individual3.uid] = individual3

        individual4 = individualPerson("I4")
        individual4.uid = "I4"
        individual4.age = 15
        ind_dict[individual4.uid] = individual4

        individual5 = individualPerson("I5")
        individual5.uid = "I5"
        individual5.age = 55
        ind_dict[individual5.uid] = individual5

        family = familyClass("F1")
        family.husb_id = "I1"
        family.wife_id = "I2"
        fam_dict[family.fid] = family

        self.assertEqual(len(single_over_30(fam_dict, ind_dict)), 2, True)

    def test_multiple_births(self):
        fam_dict = {}
        ind_dict = {}

        individual = individualPerson("I1")
        individual.uid = "I1"
        individual.birt = '10 SEP 1998'
        ind_dict[individual.uid] = individual

        individual2 = individualPerson("I2")
        individual2.uid = "I2"
        individual2.birt = '10 SEP 1998'
        ind_dict[individual2.uid] = individual2

        individual3 = individualPerson("I3")
        individual3.uid = "I3"
        individual3.birt = '10 SEP 1988'
        ind_dict[individual3.uid] = individual3

        individual4 = individualPerson("I4")
        individual4.uid = "I4"
        individual4.birt = '10 SEP 1998'
        ind_dict[individual4.uid] = individual4

        family = familyClass("F1")
        family.chil = ['I1','I2', 'I3', 'I4']
        fam_dict[family.fid] = family

        self.assertEqual(len(multiple_births(fam_dict, ind_dict)), 3, True)

if __name__ == '__main__':
    unittest.main(exit=False,verbosity=2)