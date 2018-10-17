from helperFunctions_Sprint1 import validate_date_format, change_date_format, check_two_dates
from helperFunctions_Sprint1 import convert_str_to_date, print_both
from collections import Counter

def single_over_30(family_data, individual_data):
    """ US31 - List all single over 30
    This function will take family data and individual data as input
    and list all the singles over 30 from the gedcom file and return the list
    """
    check_status = []
    single = []
    for family in family_data.values():
        husband = family.husb_id
        wife = family.wife_id
        check_status.append(husband)
        check_status.append(wife)
    for individual in individual_data.values():
        person = individual.uid
        age = individual.age
        if person not in check_status:
            if age > 30:
                single.append(individual)
    return single

def multiple_births(family_data, individual_data):
    """
    US32 - List multiple births
    This function will take family data and individual data as input
    and list all the children who are born on same day from one family.
    """
    multiple_births = []

    for family in family_data.values():
        children = family.chil
        #print('child:',children)
        siblings = []
        for individual in individual_data.values():
            if individual.uid in children:
                siblings.append(individual)
        #print(len(siblings))
        #print(siblings)
        siblings_birth = []
        for s in siblings:
            siblings_birth.append(s.birt)
        #print('birth',siblings_birth)
        
                