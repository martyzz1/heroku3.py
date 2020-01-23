# -*- coding: utf-8 -*-

"""
heroku3.helpers
~~~~~~~~~~~~~~

This module contians the helpers.
"""

import sys

# Third party libraries
from dateutil.parser import parse as parse_datetime

if sys.version_info > (3, 0):
    basestring = (str, bytes)


def is_collection(obj):
    """Tests if an object is a collection.

    Returns:
      bool: whether `obj` is considered a collection (returns True) or not
          (returns False)
    """
    col = getattr(obj, "__getitem__", False)
    val = False if (not col) else True

    if isinstance(obj, basestring):
        val = False

    return val


# from kennethreitz/python-github3
def to_python(
    obj, in_dict, strs=None, dates=None, ints=None, objects=None, arrays=None, bools=None, dicts=None, **kwargs
):
    """Extends a given object for API Consumption.

    :param obj: Object to extend.
    :param in_dict: Dict to extract data from.
    :param string_keys: List of in_dict keys that will be extracted as strings.
    :param date_keys: List of in_dict keys that will be extrad as datetimes.
    :param object_map: Dict of {key, obj} map, for nested object results.
    """
    d = dict()

    if strs:
        for in_key in strs:
            d[in_key] = in_dict.get(in_key)

    if dates:
        for in_key in dates:
            in_date = in_dict.get(in_key)
            if in_date is not None:
                try:
                    out_date = parse_datetime(in_date)
                except TypeError as e:
                    raise e

                d[in_key] = out_date
            else:
                d[in_key] = None

    if ints:
        for in_key in ints:
            if (in_dict is not None) and (in_dict.get(in_key) is not None):
                d[in_key] = int(in_dict.get(in_key))

    if bools:
        for in_key in bools:
            if in_dict.get(in_key) is not None:
                d[in_key] = bool(in_dict.get(in_key))

    if dicts:
        for in_key in dicts:
            if in_dict.get(in_key) is not None:
                d[in_key] = dict(in_dict.get(in_key))
    if objects:
        for (k, v) in objects.items():
            if in_dict.get(k):
                d[k] = v.new_from_dict(in_dict.get(k))

    if arrays:
        for (k, v) in arrays.items():
            if in_dict.get(k):
                d[k] = [v.new_from_dict(i) for i in in_dict.get(k)]

    obj.__dict__.update(d)
    obj.__dict__.update(kwargs)

    # Save the dictionary, for write comparisons.
    # obj._cache = d
    # obj.__cache = in_dict

    return obj
