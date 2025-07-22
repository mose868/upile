from django.test import TestCase
from django.core.exceptions import ValidationError
from mortuary.models import Mortuary

class MortuaryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Create a Mortuary instance for testing."""
        cls.mortuary = Mortuary.objects.create(
            id=1,
            mortuary_name='Central Mortuary',
            location='Downtown'
        )
    
    def test_mortuary_creation(self):
        """Test the creation of a Mortuary instance."""
        mortuary = Mortuary.objects.get(id=1)
        self.assertEqual(mortuary.mortuary_name, 'Central Mortuary')
        self.assertEqual(mortuary.location, 'Downtown')
    
    def test_string_representation(self):
        """Test the string representation of a Mortuary instance."""
        mortuary = Mortuary.objects.get(id=1)
        self.assertEqual(str(mortuary), 'Central Mortuary')

    def test_mortuary_creation_unhappy(self):
        """Unhappy path: Test creating a Mortuary instance with invalid data."""

        # Test with a duplicate ID
        Mortuary.objects.create(
            id=2,
            mortuary_name='East Side Mortuary',
            location='Uptown'
        )
        try:
            mortuary = Mortuary(
                id=1,  # This ID already exists
                mortuary_name='New Mortuary',
                location='Suburban'
            )
            mortuary.full_clean()  # Validate the instance
            self.fail('ValidationError not raised')  # Fail the test if no exception is raised
        except ValidationError:
            pass  # Expected outcome

        # Test with empty mortuary_name
        try:
            mortuary = Mortuary(
                id=3,
                mortuary_name='',  # Invalid: Empty name
                location='Suburban'
            )
            mortuary.full_clean()  # Validate the instance
            self.fail('ValidationError not raised')  # Fail the test if no exception is raised
        except ValidationError:
            pass  # Expected outcome

        # Test with mortuary_name exceeding max_length
        try:
            mortuary = Mortuary(
                id=4,
                mortuary_name='A' * 51,  # Exceeds max_length of 50
                location='Suburban'
            )
            mortuary.full_clean()  # Validate the instance
            self.fail('ValidationError not raised')  # Fail the test if no exception is raised
        except ValidationError:
            pass  # Expected outcome

        # Test with location exceeding max_length
        try:
            mortuary = Mortuary(
                id=5,
                mortuary_name='Valid Mortuary Name',
                location='L' * 51  # Exceeds max_length of 50
            )
            mortuary.full_clean()  # Validate the instance
            self.fail('ValidationError not raised')  # Fail the test if no exception is raised
        except ValidationError:
            pass  # Expected outcome

    def test_string_representation_unhappy(self):
        """Unhappy path: Test the __str__ method with invalid names."""
        mortuary = Mortuary.objects.create(
            id=6,
            mortuary_name='',  # Empty name
            location='Suburban'
        )
        self.assertEqual(str(mortuary), '')  # Expect an empty string

