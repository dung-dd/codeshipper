# coding: utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms.models import model_to_dict

from ..controllers import updating as controllers
from codeshipper_app.models.project import Project
from codeshipper_app.models.updating import Updating

import json, pytz, datetime 

timezone = pytz.timezone(pytz.country_timezones("VN")[0])

def left_menu_updating(request):
    updatings = Updating.objects.filter()
    context = {
        "list_data": updatings
    }
    content_type = "application/html"
    template_name = "pages/updating_list.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))


def updating_create(request):
    updates = Updating.objects.filter()
    projects = Project.objects.filter()
    
    context = {
        "list_data": updates,
        "project_list": projects
    }
    content_type = "application/html"
    template_name = "pages/updating_create.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))


def updating_detail(request, updating_id):
    update = Updating.objects.filter(id=updating_id).first()
    
    now = datetime.datetime.now() 
    now = now.astimezone(timezone)
    deploy_time = update.deploy_time 
    deploy_time = deploy_time.astimezone(timezone)
    update.deploy_time_date = deploy_time.strftime("%Y-%m-%d")
    update.deploy_time_hour = deploy_time.strftime("%H:%M")
    
    update.editable = deploy_time > now 
    
    context = {
        "item": update,
    }
    content_type = "application/html"
    template_name = "pages/updating_detail.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))