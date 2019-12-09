from django.shortcuts import render, redirect
# Create your views here.
from django.http import HttpResponse
import os

from django.contrib.auth.models import User

import codeshipper_app
from codeshipper_app.models.server import Server
from codeshipper_app.models.project import Project
from codeshipper_app.models.updating import Updating 

def root_path(request):
    if (request.get_full_path() == "/"):
        return redirect("/cs/")

    total_servers   = Server.objects.filter().count() or 0
    total_projects  = Project.objects.filter().count() or 0
    total_users     = User.objects.filter().count() or 0
    total_updatings = Updating.objects.filter().count() or 0

    context = {
        "total_servers": total_servers,
        "total_projects": total_projects,
        "total_users": total_users,
        "total_updatings": total_updatings,
    }
    content_type = "application/html"
    template_name = "pages/index.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))

def index(request):
    return root_path(request)


def left_menu_users(request):
    context = {}
    content_type = "application/html"
    template_name = "pages/user.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))


def a1ecc3b826d01251edddf29c3e4e1e97_woff(request):
    static_folder = os.path.dirname(codeshipper_app.__file__)
    font_file = os.path.join(static_folder, "static", "a1ecc3b826d01251edddf29c3e4e1e97.woff")
    try:
        with open(font_file, "rb") as f:
            woff = f.read()
    except:
        print ("[Font] " + font_file + " not found")
    return HttpResponse(woff)

def a1ecc3b826d01251edddf29c3e4e1e97_woff(request):
    static_folder = os.path.dirname(codeshipper_app.__file__)
    font_file = os.path.join(static_folder, "static", "a1ecc3b826d01251edddf29c3e4e1e97.woff")
    try:
        with open(font_file, "rb") as f:
            woff = f.read()
    except:
        print ("[Font] " + font_file + " not found")
    return HttpResponse(woff)

def af7ae505a9eed503f8b8e6982036873e_woff2(request):
    static_folder = os.path.dirname(codeshipper_app.__file__)
    font_file = os.path.join(static_folder, "static", "af7ae505a9eed503f8b8e6982036873e.woff2")
    try:
        with open(font_file, "rb") as f:
            woff = f.read()
    except:
        print ("[Font] " + font_file + " not found")
    return HttpResponse(woff)

def fee66e712a8a08eef5805a46892932ad_woff(request):
    static_folder = os.path.dirname(codeshipper_app.__file__)
    font_file = os.path.join(static_folder, "static", "fee66e712a8a08eef5805a46892932ad.woff")
    try:
        with open(font_file, "rb") as f:
            woff = f.read()
    except:
        print ("[Font] " + font_file + " not found")
    return HttpResponse(woff)
