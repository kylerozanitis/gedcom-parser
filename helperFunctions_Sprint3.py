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


def siblings_should_not_marry(family_data,  individual_data):
    print("\n\n\nSibilings")
    trouble_siblings = []

    for ind in individual_data.values():
        for fam in ind.fams:
            if fam is not "N" and fam is not "A":
                if family_data.get(fam) is not None:
                    trouble_siblings.append(family_data.get(fam))
                    print(family_data.get(fam))



    for i in trouble_siblings:
        print("{} {} {} {}".format(i.fid, i.husb_id, i.wife_id, i.chil))


    # for fam in family_data.values():
    #     for child in fam.famc:
    #         if child is fam.husb_id or child is fam.wife_id:
    #             trouble_siblings.append(individual_data[child])

    return trouble_siblings
