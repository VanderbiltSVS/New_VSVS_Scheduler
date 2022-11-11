import unittest
from src.applicant import Volunteer
from src.partners import Partners
from src.tests.test_data.sample_data_and_outputs import sample_raw_schedule, free_time_schedule, converted_schedule, \
    partner_1_schedule, partner_2_schedule, partners_combined_schedule, partner_3_schedule


class VolunteerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fake_volunteer = Volunteer(name="John Doe", phone="000-000-000", email="john.doe@vanderbilt.edu",
                                       team_leader_app=True, index=0, imported_schedule=sample_raw_schedule)

    def test_schedule_conversions(self):
        schedule_dict = self.fake_volunteer.convert_imported_list_to_schedule_dict(sample_raw_schedule)
        free_time = self.fake_volunteer.schedule_to_free_time(sample_raw_schedule)
        self.assertEqual(schedule_dict, converted_schedule)
        self.assertEqual(free_time, free_time_schedule)


class PartnersTestCase(unittest.TestCase):
    def test_create_partner_schedule(self):

        # create 3 dummy Volunteer objects for testing
        fake_partner_1 = Volunteer(name="John Doe", phone="000-000-000", email="john.doe@vanderbilt.edu",
                                   team_leader_app=True, index=0, imported_schedule=sample_raw_schedule)
        fake_partner_2 = Volunteer(name="Bob Doe", phone="000-000-000", email="bob.doe@vanderbilt.edu",
                                   team_leader_app=True, index=0, imported_schedule=sample_raw_schedule)
        fake_partner_3 = Volunteer(name="Charles Doe", phone="000-000-000", email="charles.doe@vanderbilt.edu",
                                   team_leader_app=True, index=0, imported_schedule=sample_raw_schedule)

        # Add 3 dummy schedules to each volunteer for testing
        fake_partner_1.free_time = partner_1_schedule
        fake_partner_2.free_time = partner_2_schedule
        fake_partner_3.free_time = partner_3_schedule

        # Create a partner object and test that the create_partner_schedule returns the correct output
        partners = Partners([fake_partner_1, fake_partner_2, fake_partner_3])
        self.assertEqual(partners.create_partner_schedule(), partners_combined_schedule)


if __name__ == '__main__':
    unittest.main()
