# TODO: sort robotics?
# TODO: add global constants + change methods so scheduling times collected can be changed in the future (like constants for start time (7:15), time period (15 min), and periods collected (34))
# TODO: group_number == -1 means unassigned

import csv
import src.volunteer
import src.partners
import src.classroom
import src.assign
import src.convertSchedule

MAX_TEAM_SIZE = 4
MIN_TEAM_SIZE = 4


# row[2] is first name, row[3] is last name, row[4] is phone number, row[5] is email, row[9] is robotics interest,
# row[10] is special needs interest, row[12] is team leader interest, row[13] is previous team leader, row[14] is car,
# row[15] is car passengers, row[16-49] are 15-min time slots that range from from 7:15am to 3:45pm


volunteer_list = []  # list of all the volunteers that will be iterated through
classroom_list = []  # list of all the classrooms to to assign groups to

def main():



    #  IMPORT FILE DATA

    # import individual application data
    with open('../data/individuals.csv') as individuals_csv:  # opens individuals.csv as individuals_csv
        csv_reader = csv.reader(individuals_csv, delimiter=',')  # csv_reader will divide individuals_csv by commas
        for row in csv_reader:

            # creates Volunteer objects and adds them to volunteer_list, indices correspond to columns of responses in
            # individuals.csv
            volunteer_list.append(src.volunteer.Volunteer(row[2], row[3], row[4], row[5], row[9], row[10], row[12],
                                                          row[13], row[14], row[15],
                                                          src.convertSchedule.convert_to_schedule_array(row[16:49])))

    # probably don't need anymore (if we decide individuals and partners will share application)
    # # import partner application data
    # with open('../data/partners.csv') as partners_csv:  # opens partners.csv as partners_csv
    #     csv_reader = csv.reader(partners_csv, delimiter=',')  # csv_reader will divide partners_csv by commas
    #     for row in csv_reader:
    #         volunteer_list[row[1]].add_partners(row[2], row[3], row[4], row[6])  # calling addPartner method on line of volunteer that signed partners up (volunteer_list[row[1]])

    # import classroom information
    with open('../data/classrooms.csv') as classrooms_csv:  # opens classrooms.csv as classrooms_csv
        csv_reader = csv.reader(classrooms_csv, delimiter=',')  # csv_reader will divide classrooms_csv by commas
        for row in csv_reader:
            # creates Classroom object
            classroom_list.append(src.classroom.Classroom(row[2], row[3], row[4], row[6], row[9], row[11], row[12], row[13]))

    # set preassigned volunteers in classroom data before assigning
    for volunteer in volunteer_list:
        if volunteer.group_number != -1:
            classroom_list[volunteer.group_number].add_volunteer()


    # ASSIGN VOLUNTEERS

    # assign partners
    for volunteer in volunteer_list:
        if volunteer.group_number == -1 and volunteer.partners:
            src.assign.assign_partners(volunteer)  # adds all partners to same team

    # assign drivers
    for volunteer in volunteer_list:
        if volunteer.group_number == -1 and volunteer.car_passengers >= MIN_TEAM_SIZE:  # figure this out: keep their group under car capacity or don't allow car unless it is TEAM_MAX_MEMBERS
            src.assign.assign_group(driver_list, classroom_list)

    # for unassigned people, count classrooms they can make
    for volunteer in volunteer_list:
        if volunteer.group_number == -1:
            for classroom in classroom_list:
                if src.assign.volunteer_can_make_class(volunteer, classroom):
                    volunteer.increment_classrooms_possible()

    # creates lists of partially filled and empty classrooms
    empty_classrooms = []
    nonempty_classrooms = []
    for classroom in classroom_list:
        if classroom.volunteers_assigned == 0:
            empty_classrooms.append(classroom)
        elif classroom.volunteers_assigned < MAX_TEAM_SIZE:
            nonempty_classrooms.append(classroom)

    # assign unassigned applied_t_leaders AFTER sorting them by availability
    # (from fewest to most classrooms they can make)
    applied_t_leader_list = []
    for volunteer in volunteer_list:
        if volunteer.group_number == -1 and volunteer.applied_t_leader:
            applied_t_leader_list.append(volunteer)
    src.assign.assign_group(src.assign.sort_by_availability(applied_t_leader_list), classroom_list)

    # TODO: copy results of group assignments from applied_t_leader_list to volunteer_list

    # assign everyone else still unassigned AFTER sorting them by availability
    # (from fewest to most classrooms they can make)
    unsorted_list = []
    for volunteer in volunteer_list:
        if volunteer.group_number == -1:
            unsorted_list.append(volunteer)
    src.assign.assign_group(src.assign.sort_by_availability(unsorted_list), classroom_list)

    # TODO: copy results of group assignments from unsorted_list to volunteer_list


    # OUTPUT RESULTS

    with open('../results/assignments.csv') as assignments_csv:
        csv_writer = csv.writer(assignments_csv, delimiter=',')
        for volunteer_id in range(1, len(volunteer_list)):
            csv_writer.writerow(
                [volunteer_id, volunteer_list[volunteer_id].group_number, volunteer_list[volunteer_id].first,
                 volunteer_list[volunteer_id].last, volunteer_list[volunteer_id].email,
                 volunteer_list[volunteer_id].phone])


# runs main
if __name__ == "__main__":
    main()
