from django.test import TestCase
from django.core.exceptions import ValidationError
from stations.models import PoliceStation

class PoliceStationModelTest(TestCase):

    def setUp(self):
        """Set up test data for the PoliceStation model."""
        self.station = PoliceStation.objects.create(
            station_id = 1,
            station_name='Central Police Station',
            location='Downtown'
        )

    def test_police_station_creation(self):
        """Happy path: Test the creation of a PoliceStation instance."""
        station = PoliceStation.objects.get(station_name='Central Police Station')
        self.assertEqual(station.station_name, 'Central Police Station')
        self.assertEqual(station.location, 'Downtown')
    
    def test_string_representation(self):
        """Happy path: Test the string representation of a PoliceStation instance."""
        station = PoliceStation.objects.get(station_name='Central Police Station')
        self.assertEqual(str(station), 'Central Police Station')

    def test_police_station_creation_unhappy(self):
        """Unhappy path: Test creating a PoliceStation instance with invalid data."""

        # Test with missing station name
        with self.assertRaises(ValidationError):
            station = PoliceStation(
                location='Suburb'
            )
            station.full_clean()  # Trigger validation

        # Test with missing location
        with self.assertRaises(ValidationError):
            station = PoliceStation(
                station_name='North Police Station'
            )
            station.full_clean()  # Trigger validation

