import os, random, string
from flask import Flask, json, request
import logging

_logger = logging.getLogger()
FORMAT = '%(asctime) %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.NOTSET)

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.py")

def start ():
	app.run(host=app.config["HOST"], port=app.config["PORT"])
