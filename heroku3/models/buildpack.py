# Project libraries
from . import BaseResource


class Buildpack(BaseResource):

    _strs = ["url"]
    _pks = ["url"]

    def __init__(self):
        super(Buildpack, self).__init__()

    def __repr__(self):
        return "<buildpack {}'>".format(self.url)
