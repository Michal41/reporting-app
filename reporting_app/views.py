from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Action
from .models import Profile
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from .report import Report
from django.contrib import messages

@login_required()
def driver_panel(request):
    road_list = ["956", "23", "234", "22"]

    if not Profile.objects.filter(user=request.user).last().is_driver:
        messages.error(request, 'You do not have access to this page', extra_tags='danger')
        return redirect("main_panel")


    if not(Action.objects.filter(driver=request.user).last()):
        empty_action = Action(driver=request.user, route="0")
        empty_action.save()

    context = {"road_list": road_list,
               "is_active": Action.objects.filter(driver=request.user).last().is_active,
               "route": Action.objects.filter(driver=request.user).last().route,
               "title": "Driver Panel"}
    return render(request, "reporting_app/driver_panel.html", context)

@login_required()
def main_panel(request):
    drivers_stats = [(Action.objects.filter(driver=x.user).last(),
                      i) for x, i in zip(Profile.objects.filter(is_driver=True),
                            range(1,1+len(Profile.objects.filter(is_driver=True))))]
    context = {"drivers_stats":drivers_stats,
               }
    return render(request, "reporting_app/main_panel.html", context)


def report_panel(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have access to this page', extra_tags='danger')
        return redirect("main_panel")
    return render(request, "reporting_app/report_panel.html",)

@login_required()
def driver_action_start(request):
    if request.method == "POST" and Action.objects.filter(driver=request.user).last().is_active==False:
        action = Action(route=request.POST.get('road_list'), driver=request.user, is_active=True)
        action.save()
        Report.send_report()
    return redirect("driver_panel")

@login_required()
def driver_action_stop(request):
    if (request.method == "POST") and Action.objects.filter(driver=request.user).last().is_active ==True:
        action = Action.objects.filter(driver=request.user).last()
        action.is_active = False
        action.end_time = timezone.now()
        action.save()
    return redirect("driver_panel")

@staff_member_required(login_url = "main_panel")
def send_report(request):
    messages.error(request, 'E-mail sent', extra_tags='success')
    Report.send_report()
    return redirect("main_panel")