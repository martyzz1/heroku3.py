# -*- coding: utf-8 -*-

"""
heroku3.models
~~~~~~~~~~~~~

This module contains the models that comprise the Heroku API.
"""

import sys
from pprint import pprint  # noqa

# Project libraries
from ..helpers import to_python

if sys.version_info > (3, 0):
    from urllib.parse import quote
else:
    from urllib import quote  # noqa


class BaseResource(object):

    _arrays = {}
    _bools = []
    _dicts = []
    _dates = []
    _ints = []
    _map = {}
    _pks = []
    _strs = []
    order_by = "id"

    def __init__(self):
        self._bootstrap()
        self._h = None
        super(BaseResource, self).__init__()

    def __repr__(self):
        return "<resource '{0}'>".format(self._id)

    def _bootstrap(self):
        """Bootstraps the model object based on configured values."""
        for attr in self._keys():
            setattr(self, attr, None)

    @classmethod
    def _keys(cls):
        """The list of user declared attributes for this model.

        Returns:
            List[str]: the names of the user declared attributes.
        """
        # self._pks is (should be, don't see where this is enforeced) a subset
        # of the set below, hence there is no need to include it.
        return (
            list(cls._arrays.keys())
            + cls._bools
            + cls._dates
            + cls._dicts
            + cls._ints
            + list(cls._map.keys())
            + cls._strs
        )

    @property
    def _id(self):
        try:
            return getattr(self, self._pks[0])
        except IndexError:
            return None

    @property
    def _ids(self):
        """The list of primary keys to validate against."""
        for pk in self._pks:
            yield getattr(self, pk)

        for pk in self._pks:

            try:
                yield str(getattr(self, pk))
            except ValueError:
                pass

    def dict(self):
        d = dict()
        for k in self._keys():
            d[k] = self.__dict__.get(k)

        return d

    def change_connection(self, h):
        self._h = h
        return self

    @classmethod
    def new_from_dict(cls, d, h=None, **kwargs):

        d = to_python(
            obj=cls(),
            in_dict=d,
            strs=cls._strs,
            ints=cls._ints,
            dates=cls._dates,
            bools=cls._bools,
            dicts=cls._dicts,
            objects=cls._map,
            arrays=cls._arrays,
            _h=h,
        )

        d.__dict__.update(kwargs)

        return d


class Price(BaseResource):
    """Heroku Price."""

    _strs = ["cents", "unit"]
    _pks = ["cents"]

    def __init__(self):
        self.app = None
        super(Price, self).__init__()

    def __repr__(self):
        return "<price '{0} per {1}'>".format(self.cents, self.unit)


class Plan(BaseResource):
    """Heroku Addon."""

    _strs = ["id", "name", "description", "state"]
    _pks = ["name", "id"]
    _map = {"price": Price}
    _dates = ["created_at", "updated_at"]

    def __repr__(self):
        return "<Plan '{0}'>".format(self.name)


class Stack(BaseResource):
    """Heroku Stack."""

    _strs = ["id", "name"]
    _pks = ["id", "name"]

    def __init__(self):
        self.app = None
        super(Stack, self).__init__()

    def __repr__(self):
        return "<stack '{0}'>".format(self.name)


class User(BaseResource):
    """Heroku User."""

    _strs = ["id", "email"]
    _pks = ["id", "email"]

    def __init__(self):
        self.app = None
        super(User, self).__init__()

    def __repr__(self):
        return "<user '{0}'>".format(self.email)


class Organization(BaseResource):
    """Heroku Organization."""

    _strs = ["id", "name"]
    _pks = ["id", "name"]

    def __init__(self):
        self.app = None
        super(Organization, self).__init__()

    def __repr__(self):
        return "<organization '{0}'>".format(self.name)


# class Plan(BaseResource):
# """Heroku Addon."""
#
# _strs = ['id', 'name']
# _pks = ['id', 'name']
#
# def __init__(self):
# self.app = None
# super(Plan, self).__init__()

# def __repr__(self):
# return "<plan '{0} {1}'>".format(self.id, self.name)
#


class RateLimit(BaseResource):
    _strs = ["remaining"]
    _bools = []
    _pks = ["remaining"]

    def __init__(self):
        self.app = None
        super(RateLimit, self).__init__()

    def __repr__(self):
        return "<RateLimit '{0}'>".format(self.remaining)
