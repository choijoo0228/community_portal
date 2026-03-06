from django import forms
from django.utils import timezone
from .models import EventSuggestion

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