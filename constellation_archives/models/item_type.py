from constellation_archives.db import Model


class ItemType(Model):
    _table = "item_types"
    _fields = ["id", "name", "submitter"]
    _uniques = ["id", "name"]

    def __repr__(self):
        return "<ItemType %s>" % self['name']
    
    def __str__(self):
        return "<ItemType %s>" % self['name']