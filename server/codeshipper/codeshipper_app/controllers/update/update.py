# coding: utf-8

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from django.conf import settings
import json, requests, jwt, base64
import datetime, re, os, pytz, traceback 

from codeshipper_app import secure
from codeshipper_app.models.server import Server
from codeshipper_app.models.project import Project
from codeshipper_app.models.update import Update

# from .shipper import ShipperWorkSpace
from codeshipper_app.work_space import ShipperWorkSpace

# stored_folder = settings.STORED_FOLDER

@require_http_methods(["POST"])
@csrf_exempt
def get_config_project(request):
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

    project_id = body_json.get("project_id")
    project = Project.objects.filter(id=project_id).first()
    # import pudb; pudb.set_trace()
    if not project:
        json_response["state"] = 0
        json_response["message"] = "Dữ liệu không tồn tại"
        return HttpResponse(json.dumps(json_response))

    json_response["data"] = {
        "config_path": project.config_path,
        "config_service": project.config_service,
        "script_deploy": project.script_deploy,
    }

    return HttpResponse(json.dumps(json_response))


@require_http_methods(["POST"])
@csrf_exempt
def create_update(request):
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

    project_id = body_json.get("project_id")
    version = body_json.get("version")
    update_type = body_json.get("update_type")
    source_code_file = body_json.get("source_code_file")
    source_code_file_name = body_json.get("source_code_file_name")
    deploy_type = body_json.get("deploy_type")
    deploy_time = body_json.get("deploy_time")
    source_code_path = body_json.get("source_code_path")
    config_path = body_json.get("config_path")
    config_service = body_json.get("config_service")
    deploy_script = body_json.get("deploy_script")
    deploy_script_for_rollback = body_json.get("deploy_script_for_rollback")

    deploy_time = datetime.datetime.strptime(deploy_time, "%Y-%m-%d %H:%M")
    deploy_time.astimezone(pytz.timezone(pytz.country_timezones("VN")[0]))

    rollback = body_json.get("rollback") or False
    state = "preparing"
    output = ""

    note = body_json.get("note")

    try:
        project_id = int (project_id)
        project = Project.objects.filter(id=project_id).first()
    except Exception as e:
        project = None 
    if not project:
        return HttpResponse(json.dumps({"state": 0, "message": "Dự án không tồn tại"}))
    
    if not version or not update_type or not deploy_type:
        return HttpResponse(json.dumps({"state": 0, "message": "Dữ liệu không hợp lệ"}))

    is_exists_version = Update.objects.filter(project_version=version)
    if is_exists_version:
        return HttpResponse(json.dumps({"state": 0, "message": "Tên phiên bản đã tồn tại"}))

    if source_code_file:
        try:
            source_code_file = base64.b64decode(source_code_file.encode())
        except Exception as e:
            return HttpResponse(json.dumps({"state": 0, "message": "Dữ liệu source code không hợp lệ " + source_code_file_name }))

        if not source_code_file_name:
            return HttpResponse(json.dumps({"state": 0, "message": "Xác định được tên file source code" + source_code_file_name }))

        stored_folder = settings.STORED_FOLDER
        project_version_folder = os.path.join(stored_folder, project.code, version)

        if not os.path.isdir(project_version_folder):
            try:
                os.makedirs(project_version_folder)
            except Exception as e:
                print (e)
                return HttpResponse(json.dumps({"state": 0, "message": "Không thể tạo thư mục file source code nâng cấp " + project_version_folder }))
        
        try:
            file_source_name = os.path.join(project_version_folder, "source_code_" + source_code_file_name)
            with open(file_source_name, "wb") as file_source:
                file_source.write(source_code_file)
                file_source.close()

        except Exception as e:
            print (e)
            import pudb; pudb.set_trace()
            return HttpResponse(json.dumps({"state": 0, "message": "Không thể lưu file source code " + source_code_file_name }))

    server_host = project.server.name + ":" + str(project.server.port)
    new_update = Update(    project=project,
                            project_name=project.name,
                            project_version=version,
                            server=project.server,
                            server_host=server_host,
                            deploy_type=deploy_type, # now or scheduled
                            deploy_time=deploy_time,

                            update_type=update_type, # update config, source code or all
                            source_code_path=source_code_path,
                            config_path=config_path,
                            config_service=config_service,
                            deploy_script=deploy_script,

                            rollback=rollback,
                            deploy_script_for_rollback=deploy_script_for_rollback,
                            state=state,
                            output=output,

                            note=note
                )
                
    if not new_update.id:
        new_update.id = Update.objects.count() + 1
    new_update.save()
    check_again = Update.objects.filter(id=new_update.id)
    if not check_again:
        new_update.save()

    try:
        ShipperWorkSpace(new_update.id)
    except Exception as e:
        print (traceback.print_exc())
        new_update.delete()
        json_response["state"] = 0
        json_response["message"] = "Không tạo được ShipperWorkSpace"

    return HttpResponse(json.dumps(json_response))










#
