from django import forms
from .models import CustomUser


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(), label="Firstname")
    last_name = forms.CharField(widget=forms.TextInput(), label="Lastname")
    phone_number = forms.CharField(widget=forms.TextInput(), label="Phonenumber")
    email = forms.CharField(widget=forms.TextInput(), label="Email")
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, label="Role")

    class Meta:
        model = CustomUser
        fields = ["phone_number", "email", "first_name", "last_name", "role"]


class VerificationCodeForm(forms.Form):
    phone_number = forms.CharField(max_length=15, label="Phone Number")
    code = forms.CharField(
        max_length=36, label="Enter the code sent to your phone number"
    )
