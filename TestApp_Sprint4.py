""" This file includes the unit tests for functions that were implemented in sprint 4 """

import unittest
from classes import individualPerson, familyClass
from helperFunctions_Sprint4 import sibling_spacing, list_orphans

class TestHelperFunctions(unittest.TestCase):
    def test_sibling_spacing(self):
        fam_dict = {}
        ind_dict = {}

        individual = individualPerson("I1")
        individual.uid = "I1"
        individual.birt = '15 AUG 2018'
        ind_dict[individual.uid] = individual

        individual2 = individualPerson("I2")
        individual2.uid = "I2"
        individual2.birt = '15 AUG 2018'
        ind_dict[individual2.uid] = individual2

        individual3 = individualPerson("I3")
        individual3.uid = "I3"
        individual3.birt = '16 AUG 2018'
        ind_dict[individual3.uid] = individual3

        family = familyClass("F2")
        family.chil = ['I1', 'I2', 'I3']
        fam_dict[family.fid] = family

        i1 = individualPerson('I11')
        i1.uid = 'I11'
        i1.birt = '29 SEP 2018'
        ind_dict[i1.uid] = i1

        i2 = individualPerson('I12')
        i2.udi = 'I12'
        i2.birt = '15 AUG 2018'
        ind_dict[i2.uid] = i2

        family = familyClass("F2")
        family.chil = ['I11', 'I12']
        fam_dict[family.fid] = family

        self.assertFalse(sibling_spacing(fam_dict, ind_dict))

    def test_list_orphans(self):

        ind_dict = {}
        fam_dict = {}

        individual = individualPerson("I1")
        individual.uid = "I1"
        individual.alive = False
        ind_dict[individual.uid] = individual

        individual2 = individualPerson("I2")
        individual2.uid = "I2"
        individual2.alive = False
        ind_dict[individual2.uid] = individual2

        individual3 = individualPerson("I3")
        individual3.uid = "I3"
        individual3.age = 2
        ind_dict[individual3.uid] = individual3

        family = familyClass("F1")
        family.husb_id = "I1"
        family.wife_id = "I2"
        family.chil = ["I3"]
        fam_dict[family.fid] = family

        self.assertEqual(list_orphans(fam_dict, ind_dict),['I3'])

if __name__ == '__main__':
    unittest.main(exit=False,verbosity=2)