import logging
from datetime import datetime
from mongo_adapter import MongoAdapter

LOG = logging.getLogger(__name__)

class PanelAdapter(MongoAdapter):
    """Adapter to the paneldb"""

    def setup(self, db_name='paneldb'):
        """Overrides the basic setup method"""
        if self.client is None:
            raise SyntaxError("No client is available")
        if self.db is None:
            self.db = self.client[db_name]
            self.db_name = db_name

        self.bait = self.db.bait
        self.baitset = self.db.baitset


    def add_baitset(self, name, version, build):
        """Insert a baitset object

        Args:
            name(str): Name of the baitset (more than one baitset in db could have the same name)
            version(float): version of the baitset.
            build(str): genome build

        Returns:
            result(str): Inserted document id

        """
        #create new baitset:
        new_baitset = {
            'name' : name,
            'version' : version,
            'chr_build' : build,
            'created_at' : datetime.now()
        }
        result = self.baitset.insert_one(new_baitset)
        new_baitset_id = result.inserted_id

        return new_baitset_id


    def add_bait(self, bait_obj):
        """Insert a bait object

        Args:
            bait_obj(dict)

        Returns:
            result(str): inserted document id

        """
        result = self.bait.insert_one(bait_obj)
        return result.inserted_id


    def baitsets(self):
        """Get all available baitsets in database

        Returns:
            res(pymongo.Cursor)
        """
        result = self.baitset.find()
        return result


    def baitset_baits(self, baitset_id):
        """Return baits

        Args:
            query(dict)

        Returns:
            res(pymongo.Cursor)
        """
        query = query or {}
        res = self.bait.find({'baitset_id': baitset_id})
        return res
