# -*- coding: utf-8 -*-
import logging
import os
from flask import render_template, flash, request, redirect, url_for, current_app, Blueprint
from paneldb.parser.baitparser import baits
from paneldb.adapter.baitset import available_baitsets
from . import controllers

bp = Blueprint('server', __name__)

LOG = logging.getLogger(__name__)

@bp.route('/')
def index():
    return redirect(url_for('server.baitsets'))


@bp.route('/baitsets', methods=['GET', 'POST'])
def baitsets():
    """Handles the baitsets page"""

    document = None
    available_bsets = available_baitsets(current_app.db)
    data = {
        'baitsets' : available_bsets
    }

    if request.method == 'POST': #add new baitset
    # check if the post request has the file part
        if 'inputFile' not in request.files:
            return redirect(request.url)

        baits_file = request.files['inputFile']
        document = baits_file.filename

        # if user does not select a file, browser submit an empty part without filename
        if document == '':
            return redirect(request.url)
        else:
            LOG.info("Save baitset from app interface should be fixed!")
            # this should be fixed to save baitsets and baits from web interface!!!!



            #path_to_temp_file = os.path.join(current_app.config['UPLOAD_FOLDER'], document)

            #save baisets file into temp directory
            #save_file(baits_file, path_to_temp_file)

            #call controllers to save baitset to database
            #new_baitset_id = controllers.save_baitset(adapter, name=request.form.get('baitset_name'), version='1.0', temp_path=path_to_temp_file, build=request.form.get('chr_build'))
            #flash("New baitset id: "+str(new_baitset_id))

            #remove the temp baitset file once everything is saved
            #os.remove(path_to_temp_file)
            #data = controllers.get_baitsets(adapter)

    return render_template("baitsets.html", **data)



def save_file(baits_file, full_file_path):
    """Saves a file to temp directory"""
    baits_file.save(full_file_path)
