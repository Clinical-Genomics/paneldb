# -*- coding: utf-8 -*-
import os
import logging
from flask import Flask
from mongo_adapter import (get_client, check_connection)
from paneldb.adapter.mongo import PanelAdapter

logging.basicConfig(level=logging.INFO)

LOG = logging.getLogger(__name__)

#configuration files are relative to the instance folder
app = Flask(__name__, template_folder='server/templates', instance_relative_config=True)
app.config.from_pyfile('paneldb_config.cfg')


client = get_client(mongodb=app.config['MONGODB_DATABASE_NAME'], timeout=20)
app.adapter = PanelAdapter(client=client, db_name=app.config['MONGODB_DATABASE_NAME'])

import paneldb.server.views
