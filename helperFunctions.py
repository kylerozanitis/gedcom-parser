# Lib Imports
import re
import os

from datetime import datetime, timedelta


def read_data_file(file_name):
    """Read GEDCOM file & strip data into a tuple of lists"""

    filename = os.fsdecode(file_name)
    if filename.endswith(".ged"):
        try:
            open(filename, "r")
        except FileNotFoundError:
            print(filename, "file cannot be opened!")
        except IOError:
            print('Please check that file is not corrupted.')
        else:
            # if file opens successfully
            with open(filename, 'r') as file_opened:
                # reading data from file
                each_line = file_opened.readlines()
                if len(each_line) == 0:
                    raise ValueError('{} is empty'.format(file_name))
                else:
                    data_values = tuple([e.strip('\n').split(' ') for e in each_line])
                return clean_data(data_values)
    else:
        return OSError('{} must be a .ged file'.format(file_name))


def clean_data(data):
    """Cleans data and returns only valid tags data in a tuple"""

    # LIST OF VALID TAGS
    VALID_TAGS = ('INDI', 'NAME', 'SEX',
            'BIRT', 'DEAT', 'FAMC',
            'FAMS', 'FAM', 'MARR',
            'HUSB', 'WIFE', 'CHIL',
            'DIV', 'DATE', 'HEAD',
            'TRLR', 'NOTE')

    # list of tags with invalid data
    KNOWN_INVALID_TAGS = ('id', 'invalid', ' ')

    new_list = []

    for val in data:

        # Checks of known invalid data
        if (len(val) >= 3 and val[2] in KNOWN_INVALID_TAGS):
            # if invalid continue
            pass

        # Basic manipulation to fix compatibility on INDI and id tags
        elif len(val) >= 3 and val[2] in VALID_TAGS:
            val.insert(1, val[2])
            val.pop(3)
            new_list.append(val)

        # if tags are valid
        elif val[1] in VALID_TAGS:
            new_list.append(val)

        else:
            # if invalid continue
            pass

    return tuple(new_list)


def validate_date_format(date_to_match):
    """Function takes a date and checks if the format is 'd MON YYYY' returns true if it matches false if it doesn't"""

    date = re.compile(r'^\d+\s\D{3}\s\d{4}')

    if not date.match(date_to_match):
        return False
    return True


def change_date_format(date):
    """Function takes a date and changes the format from 'd MON YYYY' to 'YYYY-MM-dd' """

    month_dict = {"JAN": "01", "FEB": "02", "MAR": "03",
                  "APR": "04", "MAY": "05", "JUN": "06",
                  "JUL": "07", "AUG": "08", "SEP": "09",
                  "OCT": "10", "NOV": "11", "DEC": "12",
                  "Jan": "01", "Feb": "02", "Mar": "03",
                  "Apr": "04", "May": "05", "Jun": "06",
                  "Jul": "07", "Aug": "08", "Sep": "09",
                  "Oct": "10", "Nov": "11", "Dec": "12" }

    temp = date.split(" ")
    date_month = month_dict.get(temp[1])

    # if Birthday is single digit day make it two digits by adding Zero
    if len(list(temp[0])) == 1:
        return temp[2] + '-' + date_month + '-' + "0"+temp[0]

    return temp[2]+'-'+date_month+'-'+temp[0]


def check_spouses_exist(family_data):
    """ Function to check that both a wife and husband exist and remove them
    from the dictionary if not. """

    problem_families = []

    for family in family_data.values():
        if family.husb_id == "NA" or family.wife_id == "NA":
            problem_families.append(family.fid)
    for family in problem_families:
        family_data.pop(family)

    return family_data


def deceased_list(individual_data):
    """US29 - List deceased. This function takes a dictionary list loops through the individual
    list to get the people that has passed away and returns a list of individuals"""

    items = []
    for individual in individual_data.values():
        if not individual.is_alive():
            items.append(individual)

    return items


def birth_before_marriage(family_data, individual_data):
    """US02 - Birth should occur before Marriage of either spouse -
    Checks for birth before marriages if marriage happens before birth,
    individual will be removed from family"""

    problematic_item = []
    for fam in family_data.values():
        if fam.marr is not "NA":
            ind = individual_data[fam.husb_id]
            if not check_two_dates(ind.birt, fam.marr):
                problematic_item.append(fam)

    if len(problematic_item) > 0:
        for i in problematic_item:
            del family_data[i.fid]

    return family_data


def agemorethan_150(status, dob, age):
    """US07 - Function Returns true or false is the individual is older the 150 yrs old
        it takes 3 parameters: status of person (if alive or not) DOB, and its Age """

    flag = True
    today = datetime.now()

    if validate_date_format(dob):
        bdate = change_date_format(dob).split('-')

    birth = '-'.join(bdate)
    birth = datetime.strptime(birth, '%Y-%m-%d')

    if status == False and birth <= today and age < 150:
        flag = True
    elif status == True and birth <= today and age <150:
        flag = True
    else:
        flag = False
    return flag


