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

def convert_str_to_date(date):
    """
    this function is helperfunction which will 
    take str date as input and convert it to datetime object format
    this will use to compare date from file with current date.
    """
    if validate_date_format(date):
        new_date = change_date_format(date).split('-')
    
    date_obj = '-'.join(new_date)
    date_obj = datetime.strptime(date_obj, '%Y-%m-%d')
    return date_obj

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

def check_marriage_status(family_data):
    """ Function to check that a family does not have 'NA' listed for marr and
    remove them from the dictionary if so. """

    problem_families = []

    for family in family_data.values():
        if family.marr == "NA":
            problem_families.append(family.fid)
    for family in problem_families:
        family_data.pop(family)

    return family_data

def check_life_status(person, marriage_date):
    """ Function to check a person's life status and whether their death date
    occurred before their marriage date; if yes, return True else, return False. """
    if person.alive == False:
        return check_two_dates(person.deat, marriage_date)
