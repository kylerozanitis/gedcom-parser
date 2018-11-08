""" This file includes the functions that were implemented in sprint 4 """

from helperFunctions_Sprint1 import convert_str_to_date, print_both, check_two_dates
from helperFunctions_Sprint2 import is_anniversary_in_next_thirty_days
import datetime
from datetime import timedelta

def sibling_spacing(family_data, individual_data):
    """ US13 - siblings spacing
    This function will take family data and individual data as input
    and checks birthdates of siblings of one family should be more than 8 months apart or
    less than 2 days apart"""

    error_story = 'US13'
    flag = True
    for family in family_data.values():
        children = family.chil
        siblings = []
        for individual in individual_data.values():
            if individual.uid in children:
                siblings.append(individual)
        #print(siblings)
        siblings_birth = []
        for s in siblings:
            birth = convert_str_to_date(s.birt)
            siblings_birth.append(birth)
        #print(siblings_birth)
        siblings_birth = sorted(siblings_birth)
        #print('sorted',siblings_birth)
        i = 0
        count = len(siblings_birth)
        while i < count - 1:
            diff = siblings_birth[i+1] - siblings_birth[i]
            #print(diff)
            if(diff > timedelta(days=2) and diff < timedelta(days=243)):
                error_descrip="Birth dates of siblings should be less than 2 days apart or more than 8 months apart"
                error_location = family.fid
                print_both('ERROR: FAMILY:',error_story,':',str(error_location),':',error_descrip)
                flag = False
            i += 1
    return flag

def unique_families_by_spouses(family_data):
    """ US24 - No more than one family with the same spouses by name and the
    same marriage date should appear in a GEDCOM file """

    problem_families = []
    
    for f1 in family_data.values():
        family_id = f1.fid
        husband = f1.husb
        wife = f1.wife
        marriage_date = f1.marr

        for f2 in family_data.values():
            family2_id = f2.fid
            husband2 = f2.husb
            wife2 = f2.wife
            marriage_date2 = f2.marr

            if family_id != family2_id:
                if husband == husband2 and wife == wife2 and marriage_date == marriage_date2:
                    families_list = [family_id, family2_id]
                    if sorted(families_list) not in problem_families:
                        problem_families.append(sorted(families_list))
    
    return problem_families

def order_siblings_by_age(family_data, individual_data):
    """ US28 - List siblings in families by decreasing age """

    children_dict = dict() # key = family fid, value = list of list of ordered children & birthday

    for family in family_data.values():
        if family.chil != "NA":
            children_list = family.chil

            if len(children_list) > 1:
                ordered_list = []
                for i in children_list:
                    child1 = individual_data[i]
                    child1_birthday = child1.birt

                    if len(ordered_list) == 0:
                        ordered_list.append([child1.uid, child1_birthday])
                    else:
                        for j in ordered_list:
                            child2 = individual_data[j[0]]
                            child2_birthday = child2.birt
                            if check_two_dates(child1_birthday, child2_birthday) == False:
                                index = ordered_list.index(j)
                                ordered_list.insert(index, [child1.uid, child1_birthday])
                                break
                            else:
                                pass
                        else:
                            ordered_list.append([child1.uid, child1_birthday])

                reversed_list = ordered_list[::-1]
                children_dict[family.fid] = reversed_list

            elif len(children_list) == 1:
                for c in children_list:
                    child = individual_data[c]
                    child_birthday = child.birt
                    children_dict[family.fid] = [[child.uid, child_birthday]]
            else:
                children_dict[family.fid] = []

    return children_dict


def list_orphans(family_data, individual_data):
    """ US33 - List all orphans
    This function will take family data and individual data as input
    and list all the individuals whoes parents are dead and age is less than 18 years
    """

    orphans = []
    siblings = []
    for family in family_data.values():
        husb_id = family.husb_id
        wife_id = family.wife_id
        children = family.chil
        husband = None
        wife = None

        if len(family.chil) == 0:
            break
        
        for individual in individual_data.values():
            if individual.uid == husb_id:
                husband = individual
            if individual.uid == wife_id:
                wife = individual
        if husband.alive == False and wife.alive == False:
            siblings = []
            for individual in individual_data.values():
                if individual.uid in children:
                    siblings.append(individual)
            #print(siblings)
            for child in siblings:
                #print(child.age)
                if child.age < 18:
                    orphans.append(child)
    return orphans


def list_spouse_large_age_difference(family_data, individual_data):
    """US34 - List all couples who were married when the older spouse was more than twice as old as the younger spouse"""
    double_age_list = []

    for data in family_data.values():
        if data.div is not "NA" or data.div is not "":
            husb = individual_data.get(data.husb_id, "NA")
            wife = individual_data.get(data.wife_id, "NA")
            if husb.age > wife.age and (husb.age / 2) > wife.age:
                double_age_list.append(data)

            if wife.age > husb.age and (wife.age / 2) > husb.age:
                double_age_list.append(data)

        return double_age_list


def list_upcoming_anniversaries(family_data, individual_data):
    """US39 - List all living couples in a GEDCOM file whose marriage anniversaries occur in the next 30 days"""
    anniversaries = []
    for data in family_data.values():
        if data.div is not "NA" or data.div is not "":
            husb = individual_data.get(data.husb_id, "NA")
            wife = individual_data.get(data.wife_id, "NA")
            if (husb is not "NA" and husb.is_alive()) and (wife is not "NA" and wife.is_alive()):
                if (data.marr is not "NA") and is_anniversary_in_next_thirty_days(data.marr):
                    anniversaries.append(data)

    return anniversaries


