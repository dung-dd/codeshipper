# coding: utf-8
import jwt, pytz, os, traceback, re
import threading, requests, requests, json
from datetime import datetime, timedelta
from django.conf import settings

from codeshipper_app.models.updating import Updating

class ShipperWorkSpace():
    def __init__(self, updating_id, ):
        self.URL = ""
        self.SECRET = ""
        self.MATERIAL = {}
        self.REASON = ""
        self.ELIGIBLE = False 

        self.UPDATING = self.get_updating(updating_id)
        # self.SHIPPER = threading.Timer( self.UPDATING.timedelta, self.pass_material, )
        self.SHIPPER = threading.Timer( 3, self.pass_material, ) 
        self.start()
        
    @staticmethod
    def get_updating(updating_id):
        if isinstance(updating_id, Updating):
            updating = updating_id
        else:
            updating = Updating.objects.filter(id=updating_id).first()
        
        if updating:
            now = datetime.now()
            now = now.astimezone(pytz.timezone(pytz.country_timezones("VN")[0]))
            updating.timedelta = (updating.deploy_time - now).seconds
        return updating


    def material_not_enough(self, state, message):
        self.UPDATING.state = state
        self.UPDATING.output = message
        self.UPDATING.save()


    # totalize everythings, but not run, somethings will be redundant 
    def get_material(self):
        material = {}
        material["url"] = "http://{}:{}/pass_material".format( self.UPDATING.server.name, self.UPDATING.server.port)
        self.SECRET = self.UPDATING.server.secret
        project = self.UPDATING.project
        
        stored_folder = settings.STORED_FOLDER
        project_version_folder = os.path.join(stored_folder, project.code, self.UPDATING.project_version )
        source_code_file_path = ""
        source_code_file_name = ""
        if os.path.isdir(project_version_folder):
            for file in os.listdir(project_version_folder):
                if file.startswith("source_code_"):
                    source_code_file_name = file
                    source_code_file_path = os.path.join(project_version_folder, file)
                    break
        
        material["rollback"] = self.UPDATING.rollback
        material["source_code_path"] = self.UPDATING.source_code_path
        material["source_code_file_name"] = source_code_file_name
        material["source_code_file_path"] = source_code_file_path
        material["config_path"] = self.UPDATING.config_path
        material["config_service"] = self.UPDATING.config_service
        material["deploy_script"] = self.UPDATING.deploy_script
        return material


    def pass_material(self):
        material = self.get_material()
        updating_type = self.UPDATING.updating_type

        if updating_type == "source_code" or updating_type == "all" :
            if not os.path.isfile(material["source_code_file_path"]):
                message = "Source code not found: file " + material["source_code_file_path"] + " not found in server"
                return self.material_not_enough("error", message )

            self.totalize_source_code(material)
        if updating_type == "config" or updating_type == "all":
            self.totalize_config(material)

        self.totalize_script_and_other(material)

        self.URL = material["url"]
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


    def totalize_script_and_other(self, material):
        self.MATERIAL["project_code"] = self.UPDATING.project.code
        self.MATERIAL["project_version"] = self.UPDATING.project_version
        self.MATERIAL["deploy_script"] = material["deploy_script"]
        self.MATERIAL["source_code_file_name"] = re.sub("^source_code_", "",material["source_code_file_name"])
        

    def send_material(self): 
        headers = { "Content-Type": "application/json" }
        data = jwt.encode(self.MATERIAL, self.SECRET)
        r = None, 
        output = ""
        print ("self.MATERIAL", self.MATERIAL.keys())
        self.UPDATING.state = "tranfering"
        self.UPDATING.save()

        try:
            r = requests.post(self.URL, data=data, headers=headers)
        except Exception as e:
            output = traceback.format_exc()
        
        if not r:
            self.UPDATING.output = output
            self.UPDATING.state = "error"
            self.UPDATING.save()

        try:
            if r.headers.get("Content-Type") == "application/json":
                res = json.loads(r.text)
            else:
                raise
        except: 
            res = {} 

        if not res:
            self.UPDATING.output = repr(res)
            self.UPDATING.state = "error"
            self.UPDATING.save()
            return 

        if not res.get("code"):
            self.UPDATING.state = "done"
            self.UPDATING.save()
        else:
            self.UPDATING.output = res.get("message") + res.get("data") if res.get("data") else ""
            self.UPDATING.state = "error"
            self.UPDATING.save()



    def start(self):
        self.SHIPPER.start()
