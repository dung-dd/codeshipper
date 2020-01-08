# coding: utf-8

import os
from django.http import HttpResponse
from django.shortcuts import render, redirect
import codeshipper_app


def accounts_settings(request):
    return HttpResponse("<h1><center>Account Settings</center></h1>")

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


def handler404(request, exception):
    context = { }
    content_type = "application/html"
    template_name = "error_pages/404.html"
    # return HttpResponse(render(request, template_name, context=context, content_type=content_type))
    return HttpResponse('Error handler content', status=404)