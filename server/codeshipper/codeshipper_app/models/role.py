# coding: utf-8

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from . import server, project


class Role(models.Model):

    def on_delete_user(self):
        print( "on delete user in role" )

    def on_delete_server(self):
        print( "on delete server in role" )

    def on_delete_project(self):
        print( "on delete project in role" )

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, default="")
    role = models.CharField(max_length=50, default="")
    
    user = models.ForeignKey(User, on_delete=models.SET(on_delete_user), blank=True, null=True)
    user_name = models.CharField(max_length=50, default="")

    server = models.ForeignKey(server.Server, on_delete=models.SET(on_delete_server), blank=True, null=True)
    server_name = models.CharField(max_length=50, default="")

    project = models.ForeignKey(project.Project, on_delete=models.SET(on_delete_project), blank=True, null=True)
    project_name = models.CharField(max_length=100, default="")

    updated_time = models.DateTimeField(default=timezone.now)
    created_time = models.DateTimeField(default=timezone.now)
