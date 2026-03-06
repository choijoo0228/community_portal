from django import forms
from django.utils import timezone
from .models import EventSuggestion, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class EventSuggestionForm(forms.ModelForm):
    class Meta:
        model = EventSuggestion
        fields = ["title", "description", "start_datetime", "location", "image"]
        widgets = {
            "start_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean_start_datetime(self):
        dt = self.cleaned_data["start_datetime"]
        if dt <= timezone.now():
            raise forms.ValidationError("Event date/time must be in the future.")
        return dt

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != "image":
                field.widget.attrs["class"] = "form-control"
            else:
                field.widget.attrs["class"] = "form-control"
                
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"].strip()
        if len(phone_number) < 7:
            raise forms.ValidationError("Enter a valid phone number.")
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                phone_number=self.cleaned_data["phone_number"]
            )
        return user