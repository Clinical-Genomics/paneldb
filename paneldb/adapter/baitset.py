import logging
import pymongo
from datetime import datetime

LOG = logging.getLogger(__name__)

def add_baitset(database, id, name, version, build):
    """Insert a baitset object

    Args:
        database(pymongo.database.Database)
        id(str); An id for the baitset
        name(str): Name of the baitset (more than one baitset in db could have the same name)
        version(float): version of the baitset.
        build(str): genome build

    Returns:
        result(str): Inserted document id
    """
    LOG.info('Creating a new baitset ')
    #create new baitset:
    new_baitset = {
        '_id' : id,
        'name' : name,
        'version' : version,
        'chr_build' : build,
        'created_at' : datetime.now()
    }
    new_baitset_id = None
    try:
        result = database['baitset'].insert_one(new_baitset)
        new_baitset_id = result.inserted_id
    except Exception as err:
        LOG.error('An error occurred while creating a new baitset:{}'.format(err))

    return new_baitset_id


def add_bait(database, bait_obj):
    """Insert a bait object

    Args:
        database(pymongo.database.Database)
        bait_obj(dict)

    Returns:
        inserted_id(strr): inserted document id

    """
    inserted_id = None
    try:
        result = database['bait'].insert_one(bait_obj)
        inserted_id = result.inserted_id

    except pymongo.errors.DuplicateKeyError:
        baitset_id = bait_obj['baitset'][0]
        updated_baitset = database['bait'].find_one_and_update( {'_id': bait_obj['_id']}, {'$push': {'baitset':baitset_id}}, upsert= True )
        inserted_id =  baitset_id

    return inserted_id


def available_baitsets(database):
    """Get all available baitsets in database

    Args:
        database(pymongo.database.Database)

    Returns:
        res(pymongo.Cursor)
    """
    result = database['baitset'].find()
    return result


def baitset_baits(database, baitset_id):
    """Return baits

    Args:
        database(pymongo.database.Database)
        query(dict)

    Returns:
        res(pymongo.Cursor)
    """
    query = query or {}
    res = database['bait'].find({'baitset': baitset_id})
    return res
