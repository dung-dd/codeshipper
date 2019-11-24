#!/usr/bin/python3
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from check_port import port_open
from tunnel import tunnel
from tunnel.tunnel import app as app_server
from models.base import Base, engine
import controllers
with app_server.app_context():
	from models import *

def migrate_db():
	# global manager
	db = SQLAlchemy(app_server)

	migrate = Migrate(app_server, db)
	manager = Manager(app_server)
	manager.add_command("db", MigrateCommand)
	manager.run()

def main():
	# pass
	Base.metadata.create_all(engine)

	if len(sys.argv) == 1:
		port_open.run()
		tunnel.start()

	if len(sys.argv) > 1:
		if sys.argv[1] == "db":
			migrate_db()


if __name__ == "__main__":
	main()
