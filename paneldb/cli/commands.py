# -*- coding: utf-8 -*-
import logging
import click

from .add import add

LOG = logging.getLogger(__name__)

@click.group()
def base():
    LOG.info("HELLO THERE!")


base.add_command(add)
