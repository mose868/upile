from django.db import models
# Create your models here.

class Mortuary(models.Model):
    """ Primary key for the Mortuary model"""
    id = models.SmallIntegerField(primary_key=True)

    mortuary_name = models.CharField(max_length=50)

    """Location of the mortuary """
    location = models.CharField(max_length=50)

    def __str__(self):
        """ String representation of the object for display purposes"""
        return self.mortuary_name
