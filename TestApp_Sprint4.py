""" This file includes the unit tests for functions that were implemented in sprint 4 """

import unittest
from classes import individualPerson, familyClass
from helperFunctions_Sprint4 import sibling_spacing, list_orphans, unique_families_by_spouses, order_siblings_by_age
from helperFunctions_Sprint4 import list_upcoming_anniversaries, list_spouse_large_age_difference
from helperFunctions_Sprint4 import no_bigamy

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

    def test_order_siblings_by_age(self):
        """ Unit tests for US28 - List siblings in families by decreasing age """

        indi_dict = {}
        fam_dict = {}

        i1 = individualPerson("I1")
        i1.uid = "I1"
        i1.name = "Kyle"
        i1.birt = "15 Jul 1992"

        indi_dict[i1.uid] = i1

        i2 = individualPerson("I2")
        i2.uid = "I2"
        i2.name = "Ryan"
        i2.birt = "13 Apr 1994"

        indi_dict[i2.uid] = i2

        i3 = individualPerson("I3")
        i3.uid = "I3"
        i3.name = "Tyler"
        i3.birt = "26 Oct 1995"

        indi_dict[i3.uid] = i3

        i4 = individualPerson("I4")
        i4.uid = "I4"
        i4.name = "Quinn"
        i4.birt = "27 Oct 1997"
        indi_dict[i4.uid] = i4

        f1 = familyClass("F1")
        f1.chil = ["I1", "I2", "I3", "I4"]
        fam_dict[f1.fid] = f1

        self.assertEqual(order_siblings_by_age(fam_dict, indi_dict), {"F1": [["I1", "15 Jul 1992"], ["I2", "13 Apr 1994"], ["I3", "26 Oct 1995"], ["I4", "27 Oct 1997"]]})
        self.assertNotEqual(order_siblings_by_age(fam_dict, indi_dict), {"F1": [["I4", "27 Oct 1997"], ["I3", "26 Oct 1995"], ["I2", "13 Apr 1994"], ["I1", "15 Jul 1992"]]})

        i5 = individualPerson("I5")
        i5.uid = "I5"
        i5.name = "Kyle"
        i5.birt = "1 Jan 2003"

        indi_dict[i5.uid] = i5

        i6 = individualPerson("I6")
        i6.uid = "I6"
        i6.name = "Ryan"
        i6.birt = "1 Jan 2002"

        indi_dict[i6.uid] = i6

        i7 = individualPerson("I7")
        i7.uid = "I7"
        i7.name = "Tyler"
        i7.birt = "1 Jan 2001"

        indi_dict[i7.uid] = i7

        f2 = familyClass("F2")
        f2.chil = ["I5", "I6", "I7"]
        fam_dict[f2.fid] = f2

        self.assertEqual(order_siblings_by_age(fam_dict, indi_dict), {"F1": [["I1", "15 Jul 1992"], ["I2", "13 Apr 1994"], ["I3", "26 Oct 1995"], ["I4", "27 Oct 1997"]], "F2": [["I7", "1 Jan 2001"], ["I6", "1 Jan 2002"], ["I5", "1 Jan 2003"]]})
        self.assertNotEqual(order_siblings_by_age(fam_dict, indi_dict), {"F1": [["I4", "27 Oct 1997"], ["I3", "26 Oct 1995"], ["I2", "13 Apr 1994"], ["I1", "15 Jul 1992"]]})


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

    def test_no_bigamy(self):
        """ Test cases for US11 --- Marriage should not occur during marriage to another spouse"""
        fam_dict = {}

        fam_F1 = familyClass("F1")
        fam_F1.husb_id = "I1"
        fam_F1.wife_id = "I2"
        fam_dict[fam_F1.fid] = fam_F1

        fam_F2 = familyClass("F2")
        fam_F2.husb_id = "I1"
        fam_F2.wife_id = "I3"
        fam_dict[fam_F2.fid] = fam_F2

        fam_F3 = familyClass("F3")
        fam_F3.husb_id = "I1"
        fam_F3.wife_id = "I4"
        fam_dict[fam_F3.fid] = fam_F3

        fam_F4 = familyClass("F4")
        fam_F4.husb_id = "I5"
        fam_F4.wife_id = "I3"
        fam_dict[fam_F4.fid] = fam_F4    

        fam_F5 = familyClass("F5")
        fam_F5.husb_id = "I6"
        fam_F5.wife_id = "I7"
        fam_dict[fam_F5.fid] = fam_F5   

        self.assertEqual(no_bigamy(fam_dict), ({'I1': ['I4', 'I2', 'I3'], 'I3': ['I5', 'I1']}))
        self.assertNotEqual(no_bigamy(fam_dict), {'F1':'I5'})
        self.assertIsNotNone(no_bigamy(fam_dict))
        self.assertIsNot(no_bigamy(fam_dict), {'F1':'I5'})
        self.assertCountEqual(no_bigamy(fam_dict), ({'I1': ['I4', 'I2', 'I3'], 'I3': ['I5', 'I1']}))

        fam_dict = {}

        fam_F6 = familyClass("F6")
        fam_F6.husb_id = "I8"
        fam_F6.wife_id = "I9"
        fam_dict[fam_F6.fid] = fam_F6

        fam_F7 = familyClass("F7")
        fam_F7.husb_id = "I10"
        fam_F7.wife_id = "I11"
        fam_dict[fam_F7.fid] = fam_F7

        self.assertEqual(no_bigamy(fam_dict), ({}))
        self.assertNotEqual(no_bigamy(fam_dict), {'F1':'I5'})
        self.assertIsNotNone(no_bigamy(fam_dict))
        self.assertIsNot(no_bigamy(fam_dict), {'F1':'I5'})
        self.assertCountEqual(no_bigamy(fam_dict), ({}))

if __name__ == '__main__':
    unittest.main(exit=False,verbosity=2)