def check_two_dates(first_Event, event_to_compare_date):
    """This function checks two events first_event (Example Birth) happened
    before the event_to_compare_date (example death or marriage), it uses validate_format() and change date format"""

    if validate_date_format(first_Event) and validate_date_format(event_to_compare_date):
        date_one = change_date_format(first_Event)
        date_two = change_date_format(event_to_compare_date)

        if date_one < date_two:
            return True
        return False
    else:
        raise ValueError('check dates, format is invalid.')


def check_marriage_before_divorce(family_data):
    """ US04 - Marriage should occur before divorce of spouses, and divorce can
    only occur after marriage; Program takes a Family ID (FID), ensures the
    wedding took place before the divorce. """
    
    problem_families = []

    for family in family_data.values():
        if family.marr == "NA":
            problem_families.append(family.fid)
        elif family.div != "NA":
            marr = change_date_format(family.marr).split("-")
            marriage = "-".join(marr)
            marriage_date = datetime.strptime(marriage, "%Y-%m-%d")
            
            div = change_date_format(family.div).split("-")
            divorce = "-".join(div)
            divorce_date = datetime.strptime(divorce, "%Y-%m-%d")
            
            if marriage_date > divorce_date:
                problem_families.append(family.fid)
        
    return problem_families


def check_marriage_before_death(family_data, individual_data):
    """ US05 - Marriage should occur before death of either spouse; Program
    takes the family and individual dictionaries. For each family, the program
    checks if either spouse is dead and if so, checks that the marriage date
    occured before the death date of that spouse. A list of problem families
    is returned from this function. """

    problem_families = []

    for family in family_data.values():
        if family.marr == "NA":
            problem_families.append(family.fid)
        else:
            husband = individual_data[family.husb_id]
            wife = individual_data[family.wife_id]

            marr = change_date_format(family.marr).split("-")
            marriage = "-".join(marr)
            marriage_date = datetime.strptime(marriage, "%Y-%m-%d")

            if husband.is_alive == False:
                deat = change_date_format(husband.deat).split("-")
                death = "-".join(deat)
                death_date = datetime.strptime(death, "%Y-%m-%d")

                if death_date < marriage_date:
                    problem_families.append(family.fid)

            elif wife.is_alive == False:
                deat = change_date_format(wife.deat).split("-")
                death = "-".join(deat)
                death_date = datetime.strptime(death, "%Y-%m-%d")

                if death_date < marriage_date:
                    problem_families.append(family.fid)
    
    return problem_families


def death_before_birth(individual_data, family_data):
    """
    US03 - Birth should occur before death of an individual - This fucntion calls US01 to check if the dates
    are ocuuring before the current date and then uses individual's birth date and death date to validate if 
    birth occured before death. It returns a dictionary containing the id and a list of string value to print error
    messages
    """
    birth_error = []
    all_error_entries = allDates_before_currentDate(individual_data, family_data)
    for uid, individual in individual_data.items():
        if individual.birt != 'NA' and individual.deat != 'NA':
            temp1 = change_date_format(individual.birt).split("-")
            indi_birt = "-".join(temp1)
            indi_birth_date = datetime.strptime(indi_birt, "%Y-%m-%d")

            temp2 = change_date_format(individual.deat).split("-")
            indi_deat = "-".join(temp2)
            indi_deat_date = datetime.strptime(indi_deat, "%Y-%m-%d")

            if indi_birth_date > indi_deat_date:
                if uid in all_error_entries.keys():
                    for error_list in all_error_entries.values():
                        error_list.append('death before birth')
                    all_error_entries[uid] = error_list
                else:
                    birth_error.append('death before birth')
                    all_error_entries[uid] = birth_error
            birth_error = []
            
    return all_error_entries

