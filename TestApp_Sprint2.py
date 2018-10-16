import unittest
from helperFunctions_Sprint2 import list_recent_survivals, living_married_list, list_upcoming_birthdays, validate_child_birth
from helperFunctions_Sprint2 import check_parents_not_too_old, check_multiple_births, marriage_after_14
from helperFunctions_Sprint2 import validate_childBirth_with_parentsDeath
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
        i2.birt = '25 OCT 1955'
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
        
    def test_child_birth(self):
        """Test cases for US08 -- Children should be born after marriage of parents (and not more than 9 months after their divorce)"""
        indi_dict = {}
        fam_dict = {}

        indi_I10 = individualPerson("I10")
        indi_I10.birt = "25 AUG 1990"
        indi_dict[indi_I10.uid] = indi_I10
        indi_I11 = individualPerson("I11")
        indi_I11.birt = "13 MAR 1996"
        indi_dict[indi_I11.uid] = indi_I11

        fam_F10 = familyClass("F10")
        fam_F10.marr = "11 OCT 1995"
        fam_F10.chil = ["I10", "I11"]
        fam_dict[fam_F10.fid] = fam_F10

        indi_I12 = individualPerson("I12")
        indi_I12.birt = "11 OCT 1953"
        indi_dict[indi_I12.uid] = indi_I12
        indi_I13 = individualPerson("I13")
        indi_I13.birt = "25 DEC 1955"
        indi_dict[indi_I13.uid] = indi_I13
        
        fam_F12 = familyClass("F12")
        fam_F12.marr = "3 MAR 1950"
        fam_F12.div = "27 NOV 1954"
        fam_F12.chil = ["I12", "I13"]
        fam_dict[fam_F12.fid] = fam_F12

        self.assertEqual(validate_child_birth(indi_dict, fam_dict), ({'F10': 'I10'}, {'F12': 'I13'}))
        self.assertNotEqual(validate_child_birth(indi_dict, fam_dict), {'F1':'I5'})
        self.assertIsNotNone(validate_child_birth(indi_dict, fam_dict))
        self.assertIsNot(validate_child_birth(indi_dict, fam_dict), {'F1':'I5'})
        self.assertCountEqual(validate_child_birth(indi_dict, fam_dict), ({'F10': 'I10'}, {'F12': 'I13'}))

    def test_check_parents_not_too_old(self):
        """ Unit tests for US12 Parents Not Too Old - checks that the mother is less
        than 60 years older than her children and the father is less than 80 years
        older than his children """

        indi_dict = {}
        fam_dict = {}

        i1 = individualPerson('I1')
        i1.sex = "M"
        i1.uid = 'I1'
        i1.name = "Mark"
        i1.birt = '1 JAN 1980'
        indi_dict[i1.uid] = i1

        i2 = individualPerson('I2')
        i2.sex = "F"
        i2.uid = 'I2'
        i2.name = "Cecily"
        i2.birt = '1 JUN 1980'
        indi_dict[i2.uid] = i2

        i3 = individualPerson('I3')
        i3.uid = 'I3'
        i3.name = "Tom"
        i3.birt = '1 MAR 2010'
        indi_dict[i3.uid] = i3

        f1 = familyClass("F1")
        f1.husb_id = "I1"
        f1.wife_id = "I2"
        f1.chil = ["I3"]
        fam_dict[f1.fid] = f1

        self.assertEqual(check_parents_not_too_old(fam_dict, indi_dict), {})
        self.assertNotEqual(check_parents_not_too_old(fam_dict, indi_dict), {"F1": ["F", "I2", "Cecily", "1 JUN 1980", "I3", "Tom", "1 MAR 2010"]})

        i4 = individualPerson('I4')
        i4.sex = "M"
        i4.uid = 'I4'
        i4.name = "John"
        i4.birt = '1 JAN 1940'
        indi_dict[i4.uid] = i4

        i5 = individualPerson('I5')
        i5.sex = "F"
        i5.uid = 'I5'
        i5.name = "Kyra"
        i5.birt = '1 JUN 1940'
        indi_dict[i5.uid] = i5

        i6 = individualPerson('I6')
        i6.uid = 'I6'
        i6.name = "Julia"
        i6.birt = '1 MAR 2010'
        indi_dict[i6.uid] = i6

        f2 = familyClass("F2")
        f2.husb_id = "I4"
        f2.wife_id = "I5"
        f2.chil = ["I6"]
        fam_dict[f2.fid] = f2

        self.assertEqual(check_parents_not_too_old(fam_dict, indi_dict), {"F2": ["F", "I5", "Kyra", "1 JUN 1940", "I6", "Julia", "1 MAR 2010"]})
        self.assertNotEqual(check_parents_not_too_old(fam_dict, indi_dict), {})

        i7 = individualPerson('I7')
        i7.sex = "M"
        i7.uid = 'I7'
        i7.name = "Ryan"
        i7.birt = '1 JAN 1929'
        indi_dict[i7.uid] = i7

        i8 = individualPerson('I8')
        i8.sex = "F"
        i8.uid = 'I8'
        i8.name = "Amanda"
        i8.birt = '1 JUN 1960'
        indi_dict[i8.uid] = i8

        i9 = individualPerson('I9')
        i9.uid = 'I9'
        i9.name = "Kevin"
        i9.birt = '1 JUN 2010'
        indi_dict[i9.uid] = i9

        f3 = familyClass("F3")
        f3.husb_id = "I7"
        f3.wife_id = "I8"
        f3.chil = ["I9"]
        fam_dict[f3.fid] = f3

        self.assertEqual(check_parents_not_too_old(fam_dict, indi_dict), {"F2": ["F", "I5", "Kyra", "1 JUN 1940", "I6", "Julia", "1 MAR 2010"], 
                                                                          "F3": ["M", "I7", "Ryan", "1 JAN 1929", "I9", "Kevin", "1 JUN 2010"]})
        self.assertNotEqual(check_parents_not_too_old(fam_dict, indi_dict), {})

    def test_check_multiple_births(self):
        """ Unit tests for US14 Multiple Births <= 5 - No more than five siblings should be born
    at the same time """

        indi_dict = {}
        fam_dict = {}

        i1 = individualPerson('I1')
        i1.uid = 'I1'
        i1.birt = '1 JAN 1980'
        indi_dict[i1.uid] = i1

        i2 = individualPerson('I2')
        i2.uid = 'I2'
        i2.birt = '1 JAN 1980'
        indi_dict[i2.uid] = i2

        i3 = individualPerson('I3')
        i3.uid = 'I3'
        i3.birt = '1 JAN 1980'
        indi_dict[i3.uid] = i3

        i4 = individualPerson('I4')
        i4.uid = 'I4'
        i4.birt = '1 JAN 1980'
        indi_dict[i4.uid] = i4

        i5 = individualPerson('I5')
        i5.uid = 'I5'
        i5.birt = '1 JAN 1980'
        indi_dict[i5.uid] = i5

        i6 = individualPerson('I6')
        i6.uid = 'I6'
        i6.birt = '1 JAN 1980'
        indi_dict[i6.uid] = i6

        f1 = familyClass("F1")
        f1.chil = ["I1", "I2", "I3", "I4", "I5", "I6"]
        fam_dict[f1.fid] = f1

        self.assertEqual(check_multiple_births(fam_dict, indi_dict), {"F1": ["I1", "I2", "I3", "I4", "I5", "I6"]})
        self.assertNotEqual(check_multiple_births(fam_dict, indi_dict), {})

        i7 = individualPerson('I7')
        i7.uid = 'I7'
        i7.birt = '1 JAN 1980'
        indi_dict[i7.uid] = i7

        i8 = individualPerson('I8')
        i8.uid = 'I8'
        i8.birt = '1 JAN 1980'
        indi_dict[i8.uid] = i8

        i9 = individualPerson('I9')
        i9.uid = 'I9'
        i9.birt = '1 JAN 1980'
        indi_dict[i9.uid] = i9

        i10 = individualPerson('I10')
        i10.uid = 'I10'
        i10.birt = '1 JAN 1980'
        indi_dict[i10.uid] = i10

        i11 = individualPerson('I11')
        i11.uid = 'I11'
        i11.birt = '1 JAN 1980'
        indi_dict[i11.uid] = i11

        i12 = individualPerson('I12')
        i12.uid = 'I12'
        i12.birt = '1 JAN 1985'
        indi_dict[i12.uid] = i12

        f2 = familyClass("F2")
        f2.chil = ["I7", "I8", "I9", "I10", "I11", "I12"]
        fam_dict[f2.fid] = f2

        self.assertEqual(check_multiple_births(fam_dict, indi_dict), {"F1": ["I1", "I2", "I3", "I4", "I5", "I6"]})
        self.assertNotEqual(check_multiple_births(fam_dict, indi_dict), {"F1": ["I1", "I2", "I3", "I4", "I5", "I6"],
                                                                         "F2": ["I7", "I8", "I9", "I10", "I11", "I12"]})
        self.assertNotEqual(check_multiple_births(fam_dict, indi_dict), {})

    def test_marriage_after_14(self):
        indi_dict = {}
        fam_dict = {}
        indi_I1 = individualPerson("I1")
        indi_I1.birt = "12 JUL 1991"
        indi_dict[indi_I1.uid] = indi_I1
        indi_I2 = individualPerson("I2")
        indi_I2.birt = "9 JAN 1988"
        indi_dict[indi_I2.uid] = indi_I2

        fam1 = familyClass("F1")
        fam1.husb_id = "I2"
        fam1.wife_id = "I1"
        fam1.marr = "1 FEB 1995"
        fam_dict[fam1.fid] = fam1       

        self.assertFalse(marriage_after_14(fam_dict, indi_dict))

    def test_validate_childBirth_with_parentsDeath(self):
        """Test cases for US09 -- Child should be born before death of mother and before nine months after death of father"""
        indi_dict = {}
        fam_dict = {}

        indi_I10 = individualPerson("I10")
        indi_I10.birt = "25 AUG 1990"
        indi_dict[indi_I10.uid] = indi_I10
        indi_I11 = individualPerson("I11")
        indi_I11.birt = "13 MAR 1960"
        indi_I11.deat = "19 JUL 1990"
        indi_dict[indi_I11.uid] = indi_I11
        indi_I12 = individualPerson("I12")
        indi_I12.birt = "16 DEC 1959"
        indi_dict[indi_I12.uid] = indi_I12

        fam_F10 = familyClass("F10")
        fam_F10.marr = "11 OCT 1988"
        fam_F10.chil = ["I10"]
        fam_F10.husb_id = "I12"
        fam_F10.wife_id = "I11"
        fam_dict[fam_F10.fid] = fam_F10

        self.assertEqual(validate_childBirth_with_parentsDeath(indi_dict, fam_dict), ({'F10': ['I10', 'I11']}, {}))
        self.assertNotEqual(validate_childBirth_with_parentsDeath(indi_dict, fam_dict), {'F1':'I5'})
        self.assertIsNotNone(validate_childBirth_with_parentsDeath(indi_dict, fam_dict))
        self.assertIsNot(validate_childBirth_with_parentsDeath(indi_dict, fam_dict), {'F1':'I5'})
        self.assertCountEqual(validate_childBirth_with_parentsDeath(indi_dict, fam_dict), ({'F10': ['I10', 'I11']}, {}))

        indi_dict = {}
        fam_dict = {}

        indi_I1 = individualPerson("I1")
        indi_I1.birt = "25 AUG 1990"
        indi_dict[indi_I1.uid] = indi_I1
        indi_I2 = individualPerson("I2")
        indi_I2.birt = "13 MAR 1960"
        indi_dict[indi_I2.uid] = indi_I2
        indi_I3 = individualPerson("I3")
        indi_I3.birt = "16 DEC 1959"
        indi_I3.deat = "13 OCT 1989"
        indi_dict[indi_I3.uid] = indi_I3

        fam_F1 = familyClass("F1")
        fam_F1.marr = "11 OCT 1988"
        fam_F1.chil = ["I1"]
        fam_F1.husb_id = "I3"
        fam_F1.wife_id = "I2"
        fam_dict[fam_F1.fid] = fam_F1

        self.assertEqual(validate_childBirth_with_parentsDeath(indi_dict, fam_dict), ({}, {'F1': ['I1', 'I3']}))
        self.assertNotEqual(validate_childBirth_with_parentsDeath(indi_dict, fam_dict), {'F1':'I5'})
        self.assertIsNotNone(validate_childBirth_with_parentsDeath(indi_dict, fam_dict))
        self.assertIsNot(validate_childBirth_with_parentsDeath(indi_dict, fam_dict), {'F1':'I5'})
        self.assertCountEqual(validate_childBirth_with_parentsDeath(indi_dict, fam_dict), ({}, {'F1': ['I1', 'I3']}))

        indi_dict = {}
        fam_dict = {}

        indi_I1 = individualPerson("I1")
        indi_I1.birt = "25 AUG 1990"
        indi_dict[indi_I1.uid] = indi_I1
        indi_I2 = individualPerson("I2")
        indi_I2.birt = "13 MAR 1960"
        indi_dict[indi_I2.uid] = indi_I2
        indi_I3 = individualPerson("I3")
        indi_I3.birt = "16 DEC 1959"
        indi_I3.deat = "13 OCT 1995"
        indi_dict[indi_I3.uid] = indi_I3

        fam_F1 = familyClass("F1")
        fam_F1.marr = "11 OCT 1988"
        fam_F1.chil = ["I1"]
        fam_F1.husb_id = "I3"
        fam_F1.wife_id = "I2"
        fam_dict[fam_F1.fid] = fam_F1

        self.assertEqual(validate_childBirth_with_parentsDeath(indi_dict, fam_dict), ({}, {}))
        self.assertNotEqual(validate_childBirth_with_parentsDeath(indi_dict, fam_dict), {'F1':'I5'})
        self.assertIsNotNone(validate_childBirth_with_parentsDeath(indi_dict, fam_dict))
        self.assertIsNot(validate_childBirth_with_parentsDeath(indi_dict, fam_dict), {'F1':'I5'})
        self.assertCountEqual(validate_childBirth_with_parentsDeath(indi_dict, fam_dict), ({}, {}))
        
if __name__ == '__main__':
    unittest.main(exit=False,verbosity=2)
