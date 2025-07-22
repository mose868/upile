from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """Serializer for user registration"""

    """Field to capture the phone number; required for registration"""
    phone_number = serializers.CharField(required=True)


class VerifyOtpSerializer(serializers.Serializer):
    """Serializer for verifying OTP (One-Time Password)"""

    """ Field to capture the generated code; required for OTP verification"""
    generated_code = serializers.CharField(max_length=20)

    # Field to capture the phone number; required for OTP verification
    phone_number = serializers.CharField(required=True)

    """Field to capture the OTP; required for OTP verification"""
    otp = serializers.CharField(required=True)
