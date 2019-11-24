# coding: utf-8

from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..controllers import project as controllers

def left_menu_project(request):
    context = {}
    content_type = "application/html"
    template_name = "pages/project_list.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))


def project_create(request):
    context = {}
    content_type = "application/html"
    template_name = "pages/project_create.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))
