# coding: utf-8

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json, requests, jwt, datetime, pytz

from codeshipper_app.models.server import Server
from codeshipper_app.models.project import Project, ProjectType
from . import project_type as pt

@require_http_methods(["POST"])
@csrf_exempt
def create_project(request):
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
    source_code_path = body_json.get("source_code_path")
    config_path = body_json.get("config_path")
    script_deploy = body_json.get("script_deploy")
    note = body_json.get("note")

    if not name or not code or not server or not type or not config_service:
        return HttpResponse(json.dumps({ "state": 0, "message": "Dữ liệu không hợp lệ" }))
    if type:
        type = ProjectType.objects.filter(id=type).first()
    if server:
        server = Server.objects.filter(id=server).first()

    new_project = Project(
        name=name,
        server=server,
        code=code,
        type=type,
        source_code_path=source_code_path,
        config_path=config_path,
        config_service=config_service,
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


@require_http_methods(["POST"])
@csrf_exempt
def update_project(request):
    json_response = {"state": 1, "message": "Cập nhật thành công" }

    body_json = {}
    try:
        body_json = json.loads(request.body)
    except:
        body_json = None

    id = body_json.get("id")
    name = body_json.get("name")
    code = body_json.get("code")
    server = body_json.get("server")
    type = body_json.get("type")
    config_service = body_json.get("config_service")
    config_path = body_json.get("config_path")
    script_deploy = body_json.get("script_deploy")
    note = body_json.get("note")

    server = int(server) if server else None
    type = int(type) if type else None
    if not id or not name or not code or not server:
        print ("id or not name or not code or not server", id , name , code , server)
        return HttpResponse(json.dumps({ "state": 0, "message": "Vui lòng cung cấp đầy đủ thông tin" }))
    
    type = ProjectType.objects.filter(id=type).first()
    server = Server.objects.filter(id=server).first()
    if not server:
        return HttpResponse(json.dumps({ "state": 0, "message": "Server không hợp lệ" }))
    project = Project.objects.filter(id=id).first()
    if not project:
        return HttpResponse(json.dumps({ "state": 0, "message": "Bản ghi không tồn tại" }))

    updated_time = datetime.datetime.now()
    updated_time.astimezone(pytz.timezone(pytz.country_timezones("Vn")[0]))
    project.name = name
    project.code = code

    project.server = server
    project.type = type
    project.config_service = config_service
    project.config_path = config_path
    project.script_deploy = script_deploy
    project.note = note
    project.updated_time = updated_time

    project.save()

    return HttpResponse(json.dumps(json_response))


@require_http_methods(["POST"])
@csrf_exempt
def delete_project(request):
    def delete_one(item_id):
        return Project.objects.filter(id=item_id).delete()
    def delete_multi(item_ids):
        for item_id in item_ids:
            delete_one(item_id)
    json_response = {"state": 1, "message": "Xóa thành công" }
    body_json = {}
    try:
        body_json = json.loads(request.body)
    except:
        body_json = None

    id = body_json.get("id")
    ids = body_json.get("ids")
    #
    if not id and not ids:
        return HttpResponse(json.dumps({ "state": 0, "message": "Thông tin không hợp lệ" }))
    #
    if id:
        delete_one(id)
    if ids:
        delete_multi(ids)

    return HttpResponse(json.dumps({"state": 1, "message": "Xóa thành công" }))
