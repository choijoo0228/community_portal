from django.urls import path
from . import views

urlpatterns = [
    path("events/", views.events_list, name="events_list"),
    path("events/<int:event_id>/", views.event_detail, name="event_detail"),
    path("resources/", views.resources_list, name="resources_list"),
    path("suggest-event/", views.suggest_event, name="suggest_event"),
]