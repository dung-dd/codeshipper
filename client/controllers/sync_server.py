# coding: utf-8

from flask import request
from sqlalchemy.orm import sessionmaker
import json, jwt, os, zipfile

from tunnel import app
from models import project, server, config
from .mapping_errors import mapping_errors, ERRORS_CODE
from models.base import engine
from .transporter import Transporter 

import random
import string

def random_string(length=15):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


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

	return response_data


@app.route("/pass_material", methods=["POST"])
def get_material():

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
		response_data["data"] = repr(e)

	project_code = json_data.get("project_code")
	project_version = json_data.get("project_version") or ""
	
	if not project_code:
		response_data["code"] = ERRORS_CODE.PROJECT_CODE_NOT_EXIST
		response_data["message"] = mapping_errors(ERRORS_CODE.PROJECT_CODE_NOT_EXIST)
		return response_data

	# (['source_code', 'source_code_path', 'config_path', 'config_service', 'project_code', 'project_version', 'deploy_script', 'rollback'])
	temp_dir = os.path.join(app.config["TEMP_DIR"], project_code, project_version)
	
	rollback = json_data.get("rollback")
	source_code = json_data.get("source_code")
	source_code_path = json_data.get("source_code_path")
	source_code_file_name = json_data.get("source_code_file_name")
	if source_code:
		_transport = Transporter(temp_dir, source_code, source_code_path, rollback=rollback )
		if _transport.error:
			response_data = _transport.response_data
			return response_data

	config_service = json_data.get("config_service")
	config_path = json_data.get("config_path")
	if json_data.get("config_service"):
		dirname_of_config = os.path.dirname(config_path)
		if not os.path.isdir(dirname_of_config):
			try:
				os.makedirs(dirname_of_config)
			except Exception as e:
				pass 

		with open(config_path, "wb") as target_config_path:
			if isinstance(config_service, str):
				config_service = config_service.encode()
			target_config_path.write(config_service)
			target_config_path.close()

	# ========================================================= #
	# 					End of code block						#
	# ========================================================= #
	deploy_script = json_data.get("deploy_script")
	rollback_deploy_script = json_data.get("rollback_deploy_script")
	
	if deploy_script:
		deploy_script_tmp_file = os.path.join ('/tmp', random_string(length=20))
		output_script_tmp_file = os.path.join ('/tmp', random_string(length=20))
		
		target = open(deploy_script_tmp_file, 'w')
		target.write(deploy_script)
		target.close()
		print (deploy_script_tmp_file, os.listdir("/tmp"))
		
		cmd_deploy_script = f"/bin/bash {deploy_script_tmp_file} > {output_script_tmp_file}"
		print ("cmd_deploy_script", cmd_deploy_script)
		script_output = os.system(cmd_deploy_script)
		
		if script_output:
			response_data["code"] = 500
			response_data["message"] = "result run script return value non-zero\n"+deploy_script
			if rollback:
				_transport.rollback_method()
			if _transport.error:
				response_data["message"] += "\nRollback error\n" + _transport.response_data["message"]  
			else:
				os.system(rollback_deploy_script + "")
				response_data["message"] += "\nRollback Ok"
		else:
			response_data["code"] = 0
			response_data["message"] = "Cập nhật thành công"
			with open(output_script_tmp_file, "rb") as target:
				cmd_output = target.read()
				cmd_output.decode("utf-8")
				target.close()
			response_data["output"] = cmd_output

	return response_data




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