""" This file takes contains classes for the Individual and Family. """


class individualPerson(object):
    """ This class uses the user's ID (UID), name, birthday, and sex to create
    an instance of an individual. """
    def __init__(self, uid):
        self.uid = uid  #umoque id of individual person
        self.name = "NA" # name of individual person
        self.birt = "NA" # Date of birthday of individual person
        self.sex = "NA" # sex of individual person
        self.deat = "NA" # Date of death of individual person
        self.alive = True # person alive or dead
        self.famc = [] # family id where individual is a child
        self.fams = [] # family id where individual is parent


class familyClass(object):
    """ This class uses the family's ID (FID) to store information about a
    particular family. """
    def __init__(self, fid):
        self.fid = fid
        self.marr = 'NA'  # marriage event for family
        self.husb = 'NA'  # for husband in family
        self.husbandName = 'NA' # name of husband
        self.wife = ''  # for wife in family
        self.wifeName = None # for name of the wife
        self.children = []  # for child in family
        self.div = None  # divorce event in family