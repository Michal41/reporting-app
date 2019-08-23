from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Action
from .models import Profile
from django.contrib.auth.decorators import login_required
from .report import Report
from django.contrib import messages

@login_required()
def driver_panel(request):
    #if Profile.objects.filter(user=request.user).first().supervisor_account:
        #messages.error(request, 'You do not have access to this page', extra_tags='danger')
        #return redirect("main_panel")
    road_list = ["956", "23", "234", "22"]
    context = {"road_list": road_list,
               "is_active": Action.objects.filter(driver=request.user).last().is_active,
               "route": Action.objects.filter(driver=request.user).last().route,
               "title": "Driver Panel"}
    return render(request, "reporting_app/driver_panel.html", context)

@login_required()
def main_panel(request):
    if not(Profile.objects.filter(user=request.user).first().supervisor_account):
        messages.error(request, 'You do not have access to this page', extra_tags='danger')
        return redirect("driver_panel")

    drivers_stats = [(Action.objects.filter(driver=x.user).last(),
                      i) for x, i in zip(Profile.objects.filter(supervisor_account=False),
                            range(1,1+len(Profile.objects.filter(supervisor_account=False))))]
    context = {"drivers_stats":drivers_stats,
               }
    return render(request, "reporting_app/main_panel.html", context)
@login_required()
def driver_action_start(request):
    if (request.method == "POST") and Action.objects.filter(driver=request.user).last().is_active==False:
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
@login_required()
def send_report(request):
    messages.error(request, 'E-mail sent', extra_tags='success')
    Report.send_report()
    return redirect("main_panel")