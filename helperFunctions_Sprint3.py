""" This file includes the functions that were implemented in sprint 23 """

# Lib Imports
from helperFunctions_Sprint1 import validate_date_format, change_date_format, check_two_dates
from helperFunctions_Sprint1 import convert_str_to_date, print_both
import datetime

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

def validate_unique_name_birthdate(individual_data):
    # US23 --- No more than one individual with the same name and birth date should appear in a GEDCOM file

    all_names_birthdate_dict = dict()
    uniq_all_names_birthdate_dict = dict()
    rep_all_names_birthdate_dict = dict()
    error_entries = []
    
    for uid, individual in individual_data.items():
        temp = []
        temp.append(individual.name)
        temp.append(change_date_format(individual.birt))
        all_names_birthdate_dict[uid] = temp
    
    for uid, each_indi in all_names_birthdate_dict.items():
        if each_indi not in uniq_all_names_birthdate_dict.values():
            uniq_all_names_birthdate_dict[uid] = each_indi
        else:
            rep_all_names_birthdate_dict[uid] = each_indi

    dup_eliminator = []
    for each_indi in rep_all_names_birthdate_dict.values():
        temp = []
        if each_indi not in dup_eliminator:
            dup_eliminator.append(each_indi)
            for uid, individual in individual_data.items():
                if each_indi[0] == individual.name and each_indi[1] == change_date_format(individual.birt):
                    temp.append(uid)
            temp.append(each_indi[0])
            temp.append(each_indi[1])
            error_entries.append(temp)
        else:
            continue

    return error_entries


def get_spouse(family_data, fam_id, ind_id):
    """Helper function to get the spouse from family_data it takes family dictionary, family id and individual id"""

    person = family_data.get(fam_id, "NA")

    if person == "NA":
        return None

    if person.husb_id == ind_id:
        return person.wife_id
    else:
        return person.husb_id


def get_children(family_data, fam_id):
    """Helper function to get the Children from family_data it takes family dictionary, family id"""

    children = family_data.get(fam_id, "NA")

    if children == "NA":
        return None

    return children.chil


def siblings_should_not_marry(family_data,  individual_data):
    """ US18 - Siblings should not marry
        This function will take family data and individual data as input
        and returns a list of siblings that are married to each other. """

    trouble_siblings = []

    for ind in individual_data.values():
        for fam in ind.fams:
            spouse = get_spouse(family_data, fam, ind.uid)
            children = get_children(family_data, fam)
            if spouse is not None and spouse in children:
                trouble_siblings.append(ind)

    return trouble_siblings


def reject_illegal_dates(date):
    """ US42 - reject illegal dates, takes a date in format day/mm/year or 2/19/2018 """

    month, day, year = date.split('/')
    try:
        if datetime.datetime(int(year), int(month), int(day)):
            return True
    except ValueError:
        return False


def correct_gender_for_role(family_data, individual_data):
    """ US21 - Husband in family should be male and wife in family should be female """

    problem_families = {} # key = family id, value = list of reported gender, expected gender, and person id

    for family in family_data.values():
        husband = individual_data[family.husb_id]
        wife = individual_data[family.wife_id]

        if husband.sex == "F" or husband.sex == "NA":
            problem_families[family.fid] = [husband.sex, "M", husband.uid]
        elif wife.sex == "M" or wife.sex == "NA":
            problem_families[family.fid] = [wife.sex, "F", wife.uid]

    return problem_families