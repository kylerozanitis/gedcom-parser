import unittest
from classes import individualPerson, familyClass
from helperFunctions_Sprint3 import single_over_30, multiple_births, validate_male_lastname, validate_unique_name_birthdate
from helperFunctions_Sprint3 import siblings_should_not_marry, get_children, get_spouse, reject_illegal_dates, correct_gender_for_role
from helperFunctions_Sprint3 import unique_first_names

class TestHelperFunctions(unittest.TestCase):
    """Unit for HelperFunction File"""
    def test_single_over_30(self):
        """ US31 --- Test cases for living singles """
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
        """ US32 --- Test cases to validate multiple births """
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
        """ Test cases for US18 --- Siblings should not marry"""
        fam_dict = {}
        ind_dict = {}

        individual = individualPerson("I1")
        individual.uid = "I1"
        individual.fams = ['F1']
        individual.famc = ["F4"]
        ind_dict[individual.uid] = individual

        individual2 = individualPerson("I2")
        individual2.uid = "I2"
        individual2.fams = ['F1']
        individual2.famc = ["F5"]
        ind_dict[individual2.uid] = individual2

        family = familyClass("F1")
        family.husb_id = "I1"
        family.wife_id = "I2"
        family.chil = ["I3", "I6"]
        fam_dict[family.fid] = family

        self.assertEqual(get_spouse(fam_dict, "F1", "I1"), "I2", True)
        self.assertEqual(get_spouse(fam_dict, "F1", "I2"), "I1", True)

        individual3 = individualPerson("I3")
        individual3.uid = "I3"
        individual3.fams = ['F2']
        individual3.famc = ["F1"]
        ind_dict[individual3.uid] = individual3

        individual4 = individualPerson("I4")
        individual4.uid = "I4"
        individual4.fams = ['F2']
        individual4.famc = ["F1"]
        ind_dict[individual4.uid] = individual4

        family = familyClass("F2")
        family.husb_id = "I1"
        family.wife_id = "I2"
        family.chil = ["I5", "I7"]
        fam_dict[family.fid] = family

        self.assertEqual(get_children(fam_dict, "F2"), ["I5", "I7"], True)
        self.assertEqual(get_children(fam_dict, "F1"), ["I3", "I6"], True)
        self.assertEqual(len(siblings_should_not_marry(fam_dict, ind_dict)), 0, True)

    def test_reject_illegal_dates(self):
        """ Test cases for US42 --- Reject Illegal date"""
        self.assertTrue(reject_illegal_dates('2/10/2018'), True)
        self.assertTrue(reject_illegal_dates('6/30/2018'), True)

        self.assertFalse(reject_illegal_dates('2/30/2018'), False)
        self.assertFalse(reject_illegal_dates('6/32/2018'), False)

    def test_correct_gender_for_role(self):
        """ Unit tests for US21 Correct Gender for Role - Husband in family
        should be male and wife in family should be female """

        indi_dict = {}
        fam_dict = {}

        i1 = individualPerson('I1')
        i1.sex = "M"
        i1.uid = 'I1'
        indi_dict[i1.uid] = i1

        i2 = individualPerson('I2')
        i2.sex = "F"
        i2.uid = 'I2'
        indi_dict[i2.uid] = i2

        f1 = familyClass("F1")
        f1.husb_id = "I1"
        f1.wife_id = "I2"
        fam_dict[f1.fid] = f1

        self.assertEqual(correct_gender_for_role(fam_dict, indi_dict), {})
        self.assertNotEqual(correct_gender_for_role(fam_dict, indi_dict), {"F1": ["F", "M", "I1"]})

        i3 = individualPerson('I3')
        i3.sex = "F"
        i3.uid = 'I3'
        indi_dict[i3.uid] = i3

        i4 = individualPerson('I4')
        i4.sex = "F"
        i4.uid = 'I4'
        indi_dict[i4.uid] = i4

        f2 = familyClass("F2")
        f2.husb_id = "I3"
        f2.wife_id = "I4"
        fam_dict[f2.fid] = f2

        self.assertEqual(correct_gender_for_role(fam_dict, indi_dict), {"F2": ["F", "M", "I3"]})
        self.assertNotEqual(correct_gender_for_role(fam_dict, indi_dict), {})

        i5 = individualPerson('I5')
        i5.sex = "M"
        i5.uid = 'I5'
        indi_dict[i5.uid] = i5

        i6 = individualPerson('I6')
        i6.sex = "M"
        i6.uid = 'I6'
        indi_dict[i6.uid] = i6

        f3 = familyClass("F3")
        f3.husb_id = "I5"
        f3.wife_id = "I6"
        fam_dict[f3.fid] = f3

        self.assertEqual(correct_gender_for_role(fam_dict, indi_dict), {"F2": ["F", "M", "I3"], "F3": ["M", "F", "I6"]})
        self.assertNotEqual(correct_gender_for_role(fam_dict, indi_dict), {"F2": ["F", "M", "I3"]})

        i7 = individualPerson('I7')
        i7.sex = "M"
        i7.uid = 'I7'
        indi_dict[i7.uid] = i7

        i8 = individualPerson('I8')
        i8.sex = "NA"
        i8.uid = 'I8'
        indi_dict[i8.uid] = i8

        f4 = familyClass("F4")
        f4.husb_id = "I7"
        f4.wife_id = "I8"
        fam_dict[f4.fid] = f4

        self.assertEqual(correct_gender_for_role(fam_dict, indi_dict), {"F2": ["F", "M", "I3"], "F3": ["M", "F", "I6"], "F4": ["NA", "F", "I8"]})
        self.assertNotEqual(correct_gender_for_role(fam_dict, indi_dict), {"F2": ["F", "M", "I3"], "F3": ["M", "F", "I6"]})

    def test_unique_first_names(self):
        """ Unit tests for US25 Unique First Names - No more than one child
        with the same name and birth date should appear in a family """

        indi_dict = {}
        fam_dict = {}

        i1 = individualPerson("I1")
        i1.uid = "I1"
        i1.name = "Tyler"
        i1.birt = "26 Oct 1995"

        indi_dict[i1.uid] = i1

        i2 = individualPerson("I2")
        i2.uid = "I2"
        i1.name = "Quinn"
        i1.birt = "26 Oct 1995"
        indi_dict[i2.uid] = i2

        f1 = familyClass("F1")
        f1.chil = ["I1", "I2"]
        fam_dict[f1.fid] = f1

        self.assertEqual(unique_first_names(fam_dict, indi_dict), set())
        self.assertNotEqual(unique_first_names(fam_dict, indi_dict), {"F1"})

        indi_dict = {}
        fam_dict = {}

        i3 = individualPerson("I3")
        i3.uid = "I3"
        i3.name = "Ryan"
        i3.birt = "13 Apr 1994"

        indi_dict[i3.uid] = i3

        i4 = individualPerson("I4")
        i4.uid = "I4"
        i4.name = "Ryan"
        i4.birt = "13 Apr 1994"
        indi_dict[i4.uid] = i4

        f2 = familyClass("F2")
        f2.chil = ["I3", "I4"]
        fam_dict[f2.fid] = f2

        self.assertEqual(unique_first_names(fam_dict, indi_dict), {"F2"})
        self.assertNotEqual(unique_first_names(fam_dict, indi_dict), {"F1"})


if __name__ == '__main__':
    unittest.main(exit=False,verbosity=2)
