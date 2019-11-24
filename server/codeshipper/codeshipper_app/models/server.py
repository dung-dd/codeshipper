# coding: utf-8

from django.db import models
from django.utils import timezone


class Server(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    port = models.IntegerField()
    secret = models.CharField(max_length=50)
    note = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(default=timezone.now)
