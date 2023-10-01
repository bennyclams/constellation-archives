from constellation_archives.db import Model
from werkzeug.security import generate_password_hash, check_password_hash


class User(Model):
    _table = "users"
    _fields = ["id", "username", "password", "email", "roles", "created_at", "updated_at"]
    _uniques = ["id", "username", "email"]
    _json_fields = ["roles"]

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self['id'])

    def has_role(self, role):
        return role in self._data["roles"]

    def add_role(self, role):
        if role not in self._data["roles"]:
            self._data["roles"].append(role)
            self['roles'] = self._data["roles"]

    def remove_role(self, role):
        if role in self._data["roles"]:
            self._data["roles"].remove(role)
            self['roles'] = self._data["roles"]
    
    def set_password(self, password):
        self._data["password"] = generate_password_hash(password)
        self['password'] = self._data["password"]

    def check_password(self, password):
        return check_password_hash(self._data["password"], password)

    def __repr__(self):
        return "<User %s>" % self['username']
    
    def __str__(self):
        return "<User %s>" % self['username']
    
    @classmethod
    def new(cls, **kwargs):
        if "password" in kwargs:
            kwargs["password"] = generate_password_hash(kwargs["password"])
        return super().new(**kwargs)
