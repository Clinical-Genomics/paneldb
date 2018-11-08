# -*- coding: utf-8 -*-
import logging
import click

LOG = logging.getLogger(__name__)

@click.command()

def add():
    LOG.info("You just called add method!")
