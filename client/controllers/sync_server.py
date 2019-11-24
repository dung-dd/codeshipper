# coding: utf-8

from flask import request
from sqlalchemy.orm import sessionmaker
import json, jwt

from tunnel import app
from models import project, server, config
from .mapping_errors import mapping_errors, ERRORS_CODE


Session = sessionmaker(bind=engine)

@app.route("/handshake", methods=["POST"])
def handshake():
	response_data = {"code": 0, "message": ""}
	print (request.date, request.data)

	session = Session()
	ss = session.query(config.Config).filter(config.Config.key=="super_secret").first()
	if not ss:
		response_data = mapping_errors(ERRORS_CODE.SUPER_SECRET_NOT_EXIST)
		return response_data

	try:
		json_data = jwt.decode(request.data, ss.value)
	except jwt.exceptions.InvalidSignatureError:
		response_data = mapping_errors(ERRORS_CODE.SUPER_SECRET_INVALID)
	except Exception as e:
		response_data = mapping_errors(ERRORS_CODE.UNKNOW_ERROR)
		response_data["data"] = e.__repr__()

	if response_data["code"]:
		return response_data

	new_server = server.Server(name="")
	session.add(new_server)
	session.commit()

	# close session before return method
	session.close()
	# return json.dumps({"code": 0, "message": ""})
	return response_data
