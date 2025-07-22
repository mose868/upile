from django.test import TestCase
from users.models import CustomUser
from stations.models import PoliceStation
from police.models import PoliceOfficer
from django.db import IntegrityError

class PoliceOfficerTests(TestCase):
    def setUp(self):
        """Set up test data."""
        self.users = CustomUser.objects.create(
        first_name='Test',
        last_name='User',
        email='test@example.com',
        phone_number='1234567890',
        role='police_officer',
        generated_code='123456'  # Ensure this is not null if required
    )
        self.station = PoliceStation.objects.create(
            station_id = 1,
            station_name='Central Station',
            location='Downtown'
        )


    def test_create_police_officer(self):
        """Test creating a PoliceOfficer."""
        officer = PoliceOfficer.objects.create(
            user = self.users,
            rank='Sergeant',
            contact='1234567890',
            station_id=self.station,
            generated_code='CODE123'
        )
        self.assertEqual(officer.station_id, self.station)
        self.assertEqual(officer.rank, 'Sergeant')

    def test_create_police_officer_missing_user(self):
        """Test creating a PoliceOfficer without a valid CustomUser."""
        with self.assertRaises(IntegrityError):  # Use IntegrityError instead
            PoliceOfficer.objects.create(
                user = None, # This should raise an IntegrityError
                rank= 'Sergeant',
                contact='1234567890',
                station_id=self.station,
                generated_code='CODE123'
            )

