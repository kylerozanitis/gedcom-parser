import unittest
from helperFunctions_Sprint2 import list_recent_survivals, living_married_list, list_upcoming_birthdays
from classes import individualPerson, familyClass


class TestHelperFunctions(unittest.TestCase):
    """Unit for HelperFunction File"""

    def test_living_married(self):
        fam_dict = {}
        ind_dict = {}

        individual = individualPerson("I1")
        individual.uid = "I1"
        individual.alive = True
        individual.deat = "NA"
        ind_dict[individual.uid] = individual

        individual2 = individualPerson("I2")
        individual2.uid = "I2"
        individual2.alive = True
        individual2.deat = 'NA'
        ind_dict[individual2.uid] = individual2

        individual3 = individualPerson("I3")
        individual3.uid = "I3"
        individual3.alive = True
        individual3.deat = 'NA'
        ind_dict[individual3.uid] = individual3

        individual4 = individualPerson("I4")
        individual4.uid = "I4"
        individual4.alive = True
        individual4.deat = 'NA'
        ind_dict[individual4.uid] = individual4

        family = familyClass("F1")
        family.husb_id = "I1"
        family.wife_id = "I2"
        family.marr = "1 JAN 2000"
        fam_dict[family.fid] = family

        family2 = familyClass("F2")
        family2.husb_id = "I3"
        family2.wife_id = "I4"
        family2.marr = "1 FEB 2004"
        fam_dict[family2.fid] = family2

        self.assertEqual(len(living_married_list(fam_dict, ind_dict)), 4, True)
        self.assertEqual(living_married_list(fam_dict, ind_dict), ['I1','I2','I3','I4'], True)


    def test_list_recent_survivals(self):
        fam_dict = {}
        ind_dict = {}

        individual = individualPerson("I1")
        individual.uid = "I1"
        individual.alive = False
        individual.birt = "1 JAN 1991"
        individual.deat = "1 OCT 2018"
        individual.name = "Fernando"
        individual.fams = ["F1"]
        individual.sex = "M"
        ind_dict[individual.uid] = individual

        individual2 = individualPerson("I2")
        individual2.uid = "I2"
        individual2.fams = ["F1"]
        individual2.alive = True
        individual2.birt = "1 JAN 1991"
        individual2.name = "Laura"
        individual2.sex = "F"
        ind_dict[individual2.uid] = individual2

        family = familyClass("F1")
        family.husb_id = "I1"
        family.wife_id = "I2"
        family.chil = ["I4", "I6"]
        family.marr = "1 JAN 2005"

        fam_dict[family.fid] = family


        self.assertEqual(len(list_recent_survivals(ind_dict, fam_dict)), 1, True)

    def test_list_upcoming_birthdays(self):
        indi_dict = {}

        i1 = individualPerson('I1')
        i1.uid = 'I11'
        i1.birt = '29 SEP 2017'
        indi_dict[i1.uid] = i1

        i2 = individualPerson('I2')
        i2.udi = 'I12'
        i2.birt = '15 OCT 1955'
        indi_dict[i2.uid] = i2

        self.assertEqual(len(list_upcoming_birthdays(indi_dict)),1,True)

        i3 = individualPerson('I3')
        i3.udi = 'I3'
        i3.birt = '30 SEP 1960'
        indi_dict[i3.uid] = i3

        i3 = individualPerson('I4')
        i3.udi = 'I4'
        i3.birt = '21 OCT 1989'
        indi_dict[i3.uid] = i3

        self.assertEqual(len(list_upcoming_birthdays(indi_dict)),2 ,True)

if __name__ == '__main__':
    unittest.main(exit=False,verbosity=2)