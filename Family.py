# class for families
class family(object):

    def __init__(self, uid):
        self.uid = uid
        self.marriage = None  # marriage event for family
        self.husband = None # for husband in family
        self.husbandName = None # name of husband
        self.wife = ''  # for wife in family
        self.wifeName = None # for name of the wife
        self.children = []  # for child in family
        self.divorce = None  # divorce event in family