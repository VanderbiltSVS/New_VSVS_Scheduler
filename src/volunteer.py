import src.classroom
import src.convert_schedule
import src.global_attributes


class Volunteer:
    def __init__(self, first, last, phone, email, year_in_school, major, robotics_interest, special_needs_interest,
                 applied_t_leader, board, driver, car_passengers, imported_schedule, is_in_person):
        """ constructor for volunteer object

        :param first: first name
        :type first: str
        :param last: last name
        :type last: str
        :param phone: phone number
        :type phone: str
        :param email: Vanderbilt email address
        :type email: str
        :param year_in_school: year at Vanderbilt (First-Year, Sophomore, Junior, Senior, Graduate)
        :type year_in_school: str
        :param major: major at Vanderbilt
        :type major: str
        :param robotics_interest: is this volunteer interested in teaching robotics?
        :type robotics_interest: bool
        :param special_needs_interest: is this volunteer interested in working with students with special needs?
        :type special_needs_interest: bool
        :param applied_t_leader: did this volunteer apply to be a team leader?
        :type applied_t_leader: bool
        :param board: is this volunteer on VSVS Board?
        :type board: bool
        :param driver: is this volunteer a driver?
        :type driver: bool
        :param car_passengers: if driver, how many passengers in car (not including driver)
        :type car_passengers: str
        :param imported_schedule: raw schedule data from Google Form
        :type imported_schedule: list[str]
        :param is_in_person: is this volunteer on-campus/in-person?
        :type is_in_person: bool
        """
        self.first = first
        self.last = last
        self.phone = phone
        self.email = email.lower()
        self.year_in_school = year_in_school
        # TODO: we don't really need major... should we just remove this?
        self.major = major
        self.robotics_interest = robotics_interest
        self.special_needs_interest = special_needs_interest

        # if volunteer applied to be a team leader
        self.applied_t_leader = applied_t_leader
        self.board = board

        # people a driver can drive (not including driver)
        if car_passengers == '':
            self.car_passengers = 0
        elif car_passengers == '4+':
            self.car_passengers = 4
        else:
            self.car_passengers = int(car_passengers)

        # if they have a car that can carry the MAX_TEAM_SIZE
        # self.driver = driver
        # they only count as drivers if they can carry a full load of passengers?
        self.driver = (self.car_passengers + 1 >= src.global_attributes.MAX_TEAM_SIZE)

        # TODO Convert directly from input schedule to free_time_array in one method. Don't need convert_to_schedule_array.
        # array containing an index for each 15-min block between the times of 7:15am-3:45pm, Monday through Thursday
        # (indexes 0-33 are Monday 7:15am to 3:45pm, 34-67 are Tuesday 7:15-3:45, 68-101 are Wednesday, etc.)
        # value at an index is 1 if volunteer is available at that time and 0 if they are busy
        self.schedule_array = src.convert_schedule.convert_to_schedule_array(imported_schedule)

        # array containing an index for each 15-min block between the times of 7:15am-3:45pm, Monday through Thursday
        # (indexes 0-33 are Monday 7:15am to 3:45pm, 34-67 are Tuesday 7:15-3:45, 68-101 are Wednesday, etc.)
        # value at an index is the minutes of consecutive free time the volunteer has starting at that time
        self.free_time_array = src.convert_schedule.convert_to_free_time_array(self.schedule_array)

        # group number of -1 means not assigned to a group
        self._group_number = -1

        # The number of other partners (NOT including this Volunteer) Volunteer applied with, set in add_partners
        # method. This is only set in the Volunteer object of the first partner in the group.
        self.partners = 0

        # Index of each of this volunteer's partners in volunteer_list.
        # Set in add_partners method. This is only set in the Volunteer object of the first partner in the group.
        self.partner_indexes = []

        # free_time_array for a partner group.
        # This is only set in the Volunteer object of the first partner in the group.
        self.partner_free_time_array = 0

        # Was the volunteer assigned to be the driver for their group?
        self.assigned_driver = False

        # Was the volunteer assigned to be their group's team leader?
        self.assigned_t_leader = False

        # Number of classrooms the volunteer can make according to their schedule.
        # Set after partners and drivers are assigned.
        self.classrooms_possible = 0

        # True if the volunteer is in person, False if they are remote.
        self.is_in_person = is_in_person

    # group number is a property (special type of Python variable) so we can have a custom setter method
    @property
    def group_number(self):
        return self._group_number

    @group_number.setter
    def group_number(self, value):
        """

        :param value: new group number
        :type value: int
        :raises ValueError: if re-assinging an already assigned volunteer
        :return:
        """
        if self._group_number != -1:
            raise ValueError("You are changing the group number of an already assigned volunteer.")
        self._group_number = value

    @group_number.deleter
    def group_number(self):
        del self._group_number

    def add_partners(self, *args):
        """ Sets the partners, partner_indexes, and partner_free_time_array attributes for the Volunteer object of
        the first partner in the group (the self object).

        :param args: any number of emails for the partners
        :type args: (str)
        :raises ValueError: if # of partners > max team size
        :return: None
        """

        for partner_email in args:
            partner_email = partner_email.strip().lower()
            found = False
            # if not empty string
            if partner_email:
                for i, volunteer in enumerate(src.global_attributes.volunteer_list):
                    if volunteer.email == partner_email:
                        self.partner_indexes.append(i)
                        found = True

                if not found:
                    print(f"WARNING: {partner_email} from {self.email}'s volunteer group was not found in the "
                          f"individual application data.")

        # count number of partners
        self.partners = len(self.partner_indexes)

        if self.partners + 1 > src.global_attributes.MAX_TEAM_SIZE:
            raise ValueError(f'{self.partners} is too many partners.')

        # If all four partners are remote, they cannot be assigned in a group together.
        # At least one volunteer in each group must be in person.
        if self.partners == 2 and not self.is_in_person and not src.global_attributes.volunteer_list[
            self.partner_indexes[0]].is_in_person and not src.global_attributes.volunteer_list[
            self.partner_indexes[1]].is_in_person and not src.global_attributes.volunteer_list[
            self.partner_indexes[2]].is_in_person:
            print("WARNING:" + self.email + "'s partner group cannot be grouped together because they are all remote.")

        elif self.partners != 0:
            # if it is fine, then generate partner free time array
            self.partner_free_time_array = src.convert_schedule.create_partner_schedule(self.schedule_array,
                                                                                        self.partners,
                                                                                        self.partner_indexes)

    def increment_classrooms_possible(self):
        self.classrooms_possible += 1

    # Designate the volunteer as the team leader for their group
    def assign_t_leader(self):
        self.assigned_t_leader = True

    def __str__(self):
        return self.first + ' ' + self.last

    def __repr__(self):
        return self.first + ' ' + self.last
