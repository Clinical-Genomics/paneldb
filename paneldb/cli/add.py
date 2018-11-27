# -*- coding: utf-8 -*-
import logging
import click
import pymongo
from pymongo import MongoClient
from paneldb.parser.baitparser import baits
from paneldb.adapter.mongo import PanelAdapter


LOG = logging.getLogger(__name__)

@click.command()
@click.option('-f', '--file',type=click.Path(exists=True), nargs=1, required=True, help='Path to panel CSV file')
@click.option('-db_uri', type=click.STRING, nargs=1, required=False, help='Mongodb database connection string: mongodb://db_user:db_password@db_host:db_port/db_name', default='mongodb://localhost:27017/paneldb')
@click.option('-email', '--email', type=click.STRING, nargs=1, required=True, help="User's email")
@click.option('-n', '--panel_name', type=click.STRING, nargs=1, required=True, help="Name of new panel")
@click.option('-v', '--version', type=click.FLOAT, nargs=1, required=False, help="Version of new panel", default=1.0)
@click.option('-g', '--genomic_build', type=click.Choice(['GRCh37', 'GRCh38']), nargs=1, required=False, default='GRCh37', help="Genome build")

def add_baitset( file, db_uri, email, panel_name, version, genomic_build):

    LOG.info("saving baitset {}.{} to database".format(panel_name, version))
    try:

        client = MongoClient(db_uri)
        db_name = db_uri.split('/')[-1]
        db = client[db_name]
        adapter = PanelAdapter(client=client, db_name=db_name)

        created_baitset_id = adapter.add_baitset(name=panel_name, version=version, build=genomic_build)

        # obtain all baits from this baitset
        baits_list = baits(path_to_file=file, created_baitset_id=created_baitset_id)

        for bait in baits_list:
            try:
                # add the bait
                inserted_bait_id = adapter.add_bait(bait)
                LOG.info(type(inserted_bait_id))

            except pymongo.errors.DuplicateKeyError:
                LOG.info('pymongo DuplicateKeyError')

            except Exception as err: #other type of error
                LOG.info(type(err))

            finally:
                if created_baitset_id:
                    updated_baitset = db.baitset.find_one_and_update( {'_id': created_baitset_id}, {'$push': {'baits':inserted_bait_id}}, upsert= True )

        #LOG.info(baits_list)

    except Exception as err:
        LOG.error("An error occurred while saving from baitset file: {}".format(err))
