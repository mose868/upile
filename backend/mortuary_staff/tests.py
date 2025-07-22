# from django.test import TestCase
# from django.core.exceptions import ValidationError
# from mortuary.models import Mortuary
# from mortuary_staff.models import MortuaryStaff  
# from users.models import CustomUser

# class MortuaryStaffModelTest(TestCase):

#     @classmethod
#     def setUpTestData(self):
#         """Create test data for Mortuary and MortuaryStaff."""
#         self.mortuary = Mortuary.objects.create(
#             id=1,
#             mortuary_name='Central Mortuary',
#             location='Downtown'
#         )

#         self.users = CustomUser.objects.create(
#         first_name='Test',
#         last_name='User',
#         email='test@example.com',
#         phone_number='1234567890',
#         role='police_officer',
#         generated_code='123456'  # Ensure this is not null if required
#     )
    
#     def test_mortuary_staff_creation(self):
#         """Test the creation of a MortuaryStaff instance."""
#         staff = MortuaryStaff.objects.create(
#             staff_id=1,
#             user = self.users,
#             position='Pathologist',
#             contact='5551234567',
#             mortuary_id=self.mortuary,
#             generated_code='ABC123'
#         )
#         self.assertEqual(staff.position, 'Pathologist')
#         self.assertEqual(staff.contact, '5551234567')
#         self.assertEqual(staff.mortuary_id, self.mortuary)
#         self.assertEqual(staff.generated_code, 'ABC123')
    
#     def test_string_representation(self):
#         """Test the string representation of a MortuaryStaff instance."""
#         staff = MortuaryStaff.objects.create(
#             staff_id=2,
#             user = self.users,
#             position='Technician',
#             contact='5559876543',
#             mortuary_id=self.mortuary,
#             generated_code='XYZ789'
#         )
#         self.assertEqual(str(staff), 'Staff 2 - Technician')

#     def test_mortuary_staff_creation_unhappy(self):
#         """Unhappy path: Test creating a MortuaryStaff instance with invalid data."""
        
#         # Test with missing Mortuary instance
#         staff = MortuaryStaff(
#             staff_id=3,
#             user = self.users,
#             position='Technician',
#             contact='5559876543',
#             mortuary_id=None,  # Invalid data: no Mortuary instance
#             generated_code='LMN456'
#         )
#         with self.assertRaises(ValidationError):
#             staff.full_clean()  # Trigger validation

#         # Test with invalid contact number
#         staff = MortuaryStaff(
#             staff_id=4,
#             user = self.users,
#             position='Receptionist',
#             contact='555123',  # Invalid contact number length
#             mortuary_id=self.mortuary,
#             generated_code='PQR123'
#         )
#         with self.assertRaises(ValidationError):
#             staff.full_clean()  # Trigger validation

#         # Test with empty position
#         staff = MortuaryStaff(
#             staff_id=5,
#             user = self.users,
#             position='',  # Empty position
#             contact='5553219876',
#             mortuary_id=self.mortuary,
#             generated_code='STU789'
#         )
#         with self.assertRaises(ValidationError):
#             staff.full_clean()  # Trigger validation

#         # Test with position exceeding max_length
#         staff = MortuaryStaff(
#             staff_id=6,
#             user = self.users,
#             position='A' * 31,  # Exceeds max_length of 30
#             contact='5556543210',
#             mortuary_id=self.mortuary,
#             generated_code='VWX789'
#         )
#         with self.assertRaises(ValidationError):
#             staff.full_clean()  # Trigger validation

#         # Test with generated_code exceeding max_length
#         staff = MortuaryStaff(
#             staff_id=7,
#             user = self.users,
#             position='Security Guard',
#             contact='5551112233',
#             mortuary_id=self.mortuary,
#             generated_code='A' * 31  # Exceeds max_length of 30
#         )
#         with self.assertRaises(ValidationError):
#             staff.full_clean()  # Trigger validation

