from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Action(models.Model):
    route = models.CharField(max_length=20)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.driver.username +" route " + self.route

