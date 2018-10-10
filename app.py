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
from helperFunctions import read_data_file, deceased_list, agemorethan_150
from helperFunctions import check_marriage_before_divorce, check_marriage_before_death, check_spouses_exist
from helperFunctions import death_before_birth, birth_before_marriage, divorce_before_death, allDates_before_currentDate
from helperFunctions import list_recent_births, list_recent_death, fewer_than15_siblings, check_unique_ids, list_upcoming_birthdays
from helperFunctions import list_recent_survivals, living_married_list, check_marriage_status
import sys
from datetime import datetime

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
                name_val = " ".join(item[2:])
                i1.name = name_val.replace('/', '')
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

    if len(sys.argv) <= 1:
        raise ValueError("Missing File argument please pass argument from command line")

    if len(sys.argv) > 2:
        raise ValueError("Only 1 argument accepted, 2 were given. try again.")

    raw_data = read_data_file(sys.argv[1])
    data_parser(raw_data)

    # Check that each family has a husband and a wife
    check_spouses_exist(family_data)

    # Check that each has a marriage date
    check_marriage_status(family_data)
    
    print('Individuals')
    t = PrettyTable(['ID', 'Name', 'Gender', 'Birthday','Age','Alive','Death','Child','Spouse'])
    for obj in individual_data.values():
        t.add_row(obj.pt_row())
    print(t)
    
    print('Families')
    t = PrettyTable(['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name','Children'])
    for obj in family_data.values():
        t.add_row(obj.pt_row())
    print(t)
    
    """
    US01 - Dates (birth, marriage, divorce, death) should not be after the current date
    US03 - Birth should occur before death of an individual
    Here, implementation of US01 is a subset of implementation of US03. First the dates are checked if they are
    occuring before the current date (US01) and then the birth dates and death dates are compared to check if
    birth dates occur before the death date (US03). Hence, executing US03 will also execute US01
    Also, all_error_entries is a dictionary that contains ids of individuals and families with a list of string
    elements and an error message is print using the string values in the list.
    """ 
    all_error_entries = death_before_birth(individual_data, family_data)
    current_date = datetime.today().strftime('%d %b %Y')
    
    for ids, msg_list in all_error_entries.items():
        for msg in msg_list:
            if msg == 'birth':
                print("ERROR: Individual: US01: " + str(ids) +" : Birthday " + str(individual_data[ids].birt) + " cannot occur before current date " + str(current_date))
            elif msg == 'death':
                print("ERROR: Individual: US01: " + str(ids) +" : Death date " + str(individual_data[ids].deat) + " cannot occur before current date " + str(current_date))
            elif msg == 'marriage':
                print("ERROR: Family: US01: " + str(ids) +" : Marriage date " + str(family_data[ids].marr) + " cannot occur before current date " + str(current_date))
            elif msg == 'divorce':
                print("ERROR: Family: US01: " + str(ids) +" : Divorce date " + str(family_data[ids].div) + " cannot occur before current date " + str(current_date))
            elif msg == 'not born':
                print("ERROR: Individual: US01: " + str(ids) + " : " + str(individual_data[ids].name) + " is not born yet")
            elif msg == 'not married':
                print("ERROR: Family: US01: " + str(ids) +" Not married ")
            else:
                print("ERROR: Individual: US03: " + str(ids) +" : Death date " + str(individual_data[ids].deat) + " cannot occur before birthday " + str(individual_data[ids].birt))
    
    # Get list of individuals who passed
    for person in deceased_list(individual_data):
        print("Date Passed: {0} Name: {1} ".format(person.deat, person.name ))
    
    # list living married
    living_married = living_married_list(family_data, individual_data)
    if len(living_married) > 0:
        print("living married: ", living_married)
    else:
        print("living married",len(living_married))

    #for person in individual_data.values():
     #   print('person name:',person.name,' - ',agemorethan_150(person.alive,person.birt,person.age))
    
    #divorce before death
    prob_family = divorce_before_death(family_data,individual_data)
    print("prob_family",prob_family)

    # US04 Print out list of families with divorce occuring before marriage
    problem_families = check_marriage_before_divorce(family_data)
    if len(problem_families) > 0:
        for item in problem_families:
            family = family_data[item]
            if family.marr == "NA":
                print("ERROR: FAMILY: US04: {}: Marriage date does not exist".format(family.fid))
            else:
                print("ERROR: FAMILY: US04: {}: Divorce date {} occurs before marriage date {}".format(family.fid, family.div, family.marr))

    # US05 Print out list of families with death of a spouse occuring before marriage
    prob_families = check_marriage_before_death(family_data, individual_data)
    if len(prob_families) > 0:
        for item in prob_families:
            family = family_data[item]
            husband = individual_data[family.husb_id]
            wife = individual_data[family.wife_id]

            if family.marr == "NA":    
                print("ERROR: FAMILY: US05: {}: Marriage date does not exist".format(family.fid))
            elif husband.alive == False:
                print("ERROR: FAMILY: US05: {}: Husband death date {} occurs before marriage date {}".format(family.fid, husband.deat, family.marr))
            elif wife.alive == False:
                print("ERROR: FAMILY: US05: {}: Wife death date {} occurs before marriage date {}".format(family.fid, wife.deat, family.marr))

    # Checks for birth before marriages if marriage happens before birth, individual will be removed from family
    for obj in birth_before_marriage(family_data, individual_data):
        print("ERROR: INDIVIDUAL: US02: {} Birth occurs before marriage".format(obj.uid))


    print("\nRecent Birthday Data")
    birth_recently = list_recent_births(individual_data)
    for individual in birth_recently:
        print(individual.birt)

    if len(birth_recently) == 0:
        print("No recent Birth\n")
    else:
        print("Total number of birth in the last 30 days: {}".format(len(birth_recently)))
        for individual in birth_recently:
            print("Name: {0}, Birth on: {1}\n".format(individual.name, individual.birt))

    print("\nRecent Death Data")
    death_recently = list_recent_death(individual_data)
    if len(death_recently) == 0:
        print("No recent Death")
    else:
        print("Total number of Death in the last 30 days: {}".format(len(death_recently)))
        for individual in death_recently:
            print("Name: {0}, Death on: {1}\n".format(individual.name, individual.deat))


    # US15 -- There should be fewer than 15 siblings in a family
    fid_list = fewer_than15_siblings(family_data)
    for fid in fid_list:
        print("ERROR: FAMILY: US15: " + str(fid) + " has more than 15 siblings")

    print("\n")
    
    # US22 Unique IDs - All individual IDs should be unique and all family IDs should be unique
    problem_indis, problem_fams = check_unique_ids(individual_data, family_data)
    if len(problem_indis) > 0:
        for individual in problem_indis:
            print("ERROR: INDIVIDUAL: US22: {} has been used for more than one individual".format(individual))
    else:
        print("ANOMALY: INDIVIDUAL: US22: All individuals have unique UIDs due to data storage in dictionaries")

    if len(problem_fams) > 0:
        for family in problem_fams:
            print("ERROR: FAMILY: US22: {} has been used for more than one individual".format(family))
    else:
        print("ANOMALY: FAMILY: US22: All families have unique FIDs due to data storage in dictionaries")

    # List of recent Birthday
    print("\nRecent Birthday Data")
    data = list_upcoming_birthdays(individual_data)
    if len(data) is not 0:
        print("\nUpcoming birthday for: ")
        for birthdays in data:
            print(birthdays.name)
    else:
        print('No upcoming birthday in the next 30 days.')

    # survival from a recent death
    print("\nRecent Death Data")
    data = list_recent_survivals(individual_data, family_data)
    if len(data) > 0:
        print("\nSurvivals List:")
        for d in data.values():
            print("""Individual who passed: {0}, event happened on: {1}\n Survival Spouse: {2} \n Survivals Children: {3}
                   """.format(d.get('name'), d.get('passed'), d.get('spouse_name'), d.get('children')))
    else:
        print("No Recent death with survivals within last 30 days")

if __name__ == '__main__':
    main()
