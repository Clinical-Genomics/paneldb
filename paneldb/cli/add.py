# -*- coding: utf-8 -*-
import logging
import click
from pymongo import MongoClient
from paneldb.parser.baitparser import read_file
from paneldb.adapter.mongo import PanelAdapter


LOG = logging.getLogger(__name__)

@click.command()
@click.option('-f', '--file',type=click.Path(exists=True), nargs=1, required=True, help='Path to panel CSV file')
@click.option('-db_uri', type=click.STRING, nargs=1, required=False, help='Mongodb database connection string: mongodb://db_user:db_password@db_host:db_port/db_name', default='mongodb://localhost:27017/paneldb')
@click.option('-email', '--email', type=click.STRING, nargs=1, required=True, help="User's email")
@click.option('-n', '--panel_name', type=click.STRING, nargs=1, required=True, help="Name of new panel")
@click.option('-v', '--version', type=click.FLOAT, nargs=1, required=False, help="Version of new panel", default=1.0)
@click.option('-g', '--genomic_build', type=click.Choice(['GRCh37', 'GRCh38']), nargs=1, required=False, default='GRCh37', help="Genome build")


def add(file, db_uri, email, panel_name, version, genomic_build):

    LOG.info("saving baitset {}.{} to database".format(panel_name, version))
    try:
        # read baitset file
        baits_list = read_file(file)
        #LOG.info(str(baits_list))

        client = MongoClient(db_uri)
        db_name = db_uri.split('/')[-1]
        db = client[db_name]

        adapter = PanelAdapter(client=client, db_name=db_name)

        LOG.info(adapter)

        created_baitset_id = adapter.add_baitset(name=panel_name, version=version, baits=baits_list, build=genomic_build)
        LOG.info("Created baitset with ID {}".format(created_baitset_id))



    except Exception as err:
        LOG.error("An error occurred while saving from baitset file: {}".format(err))
