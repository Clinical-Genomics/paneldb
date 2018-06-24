# -*- coding: utf-8 -*-
from flask import render_template
from paneldb import app

@app.route('/')
def index():
    return render_template("index.html",title="paneldb")

@app.route('/panels')
def gene_panels():
    return render_template("panels.html")
