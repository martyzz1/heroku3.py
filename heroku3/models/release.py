# Project libraries
from . import User, BaseResource
from .slug import Slug


class Release(BaseResource):
    _strs = ["description", "id", "user", "commit", "addons", "status"]
    _ints = ["version"]
    _dates = ["created_at", "updated_at"]
    _map = {"slug": Slug, "user": User}
    _pks = ["id", "version"]
    order_by = "version"

    def __init__(self):
        self.app = None
        super(Release, self).__init__()

    def __repr__(self):
        return "<release '{0} {1} {2}'>\n".format(self.version, self.created_at, self.description)
