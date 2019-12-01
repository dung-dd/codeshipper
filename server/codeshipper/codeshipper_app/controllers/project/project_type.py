# coding: utf-8

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json, requests, jwt, datetime
from codeshipper_app.models.project import Project, ProjectType


@require_http_methods(["POST"])
@csrf_exempt
def pt_create_project_type(request):
    json_response = {"state": 1, "message": "Tạo mới thành công" }
    body_json = {}
    try:
        body_json = json.loads(request.body)
    except:
        body_json = None
    if not body_json:
        json_response["state"] = 0
        json_response["message"] = "Dữ liệu không hợp lệ"
        return HttpResponse(json.dumps(json_response))

    REQUIRES = [("name", str, "Tên")]
    for field in REQUIRES:
        if not body_json[field[0]]:
            json_response["state"] = 0
            json_response["message"] = "{} không hợp lệ".format(field[2])
        if not isinstance(body_json[field[0]], field[1]):
            json_response["state"] = 0
            json_response["message"] = "Kiểu dữ liệu của trường {} không hợp lệ".format(field[2])
    if not json_response["state"]:
        return HttpResponse(json.dumps(json_response))

    new_project_type = ProjectType(
                                    name=body_json["name"],
                                    configuration=body_json["configuration"],
                                    script=body_json["script"],
                                )
    new_project_type.save()

    json_response["id"] = new_project_type.id
    return HttpResponse(json.dumps(json_response))


@require_http_methods(["POST"])
@csrf_exempt
def pt_update_project_type(request):
    json_response = {"state": 1, "message": "Cập nhật thành công" }

    body_json = {}
    try:
        body_json = json.loads(request.body)
    except:
        body_json = None

    id = body_json.get("id")
    name = body_json.get("name")
    configuration = body_json.get("configuration")
    script = body_json.get("script")

    pt = ProjectType.objects.filter(id=id).first()
    if not pt:
        json_response["state"] = 0
        json_response["message"] = "Không tồn tại bản ghi"
        return HttpResponse(json.dumps(json_response))

    print("name, configuration, script", name, configuration, script)
    pt.name = name
    pt.configuration = configuration
    pt.script = script
    pt.save()

    return HttpResponse(json.dumps(json_response))


# delete project type
@require_http_methods(["POST"])
@csrf_exempt
def pt_delete_project_type(request):
    def delete_one(item_id):
        return ProjectType.objects.filter(id=item_id).delete()
    def delete_multi(item_ids):
        for item_id in item_ids:
            delete_one(item_id)
    json_response = {"state": 1, "message": "Xóa thành công" }

    try:
        body_json = json.loads(request.body)
    except:
        body_json = None
    if not body_json:
        json_response["state"] = 0
        json_response["message"] = "Dữ liệu không hợp lệ"
        return HttpResponse(json.dumps(json_response))

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

    return HttpResponse(json.dumps(json_response))


# get config project type
@require_http_methods(["POST"])
@csrf_exempt
def get_config_project_type(request):
    json_response = {"state": 1, "data": None}
    body_json = {}

    try:
        body_json = json.loads(request.body)
    except:
        body_json = None
    if not body_json:
        json_response["state"] = 0
        json_response["message"] = "Dữ liệu không hợp lệ"
        return HttpResponse(json.dumps(json_response))

    project_type_id = body_json.get("id") or None
    pt = ProjectType.objects.filter(id=project_type_id)
    if not pt:
        json_response["state"] = 0
        json_response["data"] = None
        return HttpResponse(json.dumps(json_response))

    pt = pt[0]
    json_response["data"] = {
        "configuration": pt.configuration,
        "script": pt.script
    }
    return HttpResponse(json.dumps(json_response))
