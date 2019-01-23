# -*- coding: utf-8 -*-
import logging
import click
import pymongo
import enlighten
from pymongo import MongoClient
from flask.cli import with_appcontext, current_app
from paneldb.parser.baitparser import baits
from paneldb.adapter.baitset import add_baitset, add_bait


LOG = logging.getLogger(__name__)

@click.group()
def add():
    """Add items to database using the CLI"""
    pass

@click.command()
@with_appcontext
@click.option('-id', '--id',type=click.STRING, nargs=1, required=True, help='New baitset ID')
@click.option('-f', '--file',type=click.Path(exists=True), nargs=1, required=True, help='Path to panel CSV file')
@click.option('-n', '--panel_name', type=click.STRING, nargs=1, required=False, help="Name of new panel", default='test1')
@click.option('-v', '--version', type=click.FLOAT, nargs=1, required=False, help="Version of new panel", default=1.0)
@click.option('-g', '--genomic_build', type=click.Choice(['GRCh37', 'GRCh38']), nargs=1, required=False, default='GRCh37', help="Genome build")
def baitset(id, file, panel_name, version, genomic_build):
    """Add a baiset to the database"""

    LOG.info("saving baitset {} version {} to database".format(panel_name, version))
    database = current_app.db
    new_baitset_id = add_baitset(database=database, id=id, name=panel_name, version=version, build=genomic_build)

    inserted_baits = 0

    # if baitset creation was successful, insert baits
    if new_baitset_id:

        # obtain all baits from this baitset, formatted as objects
        baits_list = baits(path_to_file=file, created_baitset_id=new_baitset_id)

        # insert one bait at the time into db
        pbar = enlighten.Counter(total=len(baits_list), desc='', unit='baits')
        for bait in baits_list:
            inserted_bait_id = add_bait(database, bait)

            if inserted_bait_id:
                inserted_baits += 1
                updated_baitset = database['baitset'].find_one_and_update( {'_id': new_baitset_id}, {'$push': {'baits':bait['_id']}}, upsert= True )

            pbar.update()

        LOG.info('created baitset with ID {0}. Inserted {1} out of {2} new available baits into db'.format(new_baitset_id, inserted_baits, len(baits_list)))
    else:
        LOG.error("Something went wrong and the baitset coudn't be saved to db.")


add.add_command(baitset)
