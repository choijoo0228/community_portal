from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=120, validators=[MinLengthValidator(5)])
    description = models.TextField(blank=True, max_length=2000)
    start_datetime = models.DateTimeField()
    location = models.CharField(max_length=120)
    
    image = models.ImageField(upload_to="events/", blank=True, null=True)
    
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # future date validation will be added in the next step
        super().clean()

    def __str__(self):
        return self.title

class Resource(models.Model):
    CATEGORY_CHOICES = [
        ("legal", "Legal"),
        ("housing", "Housing"),
        ("jobs", "Jobs"),
        ("students", "Students"),
        ("health", "Health"),
        ("other", "Other"),
    ]
    title = models.CharField(max_length=120, validators=[MinLengthValidator(5)])
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    url = models.URLField()
    description = models.TextField(blank=True, max_length=2000)
    
    image = models.ImageField(upload_to="resources/", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class EventSuggestion(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]
    title = models.CharField(max_length=120, validators=[MinLengthValidator(5)])
    description = models.TextField(blank=True, max_length=2000)
    start_datetime = models.DateTimeField()
    location = models.CharField(max_length=120)
    image = models.ImageField(upload_to="event_suggestions/", blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.status})"