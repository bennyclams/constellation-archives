from constellation_archives.db import Model


class Category(Model):
    _table = "categories"
    _fields = ["id", "name", "description", "thumbnail", "submitter"]
    _uniques = ["id", "name"]
    _cached = True

    def __repr__(self):
        return "<Category %s>" % self['name']
    
    def __str__(self):
        return "<Category %s>" % self['name']
