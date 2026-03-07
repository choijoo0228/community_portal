from django.contrib import admin
from .models import Event, Profile, Resource, EventSuggestion

# Register your models here.
admin.site.site_header = "Community Portal Admin"
admin.site.register(Event)
admin.site.register(Resource)
admin.site.register(Profile)

@admin.action(description="Approve selected suggestions (create Events)")
def approve_suggestions(modeladmin, request, queryset):
    for s in queryset.filter(status="PENDING"):
        Event.objects.create(
            title=s.title,
            description=s.description,
            start_datetime=s.start_datetime,
            location=s.location,
            image=getattr(s, "image", None),
            is_published=True,
        )
        s.status = "APPROVED"
        s.save()

@admin.action(description="Reject selected suggestions")
def reject_suggestions(modeladmin, request, queryset):
    queryset.update(status="REJECTED")

@admin.register(EventSuggestion)
class EventSuggestionAdmin(admin.ModelAdmin):
    list_display = ("title", "start_datetime", "location", "status", "submitted_at")
    list_filter = ("status",)
    actions = ["title", "user__username"]
