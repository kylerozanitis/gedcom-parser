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
        self.famc = [] # family id where individual is a child
        self.fams = [] # family id where individual is parent

    def pt_row(self):
       return [self.uid, self.name, self.sex, self.birt, self.alive, self.deat, self.famc, self.fams]


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
       return [self.fid, self.marr, self.div, self.husb_id, self.husb, self.wife_id, self.wife, self.chil]
