# coding: utf-8
import jwt, pytz, os, traceback, re, base64
import threading, requests, requests, json
from datetime import datetime, timedelta
from django.conf import settings

from codeshipper_app.models.update import Update
from .send_mail import SendEmail 

class ShipperWorkSpace():
	def __init__(self, update_id, ):
		self.URL = ""
		self.SECRET = ""
		self.MATERIAL = {}
		self.REASON = ""
		self.ELIGIBLE = False 

		self.UPDATE = self.get_update(update_id)
		print ("Before Update", self.UPDATE, self.UPDATE.timedelta)
		self.SHIPPER = threading.Timer( self.UPDATE.timedelta, self.pass_material, )
		# self.SHIPPER = threading.Timer( 3, self.pass_material, ) 
		self.start()
		
	@staticmethod
	def get_update(update_id):
		if isinstance(update_id, Update):
			update = update_id
		else:
			update = Update.objects.filter(id=update_id).first()
		
		if update:
			now = datetime.now()
			now = now.astimezone(pytz.timezone(pytz.country_timezones("VN")[0]))
			update.timedelta = (update.deploy_time - now).total_seconds()
			
		return update


	def material_not_enough(self, state, message):
		self.UPDATE.state = state
		self.UPDATE.output = message
		self.UPDATE.save()


	# totalize everythings, but not run, somethings will be redundant 
	def get_material(self):
		material = {}
		material["url"] = "http://{}:{}/pass_material".format( self.UPDATE.server.name, self.UPDATE.server.port)
		self.SECRET = self.UPDATE.server.secret
		project = self.UPDATE.project
		
		stored_folder = settings.STORED_FOLDER
		project_version_folder = os.path.join(stored_folder, project.code, self.UPDATE.project_version )
		source_code_file_path = ""
		source_code_file_name = ""
		if os.path.isdir(project_version_folder):
			for file in os.listdir(project_version_folder):
				if file.startswith("source_code_"):
					source_code_file_name = file
					source_code_file_path = os.path.join(project_version_folder, file)
					break
		
		material["rollback"] = self.UPDATE.rollback
		material["source_code_path"] = self.UPDATE.source_code_path
		material["source_code_file_name"] = source_code_file_name
		material["source_code_file_path"] = source_code_file_path
		material["config_path"] = self.UPDATE.config_path
		material["config_service"] = self.UPDATE.config_service
		material["deploy_script"] = self.UPDATE.deploy_script
		return material


	def pass_material(self):
		material = self.get_material()
		update_type = self.UPDATE.update_type

		if update_type == "source_code" or update_type == "all" :
			if not os.path.isfile(material["source_code_file_path"]):
				message = "Source code not found: file " + material["source_code_file_path"] + " not found in server"
				return self.material_not_enough("error", message )

			self.totalize_source_code(material)
		if update_type == "config" or update_type == "all":
			self.totalize_config(material)

		self.totalize_script_and_other(material)

		self.URL = material["url"]
		self.MATERIAL["rollback"] = material["rollback"]
		self.send_material()


	def totalize_config(self, material):
		self.MATERIAL["config_path"] = material["config_path"]
		self.MATERIAL["config_service"] = material["config_service"]


	def totalize_source_code(self, material):
		with open(material["source_code_file_path"], "rb") as target:
			self.MATERIAL["source_code"] = base64.b64encode(target.read()).decode("utf-8")
			target.close()
		self.MATERIAL["source_code_path"] = material["source_code_path"]


	def totalize_script_and_other(self, material):
		self.MATERIAL["project_code"] = self.UPDATE.project.code
		self.MATERIAL["project_version"] = self.UPDATE.project_version
		self.MATERIAL["deploy_script"] = material["deploy_script"]
		self.MATERIAL["source_code_file_name"] = re.sub("^source_code_", "",material["source_code_file_name"])
		

	def send_material(self): 
		headers = { "Content-Type": "application/json" }
		data = jwt.encode(self.MATERIAL, self.SECRET)
		r = None, 
		output = "Cập nhật thành công"

		self.UPDATE.state = "tranfering"
		self.UPDATE.save()

		try:
			r = requests.post(self.URL, data=data, headers=headers)
		except Exception as e:
			output = traceback.format_exc()
		
		if not r:
			self.UPDATE.output = output
			self.UPDATE.state = "error"
			self.UPDATE.save()

		try:
			# if r.headers.get("Content-Type") == "application/json":
			res = json.loads(r.text)
		except Exception as e: 
			output = traceback.format_exc() + "\n" + str(r.text)
			res = {}

		# if not res:
		#     self.UPDATE.output = repr(res)
		#     self.UPDATE.state = "error"
		#     self.UPDATE.save()
		#     return 

		if not res.get("code"):
			self.UPDATE.state = "done"
			self.UPDATE.save()
		else:
			self.UPDATE.output = res.get("message") + res.get("data") if res.get("data") else ""
			self.UPDATE.state = "error"
			self.UPDATE.save()

		SendEmail(self.UPDATE.project.name, self.UPDATE.project_version, output)



	def start(self):
		self.SHIPPER.start()
