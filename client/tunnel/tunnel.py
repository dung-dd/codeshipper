import os, random, string
from flask import Flask, json, request
import logging

_logger = logging.getLogger()
FORMAT = '%(asctime) %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.NOTSET)

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.py")


def make_material():
	temp_dir = app.config["TEMP_DIR"]

	if not os.path.isdir(temp_dir):
		try:
			os.makedirs(temp_dir)
		except Exception as e:
			logging.error("Cannot create temp_dir in: " + temp_dir)


def start ():
	make_material()
	app.run(host=app.config["HOST"], port=app.config["PORT"])
