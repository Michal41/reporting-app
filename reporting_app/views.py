from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from .models import Action

def driver_panel(request):
    road_list = ["956", "23", "234", "22"]
    context = {"road_list": road_list,
               "is_active": Action.objects.all().last().is_active,
               "route": Action.objects.all().last().route,
               "title": "Driver Panel"}
    return render(request, "reporting_app/driver_panel.html", context)


def driver_action_start(request):
    if (request.method == "POST") and Action.objects.all().last().is_active==False:
        action = Action(route=request.POST.get('road_list'), driver=request.user, is_active=True)
        action.save()
    return redirect("driver_panel")


def driver_action_stop(request):
    if (request.method == "POST") and Action.objects.all().last().is_active==True:
        action = Action.objects.all().last()
        action.is_active = False
        action.end_time = timezone.now()
        action.save()
    return redirect("driver_panel")