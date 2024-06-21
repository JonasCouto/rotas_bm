# core/forms.py

from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    # Fields for password and confirmation
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        # Meta class to specify the model and fields to be used
        model = User
        fields = ["username", "password", "confirm_password"]

    def clean(self):
        # Clean method to validate the form data
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Check if passwords match
        if password != confirm_password:
            raise forms.ValidationError(
                "As senhas não coincidem."
            )  # Passwords do not match



