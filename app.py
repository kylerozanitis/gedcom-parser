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
from classes import individualPerson

individual_data = dict()
family_data = dict()

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
                return data_values


def data_parser(data):
    current_individual = ""
    current_tag = ""
    for item in data:
        if item[0] == "0" and len(item) < 3:
            continue
        elif item[0] == "0" and item[2] == "INDI":
            current_individual = item[1]
            individual_data[current_individual] = individualPerson(current_individual)
        elif item[0] == "1" and item[1] in ["NAME", "SEX", "FAMC", "FAMS"]:
            i1 = individual_data[current_individual]
            current_tag = item[1].lower()
            i1.current_tag = item[2:]
        elif item[0] == "1" and item[1] == ["BIRT", "DEAT"]:
            current_tag = item[1].lower()
            i1 = individual_data[current_individual]
            if current_tag == "DEAT":
                i1.alive = False
        elif item[0] == "2" and item[1] == "DATE":
            i1 = individual_data[current_individual]
            i1.current_tag = item[2:]


def create_table():
    """Example Function for PrettyTable"""
    tbl = PrettyTable()
    tbl.field_names = ["City name", "Area", "Population", "Annual Rainfall"]

    tbl.add_row(["Adelaide", 1295, 1158259, 600.5])
    tbl.add_row(["Brisbane", 5905, 1857594, 1146.4])
    tbl.add_row(["Darwin", 112, 120900, 1714.7])
    tbl.add_row(["Hobart", 1357, 205556, 619.5])
    tbl.add_row(["Sydney", 2058, 4336374, 1214.8])
    tbl.add_row(["Melbourne", 1566, 3806092, 646.9])
    tbl.add_row(["Perth", 5386, 1554769, 869.4])


    # return tbl
    if __name__ == '__main__':
        return tbl
    else:
        return 1


def main():
    """Main Function program Execution"""

    tbl = create_table()
    raw_data = read_data_file('My_Family.ged')
    data_parser(raw_data)


if __name__ == '__main__':
    main()
