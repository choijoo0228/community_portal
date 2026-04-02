import logging
from django import forms
from django.utils import timezone
from .models import EventSuggestion, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)
class EventSuggestionForm(forms.ModelForm):
    class Meta:
        model = EventSuggestion
        fields = ["title", "description", "start_datetime", "location", "image"]
        widgets = {
            "start_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean_start_datetime(self):
        try:
            dt = self.cleaned_data["start_datetime"]
            if dt <= timezone.now():
                logger.warning("Invalid start_datetime: %s is in the past", dt)
                raise forms.ValidationError("Event date/time must be in the future.")
            logger.debug("Valid start_datetime: %s", dt)
            return dt
        except forms.ValidationError:
            raise
        except Exception as e:
            logger.error("Error in clean_start_datetime: %s", str(e))
            raise forms.ValidationError("An error occurred while validating the date.")

    def clean_title(self):
        try:
            title = self.cleaned_data["title"].strip()
            if len(title) < 5:
                logger.warning("Invalid title: length too short")
                raise forms.ValidationError("Title must be at least 5 characters long.")
            logger.debug("Valid title: %s", title)
            return title
        except forms.ValidationError:
            raise
        except Exception as e:
            logger.error("Error in clean_title: %s", str(e))
            raise forms.ValidationError("An error occurred while validating the title.")
    
    def __init__(self, *args, **kwargs):
        try:
            super().__init__(*args, **kwargs)
            for name, field in self.fields.items():
                if name != "image":
                    field.widget.attrs["class"] = "form-control"
                else:
                    field.widget.attrs["class"] = "form-control"
            logger.debug("EventSuggestionForm initialized")
        except Exception as e:
            logger.error("Error initializing EventSuggestionForm: %s", str(e))
            raise
                
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "password1", "password2"]

    def clean_email(self):
        try:
            email = self.cleaned_data["email"].strip().lower()
            if User.objects.filter(email=email).exists():
                logger.warning("Email already registered: %s", email)
                raise forms.ValidationError("This email is already registered.")
            logger.debug("Email is unique: %s", email)
            return email
        except forms.ValidationError:
            raise
        except Exception as e:
            logger.error("Error in clean_email: %s", str(e))
            raise forms.ValidationError("An error occurred while validating the email.")

    def clean_phone_number(self):
        try:
            phone_number = self.cleaned_data["phone_number"].strip()
            if len(phone_number) < 7:
                logger.warning("Invalid phone number: too short")
                raise forms.ValidationError("Enter a valid phone number.")
            logger.debug("Valid phone number")
            return phone_number
        except forms.ValidationError:
            raise
        except Exception as e:
            logger.error("Error in clean_phone_number: %s", str(e))
            raise forms.ValidationError("An error occurred while validating the phone number.")

    def save(self, commit=True):
        try:
            user = super().save(commit=False)
            user.email = self.cleaned_data["email"]

            if commit:
                user.save()
                Profile.objects.create(
                    user=user,
                    phone_number=self.cleaned_data["phone_number"]
                )
                logger.info("New user registered and profile created: %s", user.username)
            return user
        except Exception as e:
            logger.error("Error in RegisterForm.save(): %s", str(e))
            raise