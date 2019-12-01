# coding: utf-8

from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..controllers import project as controllers
from codeshipper_app.models.project import Project, ProjectType
from django.forms.models import model_to_dict
from codeshipper_app.models.server import Server

def left_menu_project(request):
    projects = Project.objects.filter()
    context = {
        "list_data": projects
    }

    content_type = "application/html"
    template_name = "pages/project_list.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))


def project_create(request):
    servers = Server.objects.filter()
    project_type_list = ProjectType.objects.filter()
    context = {
        "server_list": servers,
        "project_type_list": project_type_list
    }
    content_type = "application/html"
    template_name = "pages/project_create.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))


def project_detail(request, project_id):
    project = Project.objects.filter(id=project_id)
    if len(project):
        project = project[0]
    else:
        project = None

    server_list = Server.objects.filter()
    project_type_list = ProjectType.objects.filter()

    _server_list = [ model_to_dict(_s) for _s in server_list ]
    _project_type_list = [ model_to_dict(_p) for _p in project_type_list ]

    context = {
        "item": model_to_dict(project),
        "server_list": _server_list,
        "project_type_list": _project_type_list
    }

    context["cs_data"] = context.copy()
    content_type = "application/html"
    template_name = "pages/project_detail.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))



""" ============= ============ ============ """
""" ============= project type ============ """
""" ============= ============ ============ """

def left_menu_project_type(request):
    projects_type = ProjectType.objects.filter().order_by("-updated_time", "-id")
    context = {
        "list_data": projects_type
    }

    content_type = "application/html"
    template_name = "pages/project_type.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))


def left_menu_project_type_create(request):
    context = {}

    content_type = "application/html"
    template_name = "pages/project_type_create.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))


def project_type_detail(request, project_type_id):
    project_type = ProjectType.objects.filter(id=project_type_id).first()
    project_type = model_to_dict(project_type) if project_type else {}
    
    context = {
        "item": project_type
    }
    context["cs_data"] = context.copy()

    content_type = "application/html"
    template_name = "pages/project_type_detail.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))
