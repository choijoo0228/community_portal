from time import timezone

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Event

# Create your views here.

def home(request):
    return render(request, "portal/home.html")

def events_list(request):
    events = (
        Event.objects
        .filter(is_published=True)
        .order_by("start_datetime")
    )
    return render(request, "portal/events_list.html", {"events": events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id, is_published=True)
    return render(request, "portal/event_detail.html", {"event": event})

def resources_list(request):
    return HttpResponse("Resources page")

def suggest_event(request):
    return HttpResponse("Suggest Event page")
