from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
import random
from django.utils import timezone
import uuid

class CustomUser(AbstractUser):
    """Choices for the user role"""
    ROLE_CHOICES = [
        ("police_officer", "Police Officer"),
        ("mortuary_staff", "Mortuary Staff"),
    ] 
   
    generated_code = models.CharField(max_length=6)
    """ Phone number field with unique constraint"""
    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default="police_officer"
    )
    """ Override the save method to add custom behavior before saving"""
    def save(self, *args, **kwargs):
        """Generate a code automatically if it doesn't exist"""
        if not self.generated_code:
            self.generated_code = self.generate_code()
        """Call the parent class's save method"""
        super().save(*args, **kwargs)

    """Generate a random 6-digit code for OTP"""
    def generate_code(self):
        """Generates a random 6-digit code"""
        return str(random.randint(100000, 999999))
    """String representation of the user, showing full name and role"""
    def __str__(self):
        return f"{self.first_name}"
    """Check if the user has the specified permission based on their role"""
    def has_permission(self, permission):
        if self.role == "police_officer":
            return permission in [
                "view_missing",
                "add_missing",
                "update_missing",
                "search_missing",
            ]
        elif self.role == "mortuary_staff":
            return permission in [
                "add_unidentified_body",
                "search_unidentified_body",
                "view_missing",
            ]
        return False
    """ Class method to count users by role"""
    @classmethod
    def count_by_role(cls, role):
        return cls.objects.filter(role=role).count()
    """ Many-to-many relationship with Django's Group model"""
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",
        blank=True,
        help_text="The groups this user belongs to.",
    )
    """Many-to-many relationship with Django's Permission model"""
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
    )
class RegistrationCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True, blank=True)
    def is_expired(self):
        return timezone.now() > self.expires_at