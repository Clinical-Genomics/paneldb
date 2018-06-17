from flask import render_template
from paneldb import app

@app.route('/')
def index():
    return render_template("index.html",title="paneldb")
