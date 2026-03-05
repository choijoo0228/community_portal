from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "portal/home.html")

def events_list(request):
    return HttpResponse("Events page")

def resources_list(request):
    return HttpResponse("Resources page")

def suggest_event(request):
    return HttpResponse("Suggest Event page")
