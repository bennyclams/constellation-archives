from mysql import connector
from datetime import datetime
import redis
import json
import os

def connect_redis():
    return redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

def connect():
    conn = connector.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        database=os.getenv("MYSQL_DATABASE", "constellation_archives"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "password"),
    )
    conn.autocommit = True
    cursor = conn.cursor(dictionary=True)
    return conn, cursor

def close(conn, cursor):
    cursor.close()
    conn.close()

class Model:
    _table = None
    _fields = None
    _uniques = None
    _json_fields = None
    _dt_fields = None
    _cached = False

    def __init__(self, from_dict=None, **kwargs):
        self._data = {}
        if from_dict is not None:
            for field in self._fields:
                if field in from_dict:
                    if self._json_fields and field in self._json_fields and isinstance(from_dict[field], str):
                        self._data[field] = json.loads(from_dict[field])
                    elif self._json_fields and field in self._json_fields and isinstance(from_dict[field], bytes):
                        self._data[field] = json.loads(from_dict[field].decode("utf-8"))
                    else:
                        self._data[field] = from_dict[field]
        else:
            if self._cached:
                redis_db = connect_redis()
                keyname = "CACache:%s:" % self._table
                for field in kwargs:
                    if field in self._uniques:
                        keyname += str(kwargs[field])
                        if redis_db.exists(keyname):
                            self._data = json.loads(redis_db.get(keyname))
                            if self._dt_fields is not None:
                                for field in self._dt_fields:
                                    if field in self._data:
                                        self._data[field] = datetime.fromisoformat(self._data[field])
                            return

            sql = "SELECT " + ", ".join(self._fields) + " FROM " + self._table + " WHERE "
            _ands = []
            _vals = []
            for field in self._uniques:
                if field in kwargs:
                    _ands.append(field + " = %s")
                    _vals.append(kwargs[field])
            sql += " AND ".join(_ands)
            conn, cursor = connect()
            cursor.execute(sql, tuple(_vals))
            row = cursor.fetchone()
            close(conn, cursor)
            if row is None:
                raise Exception("No such row: WHERE %s" % " AND ".join(_ands))
            if self._json_fields is not None:
                for field in self._json_fields:
                    if field in row:
                        row[field] = json.loads(row[field])
            self._data = row
            self.__write_cache()

    def __getitem__(self, name):
        if name in self._fields:
            return self._data[name]
        raise AttributeError("No such attribute: %s" % name)
    
    def __setitem__(self, name, value):
        if name in self._fields:
            if name not in self._uniques:
                self._data[name] = value
                if self._json_fields is not None:
                    if name in self._json_fields:
                        value = json.dumps(value)
                if self._dt_fields is not None:
                    if name in self._dt_fields:
                        if isinstance(value, datetime):
                            value = value.isoformat()
                conn, cursor = connect()
                if "updated_at" in self._fields:
                    sql = "UPDATE " + self._table + " SET " + name + " = %s, updated_at = NOW() WHERE "
                else:
                    sql = "UPDATE " + self._table + " SET " + name + " = %s WHERE "
                _ands = []
                _vals = [value]
                for field in self._uniques:
                    _ands.append(field + " = %s")
                    _vals.append(self._data[field])
                sql += " AND ".join(_ands)
                cursor.execute(sql, tuple(_vals))
                close(conn, cursor)
                self.__bust_cache()

    def __delitem__(self, name):
        raise Exception("Cannot delete attributes from Model objects")

    def __contains__(self, name):
        return name in self._fields

    def __repr__(self):
        return "<Model %s>" % self._table
    
    def __str__(self):
        return "<Model %s>" % self._table
    
    def __dir__(self):
        return self._fields
    
    def __write_cache(self):
        if self._cached:
            redis_db = connect_redis()
            basename = "CACache:%s:" % self._table
            if len(self._uniques) > 0:
                keynames = []
                for field in self._uniques:
                    keynames.append(self._data[field])
                for keyname in keynames:
                    # This might end up being cumbersome, but it's got the benefit of caching each unique key at once
                    # may need to be changed if site gets too big
                    cache_data = {}
                    for k, v in self._data.items():
                        if isinstance(v, datetime):
                            cache_data[k] = v.isoformat()
                        else:
                            cache_data[k] = v
                    redis_db.set(basename + str(keyname), json.dumps(cache_data))
            # if no uniques, we won't cache it

    def __bust_cache(self):
        if self._cached:
            redis_db = connect_redis()
            basename = "CACache:%s:" % self._table
            if len(self._uniques) > 0:
                keynames = []
                for field in self._uniques:
                    keynames.append(self._data[field])
                for keyname in keynames:
                    redis_db.delete(basename + str(keyname))
            # if no uniques, we won't cache it

    def delete(self):
        sql = "DELETE FROM " + self._table + " WHERE "
        _ands = []
        _vals = []
        for field in self._uniques:
            if field in self._data:
                _ands.append(field + " = %s")
                _vals.append(self._data[field])
            else:
                raise AttributeError("No such attribute: %s" % field)
        sql += " AND ".join(_ands)
        conn, cursor = connect()
        cursor.execute(sql, tuple(_vals))
        close(conn, cursor)
        self.__bust_cache()

    def update(self, **kwargs):
        sql = "UPDATE " + self._table + " SET "
        _ands = []
        _vals = []
        for field in kwargs:
            if field in self._fields:
                _ands.append(field + " = %s")
                if field in self._json_fields:
                    _vals.append(json.dumps(kwargs[field]))
                else:
                    _vals.append(kwargs[field])
            else:
                raise AttributeError("No such attribute: %s" % field)
        sql += ", ".join(_ands)
        sql += " WHERE "
        _ands = []
        for field in self._uniques:
            if field in self._data:
                _ands.append(field + " = %s")
                _vals.append(self._data[field])
            else:
                raise AttributeError("No such attribute: %s" % field)
        sql += " AND ".join(_ands)
        conn, cursor = connect()
        cursor.execute(sql, tuple(_vals))
        close(conn, cursor)
        for field in kwargs:
            if field in self._fields:
                self._data[field] = kwargs[field]
        self.__bust_cache()

    @classmethod
    def count(cls, **kwargs):
        sql = "SELECT COUNT(*) FROM " + cls._table
        if len(kwargs) > 0:
            sql += " WHERE "
        else:
            conn, cursor = connect()
            cursor.execute(sql)
            row = cursor.fetchone()
            close(conn, cursor)
            return list(row.values())[0]
        _ands = []
        _vals = []
        for field in kwargs:
            _ands.append(field + " = %s")
            _vals.append(kwargs[field])
        sql += " AND ".join(_ands)
        conn, cursor = connect()
        cursor.execute(sql, tuple(_vals))
        row = cursor.fetchone()
        close(conn, cursor)
        return list(row.values())[0]

    @classmethod
    def exists(cls, **kwargs):
        sql = "SELECT COUNT(*) FROM " + cls._table + " WHERE "
        _ands = []
        _vals = []
        for field in cls._uniques:
            if field in kwargs:
                _ands.append(field + " = %s")
                _vals.append(kwargs[field])
        sql += " AND ".join(_ands)
        conn, cursor = connect()
        cursor.execute(sql, tuple(_vals))
        row = cursor.fetchone()
        close(conn, cursor)
        return list(row.values())[0] > 0

    @classmethod
    def all(cls):
        conn, cursor = connect()
        cursor.execute("SELECT * FROM " + cls._table)
        rows = cursor.fetchall()
        close(conn, cursor)
        return [cls(from_dict=row) for row in rows]

    @classmethod
    def new(cls, **kwargs):
        sql = "INSERT INTO " + cls._table + " (" + ", ".join(cls._fields) + ") VALUES (" + ", ".join(["%s"] * len(cls._fields)) + ")"
        vals = []
        for field in cls._fields:
            if field in kwargs:
                if isinstance(kwargs[field], list):
                    vals.append(json.dumps(kwargs[field]))
                elif isinstance(kwargs[field], dict):
                    vals.append(json.dumps(kwargs[field]))
                else:
                    vals.append(kwargs[field])
            elif field == "created_at":
                vals.append(datetime.now())
            elif field == "updated_at":
                vals.append(datetime.now())
            else:
                vals.append(None)
        conn, cursor = connect()
        cursor.execute(sql, tuple(vals))
        row_id = cursor.lastrowid
        close(conn, cursor)
        if "id" in cls._fields:
            kwargs["id"] = row_id
        if "created_at" in cls._fields:
            kwargs["created_at"] = datetime.now().isoformat()
        if "updated_at" in cls._fields:
            kwargs["updated_at"] = datetime.now().isoformat()
        return cls(from_dict=kwargs)


class RedisList:
    _key = None
    _max_length = None
    _json_items = False

    def __init__(self):
        self._redis = connect_redis()

    def __len__(self):
        return self._redis.llen(self._key)
    
    def __getitem__(self, index):
        return self._redis.lindex(self._key, index)
    
    def __setitem__(self, index, value):
        self._redis.lset(self._key, index, value)

    def __delitem__(self, index):
        self._redis.lset(self._key, index, "")
    
    def __iter__(self):
        return self._redis.lrange(self._key, 0, -1).__iter__()
    
    def all(self):
        if self._json_items:
            return [json.loads(item) for item in self._redis.lrange(self._key, 0, -1)]
        return self._redis.lrange(self._key, 0, -1)

    def push(self, value):
        if isinstance(value, dict) or isinstance(value, list):
            value = json.dumps(value)
        self._redis.rpush(self._key, value)
        if self._max_length is not None:
            if len(self) > self._max_length:
                self.pop()

    def pop(self):
        return self._redis.lpop(self._key)
