from django.test import TestCase
from police.models import PoliceOfficer
from missing_persons.models import MissingPerson
from stations.models import PoliceStation
from users.models import CustomUser
from django.core.exceptions import ValidationError
from datetime import datetime

class MissingPersonTests(TestCase):
    def setUp(self):
        """Set up test data."""
        # Create a CustomUser instance
        self.user = CustomUser.objects.create(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='test@example.com',
            phone_number='1234567890',
            role='police_officer'
        )

        # Create a PoliceStation instance
        self.police_station = PoliceStation.objects.create(
            station_id = 1,
            station_name='Central Station',
            location='Downtown'
        )

        # Create a PoliceOfficer instance
        self.officer = PoliceOfficer.objects.create(
            user =self.user,  # Assign the CustomUser instance
            rank='Sergeant',
            contact='1234567890',
            station_id=self.police_station,  # Assign the PoliceStation instance
            generated_code='CODE123'
        )

        # Set up valid data for the test
        self.missing_person_data = {
            'id': 1,
            'officer_id': self.officer,
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 25,
            'gender': 'male',
            'contact': '9876543210',
            'image': 'path/to/image.jpg',
            'height': 175.5,
            'weight': 70.0,
            'status':'missing',
            'hair_color': 'brown',
            'eye_color': 'brown',
            'skin_color': 'light_skinned',
            'missing_date': datetime.now(),
            'location': 'Downtown',
            'clothes_worn': 'Blue jeans and a white t-shirt'
        }

    def test_create_missing_person(self):
        """Test creating a MissingPerson with valid data."""
        missing_person = MissingPerson.objects.create(**self.missing_person_data)
        self.assertEqual(missing_person.first_name, 'John')
        self.assertEqual(missing_person.last_name, 'Doe')
        self.assertEqual(missing_person.age, 25)
        self.assertEqual(missing_person.gender, 'male')
        self.assertEqual(missing_person.contact, '9876543210')
        self.assertEqual(missing_person.image, 'path/to/image.jpg')
        self.assertEqual(missing_person.height, 175.5)
        self.assertEqual(missing_person.weight, 70.0)
        self.assertEqual(missing_person.status, 'missing')
        self.assertEqual(missing_person.hair_color, 'brown')
        self.assertEqual(missing_person.eye_color, 'brown')
        self.assertEqual(missing_person.skin_color, 'light_skinned')
        self.assertEqual(missing_person.missing_date, datetime.now().date())
        self.assertEqual(missing_person.location, 'Downtown')
        self.assertEqual(missing_person.clothes_worn, 'Blue jeans and a white t-shirt')
        self.assertEqual(missing_person.officer_id, self.officer)  # Check the officer_id assignment

    def test_create_missing_person_missing_first_name(self):
        """Test creating a MissingPerson with an empty first_name."""
        missing_person_data = {**self.missing_person_data, 'first_name': ''}
        missing_person = MissingPerson(**missing_person_data)
        with self.assertRaises(ValidationError):
            missing_person.full_clean()  # This triggers validation

    def test_create_missing_person_negative_age(self):
        """Test creating a MissingPerson with a negative age."""
        missing_person_data = {**self.missing_person_data, 'age': -1}
        missing_person = MissingPerson(**missing_person_data)
        with self.assertRaises(ValidationError):
            missing_person.full_clean()  # This triggers validation

    def test_create_missing_person_missing_officer(self):
        """Test creating a MissingPerson without an officer."""
        missing_person_data = {**self.missing_person_data, 'officer_id': None}
        with self.assertRaises(ValidationError):
            MissingPerson(**missing_person_data).full_clean()  # This triggers validation

    def test_create_missing_person_missing_contact(self):
        """Test creating a MissingPerson with an empty contact."""
        missing_person_data = {**self.missing_person_data, 'contact': ''}
        missing_person = MissingPerson(**missing_person_data)
        with self.assertRaises(ValidationError):
            missing_person.full_clean()  # This triggers validation

