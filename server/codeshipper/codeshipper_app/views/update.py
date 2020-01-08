# coding: utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms.models import model_to_dict

from ..controllers import update as controllers
from codeshipper_app.models.project import Project
from codeshipper_app.models.update import Update

import json, pytz, datetime 

timezone = pytz.timezone(pytz.country_timezones("VN")[0])

def left_menu_update(request):
    user = request.user 
    if not user.id:
        return redirect("/accounts/login/")

    updates = Update.objects.filter().order_by("-id")
    context = {
        "list_data": updates
    }
    content_type = "application/html"
    template_name = "pages/update_list.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))


def update_create(request):
    user = request.user 
    if not user.id:
        return redirect("/accounts/login/")

    updates = Update.objects.filter().order_by("-id")
    projects = Project.objects.filter().order_by("-id")
    
    context = {
        "list_data": updates,
        "project_list": projects
    }
    content_type = "application/html"
    template_name = "pages/update_create.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))


def update_detail(request, update_id):
    user = request.user 
    if not user.id:
        return redirect("/accounts/login/")
        
    update = Update.objects.filter(id=update_id).first()
    
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
    template_name = "pages/update_detail.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))