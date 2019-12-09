# coding: utf-8
import jwt, pytz, os
import threading, requests, requests
from datetime import datetime, timedelta
from django.conf import settings

from codeshipper_app.models.updating import Updating

class ShipperWorkSpace():
    def __init__(self, updating_id, ):
        self.URL = ""
        self.SECRET = ""
        self.MATERIAL = {}
        self.UPDATING = self.get_updating(updating_id)
        self.SHIPPER = threading.Timer(self, self.UPDATING.timedelta, self.pass_material, )
        self.start()
        

    @staticmethod
    def get_updating(updating_id):
        updating = Updating.objects.filter(id=updating_id).first()
        
        if updating:
            now = datetime.now()
            now = now.astimezone(pytz.timezone(pytz.country_timezones("VN")[0]))
            updating.timedelta = updating.deploy_time - now
        return updating


    def material_not_enough(self, state, message):
        self.UPDATING.state = state
        self.UPDATING.output = message
        self.UPDATING.save()


    def get_material(self):
        material = {}
        material["url"] = "http://{}:{}/pass_material".format( self.UPDATING.server_id.name, self.UPDATING.server_id.port)
        material["secret"] = self.UPDATING.server_id.secret
        project = self.UPDATING.project

        stored_folder = settings.STORED_FOLDER
        project_version_folder = os.path.join(stored_folder, project.code, project.version )
        source_code_file_path = ""
        for file in os.listdir(project_version_folder):
            if file.startswith("source_code_"):
                source_code_file_path = file
                break

        material["source_code_file_path"] = source_code_file_path
        material["config_path"] = self.UPDATING.config_path
        material["config_service"] = self.UPDATING.config_service
        material["deploy_script"] = self.UPDATING.deploy_script

        return material


    def pass_material(self):
        material = self.get_material()
        updating_type = self.UPDATING.updating_type

        if updating_type == "source_code" or updating_type == "all" :
            if not os.isfile(material["source_code_file_path"]):
                return self.material_not_enough("error", "Source code not found: file {} not found in server".format(material["source_code_file_path"]) )

            self.totalize_source_code(material)
        if updating_type == "config" or updating_type == "all":
            self.totalize_config(material)

        self.totalize_script(material)

        self.URL = material["url"]
        self.SECRET = material["secret"]
        self.MATERIAL["rollback"] = material["rollback"]
        self.send_material()


    def totalize_config(self, material):
        self.MATERIAL["config_path"] = material["config_path"]
        self.MATERIAL["config_service"] = material["config_service"]



    def totalize_source_code(self, material):
        with open(material["source_code_file_path"]) as target:
            self.MATERIAL["source_code"] = target.read()
            target.close()
        self.MATERIAL["source_code_path"] = material["source_code_path"]


    def totalize_script(self, material):
        self.MATERIAL["deploy_script"] = material["deploy_script"]


    def send_material(self):
        headers = { "Content-Type": "application/json" }
        data = jwt.encode(self.MATERIAL, )
        requests.post(self.URL, data=data, headers=headers)


    def start(self):
        self.SHIPPER.start()
