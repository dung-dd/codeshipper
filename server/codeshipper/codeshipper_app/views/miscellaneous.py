from django.shortcuts import render, redirect
# Create your views here.
from django.http import HttpResponse
import codeshipper_app
import os

def root_path(request):
    if (request.get_full_path() == "/"):
        return redirect("/cs/")

    context = {}
    content_type = "application/html"
    template_name = "pages/index.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))

def index(request):
    context = {}
    content_type = "application/html"
    template_name = "pages/index.html"
    return HttpResponse(render(request, template_name, context=context, content_type=content_type))


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
