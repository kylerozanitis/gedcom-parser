""" This file includes the functions that were implemented in sprint 2 """

#Lib Imports
from dateutil.relativedelta import relativedelta
from helperFunctions_Sprint1 import validate_date_format, change_date_format, event_in_last_thirty_days, check_two_dates
from helperFunctions_Sprint1 import convert_str_to_date
from datetime import datetime, timedelta

def living_married_list(family_data,individual_data):
    """
    US 30 List living married. This function will take family data and individual data as input
    and list all the living married from the gedcom file and return the list
    """
    living_married = []
    for family in family_data.values():
        if family.marr != 'NA':
            husband = None
            wife = None
            for individual in individual_data.values():
                if individual.uid == family.husb_id:
                    husband = individual
                if individual.uid == family.wife_id:
                    wife = individual
            if husband.alive == True:
                living_married.append(husband)
            if wife.alive == True:
                living_married.append(wife)
    return living_married

def is_anniversary_in_next_thirty_days(date):
    """ Check for a date to see if happening within the next 30 days
        must pass a date in the format of yyyy-mm-dd
        Function returns: True or False
    """
    if validate_date_format(date):
        new_date = change_date_format(date)
        values = new_date.split('-')

        val = ((datetime.now().year - int(values[0])) + int(values[0]))
        compare_date = "{0}-{1}-{2}".format(str(val), values[1], values[2])

    if str(datetime.now().date()) <= compare_date < str(datetime.now().date() + timedelta(days=30)):
        return True
    return False

def list_recent_survivals(individual_data, family_data):
    """
        US37 - List recent survivors
        List all living spouses and descendants of people in a GEDCOM file who died in the last 30 days
        function calls: event_in_last_thirty_days()
        return: survivals dictionary type
    """
    survivals = dict()

    for ind in individual_data.values():
        if not ind.is_alive() and event_in_last_thirty_days(ind.deat):
            fam = dict()
            fam['name'] = ind.name
            fam['sex'] = ind.sex
            fam['fam_id'] = ind.fams
            fam['passed'] = ind.deat

            for i in ind.fams:
                val = family_data.get(i)
                if val is not None:
                    fam['children'] = val.chil
                    if ind.sex == "M":
                        fam['spouse_name'] = val.wife
                        fam['spouse_id'] = val.wife_id

                    if ind.sex == "F":
                        fam['spouse_name'] = val.husb
                        fam['spouse_id'] = val.husb_id
                    survivals[ind.uid] = fam
            del fam

    return survivals

def list_upcoming_birthdays(individual_data):
    """
        US38 - List upcoming birthdays
        Returns a list of individuals birthdays within the next 30 days, takes a dictionary of individuals
        Parameters: dictionary data of individuals
        Function Calls: is_anniversary_in_next_thirty_days() passing a date
    """
    list_birthdays = []

    for ind in individual_data.values():
        if is_anniversary_in_next_thirty_days(ind.birt):
            list_birthdays.append(ind)

    return list_birthdays

def validate_child_birth( individual_data,family_data):
    """US08 -- Children should be born after marriage of parents (and not more than 9 months after their divorce)"""
    marr_error_entries = dict()
    div_error_entries = dict()
    for fid, family in family_data.items():
        children_list = list(family.chil)
        if len(children_list) > 0 and (children_list != ['N', 'A']):
            for child in children_list:
                for uid, individual in individual_data.items():
                    if uid == child:
                        if check_two_dates(individual.birt, family.marr):
                            marr_error_entries[fid] = uid
                        elif family.div != 'NA':
                            if validate_date_format(family.div):
                                fam_div_date = convert_str_to_date(family.div)

                            if validate_date_format(individual.birt):
                                indi_birth_date = convert_str_to_date(individual.birt)

                            if abs((fam_div_date + relativedelta(month=9)) - indi_birth_date).days > 270:
                                div_error_entries[fid] = uid

    return marr_error_entries, div_error_entries

