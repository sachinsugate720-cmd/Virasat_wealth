from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import ConsultationRequest


class AdvisorRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Choose a username"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "you@example.com"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Create a password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Confirm password"}
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class AdvisorAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter your username"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter your password"}
        )


class ConsultationRequestForm(forms.ModelForm):
    class Meta:
        model = ConsultationRequest
        fields = ("full_name", "email", "phone", "primary_goal", "message")
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your Name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "you@example.com"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "+91 XXXXXXXXXX"}
            ),
            "primary_goal": forms.Select(attrs={"class": "form-select"}),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Share current investments and target goal.",
                }
            ),
        }