def allDates_before_currentDate(individual_data, family_data):
    """
    US01 - Dates (birth, marriage, divorce, death) should not be after the current date- This fucntion checks if  
    current date occurs after all the birth dates, marriage dates, divorce dates and death dates. It returns a 
    dictionary containing the id and a list of string value to print error messages
    """
    current_date = datetime.today().strftime('%d %b %Y')
    temp1 = change_date_format(current_date).split("-")
    temp2 = "-".join(temp1)
    today_date = datetime.strptime(temp2, "%Y-%m-%d")

    currentDate_compare_error = dict()
    indi_status_list = []
    fam_status_list = []
    for uid, individual in individual_data.items():
        if individual.birt != 'NA' and individual.deat != 'NA':
            temp1 = change_date_format(individual.birt).split("-")
            indi_birt = "-".join(temp1)
            indi_birth_date = datetime.strptime(indi_birt, "%Y-%m-%d")

            temp2 = change_date_format(individual.deat).split("-")
            indi_deat = "-".join(temp2)
            indi_deat_date = datetime.strptime(indi_deat, "%Y-%m-%d")

            if indi_birth_date > today_date:
                indi_status_list.append('birth')
            if indi_deat_date > today_date:
                indi_status_list.append('death')

        elif individual.birt != 'NA' and individual.deat == 'NA':
            temp1 = change_date_format(individual.birt).split("-")
            indi_birt = "-".join(temp1)
            indi_birth_date = datetime.strptime(indi_birt, "%Y-%m-%d")

            if indi_birth_date > today_date:
                indi_status_list.append('birth')

        else:
            indi_status_list.append('not born')
            
        if len(indi_status_list) == 0:
            continue
        else:
            currentDate_compare_error[uid] = indi_status_list
            indi_status_list = []


    for fid, family in family_data.items():
        if family.marr != 'NA' and family.div != 'NA':
            temp1 = change_date_format(family.marr).split("-")
            fam_marr = "-".join(temp1)
            fam_marr_date = datetime.strptime(fam_marr, "%Y-%m-%d")

            temp1 = change_date_format(family.div).split("-")
            fam_div = "-".join(temp1)
            fam_div_date = datetime.strptime(fam_div, "%Y-%m-%d")
            
            if fam_marr_date > today_date:
                fam_status_list.append('marriage')
            if fam_div_date > today_date:
                fam_status_list.append('divorce')
                
        elif family.marr != 'NA' and family.div == 'NA':
            temp1 = change_date_format(family.marr).split("-")
            fam_marr = "-".join(temp1)
            fam_marr_date = datetime.strptime(fam_marr, "%Y-%m-%d")

            if fam_marr_date > today_date:
                fam_status_list.append('marriage')

        else:
            fam_status_list.append('not married')

        if len(fam_status_list) == 0:
            continue
        else:
            currentDate_compare_error[fid] = fam_status_list
            fam_status_list = []


    return currentDate_compare_error


def divorce_before_death(family_data,individual_data):
    """
    US06 - Divorce can only occure before death of both spouses
    This functions takes individual data and family data data as input and 
    for dead person checks if the date of death is after date of divorce if its false
    it will return list of families with problem
    """
    prob_family = []

    for family in family_data.values():
        if family.div != 'NA':
            husband = None
            wife = None
            div = change_date_format(family.div).split('-')
            div_d = '-'.join(div)
            divorce_date = datetime.strptime(div_d,'%Y-%m-%d')

            for individual in individual_data.values():
                if individual.uid == family.husb_id:
                    husband = individual
                if individual.uid == family.wife_id:
                    wife = individual
            if husband.alive == False:
                husb_deat = change_date_format(husband.deat).split('-')
                h_deat = '-'.join(husb_deat)
                husb_death = datetime.strptime(h_deat,'%Y-%m-%d')
                if divorce_date > husb_death:
                    print(husb_death,'is less than',divorce_date)
                    prob_family.append(family.fid)
            if wife.alive == False:
                wife_deat = change_date_format(wife.deat).split('-')
                w_deat = '-'.join(wife_deat)
                wife_death = datetime.strptime(w_deat,'%Y-%m-%d')
                if divorce_date > wife_death:
                    prob_family.append(family.fid)
    return prob_family


def event_in_last_thirty_days(date):
    """Check for event happened in the last 30 days"""

    if validate_date_format(date):
        new_date = change_date_format(date)
        values = new_date.split('-')

        val = ((datetime.now().year - int(values[0])) + int(values[0]))
        compare_date = "{0}-{1}-{2}".format(str(val), values[1], values[2])

        if str(datetime.now().date() + timedelta(days=-30)) <= compare_date <= str(datetime.now().date()) and values[0] == str(datetime.now().year):
            return True
        return False


def list_recent_births(individual_data):
    """
    US35 - List all people in a GEDCOM file who were born in the last 30 days
    This fucntion will take individual data as input and 
    return list of birthdays happened in the last 30 days
    """
    recent_birth = []

    for individual in individual_data.values():
        if event_in_last_thirty_days(individual.birt):
            recent_birth.append(individual)
    return recent_birth


def list_recent_death(individual_data):
    """
    US36 - List all people in a GEDCOM file who died in the last 30 days
    This function takes individual data as input and 
    return list of death happened in the last 30 days
    """
    recent_death = []

    for individual in individual_data.values():
        if event_in_last_thirty_days(individual.deat):
            recent_death.append(individual)
    return recent_death


def fewer_than15_siblings(family_data):
    """ US15 -- There should be fewer than 15 siblings in a family""" 
    fid_list = []
    for fid, obj in family_data.items():
        if len(obj.chil) > 15:
            fid_list.append(fid)
    return fid_list


def check_unique_ids(individual_data, family_data):
    """ 
        US22 Unique IDs - All individual IDs should be unique and all
        family IDs should be unique
    """

    individual_ids = []
    problem_uids = []

    for uid in individual_data.keys():
        if uid in individual_ids:
            problem_uids.append(uid)
        else:
            individual_ids.append(uid)

    family_ids = []
    problem_fids = []

    for fid in family_data.keys():
        if fid in family_ids:
            problem_fids.append(fid)
        else:
            family_ids.append(fid)
    
    return problem_uids, problem_fids


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








    



