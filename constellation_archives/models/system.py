from constellation_archives.db import Model, connect, close
import json

class System(Model):
    _table = "systems"
    _fields = [
        "id", "name", "catalogue_id", "class", "temperature", "mass",
        "radius", "magnitude", "planet_count", "moon_count",  "level",
        "faction", "description", "banner", "submitter", "created_at",
        "updated_at"
    ]
    _uniques = ["id", "name"]

    def __repr__(self):
        return "<System %s>" % self['name']
    
    def __str__(self):
        return "<System %s>" % self['name']