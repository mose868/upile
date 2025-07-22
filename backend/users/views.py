import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, RegistrationCode
from .serializers import LoginSerializer, VerifyOtpSerializer
from django.core.cache import cache
import random
import requests
import re
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.exceptions import TemplateDoesNotExist
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http.response import HttpResponse
import json

logger = logging.getLogger(__name__)


"""Function to generate a 6-digit OTP"""
def generate_otp():
    return str(random.randint(100000, 999999))


"""Function to send OTP via SMS using the Leopard SMS API"""
def send_otp(phone_number, otp):
    headers = {
        "Authorization": f"Basic {settings.SMS_LEOPARD_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "source": "AkiraChix",
        "message": f"Your OTP code is {otp}",
        "destination": [{"number": phone_number}],
    }

    try:
        response = requests.post(
            settings.SMS_LEOPARD_API_URL, json=payload, headers=headers
        )
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Status Code: {response.status_code} - Response: {response.text}")
        return None
    except requests.RequestException as e:
        logger.error(f"Request exception occurred: {e}")
        return None

"""Function to validate phone numbers (Kenya format)"""
def validate_phone_number(phone_number):
    pattern = re.compile(r"^0[1-9]\d{8}$")
    if pattern.match(phone_number):
        return "+254" + phone_number[1:]
    return None


# Updated `login_user` view with consistent OTP cache key
@api_view(["POST"])
def login_user(request):
    try:
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            formatted_number = validate_phone_number(phone_number)

            if not formatted_number:
                return Response(
                    {"error": "Invalid phone number format. Use: 0723456789."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            otp = generate_otp()

            print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{otp}$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

            # Wrap the OTP sending in a try-except
            try:
                response = send_otp(formatted_number, otp)
                print(f"@@@@@@@@@@@@@@@@@@{response}@@@@@@@@@@@@@@@@@@")
            except Exception as e:
                logger.error(f"Error sending OTP: {e}")
                return Response(
                    {"error": "Failed to send otp"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            if response and response.get("success") == True:
                # Store OTP in cache with consistent key
                print(f"cache_otp_key::::{otp}::::")

          
                one = cache.set(settings.SMS_CACHE_KEY, otp, timeout=300)
                print(f"$$$$$$$$$$$$$$$$$$$${one}%%%%%%%%%%%%%%%%%%%%%%%5")


                user, created = CustomUser.objects.get_or_create(
                    phone_number=formatted_number
                )
                user.is_active = False
                user.save()

                return Response(
                    {"message": "OTP sent to your number."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "OTP sent to your number."},
                    status=status.HTTP_200_OK,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Unexpected error in login_user: {str(e)}")
        return Response(
            {"error": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    


@csrf_exempt
def verify_sms_otp(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                phone_number = data.get('mobile_no')
                entered_otp = data.get('otp')
            except json.JSONDecodeError:
                return JsonResponse({"detail": "Invalid JSON"}, status=400)
        else:
            phone_number = request.POST.get('mobile_no')
            entered_otp = request.POST.get('otp')
        if not phone_number or not entered_otp:
            return JsonResponse({"detail": "Please enter both the phone_number and otp"}, status=400)


        # Use the same key format as in login_user to retrieve OTP
        stored_otp = cache.get(settings.SMS_CACHE_KEY)
        print(f"otp_cache_key{stored_otp}::::::entered otp {entered_otp}___")
        if stored_otp:        
            # Retrieve the stored OTP from cache

            # Check if the entered OTP matches the cached OTP
            if entered_otp == stored_otp:
                # OTP verified successfully, reset cache for OTP
                cache.delete(settings.SMS_CACHE_KEY)  # Optionally remove OTP from cache after verification
                
                # Retrieve the user and return a success message
                user = CustomUser.objects.get(phone_number=phone_number)

                return JsonResponse({
                    "message": "OTP verified successfully",
                    "customer": {
                        "id": user.id,
                        "generated_code": user.generated_code,
                        "role": user.role,
                        "phonenumber": user.phone_number,
                        "username": user.username
                    }
                }, status=200)

        else:
            # No need for attempt counting; just return invalid OTP response
            return JsonResponse({"message": "Invalid OTP"}, status=400)

    return JsonResponse({"message": "Invalid OTP"}, status=400)

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.cache import cache


@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        phone_number = request.POST.get('mobile_no')
        entered_otp = request.POST.get('otp')

        # Use the same key format as in login_user to retrieve OTP
        otp_cache_key = f"otp_{phone_number}"
        
        # Retrieve the stored OTP from cache
        stored_otp = cache.get(otp_cache_key)

        # Check if the entered OTP matches the cached OTP
        if stored_otp and entered_otp == stored_otp:
            # OTP verified successfully, reset cache for OTP
            cache.delete(otp_cache_key)  # Optionally remove OTP from cache after verification
            
            # Retrieve the user and return a success message
            user = CustomUser.objects.get(phone_number=phone_number)

            return JsonResponse({
                "message": "OTP verified successfully",
                "customer": {
                    "id": user.id,
                    "generated_code": user.generated_code,
                    "role": user.role,
                    "phonenumber": user.phone_number,
                    "username": user.username
                }
            }, status=200)

        else:
            # No need for attempt counting; just return invalid OTP response
            return JsonResponse({"detail": "Invalid OTP"}, status=400)

    return JsonResponse({"detail": "Invalid request"}, status=400)



"""API for generating and sending a verification code via email (user registration)"""
def generate_short_code(role):
    code = random.randint(1111, 9999)
    prefix = "Po" if role == "Police Officer" else "Mo"
    return prefix + str(code)


@api_view(["POST"])
def user_register(request):
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    role = request.data.get("role")
    phone_number = request.data.get("phone_number")
    email = request.data.get("email")
    username = request.data.get("username")

  
    if CustomUser.objects.filter(phone_number=phone_number).exists():
        return Response({"message": "Phone number already exists"}, status=status.HTTP_400_BAD_REQUEST)
    if CustomUser.objects.filter(username=username).exists():
        return Response({"message": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
  
    user = CustomUser.objects.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        role=role,
        phone_number=phone_number,
        email=email,
    )

    short_code = generate_short_code(role)

    code = RegistrationCode.objects.create(
        user=user,
        code=short_code,
        created_at=timezone.now(),
    )

  
    subject = "Your Registration Code"
    context = {
        'user_name': f"{first_name} {last_name}",
        'registration_code': short_code,
    }
    
   
    html_message = render_to_string('registration_code.html', context) 
    plain_message = strip_tags(html_message)  
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

  
    try:
        email_message = EmailMultiAlternatives(subject, plain_message, from_email, recipient_list)
        email_message.attach_alternative(html_message, "text/html") 
        email_message.send()

        return Response(
            {"message": "Registration code sent successfully."},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return Response(
            {"error": f"Failed to send email: {e}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

"""API for verifying the email verification code"""
@api_view(["POST"])
@login_required
def verify_code(request):
    
    user = CustomUser(
            code= code,
            phone_number=phone_number,
        )
    try:
        code = request.data.get("code")
        phone_number = request.data.get("phone_number")

        verification_code = RegistrationCode.objects.get(
            code=code, phone_number=request.phone_number
        )
        if user.get("phone_number") != phone_number:
            return Response(
                {"error": "Phone number does not match."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not verification_code.is_expired():
            login(request, verification_code.user)
            return Response(
                {"message": "Verification successful."}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Code expired"}, status=status.HTTP_400_BAD_REQUEST
            )
    except RegistrationCode.DoesNotExist:
        return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error in verify_code: {e}")
        return Response(
            {"error": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )