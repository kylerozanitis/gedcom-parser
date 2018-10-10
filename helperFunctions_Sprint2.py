#Lib Imports
from dateutil.relativedelta import *
from helperFunctions_Sprint1 import validate_date_format, change_date_format, event_in_last_thirty_days
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
                living_married.append(husband.uid)
            if wife.alive == True:
                living_married.append(wife.uid)
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
