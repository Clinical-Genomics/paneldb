# -*- coding: utf-8 -*-
import logging
from flask import render_template, flash, request, redirect
from werkzeug.utils import secure_filename
from paneldb import app

LOG = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template("index.html",title="paneldb")

@app.route('/panels')
def gene_panels():
    return render_template("panels.html")

@app.route('/baitsets', methods=['GET', 'POST'])
def baitsets():
    LOG.info("IN BAITSETS")
    document=None
    if request.method == 'POST': #add new baitset
        if 'inputFile' not in request.files:
            flash('No file part')
            return redirect(request.url)

        baits_file = request.files['inputFile']
        if baits_file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        else:
            document=secure_filename(baits_file.filename)

    return render_template("baitsets.html", document=document)
