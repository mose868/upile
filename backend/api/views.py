import logging
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import render
from fuzzysearch import find_near_matches


from .serializers import (
    PoliceStationSerializer,
    MortuarySerializer,
    PoliceOfficerSerializer,
    CustomUserSerializer,
    UnidentifiedBodySerializer, MinimalUnidentifiedBodySerializer,
    NextOfKinSerializer,
    MissingPersonSerializer, MinimalMissingPersonSerializer,
    MortuaryStaffSerializer, MinimalMortuaryStaffSerializer
)
from rest_framework.exceptions import NotFound
from mortuary_staff.models import MortuaryStaff
from users.models import CustomUser
from unidentified_bodies.models import UnidentifiedBody
from next_of_kin.models import NextOfKin
from mortuary.models import Mortuary
from police.models import PoliceOfficer
from stations.models import PoliceStation
from missing_persons.models import MissingPerson




"""Set up logging"""
logger = logging.getLogger(__name__)


class MissingPersonListView(APIView):
    
    def get(self, request):
        """Retrieve a list of all missing persons."""
        missing_people = MissingPerson.objects.all()
        """Total number of missing persons"""
        total_missing_persons = MissingPerson.objects.all().count()
        serializer = MinimalMissingPersonSerializer(missing_people, many=True)
        return Response({
            'total_missing_persons': total_missing_persons,
            'missing_persons': serializer.data
        })

    def post(self, request):
        """Create a new missing person record."""
        serializer = MissingPersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MissingPersonDetailView(APIView):
    def get(self, request, id=None):
        """Retrieve a specific missing person by ID or search by name."""
        if id:
            # Handle retrieval by ID
            try:
                missing_person = get_object_or_404(MissingPerson, id=id)
                serializer = MissingPersonSerializer(missing_person)
                return Response(serializer.data)
            except Exception as e:
                logger.error(f"Error retrieving missing person with ID {id}: {e}")
                return Response({"error": "An error occurred while retrieving the missing person."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Handle search by name
            name = request.query_params.get('name', None)
            if name:
                try:
                    missing_persons = MissingPerson.objects.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
                    serializer = MissingPersonSerializer(missing_persons, many=True)
                    return Response(serializer.data)
                except Exception as e:
                    logger.error(f"Error searching missing persons by name '{name}': {e}")
                    return Response({"error": "An error occurred while searching for missing persons."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"error": "Name query parameter is required for search."}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, id):
        try:
            missing_person = get_object_or_404(MissingPerson, id=id)
            serializer = MissingPersonSerializer(missing_person, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response({
                "error": "Validation failed",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Error updating missing person with ID {id}: {e}")
            return Response({
                "error": "Failed to update missing person.",
                "details": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)




# View to handle listing and creating MortuaryStaff instances
class MortuaryStaffListView(APIView):
    
    def get(self, request):
        """
        Handle GET requests to retrieve a list of all MortuaryStaff.
        """
        staff = MortuaryStaff.objects.all()
        serializer = MinimalMortuaryStaffSerializer(staff, many=True)
        return Response(serializer.data)


class MortuaryStaffListView(APIView):
    
    def post(self, request):
        """
        Handle POST requests to create a new MortuaryStaff instance.
        """
        serializer = MortuaryStaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def get_staff_count(self, request):
        """
        Handle GET requests to retrieve the count of all MortuaryStaff instances.
        """
        count = MortuaryStaff.objects.count()
        return Response({'staff_count': count})

# View to handle retrieving, updating MortuaryStaff instances
class MortuaryStaffDetailView(APIView):
    
    def get_object(self, id):
        """
        Retrieve a MortuaryStaff instance by its ID.
        """
        try:
            return MortuaryStaff.objects.get(id=id)
        except MortuaryStaff.DoesNotExist:
            raise NotFound(detail="MortuaryStaff not found.")

    def get(self, request, id):
        """
        Handle GET requests to retrieve a single MortuaryStaff instance.
        """
        staff = self.get_object(id)
        serializer = MortuaryStaffSerializer(staff)
        return Response(serializer.data)

    def put(self, request, id):
        """
        Handle PUT requests to update an existing MortuaryStaff instance.
        """
        staff = self.get_object(id)
        serializer = MortuaryStaffSerializer(staff, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CustomUserDetailView(APIView):
    def get(self, request, id):
        try:
            user = CustomUser.objects.get(id=id)  
            serializer = CustomUserSerializer(user) 
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, id):
        try:
            user = CustomUser.objects.get(id=id)
            serializer = CustomUserSerializer(user, data=request.data)     
            if serializer.is_valid():
                serializer.save()              
                return Response(serializer.data, status=status.HTTP_200_OK)          
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)     
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        
class UsersListView(APIView):     
    def get(self, request):
        """Retrive users"""
        users = CustomUser.objects.all()
        total_users = CustomUser.objects.all().count()
        serializer =CustomUserSerializer(users, many=True)
        return Response({'total_users': total_users,
            'users': serializer.data})



# Create your views here.

class PoliceStationListView(APIView):
    def get(self, request):
        """Retrive the police stations"""
        stations = PoliceStation.objects.all()
        total_police_stations = PoliceStation.objects.all().count()
        serializer =PoliceStationSerializer(stations, many=True)
        return Response({'total_police_officers': total_police_stations,
            'stations': serializer.data})
    
    def post(self, request):
        serializer = PoliceStationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
class PoliceStationDetailView(APIView):
    def get(self, request, id):
        try:
            """Retrieve the PoliceStation object by ID"""
            station = PoliceStation.objects.get(id=id)
            serializer = PoliceStationSerializer(station)
            return Response(serializer.data)
        except PoliceStation.DoesNotExist:
            """Handle the case where the police station with the given ID does not exist"""
            return Response({'error': 'Police station not found'}, status=status.HTTP_404_NOT_FOUND)
    def put(self, request, id):
        try:
            """Retrieve the PoliceStation object by ID for updating"""
            station = PoliceStation.objects.get(id=id)
            serializer = PoliceStationSerializer(station, data=request.data)
            """Validate and save the updated police station details if valid"""
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            """ Return validation errors if the data is not valid"""
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PoliceStation.DoesNotExist:
            """Handle the case where the police station with the given ID does not exist"""
            return Response({'error': 'Police station not found'}, status=status.HTTP_404_NOT_FOUND)
        


    
class MortuaryListView(APIView):
    def get(self, request):
        mortuaries = Mortuary.objects.all()
        total_mortuaries = Mortuary.objects.all().count()
        serializer = MortuarySerializer(mortuaries, many=True)
        return Response({'total_mortuaries': total_mortuaries,
            'mortuaries': serializer.data})
    def post(self, request):
        serializer = MortuarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MortuaryDetailView(APIView):
    def get(self, request, id):
        try:
            """Try to retrieve the Mortuary object by ID"""
            mortuary = Mortuary.objects.get(id=id)
            serializer = MortuarySerializer(mortuary)
            return Response(serializer.data)
        except Mortuary.DoesNotExist:
            """Handle the case where the mortuary with the given ID does not exist"""
            return Response({'error': 'Mortuary not found'}, status=status.HTTP_404_NOT_FOUND)
    def put(self, request, id):
        try:
            """Try to retrieve the Mortuary object by ID for updating"""
            mortuary = Mortuary.objects.get(id=id)
            serializer = MortuarySerializer(mortuary, data=request.data)
            """Validate and save the updated mortuary details if valid"""
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            """Return validation errors if the data is not valid"""
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Mortuary.DoesNotExist:
            """Handle the case where the mortuary with the given ID does not exist"""
            return Response({'error': 'Mortuary not found'}, status=status.HTTP_404_NOT_FOUND)
        



class PoliceOfficerListView(APIView):
    def get(self, request):
        total_police_officers = PoliceOfficer.objects.all().count()
        officers = PoliceOfficer.objects.all()
        serializer = PoliceOfficerSerializer(officers, many=True)
        return Response({
            'total_police_officers': total_police_officers,
            'officers': serializer.data
        })
    def post(self, request):
        serializer = PoliceOfficerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PoliceOfficerDetailView(APIView):
    def get(self, request, id):
        try:
            """Try to retrieve the PoliceOfficer object by ID"""
            officer = PoliceOfficer.objects.get(id=id)
            serializer = PoliceOfficerSerializer(officer)
            return Response(serializer.data)
        except PoliceOfficer.DoesNotExist:
            """Handle the case where the police officer with the given ID does not exist"""
            return Response({'error': 'Police officer not found'}, status=status.HTTP_404_NOT_FOUND)
    def put(self, request, id):
        try:
            """Try to retrieve the PoliceOfficer object by ID for updating"""
            officer = PoliceOfficer.objects.get(id=id)
            serializer = PoliceOfficerSerializer(officer, data=request.data)
            """Validate and save the updated police officer details if valid"""
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            """Return validation errors if the data is not valid"""
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PoliceOfficer.DoesNotExist:
            """Handle the case where the police officer with the given ID does not exist"""
            return Response({'error': 'Police officer not found'}, status=status.HTTP_404_NOT_FOUND)
class NextOfKinListView(APIView):
    def get(self, request):
        """Retrieve a list of next of kin."""
        logger.info("Fetching list of next of kin.")
        next_of_kin = NextOfKin.objects.all()
        total_next_of_kin = NextOfKin.objects.all().count()
        serializer = NextOfKinSerializer(next_of_kin, many=True)
        logger.info("Successfully fetched next of kin data.")
        return Response({
            'total_next_of_kin': total_next_of_kin,
            'next_of_kin': serializer.data
        })

    def post(self, request):
        """Create a new next of kin entry."""
        logger.info("Creating a new next of kin entry.")
        serializer = NextOfKinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Next of kin entry created successfully.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning("Failed to create next of kin entry: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NextOfKinDetailView(APIView):
    def get(self, request, pk):
        """Retrieve a specific next of kin by primary key."""
        logger.info("Fetching next of kin with pk: %s", pk)
        try:
            next_of_kin = NextOfKin.objects.get(pk=pk)
            serializer = NextOfKinSerializer(next_of_kin)
            logger.info("Successfully fetched next of kin data for pk: %s", pk)
            return Response(serializer.data)
        except NextOfKin.DoesNotExist:
            logger.error("Next of kin with pk: %s not found.", pk)
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        """Update a specific next of kin entry."""
        logger.info("Updating next of kin with pk: %s", pk)
        try:
            next_of_kin = NextOfKin.objects.get(pk=pk)
        except NextOfKin.DoesNotExist:
            logger.error("Next of kin with pk: %s not found.", pk)
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = NextOfKinSerializer(next_of_kin, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Next of kin with pk: %s updated successfully.", pk)
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.warning("Failed to update next of kin with pk: %s: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnidentifiedBodyListView(APIView):
    def get(self, request):
        """Retrieve a list of unidentified bodies."""
        logger.info("Fetching list of unidentified bodies.")
        unidentified_bodies = UnidentifiedBody.objects.all()
        total_unidentified_bodies = UnidentifiedBody.objects.all().count()
        serializer = MinimalUnidentifiedBodySerializer(unidentified_bodies, many=True)
        logger.info("Successfully fetched unidentified bodies data.")
        return Response({
            'total_unidentified_bodies': total_unidentified_bodies,
            'unidentified_bodies': serializer.data
        })

    def post(self, request):
        """Create a new unidentified body entry."""
        logger.info("Creating a new unidentified body entry.")
        serializer = UnidentifiedBodySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Unidentified body entry created successfully.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning("Failed to create unidentified body entry: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnidentifiedBodyDetailView(APIView):
    def get(self, request, id=None):
        """Retrieve a specific unidentified body by ID or search by date."""
        if id:
            # Handle retrieval by ID
            try:
                unidentified_body = get_object_or_404(UnidentifiedBody, id=id)
                serializer = UnidentifiedBodySerializer(unidentified_body)
                return Response(serializer.data)
            except Exception as e:
                logger.error(f"Error retrieving unidentified body with ID {id}: {e}")
                return Response({"error": "An error occurred while retrieving unidentified body."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Handle search by date
            date = request.query_params.get('reporting_date', None)
            if date:
                try:
                    unidentified_body = UnidentifiedBody.objects.filter(Q(reporting_date__icontains=date))
                    serializer = UnidentifiedBodySerializer(unidentified_body, many=True)
                    return Response(serializer.data)
                except Exception as e:
                    logger.error(f"Error searching missing persons by name '{date}': {e}")
                    return Response({"error": "An error occurred while searching for an unidentified body."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"error": "Date query parameter is required for search."}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, id):
        """Update a specific unidentified body entry."""
        logger.info("Updating unidentified body with id: %s", id)
        try:
            unidentified_body = UnidentifiedBody.objects.get(id=id)
        except UnidentifiedBody.DoesNotExist:
            logger.error("Unidentified body with id: %s not found.", id)
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UnidentifiedBodySerializer(unidentified_body, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Unidentified body with id: %s updated successfully.", id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.warning("Failed to update unidentified body with id: %s: %s", id, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PoliceStationListView(APIView):
    def get(self, request):
        """Retrive the police stations"""
        stations = PoliceStation.objects.all()
        total_police_stations = PoliceStation.objects.all().count()
        serializer =PoliceStationSerializer(stations, many=True)
        return Response({'total_police_officers': total_police_stations,
            'stations': serializer.data})
    
    def post(self, request):
        serializer = PoliceStationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MissingPersonDetailView(APIView):
    def get(self, request, id=None):
        """Retrieve a specific missing person by ID or search by name."""
        if id:
            # Handle retrieval by ID
            try:
                missing_person = get_object_or_404(MissingPerson, id=id)
                serializer = MissingPersonSerializer(missing_person)
                return Response(serializer.data)
            except Exception as e:
                logger.error(f"Error retrieving missing person with ID {id}: {e}")
                return Response({"error": "An error occurred while retrieving the missing person."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Handle search by name
            name = request.query_params.get('name', None)
            if name:
                try:
                    missing_persons = MissingPerson.objects.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
                    serializer = MissingPersonSerializer(missing_persons, many=True)
                    return Response(serializer.data)
                except Exception as e:
                    logger.error(f"Error searching missing persons by name '{name}': {e}")
                    return Response({"error": "An error occurred while searching for missing persons."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"error": "Name query parameter is required for search."}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, id):
        """Update a specific missing person record by ID."""
        try:
            missing_person = get_object_or_404(MissingPerson, id=id)
            serializer = MissingPersonSerializer(missing_person, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error updating missing person with ID {id}: {e}")
            return Response({"error": "Failed to update missing person."}, status=status.HTTP_400_BAD_REQUEST)


    
class PoliceStationDetailView(APIView):
    def get(self, request, id):
        try:
            """Retrieve the PoliceStation object by ID"""
            station = PoliceStation.objects.get(id=id)
            serializer = PoliceStationSerializer(station)
            return Response(serializer.data)
        except PoliceStation.DoesNotExist:
            """Handle the case where the police station with the given ID does not exist"""
            return Response({'error': 'Police station not found'}, status=status.HTTP_404_NOT_FOUND)
    def put(self, request, id):
        try:
            """Retrieve the PoliceStation object by ID for updating"""
            station = PoliceStation.objects.get(id=id)
            serializer = PoliceStationSerializer(station, data=request.data)
            """Validate and save the updated police station details if valid"""
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            """ Return validation errors if the data is not valid"""
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PoliceStation.DoesNotExist:
            """Handle the case where the police station with the given ID does not exist"""
            return Response({'error': 'Police station not found'}, status=status.HTTP_404_NOT_FOUND)
        


    
class MortuaryListView(APIView):
    def get(self, request):
        mortuaries = Mortuary.objects.all()
        total_mortuaries = Mortuary.objects.all().count()
        serializer = MortuarySerializer(mortuaries, many=True)
        return Response({'total_mortuaries': total_mortuaries,
            'mortuaries': serializer.data})
    def post(self, request):
        serializer = MortuarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MortuaryDetailView(APIView):
    def get(self, request, id):
        try:
            """Try to retrieve the Mortuary object by ID"""
            mortuary = Mortuary.objects.get(id=id)
            serializer = MortuarySerializer(mortuary)
            return Response(serializer.data)
        except Mortuary.DoesNotExist:
            """Handle the case where the mortuary with the given ID does not exist"""
            return Response({'error': 'Mortuary not found'}, status=status.HTTP_404_NOT_FOUND)
    def put(self, request, mortuary_id):
        try:
            """Try to retrieve the Mortuary object by ID for updating"""
            mortuary = Mortuary.objects.get(id=mortuary_id)
            serializer = MortuarySerializer(mortuary, data=request.data)
            """Validate and save the updated mortuary details if valid"""
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            """Return validation errors if the data is not valid"""
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Mortuary.DoesNotExist:
            """Handle the case where the mortuary with the given ID does not exist"""
            return Response({'error': 'Mortuary not found'}, status=status.HTTP_404_NOT_FOUND)
        



class PoliceOfficerListView(APIView):
    def get(self, request):
        total_police_officers = PoliceOfficer.objects.all().count()
        officers = PoliceOfficer.objects.all()
        serializer = PoliceOfficerSerializer(officers, many=True)
        return Response({
            'total_police_officers': total_police_officers,
            'officers': serializer.data
        })
    def post(self, request):
        serializer = PoliceOfficerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PoliceOfficerDetailView(APIView):
    def get(self, request, id):
        try:
            """Try to retrieve the PoliceOfficer object by ID"""
            officer = PoliceOfficer.objects.get(id=id)
            serializer = PoliceOfficerSerializer(officer)
            return Response(serializer.data)
        except PoliceOfficer.DoesNotExist:
            """Handle the case where the police officer with the given ID does not exist"""
            return Response({'error': 'Police officer not found'}, status=status.HTTP_404_NOT_FOUND)
    def put(self, request, id):
        try:
            """Try to retrieve the PoliceOfficer object by ID for updating"""
            officer = PoliceOfficer.objects.get(id=id)
            serializer = PoliceOfficerSerializer(officer, data=request.data)
            """Validate and save the updated police officer details if valid"""
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            """Return validation errors if the data is not valid"""
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PoliceOfficer.DoesNotExist:
            """Handle the case where the police officer with the given ID does not exist"""
            return Response({'error': 'Police officer not found'}, status=status.HTTP_404_NOT_FOUND)

 


class MatchView(APIView):
    def get(self, request):
        # 1. Fetch MissingPersons and UnidentifiedBodies
        missing_persons = MissingPerson.objects.all()
        unidentified_bodies = UnidentifiedBody.objects.all()
        # 2. Perform matching
        matches = []
        for missing_person in missing_persons:
            for body in unidentified_bodies:
                match = self.match_records(missing_person, body)
                if match:
                    matches.append(match)
        # 3. Return JSON response with match results
        return Response(matches)
    def match_records(self, missing_person, unidentified_body, threshold=3):
        # This method handles fuzzy matching between missing persons and unidentified bodies
        name_matches = find_near_matches(missing_person.first_name, unidentified_body.name, max_l_dist=threshold)
        gender_matches = missing_person.gender.lower() == unidentified_body.gender.lower()
        clothes_worn = find_near_matches(missing_person.clothes_worn, unidentified_body.clothes_worn, max_l_dist=threshold)
        location = find_near_matches(missing_person.location, unidentified_body.location, max_l_dist=threshold)
        date_reported = missing_person.missing_date == unidentified_body.reporting_date
        # If any match occurs, return the match data
        if name_matches or date_reported and clothes_worn and gender_matches and location:
            return {
                'missing_person': MissingPersonSerializer(missing_person).data,
                'unidentified_body': UnidentifiedBodySerializer(unidentified_body).data,
                'name_match': bool(name_matches),
                'gender_match': gender_matches,
                'clothes_worn': bool(clothes_worn),
                'location': bool(location),
                'date_reported': bool(date_reported)
            }
        return None