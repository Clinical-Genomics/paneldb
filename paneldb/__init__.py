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

client = get_client(mongodb='reddit', timeout=20)
check_connection(client)
app.adapter = PanelAdapter(client=client, db_name='reddit')

import paneldb.server.views
