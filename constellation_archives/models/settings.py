from constellation_archives.db import Model

class IndexSettings(Model):
    _uniques = ["id"]
    _fields = ["id", "main_text", "banner_text", "banner_type", "banner_enabled"]
    _table = "index_settings"
    _cached = True

    def __str__(self):
        return "<Index Settings>"
    
    def __repr__(self):
        return "<Index Settings>"
    
    def enable_banner(self, banner_type, banner_text):
        self['banner_enabled'] = 1
        self['banner_type'] = banner_type
        self['banner_text'] = banner_text

    def disable_banner(self):
        self['banner_enabled'] = 0
        self['banner_type'] = ""
        self['banner_text'] = ""

    @classmethod
    def new(cls, **kwargs):
        raise NotImplementedError("Cannot create new Index Settings.")