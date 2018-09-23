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
    """Function takes a date and changes the format from 'd MON YYYY' to 'YYYY/MM/dd' """

    month_dict = {"JAN": "01", "FEB": "02", "MAR": "03",
                  "APR": "04", "MAY": "05", "JUN": "06",
                  "JUL": "07", "AUG": "08", "SEP": "09",
                  "OCT": "10", "NOV": "11","DEC": "12" }

    temp = date.split(" ")
    date_month = month_dict.get(temp[1])

    return temp[2]+'-'+date_month+'-'+temp[0]


def deceased_list(individual_data):
    """ This function takes a dictionary list loops through the individual list to get the people that has passed away and returns a list of individuals"""

    items = []
    for individual in individual_data.values():
        if not individual.is_alive():
            items.append(individual)

    return items

def agemorethan_150(status,dob,age):
    flag = True
    today = datetime.now()
    #print('Today-',today)
    if validate_date_format(dob):
        bdate = change_date_format(dob).split('-')
    birth = '-'.join(bdate)
    birth = datetime.strptime(birth, '%Y-%m-%d')
    #print('birth-',birth)
    if status:
        if birth <= today and age < 150:
            flag = True
        else:
            flag = False
    else:
        flag = False
    return flag
