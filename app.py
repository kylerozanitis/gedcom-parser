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

from helperFunctions_Sprint1 import read_data_file, deceased_list, agemorethan_150, print_both
from helperFunctions_Sprint1 import check_marriage_before_divorce, check_marriage_before_death, check_spouses_exist
from helperFunctions_Sprint1 import death_before_birth, birth_before_marriage, divorce_before_death
from helperFunctions_Sprint1 import list_recent_births, list_recent_death, fewer_than15_siblings, check_unique_ids, check_marriage_status
from helperFunctions_Sprint2 import list_recent_survivals, living_married_list, list_upcoming_birthdays, validate_child_birth
from helperFunctions_Sprint2 import check_parents_not_too_old, check_multiple_births, marriage_after_14
from helperFunctions_Sprint2 import validate_childBirth_with_parentsDeath
from helperFunctions_Sprint3 import single_over_30, multiple_births, validate_male_lastname, validate_unique_name_birthdate
from helperFunctions_Sprint3 import siblings_should_not_marry, correct_gender_for_role, unique_first_names, reject_illegal_dates
from helperFunctions_Sprint3 import siblings_should_not_marry, correct_gender_for_role
from helperFunctions_Sprint4 import sibling_spacing, list_orphans, unique_families_by_spouses, order_siblings_by_age
from helperFunctions_Sprint4 import list_upcoming_anniversaries, list_spouse_large_age_difference
from helperFunctions_Sprint4 import no_bigamy, not_to_marry_firstCousin

