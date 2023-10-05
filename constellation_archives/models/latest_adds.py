from constellation_archives.db import RedisList

class LatestAdds(RedisList):
    _key = "CACache:latest_adds"
    _max_length = 10
    _json_items = True