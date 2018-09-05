# -*- coding: utf-8 -*-
import logging
import os
from flask import render_template, flash, request, redirect
from werkzeug.utils import secure_filename
from paneldb import app
from paneldb.parser.baitparser import read_file

LOG = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template("index.html",title="paneldb")

@app.route('/panels')
def gene_panels():
    return render_template("panels.html")

@app.route('/baitsets', methods=['GET', 'POST'])
def baitsets():
    """Handles the submission of baitsets"""

    document = None
    data = {}
    if request.method == 'POST': #add new baitset
        # check if the post request has the file part
        if 'inputFile' not in request.files:
            return redirect(request.url)

        baits_file = request.files['inputFile']

        # if user does not select a file, browser submit an empty part without filename
        if baits_file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        else:
            # Parse the file to check that it's OK
            # Extract fields to be passes to the DB
            # Pass stuff to DB and get all updated baitsets in it.

            document = secure_filename(baits_file.filename)


                    # savefile(baits_file) How to use this function correctly?
                    # Make the data dictionary work
                   # baits_file.save(os.path.join(app.config['UPLOAD_FOLDER'], document))
            savefile(baits_file ,document)

            #get content from file:
            test = read_file(os.path.join(app.config['UPLOAD_FOLDER'], document))



            data = {
                'document': document,
                'upload_folder': app.config['UPLOAD_FOLDER'],
                'bah' : test
            }


    return render_template("baitsets.html", **data)



def allowed_file(file, filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def savefile(baits_file, filename):
    baits_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#    """Saves a file in a temporary folder"""


