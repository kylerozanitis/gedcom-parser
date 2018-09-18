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
#   For now it uses PrettyTable with Dummy Data to display it

# Library imports
from prettytable import PrettyTable
from classes import individualPerson, familyClass
from helperFunctions import read_data_file

individual_data = dict()
family_data = dict()


def data_parser(data):
    """ Reads through the passed-in clean data and creates individuals and
    families from the classes.py file. All individuals have an User ID, name, birth,
    and sex, and may also have death date, famc, or fams. Families have an Family ID,
    married date, husband ID, husband name, wife ID, wife name, and a list of children IDs.
    Families may have a divorced date as well. """
    current_individual = ""
    current_family = ""
    current_tag = ""
    for item in data:
        indi_id = ''
        fam_id = ''
        if item[0] == "0" and item[1] == "INDI":
            indi_id = item[2].strip('@')
            current_individual = indi_id
            current_tag = item[1]
            individual_data[current_individual] = individualPerson(current_individual)
        elif item[0] == "1" and item[1] in ["NAME", "SEX", "FAMC", "FAMS"]:
            i1 = individual_data[current_individual]
            if item[1] == "NAME":
                i1.name = " ".join(item[2:])
            elif item[1] == "SEX":
                i1.sex = item[2]
            elif item[1] == "FAMC":
                famc_list = i1.famc
                famc_list.append(item[2].strip('@'))
                i1.famc = famc_list
            else:
                fams_list = i1.fams
                fams_list.append(item[2].strip('@'))
                i1.fams = fams_list
        elif item[0] == "1" and item[1] == "DEAT":
            i1 = individual_data[current_individual]
            i1.alive = False
        elif item[0] == "2" and item[1] == "DATE" and current_tag == "INDI":
            i1 = individual_data[current_individual]
            if i1.alive == True:
                i1.birt = " ".join(item[2:])
            else:
                i1.deat = " ".join(item[2:])

            i1.age = i1.get_age()

        
        elif item[0] == "0" and item[1] == "FAM":
            fam_id = item[2].strip('@')
            current_family = fam_id
            current_tag = item[1]
            family_data[current_family] = familyClass(current_family)
        elif item[0] == "1" and item[1] in ["HUSB", "WIFE"]:
            f1 = family_data[current_family]
            if item[1] == "HUSB":
                f1.husb_id, f1.husb = item[2].strip('@'), individual_data[item[2].strip('@')].name
            else:
                f1.wife_id, f1.wife = item[2].strip('@'), individual_data[item[2].strip('@')].name        
        elif item[0] == "1" and item[1] == "CHIL":
            f1 = family_data[current_family]
            children_list = f1.chil
            children_list.append(item[2].strip('@'))
            f1.chil = children_list
        elif item[0] == "2" and item[1] in ["DATE"] and current_tag == "FAM":
            if f1.marr == "NA":
                f1.marr = " ".join(item[2:])
            else:
                f1.div = " ".join(item[2:])


def main():
    """Main Function program Execution"""

    raw_data = read_data_file('familytree.ged')
    data_parser(raw_data)

    print('Individuals')
    t = PrettyTable(['ID', 'Name', 'Gender', 'Birthday','Age','Alive','Death','Child','Spouse'])
    for obj in individual_data.values():
        t.add_row(obj.pt_row())
    print (t)

    print('Families')
    t = PrettyTable(['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name','Children'])
    for obj in family_data.values():
        t.add_row(obj.pt_row())
    print (t)


if __name__ == '__main__':
    main()
