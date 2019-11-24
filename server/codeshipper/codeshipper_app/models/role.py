# coding: utf-8

from django.db import models
from django.utils import timezone

class Role(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=50)
    server_id = models.IntegerField()
    server_name = models.CharField(max_length=50)
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(default=timezone.now)
