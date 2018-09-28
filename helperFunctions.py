# Lib Imports
import re
import os

from datetime import datetime

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
                  "OCT": "10", "NOV": "11","DEC": "12" }

    temp = date.split(" ")
    date_month = month_dict.get(temp[1])

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
    """ This function takes a dictionary list loops through the individual list to get the people that
    has passed away and returns a list of individuals"""

    items = []
    for individual in individual_data.values():
        if not individual.is_alive():
            items.append(individual)

    return items


def birth_before_marriage(family_data, individual_data):
    """Checks for birth before marriages if marriage happens before birth, individual will be removed from family"""
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



def agemorethan_150(status,dob,age):
    """Function Returns true or false is the individual is older the 150 yrs old
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

def death_before_birth(individual_data):
    """US03 -- Birth should occur before death of an individual --- Program uses individual's 
       birth date and death date to validate if birth occured before death. It returns a list of 
       uid of the individuals whose death date occurs before birth date along with a flag indicator
       to print error messages"""
    error_entries = []
    flag = 0
    for uid, individual in individual_data.items():
        if individual.birt != 'NA' and individual.deat != 'NA':
            temp1 = change_date_format(individual.birt).split("-")
            indi_birt = "-".join(temp1)
            indi_birth_date = datetime.strptime(indi_birt, "%Y-%m-%d")

            temp2 = change_date_format(individual.deat).split("-")
            indi_deat = "-".join(temp2)
            indi_deat_date = datetime.strptime(indi_deat, "%Y-%m-%d")

            if indi_birth_date > indi_deat_date:
                flag = 1
                error_entries.append(individual.uid)

        if individual.birt == 'NA' and individual.deat != 'NA':
            flag = 2
            error_entries.append(individual.uid)
            
    return error_entries, flag
