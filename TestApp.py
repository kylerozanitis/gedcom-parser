import unittest

from helperFunctions import change_date_format, validate_date_format, deceased_list,agemorethan_150
from helperFunctions import check_marriage_before_divorce, check_marriage_before_death, check_spouses_exist, check_two_dates
from helperFunctions import death_before_birth, birth_before_marriage, divorce_before_death, allDates_before_currentDate
from helperFunctions import list_recent_births,list_recent_death, fewer_than15_siblings, check_unique_ids
from classes import individualPerson, familyClass


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
        """Unit test for Validating date format function"""

        self.assertEqual(validate_date_format('7 MAY 2018'),True, True)
        self.assertNotEqual(validate_date_format('8/FEB/2018'), True, False)
        self.assertNotEqual(validate_date_format('8/FEB/18'), True, False)

    def test_change_date_format(self):
        """Unit test for change date function"""

        self.assertEqual(change_date_format('7 MAY 2018'), '2018-05-7', True)
        self.assertNotEqual(change_date_format('7 MAY 2018'), '2018/05/7', True)
        self.assertNotEqual(change_date_format('7 MAY 2018'), '2018/05/07', True)

    def test_check_spouses_exist(self):
        """ Unit test for checking that both spouses exist """

        fam_dict = {}

        family = familyClass("F1")
        family.husb_id = "I1"
        family.wife_id = "I2"
        fam_dict[family.fid] = family

        value = check_spouses_exist(fam_dict)
        self.assertEqual(len(value), 1)
        self.assertEqual(list(value.keys()), ["F1"])

        family2 = familyClass("F2")
        family2.husb_id = "I3"
        family2.wife_id = "NA"
        fam_dict[family2.fid] = family2

        self.assertEqual(list(fam_dict.keys()), ["F1", "F2"])

        check_spouses_exist(fam_dict)
        self.assertEqual(len(fam_dict), 1)
        self.assertEqual(list(fam_dict.keys()), ["F1"])

        family3 = familyClass("F3")
        family3.husb_id = "NA"
        family3.wife_id = "I6"
        fam_dict[family3.fid] = family3

        self.assertEqual(list(fam_dict.keys()), ["F1", "F3"])

        check_spouses_exist(fam_dict)
        self.assertEqual(len(fam_dict), 1)
        self.assertEqual(list(fam_dict.keys()), ["F1"])

    def test_deceased_list(self):
        """Unit test to validate return of list of deceased people"""

        ind_dict = dict()

        individual = individualPerson('I123')
        individual.alive = False
        ind_dict[individual.uid] = individual

        individual2 = individualPerson('I456')
        ind_dict[individual2.uid] = individual2

        self.assertEqual(len(deceased_list(ind_dict)), 1, True)

        individual3 = individualPerson('I789')
        ind_dict[individual3.uid] = individual3
        individual3.alive = False
        self.assertEqual(len(deceased_list(ind_dict)), 2, True)

        individual4 = individualPerson('I987')
        ind_dict[individual4.uid] = individual4
        individual4.alive = True
        self.assertEqual(len(deceased_list(ind_dict)), 2, True)

        individual5 = individualPerson('I744')
        ind_dict[individual5.uid] = individual5
        individual5.alive = False
        self.assertEqual(len(deceased_list(ind_dict)), 3, True)

    def test_agemorethan150(self):
        """Unit test to validate if the person is more than 150 yrs old"""

        person1_dob = '17 AUG 1954'
        person1_age = 64
        person1_isalive = True
        self.assertTrue(agemorethan_150(person1_isalive,person1_dob,person1_age))

        person2_dob = '23 SEP 1921'
        person2_age = 152
        person2_isalive = False
        self.assertFalse(agemorethan_150(person2_isalive,person2_dob,person2_age))

        person3_dob = '23 SEP 2018'
        person3_age = 0
        person3_status = True
        result = str(agemorethan_150(person3_status,person3_dob,person3_age))
        self.assertEqual(result,'True')

        person4_dob = '01 JAN 1688'
        person4_age = 330
        person4_isalive = False
        result4 = str(agemorethan_150(person4_isalive,person4_dob,person4_age))
        self.assertNotEqual(result4,'True')

        person5_dob = '01 JAN 1988'
        person5_age = 30
        person5_isalive = False
        result5 = str(agemorethan_150(person5_isalive,person5_dob,person5_age))
        self.assertIs(result5,'True')

    def test_check_marriage_before_divorce(self):
        """ Unit test for checking that marriage occured before divorce """
        
        fam_dict = {}

        family = familyClass("F1")
        family.marr = "1 JAN 2000"
        family.div = "1 JAN 2005"
        fam_dict[family.fid] = family

        self.assertNotEqual(len(check_marriage_before_divorce(fam_dict)), 1, True)

        family2 = familyClass("F2")
        family2.marr = "1 JAN 2005"
        family2.div = "1 JAN 2000"
        fam_dict[family2.fid] = family2

        self.assertEqual(len(check_marriage_before_divorce(fam_dict)), 1, True)
        self.assertEqual(check_marriage_before_divorce(fam_dict), ["F2"], True)

        family3 = familyClass("F3")
        family3.marr = "1 JAN 2000"
        family3.div = "1 JAN 2000"
        fam_dict[family3.fid] = family3

        self.assertEqual(len(check_marriage_before_divorce(fam_dict)), 1, True)
        self.assertEqual(check_marriage_before_divorce(fam_dict), ["F2"], True)

        family4 = familyClass("F4")
        family4.marr = "1 JAN 2000"
        family4.div = "NA"
        fam_dict[family4.fid] = family4

        self.assertEqual(len(check_marriage_before_divorce(fam_dict)), 1, True)
        self.assertEqual(check_marriage_before_divorce(fam_dict), ["F2"], True)

        family5 = familyClass("F5")
        family5.marr = "1 DEC 2000"
        family5.div = "30 NOV 2000"
        fam_dict[family5.fid] = family5

        self.assertEqual(len(check_marriage_before_divorce(fam_dict)), 2, True)
        self.assertEqual(check_marriage_before_divorce(fam_dict), ["F2", "F5"], True)

        family6 = familyClass("F6")
        family6.marr = "NA"
        family6.div = "1 JAN 2020"
        fam_dict[family6.fid] = family6

        self.assertEqual(len(check_marriage_before_divorce(fam_dict)), 3, True)
        self.assertEqual(check_marriage_before_divorce(fam_dict), ["F2", "F5", "F6"], True)

    def test_check_marriage_before_death(self):
        """ Unit test for checking that marriage occured before death of
        either spouse """

        fam_dict = {}
        ind_dict = {}

        individual = individualPerson("I1")
        individual.uid = "I1"
        individual.is_alive = True
        individual.deat = "NA"
        ind_dict[individual.uid] = individual

        individual2 = individualPerson("I2")
        individual2.uid = "I2"
        individual2.is_alive = False
        individual2.deat = "1 JAN 2010"
        ind_dict[individual2.uid] = individual2

        family = familyClass("F1")
        family.husb_id = "I1"
        family.wife_id = "I2"
        family.marr = "1 JAN 2000"
        fam_dict[family.fid] = family

        self.assertEqual(len(check_marriage_before_death(fam_dict, ind_dict)), 0, True)
        self.assertEqual(check_marriage_before_death(fam_dict, ind_dict), [], True)

        individual3 = individualPerson("I3")
        individual3.uid = "I3"
        individual3.is_alive = True
        individual3.deat = "NA"
        ind_dict[individual3.uid] = individual3

        individual4 = individualPerson("I4")
        individual4.uid = "I4"
        individual4.is_alive = False
        individual4.deat = "1 JAN 1999"
        ind_dict[individual4.uid] = individual4

        family2 = familyClass("F2")
        family2.husb_id = "I3"
        family2.wife_id = "I4"
        family2.marr = "1 JAN 2000"
        fam_dict[family2.fid] = family2

        self.assertEqual(len(check_marriage_before_death(fam_dict, ind_dict)), 1, True)
        self.assertEqual(check_marriage_before_death(fam_dict, ind_dict), ["F2"], True)

        individual5 = individualPerson("I5")
        individual5.uid = "I5"
        individual5.is_alive = True
        individual5.deat = "NA"
        ind_dict[individual5.uid] = individual5

        individual6 = individualPerson("I6")
        individual6.uid = "I6"
        individual6.is_alive = False
        individual6.deat = "1 JAN 1999"
        ind_dict[individual6.uid] = individual6

        family3 = familyClass("F3")
        family3.husb_id = "I6"
        family3.wife_id = "I5"
        family3.marr = "1 JAN 2000"
        fam_dict[family3.fid] = family3

        self.assertEqual(len(check_marriage_before_death(fam_dict, ind_dict)), 2, True)
        self.assertEqual(check_marriage_before_death(fam_dict, ind_dict), ["F2", "F3"], True)
        
    def test_divorce_brfore_death(self):
        family_dict = {}
        individual_dict = {}

        family1 = familyClass('F12')
        family1.div = '1 JAN 2009'
        family1.husb_id = 'I11'
        family1.wife_id = 'I10'
        family_dict[family1.fid] = family1
        indi1 = individualPerson('I11')
        indi1.alive = False
        indi1.deat = '2 MAR 2007'
        individual_dict[indi1.uid] = indi1
        indi2 = individualPerson('I10')
        indi2.alive = True
        indi2.deat = 'NA'
        individual_dict[indi2.uid] = indi2

        self.assertEqual(len(divorce_before_death(family_dict,individual_dict)), 1, True)
        self.assertEqual(divorce_before_death(family_dict,individual_dict), ["F12"], True)

    def test_birth_before_death(self):
        """ Unit test for US03 -- Birth should occur before death of an individual """
        indi_dict = {}
        fam_dict = {}

        indi_I7 = individualPerson("I7")
        indi_I7.birt = "1 JUL 2000"
        indi_I7.deat = "5 DEC 1995"
        indi_dict[indi_I7.uid] = indi_I7

        indi_I10 = individualPerson("I10")
        indi_I10.birt = "25 AUG 1980"
        indi_I10.deat = "13 MAR 1955"
        indi_dict[indi_I10.uid] = indi_I10
        
        indi_I12 = individualPerson("I12")
        indi_I12.birt = "25 AUG 1920"
        indi_I12.deat = "13 MAR 1955"
        indi_dict[indi_I12.uid] = indi_I12

        self.assertEqual(death_before_birth(indi_dict, fam_dict), ({'I7':['death before birth'], 'I10':['death before birth']}))
        self.assertNotEqual(death_before_birth(indi_dict, fam_dict), ({'I1':['death before birth'], 'I6':['death before birth']}))
        self.assertIsNotNone(death_before_birth(indi_dict, fam_dict))
        self.assertIsNot(death_before_birth(indi_dict, fam_dict), "")
        self.assertCountEqual(death_before_birth(indi_dict, fam_dict), ({'I7':['death before birth'], 'I10':['death before birth']}))
        
    def test_dates_before_currentDate(self):
        """ Unit test for US01 -- Dates (birth, marriage, divorce, death) should not be after the current date """ 

        indi_dict = {}
        fam_dict = {}

        indi_I7 = individualPerson("I7")
        indi_I7.birt = "1 JUL 2019"
        indi_I7.deat = "22 JUL 2060"
        indi_dict[indi_I7.uid] = indi_I7
        fam_F7 = familyClass("F7")
        fam_F7.marr = "5 DEC 2050"
        fam_dict[fam_F7.fid] = fam_F7

        indi_I10 = individualPerson("I10")
        indi_I10.birt = "25 AUG 2030"
        indi_dict[indi_I10.uid] = indi_I10
        fam_F10 = familyClass("F10")
        fam_F10.marr = "11 OCT 2064"
        fam_F10.div = "13 MAR 2065"
        fam_dict[fam_F10.fid] = fam_F10
        
        indi_I12 = individualPerson("I12")
        indi_I12.birt = "25 AUG 1920"
        indi_I12.deat = "13 MAR 1955"
        indi_dict[indi_I12.uid] = indi_I12
        fam_F12 = familyClass("F12")
        fam_F12.marr = "3 MAR 1950"
        fam_F12.div = "27 NOV 1954"
        fam_dict[fam_F12.fid] = fam_F12

        output = {'I7':['birth', 'death'], 'I10':['birth'], 'F7':['marriage'], 'F10':['marriage', 'divorce']}

        self.assertEqual(allDates_before_currentDate(indi_dict, fam_dict), (output))
        self.assertNotEqual(allDates_before_currentDate(indi_dict, fam_dict), ({'I1':['death before birth'], 'I6':['death before birth']}))
        self.assertIsNotNone(allDates_before_currentDate(indi_dict, fam_dict))
        self.assertIsNot(allDates_before_currentDate(indi_dict, fam_dict), "")
        self.assertCountEqual(allDates_before_currentDate(indi_dict, fam_dict), (output))    
        
    def test_check_two_dates(self):
        """ Unit testing events before another happened """

        birth = "25 AUG 1920"
        death = "13 MAR 1955"
        marriage = "21 APR 1999"

        self.assertTrue(check_two_dates(birth, death), True)
        self.assertFalse(check_two_dates(marriage, death), True)
        self.assertFalse(check_two_dates(marriage, birth), True)


    def test_birth_before_marriage(self):
        """ Unit testing to check birth before marriages """
        fam_dict = {}
        ind_dict = {}

        individual = individualPerson("I1")
        individual.uid = "I1"
        individual.is_alive = True
        individual.birt = "1 JAN 2001"
        ind_dict[individual.uid] = individual

        individual2 = individualPerson("I2")
        individual2.uid = "I2"
        individual2.is_alive = True
        individual2.birt = "1 JAN 2010"
        ind_dict[individual2.uid] = individual2

        family = familyClass("F1")
        family.husb_id = "I1"
        family.wife_id = "I2"
        family.marr = "1 JAN 2000"
        fam_dict[family.fid] = family

        self.assertEqual(len(birth_before_marriage(fam_dict, ind_dict)), 0, True)

        individual = individualPerson("I3")
        individual.uid = "I3"
        individual.is_alive = True
        individual.birt = "20 OCT 1990"
        ind_dict[individual.uid] = individual

        individual2 = individualPerson("I4")
        individual2.uid = "I4"
        individual2.is_alive = True
        individual2.birt = "1 JAN 1991"
        ind_dict[individual2.uid] = individual2

        family = familyClass("F2")
        family.husb_id = "I3"
        family.wife_id = "I4"
        family.marr = "1 JAN 2000"
        fam_dict[family.fid] = family

        self.assertEqual(len(birth_before_marriage(fam_dict, ind_dict)), 1, True)

    def test_recent_deaths(self):
        """ Unit Test for Checking recent deaths """
        indi_dict = {}
        recent_death = []
        i1 = individualPerson('I1')
        i1.uid = 'I1'
        i1.deat = '29 SEP 2018'
        indi_dict[i1.uid] = i1

        i2 = individualPerson('I2')
        i2.udi = 'I2'
        i2.deat = '15 AUG 2018'
        indi_dict[i2.uid] = i2

        self.assertEqual(len(list_recent_death(indi_dict)),1,True)

    def test_recent_births(self):
        """ Unit Test for Checking recent births """
        indi_dict = {}
        recent_death = []
        i1 = individualPerson('I11')
        i1.uid = 'I11'
        i1.birt = '29 SEP 2017'
        indi_dict[i1.uid] = i1

        i2 = individualPerson('I12')
        i2.udi = 'I12'
        i2.birt = '15 AUG 2018'
        indi_dict[i2.uid] = i2

        i3 = individualPerson('I13')
        i3.udi = 'I13'
        i3.birt = '30 SEP 2018'
        indi_dict[i3.uid] = i3

        self.assertEqual(len(list_recent_births(indi_dict)),1,True)

    def test_fewer_than15_siblings(self):
        "Test cases -- US15 -- There should be fewer than 15 siblings in a family"
        fam_dict = dict()
        family = familyClass("F2")
        family.chil = ['i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8', 'i9', 'i10', 'i11', 'i12', 'i13', 'i14', 'i15', 'i16']
        fam_dict[family.fid] = family
        self.assertEqual(fewer_than15_siblings(fam_dict), ['F2'])

        fam_dict = dict()
        family = familyClass("F1")
        family.chil = ['i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8', 'i9', 'i10', 'i11', 'i12', 'i13', 'i14', 'i15']
        fam_dict[family.fid] = family
        self.assertEqual(fewer_than15_siblings(fam_dict), [])

        fam_dict = dict()
        family = familyClass("F3")
        family.chil = []
        fam_dict[family.fid] = family
        self.assertEqual(fewer_than15_siblings(fam_dict), [])

    def test_check_unique_ids(self):
        """ Test cases for US22 - Unique IDs - All individual IDs should be
        unique and all family IDs should be unique. """
        indi_dict = {}
        fam_dict = {}

        i1 = individualPerson('I1')
        indi_dict[i1.uid] = i1

        i2 = individualPerson('I2')
        indi_dict[i2.uid] = i2

        family = familyClass("F1")
        fam_dict[family.fid] = family

        family2 = familyClass("F2")
        fam_dict[family2.fid] = family2

        self.assertEqual(check_unique_ids(indi_dict, fam_dict), ([], []))
        self.assertNotEqual(check_unique_ids(indi_dict, fam_dict), (["I2"], ["F2"]))
        self.assertIsNotNone(check_unique_ids(indi_dict, fam_dict))
        self.assertIsNot(check_unique_ids(indi_dict, fam_dict), (["I2"], ["F2"]))

    
if __name__ == '__main__':
    unittest.main(exit=False,verbosity=2)