def check_parents_not_too_old(family_data, individual_data):
    """ US12 Parents Not Too Old - Mother should be less than 60 years older
    than her children and father should be less than 80 years older than his children """
    
    problem_families = {} # key = family id, value = list of husband/wife id, birthdate, child id, child birthdate

    for family in family_data.values():
        husband = individual_data[family.husb_id]
        husband_age = husband.get_age()
        wife = individual_data[family.wife_id]
        wife_age = wife.get_age()

        if family.chil != "NA":
            for person in family.chil:
                child = individual_data[person]
                child_age = child.get_age()
                if wife_age - child_age > 60:
                    problem_families[family.fid] = [wife.sex, wife.uid, wife.name, wife.birt, child.uid, child.name, child.birt]
                elif husband_age - child_age > 80:
                    problem_families[family.fid] = [husband.sex, husband.uid, husband.name, husband.birt, child.uid, child.name, child.birt]
    
    return problem_families

def check_multiple_births(family_data, individual_data):
    """ US14 Multiple Births <= 5 - No more than five siblings should be born
    at the same time """

    problem_families = {} # key = family id, value = list of children ids

    for family in family_data.values():
        if family.chil != "NA" and len(family.chil) > 5:
            problem_children = {} # key = birthday, value = list of children
            
            for person in family.chil:
                child = individual_data[person]
                child_birthday = child.birt

                if child_birthday in problem_children.keys():
                    if len(problem_children[child_birthday]) >= 5:
                        temp_list = problem_children[child_birthday]
                        temp_list.append(child.uid)
                        problem_children[child_birthday] = temp_list
                        problem_families[family.fid] = temp_list
                    else:
                        temp_list = problem_children[child_birthday]
                        temp_list.append(child.uid)
                        problem_children[child_birthday] = temp_list
                else:
                    problem_children[child_birthday] = [child.uid]
                
    return problem_families

def marriage_after_14(family_data, individual_data):
    """
    US10 Marriage should be at least 14 years after birth of both spouses
    this fucntion takes family and individual data as input and 
    returns true or false based on data.
    """

    problem_families = {} # key = spouse id, value = list of sex and family ID

    for family in family_data.values():
        if family.marr != 'NA':
            husband = None
            wife = None
            marriage_date = convert_str_to_date(family.marr)
            min_birt = datetime(marriage_date.year-14, marriage_date.month, marriage_date.day)

            for individual in individual_data.values():
                if individual.uid == family.husb_id:
                    husband = individual
                if individual.uid == family.wife_id:
                    wife = individual
            if husband != None and wife != None:
                h_birth = convert_str_to_date(husband.birt)
                if h_birth > min_birt:
                    problem_families[family.husb_id] = ["M", family.fid]
                
                w_birth = convert_str_to_date(wife.birt)
                if w_birth > min_birt:
                    problem_families[family.wife_id] = ["F", family.fid]

    return problem_families

def validate_childBirth_with_parentsDeath(individual_data, family_data):
    """US09 -- Child should be born before death of mother and before nine months after death of father"""
    child_mother_error = dict()
    child_father_error =dict()
    for fid, family in family_data.items():
        children_list = list(family.chil)
        if len(children_list) > 0 and (children_list != ['N', 'A']):
            for child in children_list:
                fam_obj = family_data[family.fid]
                if individual_data[fam_obj.wife_id].deat != 'NA':
                    if check_two_dates(individual_data[fam_obj.wife_id].deat, individual_data[child].birt):
                        child_mother_error[fid] = [child, fam_obj.wife_id]
                        
                if individual_data[fam_obj.husb_id].deat != 'NA':
                    if validate_date_format(individual_data[fam_obj.husb_id].deat):
                        father_death_date = convert_str_to_date(individual_data[fam_obj.husb_id].deat)

                    if validate_date_format(individual_data[child].birt):
                        child_birth_date = convert_str_to_date(individual_data[child].birt)
                        
                    if ((father_death_date + relativedelta(months=+9)) - child_birth_date).days < 0:
                        child_father_error[fid] = [child, fam_obj.husb_id]
                            
    return child_mother_error, child_father_error
