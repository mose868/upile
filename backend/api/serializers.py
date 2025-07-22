from rest_framework import serializers
from missing_persons.models import MissingPerson
from police.models import PoliceOfficer
from mortuary.models import Mortuary
from stations.models import PoliceStation
from mortuary_staff.models import MortuaryStaff
from users.models import CustomUser
from next_of_kin.models import NextOfKin  
from unidentified_bodies.models import UnidentifiedBody 


"""Serializer class to handle full representation of MissingPerson model"""

class MissingPersonSerializer(serializers.ModelSerializer):
    class Meta:
        """Define which model this serializer is associated with"""
        model = MissingPerson
        """Include all fields of the model in the serialized output"""
        fields = "__all__"

""" Serializer class to handle a minimal representation of MissingPerson model"""
class MinimalMissingPersonSerializer(serializers.ModelSerializer):
    class Meta:
        """ Define which model this serializer is associated with"""
        model = MissingPerson
        """Include only specific fields ('first_name' and 'age') in the serialized output"""
        fields = ["id","first_name","last_name","age","location","gender","image","clothes_worn","missing_date","status"]



"""Serializer for PoliceStation model"""
class PoliceStationSerializer(serializers.ModelSerializer):
    # officers = PoliceOfficerSerializer(many=True, read_only=True)
    class Meta:
        model = PoliceStation
        fields = "__all__"


"""Serializer for Mortuary model"""
class MortuarySerializer(serializers.ModelSerializer):
    # staff = MortuaryStaffSerializer(many=True, read_only=True)
    class Meta:
        model = Mortuary
        fields = "__all__"

        
"""Serializer for PoliceOfficer model"""
class PoliceOfficerSerializer(serializers.ModelSerializer):
    # user = MinimalUserSerializer()
    class Meta:
        model = PoliceOfficer
        fields = "__all__"
 


class MortuaryStaffSerializer(serializers.ModelSerializer):
    """
    Serializer for the MortuaryStaff model that includes all fields.
    """
    class Meta:
        model = MortuaryStaff
        fields = "__all__"

class MinimalMortuaryStaffSerializer(serializers.ModelSerializer):
    """db.sqlite3
    Serializer for the MortuaryStaff model that includes only a subset of fields.
    """
    class Meta:
        model = MortuaryStaff
        fields = ["name", "location"]


class CustomUserSerializer(serializers.ModelSerializer):
    # officers = PoliceOfficerSerializer(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = "__all__"


class MinimalCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["user_id", "role"] 


"""Serializer for the NextOfKin model & UnidentifiedBody model"""
class NextOfKinSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextOfKin  
        fields = '__all__'  
  

"""Serializer for the NextOfKin model & UnidentifiedBody model"""
class NextOfKinSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextOfKin  
        fields = '__all__'  

class UnidentifiedBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidentifiedBody  
        fields = '__all__'

class MinimalUnidentifiedBodySerializer(serializers.ModelSerializer):
    class Meta:
        """ Define which model this serializer is associated with"""
        model = UnidentifiedBody
        """Include only specific fields in the serialized output"""
        fields = ["name","clothes_worn" ,"gender", "reporting_date", "location"]


class MatchSerializer(serializers.Serializer):
    missing_person = serializers.CharField()
    unidentified_body = serializers.CharField()
    name_match = serializers.BooleanField()
    clothes_worn = serializers.BooleanField()
    gender= serializers.BooleanField()
    location= serializers.BooleanField()
    date_reported= serializers.BooleanField()
    
