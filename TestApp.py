import unittest
from helperFunctions import change_date_format, validate_date_format, deceased_list,agemorethan_150, check_marriage_before_divorce
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

    def test_deceased_list(self):
        """Unit test to validate return of list of deceased people """

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

        person1_dob = '17 AUG 1954'
        person1_age = 64
        person1_isalive = True
        #status = agemorethan_150(person1_dob,person1_age)
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


if __name__ == '__main__':
    unittest.main()
