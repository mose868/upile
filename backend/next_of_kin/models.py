from django.core.exceptions import ValidationError
from django.db import models
from missing_persons.models import MissingPerson

class NextOfKin(models.Model):
    """
    Model representing a next of kin for a missing person. 
    """
    id = models.AutoField(primary_key=True)
    missing_person_id = models.ForeignKey(MissingPerson, on_delete=models.CASCADE)  
    first_name = models.CharField(max_length=50)  
    last_name = models.CharField(max_length=50)  
    address = models.CharField(max_length=50, default='Unknown')
    relationship = models.CharField(max_length=50)
    contact = models.CharField(max_length=30)  
    alternative_contact = models.CharField(max_length=30, default='Unknown')

    def __str__(self):
        """String representation of the NextOfKin instance"""
        return f"{self.first_name} ({self.last_name})"


    def clean(self):
        if not self.first_name.strip() or not self.last_name.strip():
            raise ValidationError('First name and last name cannot be blank or whitespace')
        if len(self.contact) < 10 or len(self.contact) > 15:
            raise ValidationError('Contact number must be between 10 and 15 characters')
        if self.alternative_contact != 'Unknown' and len(self.alternative_contact) < 10:
            raise ValidationError('Alternative contact must be at least 10 characters')


    def save(self, *args, **kwargs):
        self.clean()  # Ensure custom validation is applied
        super().save(*args, **kwargs)

  