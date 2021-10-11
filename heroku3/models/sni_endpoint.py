# Project libraries
from . import BaseResource
from .ssl_cert import SSLCert


class SNIEndpoint(BaseResource):
    """SSL Endpoint."""

    _strs = ["certificate_chain", "cname", "display_name", "id", "name"]
    _dates = ["created_at", "updated_at"]
    _map = {"ssl_cert": SSLCert}
    _pks = ["id"]
    order_by = "id"

    def __init__(self):
        self.app = None
        super(SNIEndpoint, self).__init__()

    def __repr__(self):
        return "<SSL Endpoint '{0}'>".format(self.name)
