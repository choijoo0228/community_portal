import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .forms import EventSuggestionForm, RegisterForm
from django.contrib.auth.decorators import login_required

from .models import Event, Resource, EventSuggestion
from django.contrib.auth import login
from django.utils import timezone
# Create your views here.
logger = logging.getLogger(__name__)


# show home page; upcoming events and recent resources
def home(request):
    try:
        # get 3 future events that are published
        upcoming_events = (
            Event.objects
            .filter(is_published=True, start_datetime__gte=timezone.now())
            .order_by("start_datetime")[:3]
        )
        
        # get 3 recent resources
        latest_resources = Resource.objects.order_by("-created_at")[:3]
        
        logger.info("Upcoming events count: %s, Resources count: %s", upcoming_events.count(), latest_resources.count())
        
        context = {
            "upcoming_events": upcoming_events,
            "latest_resources": latest_resources,
        }
        
        return render(request, "portal/home.html", context)
    except Exception as e:
        logger.error("Error in home view: %s", str(e))
        return render(request, "portal/home.html", {"error": "An error occurred while loading the home page. Please try again."})

# show all published future events in a list
def events_list(request):
    try:
        # get all future events that are published
        events = (
            Event.objects
            .filter(is_published=True, start_datetime__gte=timezone.now())
            .order_by("start_datetime") # ordering by start date
        )
        logger.info("Retrieved events list")
        return render(request, "portal/events_list.html", {"events": events})
    except Exception as e:
        logger.error("Error in events_list view: %s", str(e))
        return render(request, "portal/events_list.html", {"events": [], "error": "An error occurred while loading events. Please try again."})


# show details of one event
def event_detail(request, event_id):
    try:
        # get the event by ID. If not found or not published, show 404 error
        event = get_object_or_404(Event, id=event_id, is_published=True)
        
        logger.info("Retrieved event detail for event_id: %s", event_id)
        return render(request, "portal/event_detail.html", {"event": event})
    except Exception as e:
        logger.error("Error in event_detail view: %s", str(e))
        return render(request, "portal/event_detail.html", {"error": "An error occurred while loading event details. Please try again."})

# shows all resources; user can search by keyword or category
def resources_list(request):
    try:
        # get all resources ordered by newest first
        resources = Resource.objects.all().order_by("-created_at")

        # get search parameters from typing /query string and category/
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
        
        logger.info("Retrieved resources list with query: %s, category: %s", query, category)
        return render(request, "portal/resources_list.html", context)
    except Exception as e:
        
        logger.error("Error in resources_list view: %s", str(e))
        return render(request, "portal/resources_list.html", {"resources": [], "error": "An error occurred while loading resources. Please try again."})

# logged-in users suggest new events
@login_required
def suggest_event(request):
    try:
        if request.method == "POST":
            # user submitted the form
            form = EventSuggestionForm(request.POST, request.FILES)
            if form.is_valid():
                suggestion = form.save(commit=False)
                suggestion.user = request.user 
                suggestion.status = "PENDING"   # new suggestions set in pending status for admin review
                suggestion.save()  # save to database
                
                logger.info("Event suggestion submitted by user: %s", request.user.username)
                return redirect("suggest_event_success")
        else:
            # create empty form
            form = EventSuggestionForm()

        return render(request, "portal/suggest_event.html", {"form": form})
    except Exception as e:
        logger.error("Error in suggest_event view: %s", str(e))
        return render(request, "portal/suggest_event.html", {"form": EventSuggestionForm(), "error": "An error occurred while submitting your suggestion. Please try again."})


# show a success message after event suggestion is submitted
def suggest_event_success(request):
    try:
        logger.info("Reached suggest_event_success page")
        return render(request, "portal/suggest_event_success.html")
    except Exception as e:
        logger.error("Error in suggest_event_success view: %s", str(e))
        return render(request, "portal/suggest_event_success.html", {"error": "An error occurred. Please try again."})

# new users create an account
def register(request):
    try:
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)

                logger.info("New user registered: %s", user.username)
                return redirect("home")
        else:
            # create empty form
            form = RegisterForm()

        return render(request, "portal/register.html", {"form": form})
    except Exception as e:
        # If error happens, log it and show error message
        logger.error("Error in register view: %s", str(e))
        return render(request, "portal/register.html", {"form": RegisterForm(), "error": "An error occurred during registration. Please try again."})

# show the user profile page
@login_required # only logged-in users
def user_section(request):
    try:
        profile = getattr(request.user, "profile", None)
        
        logger.info("User section accessed by user: %s", request.user.username)
        return render(request, "portal/user_section.html", {"profile": profile})
    except Exception as e:
        
        logger.error("Error in user_section view: %s", str(e))
        return render(request, "portal/user_section.html", {"error": "An error occurred while loading user section. Please try again."})

# show all event suggestions submitted by the logged-in user
@login_required
def my_suggestions(request):
    try:
        # get all suggestions from this user
        suggestions = EventSuggestion.objects.filter(user=request.user).order_by("-submitted_at")
        
        logger.info("Retrieved suggestions for user: %s", request.user.username)
        return render(request, "portal/my_suggestions.html", {"suggestions": suggestions})
    except Exception as e:
        logger.error("Error in my_suggestions view: %s", str(e))
        return render(request, "portal/my_suggestions.html", {"suggestions": [], "error": "An error occurred while loading your suggestions. Please try again."})