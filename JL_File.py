from helperFunctions_Sprint2 import is_anniversary_in_next_thirty_days

def list_upcoming_anniversaries(family_data, individual_data):
    anniversaries = []
    for data in family_data.values():
        if data.div is not "NA" or data.div is not "":
            husb = individual_data.get(data.husb_id, "NA")
            wife = individual_data.get(data.wife_id, "NA")
            if (husb is not "NA" and husb.is_alive()) and (wife is not "NA" and wife.is_alive()):
                if (data.marr is not "NA") and is_anniversary_in_next_thirty_days(data.marr):
                    anniversaries.append(data)

    return anniversaries


def list_spouse_large_age_difference(family_data, individual_data):
    double_age_list = []

    for data in family_data.values():
        if data.div is not "NA" or data.div is not "":
            husb = individual_data.get(data.husb_id, "NA")
            wife = individual_data.get(data.wife_id, "NA")
            husb.age = 190
            if husb.age > wife.age and (husb.age / 2) > wife.age:
                double_age_list.append(data)

            if wife.age > husb.age and (wife.age / 2) > husb.age:
                double_age_list.append(data)

        return double_age_list


    # anniversaries = list_upcoming_anniversaries(family_data, individual_data)
    # print_both('US39 - Total number of upcoming anniversaries within 30 days: ', len(anniversaries))
    # if len(anniversaries) > 0:
    #     for family in anniversaries:
    #         day, month, year = str(family.marr).split(" ")
    #         date = month + " " + day
    #         print("US39 - Next anniversary is for {} and {} on {}".format(family.husb, family.wife, date ))
    # else:
    #     print("US39 - No anniversary in the next 30 days")
    #
    # spouse_list = list_spouse_large_age_difference(family_data, individual_data)
    # print_both('US34 - Total number of Spouses with twice as much age: ', len(spouse_list))
    # if len(spouse_list) > 0:
    #     for family in spouse_list:
    #         husb = individual_data.get(family.husb_id, "NA")
    #         wife = individual_data.get(family.wife_id, "NA")
    #         print("US34 - Spouses twice as much age: {}, age: {} and {}, age {}".format(husb.name, husb.age, wife.name, wife.age))
    # else:
    #     print("US34 - No spouses with twice as much age.")