# Project libraries
from . import Stack, BaseResource


class Slug(BaseResource):
    _strs = ["buildpack_provided_description", "checksum", "commit", "commit_description", "id"]
    _ints = ["size"]
    _dates = ["created_at", "updated_at"]
    _map = {"stack": Stack}
    _pks = ["id"]
    order_by = "created_at"

    def __init__(self):
        super(Slug, self).__init__()

    def __repr__(self):
        return "<slug '{0}'>\n".format(self.id)
