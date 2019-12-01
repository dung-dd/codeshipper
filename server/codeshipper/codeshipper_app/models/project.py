# coding: utf-8

from django.db import models
from django.utils import timezone


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, unique=True)
    server = models.IntegerField(max_length=50, default="")
    type = models.IntegerField(max_length=50, blank=True, null=True)
    config_path = models.CharField(max_length=100, default="")
    config_service = models.TextField(max_length=50, default="")
    script_deploy = models.TextField(max_length=50, default="")
    version = models.CharField(max_length=50, default="")
    note = models.TextField(max_length=50, default="")
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(default=timezone.now)


class ProjectType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    configuration = models.TextField(default="")
    script = models.TextField(default="")
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(default=timezone.now)
