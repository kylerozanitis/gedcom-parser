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


def read_data_file(file_name):
    """Read GEDCOM files Strip data into a tuple of list"""

    try:
        open(file_name, "r")

    except FileNotFoundError:
        print(file_name, "file cannot be opened!")

    except IOError:
        print('Please check that file is not corrupted.')

    else:
        # if file opens successfully
        with open(file_name, 'r') as file_opened:
            # reading data from file
            each_line = file_opened.readlines()


            if len(each_line) == 0:
                raise ValueError('{} is empty'.format(file_name))
            else:
                data_values = tuple([e.strip('\n').split(' ') for e in each_line])

            return data_values


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
    print(read_data_file('My_Family.ged'))


if __name__ == '__main__':
    main()

