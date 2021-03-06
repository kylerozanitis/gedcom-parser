""" This file includes the functions that were implemented in sprint 1 and any
functions that assisted in parsing of the data """

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

    return problematic_item

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

def agemorethan_150(individual_data):
    """US07 - Function Returns true or false is the individual is older the 150 yrs old
        it takes 3 parameters: status of person (if alive or not) DOB, and its Age """

    flag = True
    error_story = "US07"
    #today = datetime.now()
    for individual in individual_data.values():
        person = individual.uid
        #birth = convert_str_to_date(individual.birt)
        if individual.alive == False and individual.age > 150:
            error_descrip="lived longer than 150 years"
            error_location = person
            print_both('ERROR: INDIVIDUAL:',error_story,':',str(error_location),':',error_descrip)
            flag = False
        elif individual.alive == True and individual.age > 150:
            error_descrip="lived longer than 150 years"
            error_location = person
            print_both('ERROR: INDIVIDUAL:',error_story,':',str(error_location),':',error_descrip)
            flag = False
        else:
            flag = True
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
        return 'check dates, format is invalid.'


def check_marriage_before_divorce(family_data):
    """ US04 - Marriage should occur before divorce of spouses, and divorce can
    only occur after marriage; Program takes a Family ID (FID), ensures the
    wedding took place before the divorce. """

    problem_families = []

    for family in family_data.values():
        if family.div != "NA":
            if check_two_dates(family.div, family.marr) == True:
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
        husband = individual_data[family.husb_id]
        wife = individual_data[family.wife_id]

        if check_life_status(husband, family.marr) == True or check_life_status(wife, family.marr) == True:
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
            if check_two_dates(individual.deat, individual.birt):
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
    
    currentDate_compare_error = dict()
    indi_status_list = []
    fam_status_list = []
    for uid, individual in individual_data.items():
        if individual.birt != 'NA' and individual.deat != 'NA':
            if check_two_dates(current_date, individual.birt):
                indi_status_list.append('birth')
            if check_two_dates(current_date, individual.deat):
                indi_status_list.append('death')
        elif individual.birt != 'NA' and individual.deat == 'NA':
            if check_two_dates(current_date, individual.birt):
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
            if check_two_dates(current_date, family.marr):
                fam_status_list.append('marriage')
            if check_two_dates(current_date, family.div):
                fam_status_list.append('divorce')                
        elif family.marr != 'NA' and family.div == 'NA':
            if check_two_dates(current_date, family.marr):
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
    error_story = 'US06'

    for family in family_data.values():
        if family.div != 'NA':
            husband = None
            wife = None
            divorce_date = convert_str_to_date(family.div)

            for individual in individual_data.values():
                if individual.uid == family.husb_id:
                    husband = individual
                if individual.uid == family.wife_id:
                    wife = individual
            if husband.alive == False:
                husb_death = convert_str_to_date(husband.deat)
                if divorce_date > husb_death:
                    error_descrip = "Death of Husband {} occurs before date of divorce {}".format(husband.deat,family.div)
                    error_location = husband.uid
                    print_both('ERROR: INDIVIDUAL:',error_story,':',str(error_location),':',error_descrip)
                    prob_family.append(family.fid)
            if wife.alive == False:
                wife_death = convert_str_to_date(wife.deat)
                if divorce_date > wife_death:
                    error_descrip = "Death of wife {} occurs before date of divorce {}".format(wife.deat,family.div)
                    error_location = wife.uid
                    print_both('ERROR: INDIVIDUAL:',error_story,':',str(error_location),':',error_descrip)
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
    This function will take individual data as input and
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


def check_marriage_status(family_data):
    """ Function to check that a family does not have 'NA' listed for marr and
    remove them from the dictionary if so. """

    problem_families = []

    for family in family_data.values():
        if family.marr == "NA":
            problem_families.append(family.fid)

    return problem_families


def check_life_status(person, marriage_date):
    """ Function to check a person's life status and whether their death date
    occurred before their marriage date; if yes, return True else, return False. """
    if person.alive == False:
        return check_two_dates(person.deat, marriage_date)


def print_both(*args):
    """ Function to print the text to the command line/terminal and write to a file """
    print(*args)
    with open("Output.txt", "a") as file_name:
        print(*args, file=file_name)