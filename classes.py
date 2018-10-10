from datetime import datetime
from helperFunctions_Sprint1 import validate_date_format, change_date_format

""" This file has 2 classes for the parser
1 for individuals and 1 for families """

class individualPerson(object):
    """ This class creates an instance of an individual using all the details
    like name, bithdate, sex, death date, etc. Also includes a method to return
    the details in a list for a prettytable. """
    def __init__(self, uid):
        self.uid = uid  #unique id of individual person
        self.name = "NA" # name of individual person
        self.birt = "NA" # Date of birthday of individual person
        self.sex = "NA" # sex of individual person
        self.deat = "NA" # Date of death of individual person
        self.alive = True # person alive or dead
        self.age = 0
        self.famc = [] # family id where individual is a child
        self.fams = [] # family id where individual is parent

    def is_alive(self):
        """Returns if the person is alive as True or False if not """
        return self.alive

    def get_age(self):
        """US27 - Individual Age. Returns the age of the individual"""
        if validate_date_format(self.birt):
            birth_year, birth_month, birth_day = change_date_format(self.birt).split('-')

            if self.alive:
                provided_date = datetime.today().date()
                age = (provided_date.year - int(birth_year) - ((datetime.today().month, datetime.today().day) < (int(birth_month), int(birth_day))))
            else:
                death_year, death_month, death_day = change_date_format(self.deat).split('-')
                age = (int(death_year) - int(birth_year) - ((int(death_month), int(death_day)) < (int(birth_month), int(birth_day))))

        return age

    def set_birthdate(self, date):
        """Sets the birthdate for an individual, it call valid_date_format from helperFunctions to ensure birthday is in right format"""

        if validate_date_format(self.birt):
            self.birt = date
        else:
            raise ValueError('Invalid date!')


    def pt_row(self):
        if len(self.famc) == 0:
            self.famc = 'NA'
        if len(self.fams) == 0:
            self.fams = 'NA'
        return [self.uid, self.name, self.sex, self.birt, self.age, self.alive, self.deat, self.famc, self.fams]


class familyClass(object):
    """ This class stores information about each famiy using unique ID
    for particular family. Information includes married date, husband ID,
    husband name, wife ID, wife name, list of children, and optional
    divorced date. Also includes a method to return the details in a list 
    for a prettytable. """
    def __init__(self, fid):
        self.fid = fid
        self.marr = "NA"  # marriage event for family
        self.husb_id = "NA" #husband's id
        self.husb = "NA"  # for husband in family
        self.wife_id = "NA" #wife's id
        self.wife = "NA"  # for wife in family
        self.chil = []  # for child in family
        self.div = "NA"  # divorce event in family

    def pt_row(self):
        if len(self.chil) == 0:
            self.chil = 'NA'
        return [self.fid, self.marr, self.div, self.husb_id, self.husb, self.wife_id, self.wife, self.chil]
