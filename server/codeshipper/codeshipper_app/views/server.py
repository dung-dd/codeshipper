# coding: utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..controllers import server as controllers
from codeshipper_app.models.server import Server
import json, pytz

def left_menu_server(request):
    user = request.user 
    if not user.id:
        return redirect("/accounts/login/")

    servers = Server.objects.filter().order_by("-id")
    context = {
        "list_data": servers
    }
    content_type = "application/html"
    template_name = "pages/server_list.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))


def server_create(request):
    user = request.user 
    if not user.id:
        return redirect("/accounts/login/")

    context = {}
    content_type = "application/html"
    template_name = "pages/server_create.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))


def server_detail(request, server_id):
    user = request.user 
    if not user.id:
        return redirect("/accounts/login/")

    server = Server.objects.filter(id=server_id)
    if (len(server)):
        server = server[0]
        server = {
            "id": server.id,
            "name": server.name,
            "port": server.port,
            "secret": server.secret,
            "note": server.note,
            "updated_time": server.updated_time.astimezone(pytz.timezone(pytz.country_timezones("VN")[0])).__str__(),
            "created_time": server.created_time.astimezone(pytz.timezone(pytz.country_timezones("VN")[0])).__str__()
        }
    else:
        server = None

    context = {
        "item": server,
    }
    context["cs_data"] = context.copy()

    content_type = "application/html"
    template_name = "pages/server_detail.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))


def server_edit(request):
    user = request.user 
    if not user.id:
        return redirect("/accounts/login/")
        
    context = {}
    content_type = "application/html"
    template_name = "pages/server_edit.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))
