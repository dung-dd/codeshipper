# coding: utf-8
import zipfile, os
import base64

class Transporter:
	def __init__(self, temp_dir, source_code, source_code_path, rollback=False ):
		super().__init__()
		self.temp_dir = temp_dir
		self.source_code = base64.b64decode(source_code)
		self.source_code_path = source_code_path

		self.backup_file_path = os.path.join(temp_dir, "before.zip")
		self.rollback = rollback
		self.response_data = {}
		self.error = None 
		self.do()


	def do(self):
		self.make_dirs()
		self.save_temp()
		self.update()
		# if self.rollback:
		# 	self.make_backup()


	def make_dirs(self):
		if not os.path.isdir(self.temp_dir):
			try:
				os.makedirs(self.temp_dir)
			except Exception as e:
				pass
		if not os.path.isdir(self.source_code_path):
			try:
				os.makedirs(self.source_code_path)
			except Exception as e:
				pass


	def save_temp(self):
		self.source_zip_file_temp_path = os.path.join(self.temp_dir, "update.zip")
		with open(self.source_zip_file_temp_path, "wb") as target:
			target.write(self.source_code)
			target.close()

	
	def update(self):
		z = zipfile.ZipFile(self.source_zip_file_temp_path)
		try:
			z.extractall(self.source_code_path)
		except Exception as e:
			self.error = True 
			self.response_data["code"] = 500
			self.response_data["message"] = repr(e)


	def make_backup(self):
		source_code_zipfile = zipfile.ZipFile(self.source_zip_file_temp_path)
		backup_file = zipfile.ZipFile(self.backup_file_path, "w")

		for file in source_code_zipfile.filelist:
			if file.is_dir():
				continue
			file_before = os.path.join(self.source_code_path, file.filename)
			if not os.path.isfile(file_before):
				pass 
			backup_file.write(file_before)
		backup_file.close()


	def rollback_method(self):
		z = zipfile.ZipFile(self.backup_file_path)
		try:
			z.extractall(self.source_code_path)
		except Exception as e:
			self.error = True 
			self.response_data["code"] = 500 
			self.response_data["message"] = repr(e)

	def get_response(self):
		return self.response_data