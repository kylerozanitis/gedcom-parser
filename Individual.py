class individual(object):

    def __init__(self, uid,name,birthday,sex):
        self.uid = uid  #umoque id of individual person
        self.name = name # name of individual person
        self.birthday = birthday # Date of birthday of individual person
        self.sex = sex # sex of individual person
        self.deathDate = None # Date of death of individual person
        self.alive = True # person alive or dead
        self.famc = [] # family id where individual is a child
        self.fams = [] # family id where individual is parent

