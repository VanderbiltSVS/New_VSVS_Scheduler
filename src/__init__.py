# contains all of the Volunteer objects, one for each VSVS volunteer
volunteer_list = []

# contains all of the Classroom objects, one for each VSVS group that needs to be created
classroom_list = []
# contains all Classroom objects that are partially filled; starts being filled after partners and drivers have been
# assigned
partially_filled_classrooms = []
# contains all Classroom objects that are empty; starts being used after partners and drivers have been updated
empty_classrooms = []

# minutes to travel one-way to any school
SCHOOL_TRAVEL_TIME = 15
# maximum number of volunteers to allow in a classroom group
MAX_TEAM_SIZE = 4
# minimum acceptable number of volunteers in a classroom group that can visit a classroom
MIN_TEAM_SIZE = 3