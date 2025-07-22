from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime
from users.models import CustomUser
from stations.models import PoliceStation
from police.models import PoliceOfficer
from missing_persons.models import MissingPerson
from next_of_kin.models import NextOfKin

class NextOfKinTests(TestCase):
    def setUp(self):
        """Set up test data."""
        self.users = CustomUser.objects.create(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            phone_number='1234567890',
            role='police_officer'
        )

        self.station = PoliceStation.objects.create(
            station_id = 1,
            station_name='Central Station',
            location='Downtown'
        )

        self.officer = PoliceOfficer.objects.create(
            user=self.users,
            rank='Sergeant',
            contact='1234567890',
            station_id=self.station,
            generated_code='CODE123'
        )

        self.missing_person = MissingPerson.objects.create(
            id=2,
            officer_id=self.officer,
            first_name='John',
            last_name='Doe',
            age=25,
            gender='male',
            contact='9876543210',
            image='path/to/image.jpg',
            height=175.5,
            weight=70.0,
            status='missing',
            hair_color='brown',
            eye_color='brown',
            skin_color='light_skinned',
            missing_date=datetime.now(),
            location='Downtown',
            clothes_worn='Blue jeans and a white t-shirt'
        )

        self.valid_next_of_kin_data = {
            'missing_person_id': self.missing_person,
            'first_name': 'Jane',
            'last_name': 'Doe',
            'address': '123 Main St',
            'relationship': 'Sister',
            'contact': '0987654321',
            'alternative_contact': '0123456789'
        }

    def test_create_next_of_kin_valid(self):
        """Test creating a NextOfKin with valid data."""
        next_of_kin = NextOfKin.objects.create(**self.valid_next_of_kin_data)
        self.assertEqual(next_of_kin.first_name, 'Jane')
        self.assertEqual(next_of_kin.last_name, 'Doe')
        self.assertEqual(next_of_kin.address, '123 Main St')
        self.assertEqual(next_of_kin.relationship, 'Sister')
        self.assertEqual(next_of_kin.contact, '0987654321')
        self.assertEqual(next_of_kin.alternative_contact, '0123456789')
        self.assertEqual(next_of_kin.missing_person_id, self.missing_person)

    def test_create_next_of_kin_missing_first_name(self):
        """Test creating a NextOfKin with an empty first_name."""
        with self.assertRaises(ValidationError) as context:
            next_of_kin = NextOfKin(
                **{**self.valid_next_of_kin_data, 'first_name': ''}  # Invalid first_name
            )
            next_of_kin.full_clean()  # This triggers validation
        self.assertIn('First name and last name cannot be blank or whitespace', str(context.exception))

    def test_create_next_of_kin_missing_last_name(self):
        """Test creating a NextOfKin with an empty last_name."""
        with self.assertRaises(ValidationError) as context:
            next_of_kin = NextOfKin(
                **{**self.valid_next_of_kin_data, 'last_name': ''}  # Invalid last_name
            )
            next_of_kin.full_clean()  # This triggers validation
        self.assertIn('First name and last name cannot be blank or whitespace', str(context.exception))

    def test_create_next_of_kin_invalid_contact_length(self):
        """Test creating a NextOfKin with a contact number that is too short."""
        with self.assertRaises(ValidationError) as context:
            next_of_kin = NextOfKin(
                **{**self.valid_next_of_kin_data, 'contact': '123456789'}  # Invalid contact length
            )
            next_of_kin.full_clean()  # This triggers validation
        self.assertIn('Contact number must be between 10 and 15 characters', str(context.exception))

    def test_create_next_of_kin_invalid_alternative_contact_length(self):
        """Test creating a NextOfKin with an alternative contact number that is too short."""
        with self.assertRaises(ValidationError) as context:
            next_of_kin = NextOfKin(
                **{**self.valid_next_of_kin_data, 'alternative_contact': '12345'}  # Invalid alternative_contact length
            )
            next_of_kin.full_clean()  # This triggers validation
        self.assertIn('Alternative contact must be at least 10 characters', str(context.exception))

    def test_create_next_of_kin_missing_contact(self):
        """Test creating a NextOfKin with an empty contact."""
        with self.assertRaises(ValidationError) as context:
            next_of_kin = NextOfKin(
                **{**self.valid_next_of_kin_data, 'contact': ''}  # Invalid contact
            )
            next_of_kin.full_clean()  # This triggers validation
        self.assertIn('This field cannot be blank.', str(context.exception))

    def test_create_next_of_kin_alternative_contact_unknown(self):
        """Test creating a NextOfKin with the default value 'Unknown' for alternative_contact."""
        next_of_kin = NextOfKin.objects.create(
            **{**self.valid_next_of_kin_data, 'alternative_contact': 'Unknown'}  # Default value
        )
        self.assertEqual(next_of_kin.alternative_contact, 'Unknown')

