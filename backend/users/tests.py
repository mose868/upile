from django.test import TestCase
from django.utils import timezone
from .models import CustomUser, RegistrationCode

class CustomUserTestCase(TestCase):
    def setUp(self):
        """Create a user for testing."""
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass',
            phone_number='1234567890',
        )

    def test_user_creation(self):
        """Test that a user is created successfully and generated_code is set."""
        self.assertIsNotNone(self.user.generated_code)
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_generate_code(self):
        """Test the generate_code method."""
        code = self.user.generate_code()
        self.assertEqual(len(code), 6)
        self.assertTrue(code.isdigit())

    def test_user_role_permissions(self):
        """Test the permissions based on user role."""
        self.user.role = 'police_officer'
        self.assertTrue(self.user.has_permission('view_missing'))
        self.assertFalse(self.user.has_permission('add_unidentified_body'))

        self.user.role = 'mortuary_staff'
        self.assertTrue(self.user.has_permission('add_unidentified_body'))
        self.assertFalse(self.user.has_permission('update_missing'))

    def test_count_by_role(self):
        """Test counting users by role."""
        CustomUser.objects.create_user(username='police1', password='testpass', phone_number='1234567891', role='police_officer')
        CustomUser.objects.create_user(username='mortuary1', password='testpass', phone_number='1234567892', role='mortuary_staff')
        self.assertEqual(CustomUser.count_by_role('police_officer'), 2)
        self.assertEqual(CustomUser.count_by_role('mortuary_staff'), 1)

    def test_user_creation_with_duplicate_phone(self):
        """Test creating a user with a duplicate phone number."""
        with self.assertRaises(Exception):
            CustomUser.objects.create_user(
                username='testuser2',
                password='testpass',
                phone_number='1234567890'
            )

    def test_user_role_permissions_invalid_permission(self):
        """Test checking for an invalid permission."""
        self.user.role = 'police_officer'
        self.assertFalse(self.user.has_permission('non_existent_permission'))

    def test_generate_code_invalid_length(self):
        """Test the generate_code method if it returns an invalid length."""
        code = self.user.generate_code()
        self.assertNotEqual(len(code), 5)  # Ensuring it's not 5

class RegistrationCodeTestCase(TestCase):
    def setUp(self):
        """Create a user and registration code for testing."""
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass',
            phone_number='1234567890',
        )
        self.registration_code = RegistrationCode.objects.create(
            user=self.user,
            code='123456',
            expires_at=timezone.now() + timezone.timedelta(hours=1)
        )


    def test_registration_code_without_expiration(self):
        """Test creating a registration code without expiration."""
        registration_code = RegistrationCode.objects.create(
            user=self.user,
            code='654321',
            expires_at=None
        )
        self.assertIsNone(registration_code.expires_at)
