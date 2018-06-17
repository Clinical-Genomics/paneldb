from flask import Flask

app = Flask(__name__, template_folder='server/templates')

import paneldb.server.views
