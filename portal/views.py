from time import timezone

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .forms import EventSuggestionForm, RegisterForm
from django.contrib.auth.decorators import login_required

from .models import Event, Resource, EventSuggestion
from django.contrib.auth import login
# Create your views here.

def home(request):
    upcoming_events = (
        Event.objects
        .filter(is_published=True, start_datetime__gte=timezone.now())
        .order_by("start_datetime")[:3]
    )
    
    latest_resources = Resource.objects.order_by("-created_at")[:3]
    
    print("Upcoming events count:", upcoming_events.count())
    print("Resources count:", latest_resources.count())
    
    context = {
        "upcoming_events": upcoming_events,
        "latest_resources": latest_resources,
    }
    
    return render(request, "portal/home.html", context)

def events_list(request):
    events = (
        Event.objects
        .filter(is_published=True, start_datetime__gte=timezone.now())
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

@login_required
def suggest_event(request):
    if request.method == "POST":
        form = EventSuggestionForm(request.POST, request.FILES)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.user = request.user
            suggestion.status = "PENDING"
            suggestion.save()
            return redirect("suggest_event_success")
    else:
        form = EventSuggestionForm()

    return render(request, "portal/suggest_event.html", {"form": form})


def suggest_event_success(request):
    return render(request, "portal/suggest_event_success.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "portal/register.html", {"form": form})

@login_required
def user_section(request):
    profile = getattr(request.user, "profile", None)
    return render(request, "portal/user_section.html", {"profile": profile})

@login_required
def my_suggestions(request):
    suggestions = EventSuggestion.objects.filter(user=request.user).order_by("-submitted_at")
    return render(request, "portal/my_suggestions.html", {"suggestions": suggestions})