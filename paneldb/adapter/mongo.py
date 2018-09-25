import logging

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
        self.bait_set = self.db.bait_set

    def add_bait(self, bait_obj):
        """Insert a bait object

        Args:
            bait_obj(dict)

        """
        try:
            self.bait.insert_one(bait)
        except Exception as err:
            LOG.warning("Bait {} already exists".format(bait.get('_id')))
            raise err

    def baits(query = None):
        """Return baits

        Args:
            query(dict)

        Returns:
            res(pymongo.Cursor)
        """
        query = query or {}
        res = self.bait.find(query)
        return res
