# -*- coding: utf-8 -*-
import logging
import pymongo
LOG = logging.getLogger(__name__)
from paneldb.parser.baitparser import read_file

def save_baitset(adapter, name, version, temp_path, build='GRCh37'):
    """Calls adapter functions to insert a baitset and its baits into database

    Args:
        name(str): name of the baitset to be saved
        version(str): baitset version
        temp_path(str): path to temporary baitset_file

    Returns:
        result(dict): baitset object inserted into database

    """
    LOG.info("saving baitset {}.{} to database".format(name, version))
    #read from baitset file and collect baits
    baits_list = read_file(temp_path)
    if baits_list:
        return adapter.add_baitset(name=name, version=version, baits=baits_list, build=build)
    else:
        return None


def get_baitsets(adapter):
    """Gets all available baitsets from database"""

    LOG.info('Getting available baitsets')
    baitsets = list(adapter.baitsets()) # convert pymongo.Cursor to object list

    data = {
        'baitsets' : baitsets,
    }

    return data
