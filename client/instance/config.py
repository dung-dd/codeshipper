# config of flask
import random, string, os

db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database", "database.sqlite"))
SQLALCHEMY_TRACK_MODIFICATIONS=True

HOST = '0.0.0.0'
PORT = 5556

SUPPER_SECRET = "erudite"
# SECRET_KEY = "".join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for i in range(32))
SQLALCHEMY_DATABASE_URI = "sqlite:///"+db_file
MY_FIELD  = "myconfig"

DEBUG = False
