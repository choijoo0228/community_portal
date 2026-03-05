from django.contrib import admin
from .models import Event, Resource, EventSuggestion

# Register your models here.
admin.site.site_header = "Community Portal Admin"
admin.site.register(Event)
admin.site.register(Resource)
admin.site.register(EventSuggestion)
