# coding: utf-8

from django.db import models
from django.utils import timezone


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50, default="")
    config_service = models.CharField(max_length=50, default="")
    variables = models.CharField(max_length=50, default="")
    script_deploy = models.CharField(max_length=50, default="")
    version = models.CharField(max_length=50, default="")
    note = models.TextField(max_length=50, default="")
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(default=timezone.now)
