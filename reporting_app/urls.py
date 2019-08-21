from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from crispy_forms.helper import FormHelper
urlpatterns = [
    path('driver_panel/', views.driver_panel, name="driver_panel"),
    path('main_panel/', views.main_panel, name="main_panel"),
    path('driver_action_start/', views.driver_action_start, name="driver_action_start"),
    path('driver_action_stop/', views.driver_action_stop, name="driver_action_stop"),
    path('', auth_views.LoginView.as_view(template_name='reporting_app/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
]
