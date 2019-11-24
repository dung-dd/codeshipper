# coding: utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..controllers import server as controllers
from codeshipper_app.models.server import Server 


def left_menu_server_list(request):
    servers = Server.objects.filter()
    context = {
        "list_data": servers
    }
    content_type = "application/html"
    template_name = "pages/server_list.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))


def left_menu_server_create(request):
    context = {}
    content_type = "application/html"
    template_name = "pages/server_create.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))


def left_menu_server_detail(request):
    context = {}
    content_type = "application/html"
    template_name = "pages/servers_create.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))


print ("controllers", dir(controllers))
