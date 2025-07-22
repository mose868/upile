# # tests.py
# from django.test import TestCase
# from django.core.exceptions import ValidationError
# from django.db import IntegrityError
# from django.utils import timezone
# from mortuary_staff.models import MortuaryStaff
# from unidentified_bodies.models import UnidentifiedBody
# from mortuary.models import Mortuary
# from users.models import CustomUser

# class UnidentifiedBodyModelTest(TestCase):
#     def setUp(self):
#         # Setup a Mortuary instance
#         self.mortuary = Mortuary.objects.create(
#             id=1,
#             mortuary_name="Main Mortuary",
#             location="Downtown"
#         )

#         self.users = CustomUser.objects.create(
#         first_name='Test',
#         last_name='User',
#         email='test@example.com',
#         phone_number='1234567890',
#         role='police_officer',
#         generated_code='123456'  # Ensure this is not null if required
#     )

#         # Setup a MortuaryStaff instance
#         self.staff = MortuaryStaff.objects.create(
#             staff_id=1,
#             user = self.users,
#             position="Mortuary Staff",
#             contact="0701234567",
#             mortuary_id=self.mortuary,  # Use Mortuary instance
#             generated_code="CODE123"
#         )

#     def test_create_unidentified_body(self):
#         # Happy Path Test: Create a valid UnidentifiedBody instance
#         body = UnidentifiedBody.objects.create(
#             id=1,
#             staff_id=self.staff,  # Provide valid MortuaryStaff instance
#             name="John Doe",
#             gender="Male",
#             location="Central Park",
#             skin_color="dark_skinned",
#             weight=75.0,
#             height=180.0,
#             body_marks="None",
#             reporting_date=timezone.now(),
#             clothes_worn="Blue jeans, white shirt",
#             hair_color="Black"
#         )
        
#         # Check if the instance was created and saved properly
#         self.assertEqual(UnidentifiedBody.objects.count(), 1)
#         self.assertEqual(body.name, "John Doe")
#         self.assertEqual(body.gender, "Male")
#         self.assertEqual(body.staff_id, self.staff)

#     def test_missing_required_fields(self):
#         # Unhappy Path Test: Test for missing required fields
#         with self.assertRaises(IntegrityError):
#             UnidentifiedBody.objects.create(
#                 id=1,
#                 staff_id=self.staff,  # Provide valid MortuaryStaff instance
#                 name="John Doe"
#                 # Missing required fields
#             )

#     def test_invalid_skin_color(self):
#         # Unhappy Path Test: Test for invalid choice
#         with self.assertRaises(ValidationError):
#             body = UnidentifiedBody(
#                 id=1,
#                 staff_id=self.staff,
#                 name="John Doe",
#                 gender="Male",
#                 location="Central Park",
#                 skin_color="invalid_color",  # Invalid choice
#                 weight=75.0,
#                 height=180.0,
#                 body_marks="None",
#                 reporting_date=timezone.now(),
#                 clothes_worn="Blue jeans, white shirt",
#                 hair_color="Black"
#             )
#             body.full_clean()  # This triggers the validation

#     def test_invalid_staff_foreign_key(self):
#         # Unhappy Path Test: Test for invalid staff_id (foreign key constraint)
#         # Create a valid MortuaryStaff instance
#         valid_staff = MortuaryStaff.objects.create(
#             staff_id=2,
#             user = self.users,
#             position="Another Staff",
#             contact="0707654321",
#             mortuary_id=self.mortuary,
#             generated_code="CODE456"
#         )

#         # Try to create UnidentifiedBody with a non-existent MortuaryStaff ID
#         # This ID should be different from the valid ones to trigger the constraint

#         with self.assertRaises(IntegrityError):
#             UnidentifiedBody.objects.create(
#                 id=2,
#                 staff_id=None,  # Use non-existent staff ID
#                 name="Jane Doe",
#                 gender="Female",
#                 location="Central Park",
#                 skin_color="light_skinned",
#                 weight=60.0,
#                 height=170.0,
#                 body_marks="None",
#                 reporting_date=timezone.now(),
#                 clothes_worn="Green dress",
#                 hair_color="Blonde"
#             )