import sys
from datetime import datetime
from prettytable import PrettyTable
from classes import individualPerson, familyClass

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

    # Creating the text file each time
    text_file = open("Output.txt", "w")
    text_file.write("GEDCOM Parser - Kyle Rozanitis, Jose Lara, Kshiti Rana, Pratik Shah \n \n")
    text_file.close()
    
    print_both('Individuals')
    t = PrettyTable(['ID', 'Name', 'Gender', 'Birthday','Age','Alive','Death','Child','Spouse'])
    for obj in individual_data.values():
        t.add_row(obj.pt_row())
    print_both(t)
    
    print_both('Families')
    t = PrettyTable(['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name','Children'])
    for obj in family_data.values():
        t.add_row(obj.pt_row())
    print_both(t)
    
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
                print_both("ERROR: Individual: US01: " + str(ids) +" : Birthday " + str(individual_data[ids].birt) + " cannot occur before current date " + str(current_date))
            elif msg == 'death':
                print_both("ERROR: Individual: US01: " + str(ids) +" : Death date " + str(individual_data[ids].deat) + " cannot occur before current date " + str(current_date))
            elif msg == 'marriage':
                print_both("ERROR: Family: US01: " + str(ids) +" : Marriage date " + str(family_data[ids].marr) + " cannot occur before current date " + str(current_date))
            elif msg == 'divorce':
                print_both("ERROR: Family: US01: " + str(ids) +" : Divorce date " + str(family_data[ids].div) + " cannot occur before current date " + str(current_date))
            elif msg == 'not born':
                print_both("ERROR: Individual: US01: " + str(ids) + " : " + str(individual_data[ids].name) + " is not born yet")
            elif msg == 'not married':
                print_both("ERROR: Family: US01: " + str(ids) +" Not married ")
            else:
                print_both("ERROR: Individual: US03: " + str(ids) +" : Death date " + str(individual_data[ids].deat) + " cannot occur before birthday " + str(individual_data[ids].birt))
    
    #US02 - Checks for birth before marriages if marriage happens before birth, individual will be removed from family
    for obj in birth_before_marriage(family_data, individual_data):
        print_both("ERROR: INDIVIDUAL: US02: {} Birth occurs before marriage".format(obj.fid))
    
    # US04 Print out list of families with divorce occuring before marriage
    problem_families = check_marriage_before_divorce(family_data)
    if len(problem_families) > 0:
        for item in problem_families:
            family = family_data[item]
            if family.marr == "NA":
                print_both("ERROR: FAMILY: US04: {}: Marriage date does not exist".format(family.fid))
            else:
                print_both("ERROR: FAMILY: US04: {}: Divorce date {} occurs before marriage date {}".format(family.fid, family.div, family.marr))

    # US05 Print out list of families with death of a spouse occuring before marriage
    prob_families = check_marriage_before_death(family_data, individual_data)
    if len(prob_families) > 0:
        for item in prob_families:
            family = family_data[item]
            husband = individual_data[family.husb_id]
            wife = individual_data[family.wife_id]

            if family.marr == "NA":    
                print_both("ERROR: FAMILY: US05: {}: Marriage date does not exist".format(family.fid))
            elif husband.alive == False:
                print_both("ERROR: FAMILY: US05: {}: Husband death date {} occurs before marriage date {}".format(family.fid, husband.deat, family.marr))
            elif wife.alive == False:
                print_both("ERROR: FAMILY: US05: {}: Wife death date {} occurs before marriage date {}".format(family.fid, wife.deat, family.marr))
    
    #US06 - divorce before death
    divorce_before_death(family_data,individual_data)
    
    #US07 - age more than 150
    agemorethan_150(individual_data)

    # US08 - Children should be born after marriage of parents (and not more than 9 months after their divorce)
    marr_error_entries, div_error_entries = validate_child_birth(individual_data,family_data)
    for fid, uid in marr_error_entries.items():
        print_both("ANOMALY: FAMILY: US08: " + str(fid) + ": Birthday " + str(individual_data[uid].birt) + " of child " + str(uid) + " occurs before marriage " + str(family_data[fid].marr))
    for fid, uid in div_error_entries.items():
        print_both("ANOMALY: FAMILY: US08: " + str(fid) + ": Birthday " + str(individual_data[uid].birt) + " of child " + str(uid) + " occurs after more than 9 months of divorce " + str(family_data[fid].div))    
    
    
    #US09 - Child should be born before death of mother and before nine months after death of father
    child_mother_error, child_father_error = validate_childBirth_with_parentsDeath(individual_data, family_data)
    for fid, uid in child_mother_error.items():
        print_both("ERROR: FAMILY: US09: " + str(fid) + ": Birthday " + str(individual_data[uid[0]].birt) + " of child " + str(uid[0]) + " should be born before death " + str(individual_data[uid[1]].deat) + " of mother " + str(uid[1]))
    for fid, uid in child_father_error.items():
        print_both("ERROR: FAMILY: US09: " + str(fid) + ": Birthday " + str(individual_data[uid[0]].birt) + " of child " + str(uid[0]) + " should be born before 9 months after death " + str(individual_data[uid[1]].deat) + " of father " + str(uid[1]))    

    # US10 - Marriage After 14
    problem_fam_dict = marriage_after_14(family_data, individual_data)
    if len(problem_fam_dict) > 0:
        for k, v in problem_fam_dict.items():
            if v[0] == "M":
                print_both("ANOMALY: FAMILY: US10: Husband {} in Family {} is married before 14 years old".format(k, v[1]))
            else:
                print_both("ANOMALY: FAMILY: US10: Wife {} in Family {} is married before 14 years old".format(k, v[1]))
                
    # US11 --- Marriage should not occur during marriage to another spouse
    error_entries = no_bigamy(family_data)
    if len(error_entries) > 0:
        for uid, uid_spouse_list in error_entries.items():
            organize_id_name = ""
            req_list = []
            for spouse_id in uid_spouse_list[:-1]:
                req_list.append(spouse_id)
            for element in range(len(req_list)):
                organize_id_name += req_list[element] +": " + individual_data[req_list[element]].name + ", "
            organize_id_name = organize_id_name + str(uid_spouse_list[-1]) + ": " + individual_data[uid_spouse_list[-1]].name

            print_both("ERROR: FAMILY: US11: Individual UID: " +str(uid) +": " +individual_data[uid].name + " has " +str(len(uid_spouse_list)) +" spouses -- " +organize_id_name)                
    
    # US12 - Parents Not Too Old - Mother should be less than 60 years older than her children and father should be less than 80 years older than his children
    problem_families_dict = check_parents_not_too_old(family_data, individual_data)
    if len(problem_families_dict) > 0:
        for k, v in problem_families_dict.items():
            if v[0] == "M":
                print_both("ERROR: FAMILY: US12: Parent {} named {} born on {} is more than 80 years older than child {} named {} born on {} in family {}".format(v[1], v[2], v[3], v[4], v[5], v[6], k))
            else:
                print_both("ERROR: FAMILY: US12: Parent {} named {} born on {} is more than 60 years older than child {} named {} born on {} in family {}".format(v[1], v[2], v[3], v[4], v[5], v[6], k))

    #US13
    sibling_spacing(family_data, individual_data)

    # US14 - Multiple Births <= 5 - No more than five siblings should be born at the same time
    problem_fams_dict = check_multiple_births(family_data, individual_data)
    if len(problem_fams_dict) > 0:
        for k, v in problem_fams_dict.items():
            print_both("ERROR: FAMILY: US14: Family {} has more than 5 siblings born on the same day: {}".format(k, v))

    # US15 -- There should be fewer than 15 siblings in a family
    fid_list = fewer_than15_siblings(family_data)
    for fid in fid_list:
        print_both("ERROR: FAMILY: US15: " + str(fid) + " has more than 15 siblings")
    
    # US16 --- All male members of the family should have the same last name
    invaild_lastname_error = validate_male_lastname(individual_data, family_data)
    for fid, details in invaild_lastname_error.items():
        print_both("ERROR: FAMILY: US16: Lastname " + str(details[2]) + " of " + str(details[1]) + " is not same as family's last name " + str(details[0]))            

    #US18 - List Siblings should not marry
    family = siblings_should_not_marry(family_data, individual_data)
    print_both('US18 - Total number of marriage with their sibling: ', len(family))
    if len(family) > 0:
        for person in family:
            print_both("""Individual Name who marry their sibling: {0} """.format(person.name))
    else:
        print_both("No Siblings are married")
    
    # US19 --- First cousins should not marry one another
    error_entries = not_to_marry_firstCousin(family_data)
    if len(error_entries) > 0:
        for fid, married_cousin_list in error_entries.items():
            print_both("ERROR: FAMILY: US19: First cousins UID: " + str(married_cousin_list[0]) +" " +individual_data[married_cousin_list[0]].name +" and " + str(married_cousin_list[1]) +" " +individual_data[married_cousin_list[1]].name +" are married to each other in Family: " +str(fid))
    
    # US21 - Husband in family should be male and wife in family should be female
    prob_fams_dict = correct_gender_for_role(family_data, individual_data)

    if len(prob_fams_dict) > 0:
        for k, v in prob_fams_dict.items():
            if v[0] == "NA":
                print_both("ANOMALY: FAMILY: US21: Spouse {} in Family {} gender listed as {} but expected {}".format(v[2], k, v[0], v[1]))
            else:
                print_both("ERROR: FAMILY: US21: Spouse {} in Family {} gender listed as {} but expected {}".format(v[2], k, v[0], v[1]))

    # US22 Unique IDs - All individual IDs should be unique and all family IDs should be unique
    problem_indis, problem_fams = check_unique_ids(individual_data, family_data)
    if len(problem_indis) > 0:
        for individual in problem_indis:
            print_both("ERROR: INDIVIDUAL: US22: {} has been used for more than one individual".format(individual))
    else:
        print_both("ANOMALY: INDIVIDUAL: US22: All individuals have unique UIDs due to data storage in dictionaries")

    if len(problem_fams) > 0:
        for family in problem_fams:
            print_both("ERROR: FAMILY: US22: {} has been used for more than one individual".format(family))
    else:
        print_both("ANOMALY: FAMILY: US22: All families have unique FIDs due to data storage in dictionaries")
    
    # US23 --- No more than one individual with the same name and birth date should appear in a GEDCOM file
    error_entries = validate_unique_name_birthdate(individual_data)
    if len(error_entries) > 0:  
        for each_error_list in error_entries:
            separate_uid = ""
            req_list = []
            for uid in each_error_list[:-2]:
                req_list.append(uid)
            for element in range(len(req_list) - 1):
                separate_uid += req_list[element] + ", "
            separate_uid = separate_uid + str(req_list[-1])
            print_both("WARNING: Individual: US23: " + str(len(req_list)) + " individual(s) named " + str(each_error_list[-2]) + " born on " + str(each_error_list[-1]) + ": " + str(separate_uid))        

    # US24 - No more than one family with the same spouses by name and the same marriage date should appear in a GEDCOM file
    non_unique_families = unique_families_by_spouses(family_data)
    if len(non_unique_families) > 0:
        for family in non_unique_families:
            print_both("ERROR: FAMILY: US24: Family {} and Family {} have the same husband name, wife name, and marriage date".format(family[0], family[1]))
  
    # US25 - No more than one child with the same name and birth date should appear in a family
    problem_children_list = unique_first_names(family_data, individual_data)
    
    if len(problem_children_list) > 0:
        for family in problem_children_list:
            print_both("ERROR: FAMILY: US25: Multiple children in Family {} have the same birthday and name".format(family))

    # US28 - List siblings in families by decreasing age
    children_dict = order_siblings_by_age(family_data, individual_data)
    for k, v in children_dict.items():
        if len(v) > 1:
            print_both("ANNOUNCEMENT: FAMILY: US28: The children of Family {} ordered by age: {}".format(k, v))
        elif len(v) == 1:
            print_both("ANNOUNCEMENT: FAMILY: US28: Family {} only has one child: {}".format(k, v))
        else:
            print_both("ANNOUNCEMENT: FAMILY: US28: Family {} does not have any children".format(k))

    #US29 - Get list of individuals who passed
    data = deceased_list(individual_data)
    print_both('US29 - Total number of deceased individuals: ',len(data))
    for person in deceased_list(individual_data):
        print_both("Name: {1} Date Passed: {0}".format(person.deat, person.name ))

    #US30 - list living married
    living_married = living_married_list(family_data, individual_data)
    print_both('US30 - Total number of living married: ',len(living_married))
    for person in living_married:
        print_both("ID: {0} Name: {1}".format(person.uid ,person.name))

    #US31 - List singles over 30
    single = single_over_30(family_data, individual_data)
    print_both('US31 - Total number of singles over 30: ',len(single))
    for person in single:
        print_both("Name: {0} Age: {1}".format(person.name, person.age))

    #US32 - List multiple birth
    list_multiple_birth = multiple_births(family_data, individual_data)
    print_both('US32 - Total number of multiple births: ',len(list_multiple_birth))
    for person in list_multiple_birth:
        print_both("Family id: {0} Birth on: {2} Name: {1}".format(''.join(person.famc), person.name, person.birt))

    #US33 - List Orphans
    orphans = list_orphans(family_data, individual_data)
    print_both('US33 - Total number of Orphans: ',len(orphans))
    for person in orphans:
        print_both("Name: {0} Age: {1}".format(person.name, person.age))

    #US34 - List large age Difference
    spouse_list = list_spouse_large_age_difference(family_data, individual_data)
    print_both('US34 - Total number of Spouses with twice as much age: ', len(spouse_list))
    if len(spouse_list) > 0:
        for family in spouse_list:
            husb = individual_data.get(family.husb_id, "NA")
            wife = individual_data.get(family.wife_id, "NA")
            print_both("US34 - Spouses twice as much age: {}, age: {} and Spouse is {}, age {}".format(husb.name, husb.age, wife.name, wife.age))
    else:
        print_both("US34 - No spouses with twice as much age.")

    #US35 - List recent birthdays
    birth_recently = list_recent_births(individual_data)
    print_both('US35 - Total number of recent births: ',len(birth_recently))
    if len(birth_recently) == 0:
        print_both("No recent Birth")
    else:
        for individual in birth_recently:
            print_both("Name: {0} Birth on: {1}".format(individual.name, individual.birt))

    #US36 - List recent deaths
    death_recently = list_recent_death(individual_data)
    print_both('US36 - Total number of recent deaths: ',len(death_recently))
    if len(death_recently) == 0:
        print_both("No recent Death")
    else:
        for individual in death_recently:
            print_both("Name: {0} Death on: {1}".format(individual.name, individual.deat))
    
    #US37 - survival from a recent death
    data = list_recent_survivals(individual_data, family_data)
    print_both('US37 - Total number of recent survivors: ',len(data))
    if len(data) > 0:
        print_both("Survivals List:")
        for d in data.values():
            print_both("""Individual who passed: {0}, event happened on: {1}\n Survival Spouse: {2} \n Survivals Children: {3}
                   """.format(d.get('name'), d.get('passed'), d.get('spouse_name'), d.get('children')))
    else:
        print_both("No Recent death with survivals within last 30 days")

    #US38 - List of Upcoming Birthday
    data = list_upcoming_birthdays(individual_data)
    print_both('US38 - Total number of Upcoming birthdays: ',len(data))
    if len(data) is not 0:
        for birthdays in data:
            print_both("Name: {0}, Birth on: {1}".format(birthdays.name, birthdays.birt))
    else:
        print_both('No upcoming birthday in the next 30 days.')

    #US39 - List upcoming anniversaries
    anniversaries = list_upcoming_anniversaries(family_data, individual_data)
    print_both('US39 - Total number of upcoming anniversaries within 30 days: ', len(anniversaries))
    if len(anniversaries) > 0:
        for family in anniversaries:
            day, month, year = str(family.marr).split(" ")
            date = month + " " + day
            print_both("US39 - Next anniversary is for {} and {} on {}".format(family.husb, family.wife, date ))
    else:
        print_both("US39 - No anniversary in the next 30 days")
    
    #US42 - Check for valid date
    family = siblings_should_not_marry(family_data, individual_data)
    print_both('US42 - Check for valid date: ')
    print("US42 - check for 2/30/2018 is valid: ", reject_illegal_dates('2/30/2018'))
    print("US42 - check for 2/29/2018 is valid: ", reject_illegal_dates('2/29/2018'))
    print("US42 - check for 2/28/2018 is valid: ", reject_illegal_dates('2/28/2018'))
    print("US42 - check for 11/31/2018 is valid: ", reject_illegal_dates('11/31/2018'))
    print("US42 - check for 11/30/2018 is valid: ", reject_illegal_dates('11/30/2018'))
    print("US42 - check for 12/31/2018 is valid: ", reject_illegal_dates('12/31/2018'))












if __name__ == '__main__':
    main()
