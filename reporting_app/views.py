from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from .models import Action
from django.contrib.auth.models import User
from .models import Profile
def driver_panel(request):
    road_list = ["956", "23", "234", "22"]
    context = {"road_list": road_list,
               "is_active": Action.objects.filter(driver=request.user).last().is_active,
               "route": Action.objects.filter(driver=request.user).last().route,
               "title": "Driver Panel"}
    return render(request, "reporting_app/driver_panel.html", context)


def main_panel(request):
    drivers_stats = [(Action.objects.filter(driver=x.user).last(),
                      i) for x, i in zip(Profile.objects.filter(is_driver=True),
                            range(1,1+len(Profile.objects.filter(is_driver=True))))]
    context = {"drivers_stats":drivers_stats,
               }
    return render(request, "reporting_app/main_panel.html", context)

def driver_action_start(request):
    if (request.method == "POST") and Action.objects.filter(driver=request.user).last().is_active==False:
        action = Action(route=request.POST.get('road_list'), driver=request.user, is_active=True)
        action.save()
    return redirect("driver_panel")


def driver_action_stop(request):
    if (request.method == "POST") and Action.objects.filter(driver=request.user).last().is_active==True:
        action = Action.objects.filter(driver=request.user).last()
        action.is_active = False
        action.end_time = timezone.now()
        action.save()
    return redirect("driver_panel")