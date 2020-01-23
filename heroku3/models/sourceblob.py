# Project libraries
from . import BaseResource


class SourceBlob(BaseResource):
    _strs = ["checksum", "url", "version"]

    def __init__(self):
        super(SourceBlob, self).__init__()

    def __repr__(self):
        return "<sourceblob '{}'>".format(self.version)
