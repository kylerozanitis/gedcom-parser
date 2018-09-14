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
    print(tbl)


if __name__ == '__main__':
    main()

