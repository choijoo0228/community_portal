from time import timezone

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .forms import EventSuggestionForm

from .models import Event, Resource, EventSuggestion

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
    resources = Resource.objects.all().order_by("-created_at")

    query = request.GET.get("q", "")
    category = request.GET.get("category", "")

    if query:
        resources = resources.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    if category:
        resources = resources.filter(category=category)

    categories = Resource.CATEGORY_CHOICES

    context = {
        "resources": resources,
        "query": query,
        "selected_category": category,
        "categories": categories,
    }
    return render(request, "portal/resources_list.html", context)

def suggest_event(request):
    if request.method == "POST":
        form = EventSuggestionForm(request.POST, request.FILES)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.status = "PENDING"
            suggestion.save()
            return redirect("suggest_event_success")
    else:
        form = EventSuggestionForm()

    return render(request, "portal/suggest_event.html", {"form": form})


def suggest_event_success(request):
    return render(request, "portal/suggest_event_success.html")
