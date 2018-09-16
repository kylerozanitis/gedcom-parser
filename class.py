class individualPerson(object):

    def __init__(self, uid,name,birthday,sex):
        self.uid = uid  #umoque id of individual person
        self.name = name # name of individual person
        self.birthday = birthday # Date of birthday of individual person
        self.sex = sex # sex of individual person
        self.deathDate = 'NA' # Date of death of individual person
        self.alive = True # person alive or dead
        self.famc = [] # family id where individual is a child
        self.fams = [] # family id where individual is parent

# class for families
class familyClass(object):

    def __init__(self, uid):
        self.uid = uid
        self.marriage = 'NA'  # marriage event for family
        self.husband = 'NA'  # for husband in family
        self.husbandName = 'NA' # name of husband
        self.wife = ''  # for wife in family
        self.wifeName = None # for name of the wife
        self.children = []  # for child in family
        self.divorce = None  # divorce event in family