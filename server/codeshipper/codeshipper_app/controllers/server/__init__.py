# coding: utf-8

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json, requests, jwt, datetime, re

from codeshipper_app import secure
from codeshipper_app.models.server import Server

@require_http_methods(["POST"])
@csrf_exempt
def test_connection(request):
    connect_state = 0
    connect_message = "Kết nối không thành công"

    body_json = {}
    try:
        body_json = json.loads(request.body)
    except:
        body_json = None

    if not body_json or not body_json.get("name") or not body_json.get("name").strip() or not body_json.get("port") or not body_json.get("port").strip() or not body_json.get("secret"):
        return HttpResponse(json.dumps({ "state": 0, "message": "Dữ liệu không hợp lệ" }))

    uri = body_json.get("name")+":"+body_json.get("port") + "/test_connection"
    if not uri.startswith("https?://"):
        uri += "http://"

    data = json.dumps({
        "command": "test_connection",
        "echo": "hello client"
    })
    headers = { "Content-Type": "application/json" }
    try:
        r = requests.post(uri, data=data, headers=headers)
        connect_ok = r.data.state

        if not connect_ok:
            connect_error = connect_ok = r.data.message
    except:
        r = None

    return HttpResponse(json.dumps({"state": connect_state, "message": connect_message}))


@require_http_methods(["POST"])
@csrf_exempt
def create_server(request):
    json_response = {"state": 1, "message": "Tạo mới thành công" }
    body_json = {}
    try:
        body_json = json.loads(request.body)
    except:
        body_json = None

    if not body_json:
        return HttpResponse(json.dumps({ "state": 0, "message": "Dữ liệu không hợp lệ" }))
    if not body_json.get("name") or not body_json.get("name").strip():
        return HttpResponse(json.dumps({ "state": 0, "message": "Đia chỉ không hợp lệ" }))
    if not body_json.get("port") or not body_json.get("port").strip():
        return HttpResponse(json.dumps({ "state": 0, "message": "Port không hợp lệ" }))
    if not body_json.get("secret") or not body_json.get("secret").strip():
        return HttpResponse(json.dumps({ "state": 0, "message": "Secret Code không hợp lệ" }))

    new_server = Server(    name=body_json.get("name"),
                            port=body_json.get("port"),
                            secret=body_json.get("secret"),
                            note=body_json.get("note") or "",
                        )
    new_server.save()
    json_response["id"] = new_server.id
    return HttpResponse(json.dumps(json_response))


@require_http_methods(["POST"])
@csrf_exempt
def update_server(request):
    body_json = {}
    try:
        body_json = json.loads(request.body)
    except:
        body_json = None

    if not body_json:
        return HttpResponse(json.dumps({ "state": 0, "message": "Dữ liệu không hợp lệ" }))
    id = body_json.get("id")
    name = body_json.get("name")
    port = body_json.get("port")
    secret = body_json.get("secret")
    note = body_json.get("note")

    if not id or not name or not port or not secret or not note:
        return HttpResponse(json.dumps({ "state": 0, "message": "Dữ liệu không hợp lệ." }))

    if not re.match("^[0-9]+$", port):
        return HttpResponse(json.dumps({ "state": 0, "message": "Số Cổng không hợp lệ." }))

    server = Server.objects.get(id=id)
    if not server:
        return HttpResponse(json.dumps({"state": 0, "message": "Không tồn tại bản ghi" }))

    server.name = name
    server.port = port
    server.secret = secret
    server.note = note
    server.save()

    return HttpResponse(json.dumps({"state": 1, "message": "Cập nhật thành công" }))


@require_http_methods(["POST"])
@csrf_exempt
def delete_server(request):
    def delete_one(server_id):
        return Server.objects.filter(id=server_id).delete()
    def delete_multi(server_ids):
        for server_id in server_ids:
            delete_one(server_id)

    body_json = {}
    try:
        body_json = json.loads(request.body)
    except:
        body_json = None
    #
    if not body_json:
        return HttpResponse(json.dumps({ "state": 0, "message": "Dữ liệu không hợp lệ" }))
    id = body_json.get("id")
    ids = body_json.get("ids")

    if not id and not ids:
        return HttpResponse(json.dumps({ "state": 0, "message": "Thông tin không hợp lệ" }))

    if id:
        delete_one(id)
    if ids:
        delete_multi(ids)

    return HttpResponse(json.dumps({"state": 1, "message": "Xóa thành công" }))
