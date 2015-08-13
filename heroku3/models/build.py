from . import BaseResource
from . import User
from .buildpack import Buildpack

class Build(BaseResource):
    _dates = ['created_at','updated_at']
    _strs  = ['id','status']
    _pks   = ['id']
    _map   = {'user' : User }
    _arrays = { 'buildpacks' : Buildpack }

    def __init__(self):
        super(Build, self).__init__()
 
    def __repr__(self):
        return "<build '{0} - {1}'>".format(self.id, self.status)

