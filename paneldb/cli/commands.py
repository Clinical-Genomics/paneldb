# -*- coding: utf-8 -*-
import logging
import click
from flask.cli import FlaskGroup, with_appcontext, current_app
from paneldb import create_app
from .add import add

cli = FlaskGroup(create_app=create_app)
LOG = logging.getLogger(__name__)

@cli.command()
@with_appcontext
def testconnect():
    """Retrieves the names of all collections in db"""
    collections = current_app.db.collection_names()
    click.echo('Testing connection. Collections in database: {}'.format(collections))




cli.add_command(testconnect)
cli.add_command(add)
