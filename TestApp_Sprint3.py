import unittest
from classes import individualPerson, familyClass
from helperFunctions_Sprint3 import single_over_30, multiple_births, validate_male_lastname, validate_unique_name_birthdate
from helperFunctions_Sprint3 import siblings_should_not_marry, get_children, get_spouse

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

        individual31 = individualPerson("I31")
        individual31.uid = "I31"
        individual31.birt = '9 JAN 1988'
        ind_dict[individual31.uid] = individual31

        individual41 = individualPerson("I41")
        individual41.uid = "I41"
        individual41.birt = '9 JAN 1988'
        ind_dict[individual41.uid] = individual41

        family1 = familyClass("F2")
        family1.chil = ['I31', 'I41']
        fam_dict[family1.fid] = family1

        self.assertEqual(len(multiple_births(fam_dict, ind_dict)), 5, True)
        
    def test_validate_male_lastname(self):
        """ Test cases for US16 --- All male members of the family should have the same last name"""
        indi_dict = {}
        fam_dict = {}

        indi_I3 = individualPerson("I3")
        indi_I3.name = "John Hernandez"
        indi_I3.sex = 'M'
        indi_dict[indi_I3.uid] = indi_I3
        indi_I4 = individualPerson("I4")
        indi_I4.name = "Sam Jackson"
        indi_I4.sex = 'M'
        indi_dict[indi_I4.uid] = indi_I4

        fam_F1 = familyClass("F1")
        fam_F1.chil = ["I3", "I4"]
        fam_F1.husb = "David Hernandez"
        fam_F1.wife = "Sofia Martinez"
        fam_dict[fam_F1.fid] = fam_F1

        self.assertEqual(validate_male_lastname(indi_dict, fam_dict), ({'F1': ['Hernandez', 'I4', 'Jackson']}))
        self.assertNotEqual(validate_male_lastname(indi_dict, fam_dict), {'F1':'I5'})
        self.assertIsNotNone(validate_male_lastname(indi_dict, fam_dict))
        self.assertIsNot(validate_male_lastname(indi_dict, fam_dict), {'F1':'I5'})
        self.assertCountEqual(validate_male_lastname(indi_dict, fam_dict), ({'F1': ['Hernandez', 'I4', 'Jackson']}))

        indi_dict = {}
        fam_dict = {}

        indi_I8 = individualPerson("I8")
        indi_I8.name = "John Hernandez"
        indi_I8.sex = 'M'
        indi_dict[indi_I8.uid] = indi_I8
        indi_I9 = individualPerson("I9")
        indi_I9.name = "Sonia Jackson"
        indi_I9.sex = 'F'
        indi_dict[indi_I9.uid] = indi_I9

        fam_F2 = familyClass("F2")
        fam_F2.chil = ["I9", "I9"]
        fam_F2.husb = "David Hernandez"
        fam_F2.wife = "Sofia Martinez"
        fam_dict[fam_F2.fid] = fam_F2

        self.assertEqual(validate_male_lastname(indi_dict, fam_dict), ({}))
        self.assertNotEqual(validate_male_lastname(indi_dict, fam_dict), {'F1':'I5'})
        self.assertIsNotNone(validate_male_lastname(indi_dict, fam_dict))
        self.assertIsNot(validate_male_lastname(indi_dict, fam_dict), {'F1':'I5'})
        self.assertCountEqual(validate_male_lastname(indi_dict, fam_dict), ({}))        
    
    def test_validate_unique_name_birthdate(self):
        """ Test cases for US23 --- No more than one individual with the same name and birth date should appear in a GEDCOM file"""
        indi_dict = {}

        indi_I3 = individualPerson("I3")
        indi_I3.name = "John Hernandez"
        indi_I3.birt = "15 AUG 1947"
        indi_dict[indi_I3.uid] = indi_I3
        indi_I4 = individualPerson("I4")
        indi_I4.name = "Ricky Pointing"
        indi_I4.birt = "09 NOV 1949"
        indi_dict[indi_I4.uid] = indi_I4
        indi_I5 = individualPerson("I5")
        indi_I5.name = "John Hernandez"
        indi_I5.birt = "15 AUG 1947"
        indi_dict[indi_I5.uid] = indi_I5
        indi_I6 = individualPerson("I6")
        indi_I6.name = "John Hernandez"
        indi_I6.birt = "15 AUG 1947"
        indi_dict[indi_I6.uid] = indi_I6 
        indi_I7 = individualPerson("I7")
        indi_I7.name = "John Hernandez"
        indi_I7.birt = "15 AUG 1947"
        indi_dict[indi_I7.uid] = indi_I7        

        self.assertEqual(validate_unique_name_birthdate(indi_dict), ([['I3', 'I5', 'I6', 'I7', 'John Hernandez', '1947-08-15']]))
        self.assertNotEqual(validate_unique_name_birthdate(indi_dict), {'F1':'I5'})
        self.assertIsNotNone(validate_unique_name_birthdate(indi_dict))
        self.assertIsNot(validate_unique_name_birthdate(indi_dict), {'F1':'I5'})
        self.assertCountEqual(validate_unique_name_birthdate(indi_dict), ([['I3', 'I5', 'I6', 'I7', 'John Hernandez', '1947-08-15']]))

        indi_dict = {}

        indi_I8 = individualPerson("I8")
        indi_I8.name = "John Hernandez"
        indi_I8.birt = "15 AUG 1947"
        indi_dict[indi_I8.uid] = indi_I8
        indi_I9 = individualPerson("I9")
        indi_I9.name = "Ricky Pointing"
        indi_I9.birt = "09 FEB 1935"
        indi_dict[indi_I9.uid] = indi_I9

        self.assertEqual(validate_unique_name_birthdate(indi_dict), ([]))
        self.assertNotEqual(validate_unique_name_birthdate(indi_dict), {'F1':'I5'})
        self.assertIsNotNone(validate_unique_name_birthdate(indi_dict))
        self.assertIsNot(validate_unique_name_birthdate(indi_dict), {'F1':'I5'})
        self.assertCountEqual(validate_unique_name_birthdate(indi_dict), ([]))

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
