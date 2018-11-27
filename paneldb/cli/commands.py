# -*- coding: utf-8 -*-
import logging
import click

from .add import add_baitset

LOG = logging.getLogger(__name__)

@click.group()
def base():
    LOG.info('inovoked the CLI')

base.add_command(add_baitset)
