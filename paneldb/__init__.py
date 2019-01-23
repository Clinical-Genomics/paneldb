# -*- coding: utf-8 -*-
import os
import logging
from flask import Flask
from pymongo import MongoClient
from paneldb.server.views import bp

logging.basicConfig(level=logging.INFO)

LOG = logging.getLogger(__name__)

def create_app():
    #configuration files are relative to the instance folder

    #configuration files are relative to the instance folder
    app = Flask(__name__, template_folder='server/templates', instance_relative_config=True)
    app.config.from_pyfile('paneldb_config.cfg')

    client = MongoClient(app.config['MONGODB_URI'])
    app.db = client[app.config['MONGODB_DATABASE_NAME']]

    app.register_blueprint(bp)
    return app


def run_app():
    app = create_app()
    app.run()


if __name__ == '__main__':
    create_app()
