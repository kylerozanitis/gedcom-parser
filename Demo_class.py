""" This file takes contains classes for the Individual and Family. """

from datetime import datetime


class individualPerson(object):
    """ This class uses the user's ID (UID), name, birthday, and sex to create
    an instance of an individual. """
    def __init__(self, uid):
        self.uid = uid  #umoque id of individual person
        self.name = "NA" # name of individual person
        self.age = "NA"
        self.birt = "" # Date of birthday of individual person
        self.sex = "NA" # sex of individual person
        self.deat = "NA" # Date of death of individual person
        self.alive = True # person alive or dead
        self.famc = [] # family id where individual is a child
        self.fams = [] # family id where individual is parent

    def calculate_age(self,index,tagged_date):
        if index == 'Death':
            birt = datetime.strptime(self.birt,'%Y-%m-%d')
            provided_date = datetime.strptime(tagged_date, '%Y-%m-%d')
        else:
            birt = datetime.strptime(self.birt,'%Y-%m-%d')
            provided_date = datetime.today()
        age = provided_date - birt - ((provided_date.month, provided_date.day) < (birt.month, birt.day))
        self.age = age

    def pt_row(self):
       return [self.uid, self.name, self.sex, self.birt, self.age, self.alive, self.deat, self.famc, self.fams]


class familyClass(object):
    """ This class uses the family's ID (FID) to store information about a
    particular family. """
    def __init__(self, fid):
        self.fid = fid
        self.marr = "NA"  # marriage event for family
        self.husb_id = "NA"
        self.husb = "NA"  # for husband in family
        self.wife_id = "NA"
        self.wife = "NA"  # for wife in family
        self.chil = []  # for child in family
        self.div = None  # divorce event in family

    def pt_row(self):
       return [self.fid, self.div, self.marr, self.husb_id, self.husb, self.wife_id, self.wife, self.chil]