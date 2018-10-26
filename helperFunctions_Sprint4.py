""" This file includes the functions that were implemented in sprint 4 """

from helperFunctions_Sprint1 import convert_str_to_date, print_both
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