from django.db import models
from django.utils import timezone
from mortuary_staff.models import MortuaryStaff

def get_default_staff():
    return MortuaryStaff.objects.first()

class UnidentifiedBody(models.Model):
    SKIN_COLOR_CHOICES = [
        ('light_skinned', 'Light Skinned'),
        ('dark_skinned', 'Dark Skinned')
    ]

    id = models.AutoField(primary_key=True)  
    staff_id = models.ForeignKey(MortuaryStaff, on_delete=models.CASCADE, default=get_default_staff)  
    name = models.CharField(max_length=50)  
    gender = models.CharField(max_length=50)  
    location = models.CharField(max_length=50)  
    skin_color = models.CharField(max_length=50, choices=SKIN_COLOR_CHOICES, default='dark_skinned')
    weight = models.FloatField()  
    height = models.FloatField()  
    body_marks = models.TextField()  
    reporting_date = models.DateField()  
    clothes_worn = models.TextField()  
    hair_color = models.CharField(max_length=50) 
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        """String representation of the UnidentifiedBody instance"""
        return self.name
