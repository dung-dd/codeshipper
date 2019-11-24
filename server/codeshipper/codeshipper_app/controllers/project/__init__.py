# coding: utf-8

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json, requests, jwt, datetime

from codeshipper_app.models.project import Project


@require_http_methods(["POST"])
@csrf_exempt
def create_new_project(request):
    json_response = {"state": 1, "message": "Tạo mới thành công" }
    body_json = {}
    try:
        body_json = json.loads(request.body)
    except:
        body_json = None

    name = body_json.get("name")
    code = body_json.get("code")
    server = body_json.get("server")
    type = body_json.get("type")
    config_service = body_json.get("config_service")
    variables = body_json.get("variables")
    script_deploy = body_json.get("script_deploy")
    note = body_json.get("note")

    if not name or not code or not server or not type or not config_service:
        return HttpResponse(json.dumps({ "state": 0, "message": "Dữ liệu không hợp lệ" }))

    new_project = Project(
        name=name,
        code=code,
        type=type,
        config_service=config_service,
        variables=variables,
        script_deploy=script_deploy,
        note=note
    )

    try:
        x = new_project.save()
    except Exception as e:
        print (e)
        json_response["state"] = 0
        json_response["message"] = "Project Code đã tồn tại, hãy tạo Project Code khác trước khi lưu"

    return HttpResponse(json.dumps(json_response))
