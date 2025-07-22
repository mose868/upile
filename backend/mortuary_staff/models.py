
from django.db import models
from mortuary.models import Mortuary #Import the Mortuary model
from django.core.exceptions import ValidationError
from users.models import CustomUser
  

class MortuaryStaff(models.Model):
    """
    Model representing staff members working at a mortuary.
    """
    staff_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    position = models.CharField(max_length=30)
    contact = models.CharField(max_length=15)
    mortuary_id = models.ForeignKey(Mortuary, on_delete=models.CASCADE)
    generated_code = models.CharField(max_length=30)

    def __str__(self):
        """
        String representation of the MortuaryStaff object.
        """
        return f"Staff {self.staff_id} - {self.position}"

    def clean(self):
        # Custom validation
        if not self.position.strip():
            raise ValidationError('Position cannot be blank or whitespace')
        if len(self.contact) < 10 or len(self.contact) > 15:
            raise ValidationError('Contact number must be between 10 and 15 characters')
        if not self.generated_code.strip():
            raise ValidationError('Generated code cannot be blank or whitespace')

    def save(self, *args, **kwargs):
        self.clean()  # Ensure custom validation is applied
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the MortuaryStaff object.
        """
        return f"Staff {self.staff_id} - {self.position}"