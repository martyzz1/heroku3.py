# Project libraries
from . import BaseResource


class Invoice(BaseResource):
    _dates = ["created_at", "updated_at"]
    _ints = ["number", "credits_total", "total", "charges_total"]
    _strs = ["id"]
    _pks = ["id", "number"]

    def __init__(self):
        super(Invoice, self).__init__()

    def __repr__(self):
        return "<invoice '{}-{}'>".format(self.id, self.number)
