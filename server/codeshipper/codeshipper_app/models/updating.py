# coding: utf-8

from django.db import models
from django.utils import timezone
from . import server
from . import project

class Updating(models.Model):

    def on_delete_server(*args, **kwargs):
        print ("on_delete_server", args, kwargs)

    def on_delete_project(*args, **kwargs):
        print ("on_delete_project", args, kwargs)


    id = models.AutoField(primary_key=True)
    project_id = models.ForeignKey(project.Project, on_delete=models.SET(on_delete_project))
    project_name = models.CharField(max_length=50)
    project_version = models.CharField(max_length=10, unique=True)
    server_id = models.ForeignKey(server.Server, on_delete=models.SET(on_delete_server))
    deploy_type = models.CharField(max_length=50)
    deploy_time = models.DateTimeField()
    command_name = models.CharField(max_length=50)
    command_data = models.CharField(max_length=50)

    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(default=timezone.now)
