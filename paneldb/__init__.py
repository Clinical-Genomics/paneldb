# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask_pymongo import PyMongo

#configuration files are relative to the instance folder
app = Flask(__name__, template_folder='server/templates', instance_relative_config=True)
app.config.from_pyfile('paneldb_config.cfg')

import paneldb.server.views
