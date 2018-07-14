import requests

from . import BaseResource, User
from .buildpack import Buildpack
from .slug import Slug
from .sourceblob import SourceBlob


class Build(BaseResource):
    _dates = ['created_at','updated_at']
    _strs  = ['id', 'status', 'output_stream_url', 'stack']
    _pks   = ['id']
    _map   = {'slug': Slug, 'source_blob': SourceBlob, 'user' : User }
    _arrays = { 'buildpacks' : Buildpack }

    def __init__(self):
        super(Build, self).__init__()
 
    def __repr__(self):
        return "<build '{0} - {1}'>".format(self.id, self.status)

    def stream_output(self, timeout=None):
        resp = requests.get(self.output_stream_url, verify=False, stream=True, timeout=timeout)
        resp.raise_for_status()
        return resp.iter_lines()
