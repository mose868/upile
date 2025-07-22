from django.db import models
from django.core.exceptions import ValidationError
import os
from police.models import PoliceOfficer

def validate_image_format(image):
    ext = os.path.splitext(image.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if ext not in valid_extensions:
        raise ValidationError(f'Unsupported file extension: {ext}. Allowed extensions are: .jpg, .jpeg, .png.')

def get_default_officer():
    return PoliceOfficer.objects.first() 

class MissingPerson(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    SKIN_COLOR_CHOICES = [
        ('light_skinned', 'Light Skinned'),
        ('dark_skinned', 'Dark Skinned')
    ]

    EYE_COLOR_CHOICES = [
        ('black', 'Black'),
        ('brown', 'Brown')
    ]

    STATUS = [
        ('missing', 'Missing'),
        ('found', 'Found'),
        ('departed', 'Departed')
    ]

    id = models.AutoField(primary_key=True)
    officer_id = models.ForeignKey(PoliceOfficer, on_delete=models.CASCADE, default=get_default_officer)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, default='Unknown')
    age = models.SmallIntegerField()
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='other')
    contact = models.CharField(max_length=20)
    image = models.ImageField(upload_to='missing_persons_images/', validators=[validate_image_format])
    height = models.FloatField()
    weight = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS, default='missing', blank=True)
    hair_color = models.CharField(max_length=20)
    eye_color = models.CharField(max_length=20, choices=EYE_COLOR_CHOICES, default='black')
    skin_color = models.CharField(max_length=20, choices=SKIN_COLOR_CHOICES, default='dark_skinned')
    missing_date = models.DateField()
    location = models.CharField(max_length=20)
    clothes_worn = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        if not self.first_name.strip():
            raise ValidationError('First name cannot be blank or whitespace')
        if self.age < 0:
            raise ValidationError('Age cannot be negative')

    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)
