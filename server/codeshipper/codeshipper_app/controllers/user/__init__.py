# coding: utf-8

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json, requests, jwt, base64
import datetime, re, os, pytz, traceback 

from codeshipper_app import secure
from codeshipper_app.models.server import Server
from codeshipper_app.models.project import Project
from codeshipper_app.models.role import Role
from django.contrib.auth.models import User


@require_http_methods(["POST"])
@csrf_exempt
def add_role(request):
    json_response = {"state": 1, "message": "Thành công" }
    body_json = {}
    try:
        body_json = json.loads(request.body)
    except:
        body_json = None
    if not body_json:
        json_response["state"] = 0
        json_response["message"] = "Dữ liệu không hợp lệ"
        return HttpResponse(json.dumps(json_response))
    role_type = body_json.get("type") or ""

    server = None
    server_name = ""
    project = None
    project_name = ""

    role_name = "manage" 
    if role_type == "server":
        server_id = body_json.get("server_id")
        server = Server.objects.filter(id=server_id).first()
        if server:
            server_name = server.name

    if role_type == "project":
        project_id = body_json.get("project_id")
        project = Project.objects.filter(id=project_id).first()
        if project:
            project_name = project.name 

    if not project and not server:
        json_response["state"] = 0
        json_response["message"] = "Dữ liệu không tồn tại"
        return HttpResponse(json.dumps(json_response))
    
    user_id = body_json.get("user_id")
    user = User.objects.filter(id=user_id).first()
    user_name = ""
    if user:
        user_name = user.username
    new_role = Role(
                    type=role_type,
                    role=role_name,
                    server=server,
                    server_name=server_name, 
                    project=project,
                    project_name=project_name,
                    user=user,
                    user_name=user_name
    )
    new_role.save()
    
    return HttpResponse(json.dumps(json_response))


@require_http_methods(["POST"])
@csrf_exempt
def delete_role(request):
    json_response = {"state": 1, "message": "Thành công" }
    body_json = {}
    try:
        body_json = json.loads(request.body)
    except:
        body_json = None
    if not body_json:
        json_response["state"] = 0
        json_response["message"] = "Dữ liệu không hợp lệ"
        return HttpResponse(json.dumps(json_response))
    role_id = body_json.get("role_id") or ""
    role_obj = Role.objects.filter(id=role_id).first()
    if role_obj:
        role_obj.delete()
    else:
        json_response["state"] = 0
        json_response["message"] = "Dữ liệu không hợp lệ"
    return HttpResponse(json.dumps(json_response))