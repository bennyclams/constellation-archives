from constellation_archives.db import Model, connect, close
import json


class Item(Model):
    _table = "items"
    _fields = ["id", "name", "item_type", "description", "images", "categories", "submitter", "created_at", "updated_at"]
    _uniques = ["id"]
    _json_fields = ["images", "categories"]
    _dt_fields = ["created_at", "updated_at"]
    _cached = True
    
    def add_image(self, image):
        if image not in self._data["images"]:
            self._data["images"].append(image)
            self['images'] = self._data["images"]

    def remove_image(self, image):
        if image in self._data["images"]:
            self._data["images"].remove(image)
            self['images'] = self._data["images"]

    def add_category(self, category):
        if category not in self._data["categories"]:
            self._data["categories"].append(category)
            self['categories'] = self._data["categories"]

    def remove_category(self, category):
        if category in self._data["categories"]:
            self._data["categories"].remove(category)
            self['categories'] = self._data["categories"]

    @classmethod
    def by_category(cls, category):
        conn, cursor = connect()
        cursor.execute("SELECT * FROM " + cls._table + " WHERE JSON_CONTAINS(categories, %s)", (json.dumps(category),))
        rows = cursor.fetchall()
        close(conn, cursor)
        return [cls(from_dict=row) for row in rows]

    @classmethod
    def by_type(cls, item_type):
        conn, cursor = connect()
        cursor.execute("SELECT * FROM " + cls._table + " WHERE item_type = %s", (item_type,))
        rows = cursor.fetchall()
        close(conn, cursor)
        return [cls(from_dict=row) for row in rows]

    def __repr__(self):
        return "<Item %s>" % self['name']
    
    def __str__(self):
        return "<Item %s>" % self['name']