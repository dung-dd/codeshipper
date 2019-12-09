# coding: utf-8

from django.db import models
from django.utils import timezone
from . import server
from . import project

class Updating(models.Model):

    def on_delete_server(self, *args, **kwargs):
        print ("on_delete_server", args, kwargs)

    def on_delete_project(self, *args, **kwargs):
        print ("on_delete_project", args, kwargs)

    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(project.Project, on_delete=models.SET(on_delete_project))
    project_name = models.CharField(max_length=50, default="")
    project_version = models.CharField(max_length=50, default="", unique=True)
    server = models.ForeignKey(server.Server, on_delete=models.SET(on_delete_server), default="")
    server_host = models.CharField(max_length=100, default="")
    deploy_type = models.CharField(max_length=50, default="")
    deploy_time = models.DateTimeField()

    updating_type = models.CharField(max_length=50, default="")
    source_code_path = models.CharField(max_length=100, default="")
    config_path = models.CharField(max_length=100, default="")
    config_service = models.CharField(max_length=50, default="")
    deploy_script = models.CharField(max_length=50, default="")
    note = models.TextField(default="")

    rollback = models.BooleanField(default=True)
    state= models.CharField(max_length=50, default="undefined")
    output = models.TextField(default="")

    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(default=timezone.now)
