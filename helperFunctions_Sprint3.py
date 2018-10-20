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
    birth_dict = {} #date key and count value
    count = 0
    bd = ''
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
        for s in siblings_birth:
            if s in birth_dict.keys():
                count += 1
            else:
                count = 1
            birth_dict[s] = count
        #print(birth_dict)
    for i,j in birth_dict.items():
        if j > 1:
            bd = i
        else:
            continue
        #print(bd)
        for family in family_data.values():
            children = family.chil
            for individual in individual_data.values():
                if individual.uid in children:
                    if individual.birt == bd:
                        multiple_births.append(individual)
    return multiple_births

def validate_male_lastname(individual_data, family_data):
    # US16 --- All male members of the family should have the same last name
    def firstname_lastname_list(name):
        names_list = name.split(" ")
        return names_list

    invaild_lastname_error = dict()
    fam_lastname = ""
    for fid, family in family_data.items():
        fam_lastname = firstname_lastname_list(family.husb)[1]
        if len(family.chil) > 0 and family.chil != 'NA':
            for child in family.chil:
                if individual_data[child].sex == 'M':
                    child_lastname = firstname_lastname_list(individual_data[child].name)[1]
                    if fam_lastname == child_lastname:
                        continue
                    else:
                        invaild_lastname_error[fid] = [fam_lastname, child, child_lastname]

    return invaild_lastname_error

            
