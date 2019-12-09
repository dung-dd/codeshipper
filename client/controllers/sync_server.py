# coding: utf-8

from flask import request
from sqlalchemy.orm import sessionmaker
import json, jwt, os

from tunnel import app
from models import project, server, config
from .mapping_errors import mapping_errors, ERRORS_CODE
from models.base import engine

Session = sessionmaker(bind=engine)

@app.route("/test_connection", methods=["POST"])
def handshake():
	response_data = { "code": 0, "message": ""}
	ss = app.config["SUPPER_SECRET"]

	if not ss:
		response_data = mapping_errors(ERRORS_CODE.SUPER_SECRET_NOT_EXIST)
		return response_data
	try:
		json_data = jwt.decode(request.data, ss)
	except jwt.exceptions.InvalidSignatureError:
		response_data = mapping_errors(ERRORS_CODE.SUPER_SECRET_INVALID)
	except Exception as e:
		response_data = mapping_errors(ERRORS_CODE.UNKNOW_ERROR)
		response_data["data"] = e.__repr__()

	if response_data["code"]:
		return response_data

	# session = Session()
	# new_server = server.Server(name="")
	# session.add(new_server)
	# session.commit()

	# close session before return method
	# session.close()
	# return json.dumps({"code": 0, "message": ""})
	return response_data


@app.route("/pass_material", methods=["POST"])
def pass_material():
	response_data = {"code": 0, "message": ""}

	session = Session()
	ss = app.config["SUPPER_SECRET"]
	if not ss:
		response_data = mapping_errors(ERRORS_CODE.SUPER_SECRET_NOT_EXIST)
		return response_data

	try:
		json_data = jwt.decode(request.data, ss)
	except jwt.exceptions.InvalidSignatureError:
		response_data = mapping_errors(ERRORS_CODE.SUPER_SECRET_INVALID)
	except Exception as e:
		response_data["code"] = ERRORS_CODE.UNKNOW_ERROR
		response_data["message"] = mapping_errors(ERRORS_CODE.UNKNOW_ERROR)
		response_data["data"] = e.__repr__()

	project_code = json_data.get("project_code")
	project_version = json_data.get("project_version") or ""
	if not project_code:
		response_data["code"] = ERRORS_CODE.PROJECT_CODE_NOT_EXIST
		response_data["message"] = mapping_errors(ERRORS_CODE.PROJECT_CODE_NOT_EXIST)
		return response_data

	# (['source_code', 'source_code_path', 'config_path', 'config_service', 'project_code', 'project_version', 'deploy_script', 'rollback'])
	source_code = json_data.get("source_code")
	source_code_path = json_data.get("source_code_path")
	source_code_file_name = json_data.get("source_code_file_name")
	if json_data.get("source_code"):
		if not os.path.isdir(source_code_path):
			try:
				os.makedirs(source_code_path)
			except:
				pass

			if not os.path.isdir(source_code_path):
				response_data["code"] = 101
				response_data["message"] = "Không thể tạo thư mục " + source_code_path
				return response_data

		source_code_file = os.path.join(source_code_path, source_code_file_name)
		with open(source_code_file, "wb") as target:
			if isinstance(source_code, str):
				source_code = source_code.encode()
			target.write(source_code)
			target.close()


	config_service = json_data.get("config_service")
	config_path = json_data.get("config_path")
	if json_data.get("config_service"):
		with open(config_path, "wb") as target_config_path:
			if isinstance(config_service, str):
				config_service = config_service.encode()
			target_config_path.write(config_service)
			target_config_path.close()

	# ========================================================= #
	# 					End of code block						#
	# ========================================================= #
	if json_data.get("deploy_script"):
		deploy_script = json_data.get("deploy_script")
		script_out_put = os.system(deploy_script)
		if not script_out_put:
			response_data["code"] = 500
			response_data["message"] = "result run script return value non-zero\n"+deploy_script

	# _p = project.Project.query.filter_by(code=project_code).first()
	# if not _p:
	# 	_p = project.Project(code=project_code,)
	# _p.source_code_path = source_code_path
	# _p.config_file_path = config_path
	#
	# if not response_data["code"]:
	# 	_p.version = project_version
	# session.add(_p)
	# session.commit()
	# if response_data["code"]:
	# 	return response_data

	return response_data
