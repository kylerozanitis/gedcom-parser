#   File Name: app.py
#   Assignment: # 3
#
#   Class: SSW 555 - Agile Methods for Software Engineering
#
#   Team:
#       Kshiti Rana,
#       Jose Lara,
#       Kyle Rozanitis,
#       Pratik Shah
#
#   This program is the main Function for our GEDCOM program.
#   For now it uses Pretty table with Dummy Data to display it

# Library imports
from prettytable import PrettyTable
import os
from classes import individualPerson, familyClass
from _collections import defaultdict

individual_data = defaultdict(lambda: defaultdict(str))
family_data = defaultdict(lambda: defaultdict(str))

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

def data_parser_try(data):
    """Check if tag is individual or family and create a dictionary for each and add them to correspondent list"""
    individual = []
    family = []
    individual_dict = defaultdict(lambda: defaultdict(str))
    family_dict = defaultdict(lambda: defaultdict(str))
    indi_or_fam_tag = ""

    for each in data:
        if each[1] in ("INDI", "FAM"):

            if each[1] == "INDI":
                individual_dict = {"ID": each[2], "NAME": '', "SEX": '', "BIRT": '', "DEAT": ''}
                indi_or_fam_tag = each[1]
                individual.append(individual_dict)
            if each[1] == "FAM":
                family_dict = {"ID": each[2], "MARR": '', "HUSB": '', "WIFE": '', "CHIL": [], "DIV": ''}
                family.append(family_dict)

        elif each[1] in ("NAME", "SEX"):
            individual_dict[each[1]] = " ".join(each[2:])

        elif each[1] in ("BIRT", "DEAT", "MARR", "DIV"):
            this_tag = each[1]

        elif each[1] in ("DATE"):
            if indi_or_fam_tag == 'INDI':
                individual_dict[this_tag] = " ".join(each[2:])

            elif indi_or_fam_tag == 'FAM':
                family_dict[this_tag] = " ".join(each[2:])

        elif each[1] in ("HUSB", "WIFE"):
            family_dict[each[1]] = " ".join(each[2:])

        elif each[1] == "CHIL":
            family_dict[each[1]].append(each[2])

    return family, individual

def data_parser(data):
    """ Reads through the passed-in clean data and creates individuals and
    families from the classes.py file. All individuals have a UID, name, birth,
    and sex, and may also have death date, famc, or fams. Families have an FID,
    married date, husband ID, wife ID, and a list of children IDs, and may have
    a divorced date as well. """
    current_individual = ""
    current_family = ""
    for item in data:
        if item[0] == "0" and len(item) < 3:
            continue
        elif item[0] == "0" and item[1] == "INDI":
            current_individual = item[2]
            individual_data[current_individual] = individualPerson(current_individual)
        elif item[0] == "1" and item[1] in ["NAME", "SEX", "FAMC", "FAMS"]:
            i1 = individual_data[current_individual]
            if item[1] == "NAME":
                i1.name = " ".join(item[2:])
            elif item[1] == "SEX":
                i1.sex = item[2]
            elif item[1] == "FAMC":
                famc_list = i1.famc
                famc_list.append(item[2])
                i1.famc = famc_list
            else:
                fams_list = i1.fams
                fams_list.append(item[2])
                i1.fams = fams_list
        elif item[0] == "1" and item[1] == "DEAT":
            i1 = individual_data[current_individual]
            i1.alive = False
        elif item[0] == "2" and item[1] == "DATE":
            i1 = individual_data[current_individual]
            if i1.alive == True:
                i1.birt = " ".join(item[2:])
            else:
                i1.deat = " ".join(item[2:])
        
        elif item[0] == "0" and item[1] == "FAM":
            current_family = item[2]
            family_data[current_family] = familyClass(current_family)
        elif item[0] == "1" and item[1] in ["HUSB", "WIFE"]:
            f1 = family_data[current_family]
            if item[1] == "HUSB":
                f1.husb = item[2]
            else:
                f1.wife = item[2]           
        elif item[0] == "1" and item[1] == "CHIL":
            f1 = family_data[current_family]
            children_list = f1.chil
            children_list.append(item[2])
            f1.chil = children_list
        elif item[0] == "1" and item[1] in ["MARR", "DIV"]:
            if item[1] == "MARR":
                f1.marr = " ".join(item[2:])
            else:
                f1.marr = " ".join(item[2:])


def create_table_individual(data):
    """Example Function for PrettyTable"""

    tbl = PrettyTable()
    tbl.field_names = ["ID", "Name", "Gender", "Birthdate", "Age", "Alive", "Death", "Child", "Spouse"]

    for d in data:
        tbl.add_row([ d.get('ID', "N/A"), d.get('NAME', "N/A"), d.get('SEX', "N/A"), d.get('BIRT', "N/A"), d.get('AGE', "N/A"),  d.get('ALIVE', "N/A"),  d.get('DEAT', "N/A"),  d.get('CHILD', "N/A"),  d.get('SPOUSE', "N/A")])


    return tbl



def main():
    """Main Function program Execution"""

    raw_data = read_data_file('My_Family.ged')
    # fam, ind = data_parser(raw_data)
    fam, ind = data_parser_try(raw_data)

    print(create_table_individual(ind))
    # print(create_table_family(fam))

    for i in ind:
        print("individual: ", i)

    for f in fam:
        print("Fam: ", f)



if __name__ == '__main__':
    main()
