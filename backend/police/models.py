from django.db import models
from users.models import CustomUser
from stations.models import PoliceStation

class PoliceOfficer(models.Model):
    officer_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rank = models.CharField(max_length=30)
    contact = models.CharField(max_length=15)
    station_id = models.ForeignKey(PoliceStation, on_delete=models.CASCADE)
    generated_code = models.CharField(max_length=30)

    def __str__(self):
        return f"Officer {self.officer_id} - {self.rank}"
