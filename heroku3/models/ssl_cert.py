# Project libraries
from . import BaseResource


class SSLCert(BaseResource):
    """SSL Certificate."""

    _strs = ["cert_domains", "issuer", "id", "subject"]
    _dates = ["expires_at", "starts_at"]
    _pks = ["id"]
    _bools = ["ca_signed?", "self_signed?"]
    order_by = "created_at"

    def __init__(self):
        self.app = None
        super(SSLCert, self).__init__()

    def __repr__(self):
        return "<SSL Cert '{0}'>".format(self.id)
