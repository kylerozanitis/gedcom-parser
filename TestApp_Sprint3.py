import unittest
from classes import individualPerson, familyClass
from helperFunctions_Sprint3 import single_over_30, siblings_should_not_marry, get_spouse, get_children

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

    def test_siblings_should_not_marry(self):
        fam_dict = {}
        ind_dict = {}

        individual = individualPerson("I1")
        individual.uid = "I1"
        individual.fams = ['F5']
        individual.famc = ["F4"]
        ind_dict[individual.uid] = individual

        individual2 = individualPerson("I2")
        individual2.uid = "I2"
        individual2.fams = ['F2']
        individual2.famc = ["F4"]
        ind_dict[individual2.uid] = individual2

        family = familyClass("F1")
        family.husb_id = "I1"
        family.wife_id = "I2"
        family.chil = ["I3", "I4"]
        fam_dict[family.fid] = family

        self.assertEqual(get_spouse(fam_dict, "F1", "I1"), "I2", True)
        self.assertEqual(get_spouse(fam_dict, "F1", "I2"), "I1", True)

        individual3 = individualPerson("I3")
        individual3.fams = ['F5']
        individual3.famc = ["F4"]
        ind_dict[individual3.uid] = individual3

        individual4 = individualPerson("I4")
        individual4.fams = ['F2']
        individual4.famc = ["F4"]
        ind_dict[individual4.uid] = individual4

        family = familyClass("F2")
        family.husb_id = "I1"
        family.wife_id = "I2"
        family.chil = ["I1", "I2"]
        fam_dict[family.fid] = family

        self.assertEqual(get_children(fam_dict, "F2"), ["I1", "I2"], True)
        self.assertEqual(len(siblings_should_not_marry(fam_dict, ind_dict)), 2, True)



if __name__ == '__main__':
    unittest.main(exit=False,verbosity=2)