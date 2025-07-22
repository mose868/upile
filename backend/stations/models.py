from django.core.exceptions import ValidationError
from django.db import models


class PoliceStation(models.Model):
    """Defines a PoliceStation model with an ID, name, and location,
    where the station ID is the primary key, and the string representation returns the station name."""
    station_id = models.SmallIntegerField(primary_key=True)
    station_name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    def __str__(self):
        return self.station_name