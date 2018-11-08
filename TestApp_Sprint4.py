""" This file includes the unit tests for functions that were implemented in sprint 4 """

import unittest
from classes import individualPerson, familyClass
from helperFunctions_Sprint4 import sibling_spacing, list_orphans, unique_families_by_spouses
from helperFunctions_Sprint4 import list_upcoming_anniversaries, list_spouse_large_age_difference

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

    def test_unique_families_by_spouses(self):
        """ Unit tests for US24 - No more than one family with the same spouses
        by name and the same marriage date should appear in a GEDCOM file """

        fam_dict = {}

        f1 = familyClass("F1")
        f1.fid = "F1"
        f1.husb = "Kyle"
        f1.wife = "Eleni"
        f1.marr = "1 JAN 2004"
        fam_dict[f1.fid] = f1

        f2 = familyClass("F2")
        f2.fid = "F2"
        f2.husb = "Kyle"
        f2.wife = "Eleni"
        f2.marr = "1 JAN 2004"
        fam_dict[f2.fid] = f2

        self.assertEqual(unique_families_by_spouses(fam_dict), [["F1", "F2"]])
        self.assertNotEqual(unique_families_by_spouses(fam_dict), [])

        f3 = familyClass("F3")
        f3.fid = "F3"
        f3.husb = "Joe"
        f3.wife = "Anna"
        f3.marr = "1 JAN 2008"
        fam_dict[f3.fid] = f3

        f4 = familyClass("F4")
        f4.fid = "F4"
        f4.husb = "Joe"
        f4.wife = "Anna"
        f4.marr = "1 JAN 2008"
        fam_dict[f4.fid] = f4

        self.assertEqual(unique_families_by_spouses(fam_dict), [["F1", "F2"], ["F3", "F4"]])
        self.assertNotEqual(unique_families_by_spouses(fam_dict), [["F1", "F2"]])

        f5 = familyClass("F5")
        f5.fid = "F5"
        f5.husb = "Joe"
        f5.wife = "Anna"
        f5.marr = "1 JAN 2008"
        fam_dict[f5.fid] = f5

        self.assertEqual(unique_families_by_spouses(fam_dict), [["F1", "F2"], ["F3", "F4"], ["F3", "F5"], ["F4", "F5"]])
        self.assertNotEqual(unique_families_by_spouses(fam_dict), [["F1", "F2"], ["F3", "F4"]])

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

        self.assertEqual(len(list_orphans(fam_dict, ind_dict)),1)

    def test_list_upcoming_anniversaries(self):
        """Test Case for US39 - List all living couples in a GEDCOM file whose marriage anniversaries occur in the next 30 days"""
        fam_dict = {}
        ind_dict = {}

        individual = individualPerson("I1")
        individual.uid = "I1"
        individual.age = 87
        ind_dict[individual.uid] = individual

        individual2 = individualPerson("I2")
        individual2.uid = "I2"
        individual2.age = 35
        ind_dict[individual2.uid] = individual2

        family = familyClass("F1")
        family.husb_id = "I1"
        family.wife_id = "I2"
        family.marr = "29 NOV 2000"
        fam_dict[family.fid] = family


        self.assertEqual(len(list_upcoming_anniversaries(fam_dict, ind_dict)), 1, True)


    def test_list_spouse_large_age_difference(self):
        """Test case for US34 - List all couples who were married when the older spouse was more than twice as old as the younger spouse"""
        fam_dict = {}
        ind_dict = {}

        individual3 = individualPerson("I3")
        individual3.uid = "I3"
        individual3.age = 78
        ind_dict[individual3.uid] = individual3

        individual4 = individualPerson("I4")
        individual4.uid = "I4"
        individual4.age = 25
        ind_dict[individual4.uid] = individual4

        family = familyClass("F2")
        family.husb_id = "I3"
        family.wife_id = "I4"
        family.marr = "9 NOV 2016"
        fam_dict[family.fid] = family

        self.assertEqual(len(list_spouse_large_age_difference(fam_dict, ind_dict)), 1, True)



if __name__ == '__main__':
    unittest.main(exit=False,verbosity=2)