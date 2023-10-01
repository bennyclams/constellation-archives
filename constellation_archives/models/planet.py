from constellation_archives.db import Model, connect, close
import json

class Planet(Model):
    _table = "planets"
    _fields = [
        "id", "name", "system", "type", "gravity", "temperature", "atmosphere",
        "magnetosphere", "fauna", "flora", "water", "resources", "traits", "moons",
        "description", "submitter", "created_at", "updated_at"
    ]
    _uniques = ["id", "name"]
    _json_fields = ["resources", "traits"]

    def __repr__(self):
        return "<Planet %s>" % self['name']
    
    def __str__(self):
        return "<Planet %s>" % self['name']