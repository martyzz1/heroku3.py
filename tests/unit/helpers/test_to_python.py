# -*- coding: utf-8; -*-
# General libraries
from __future__ import division, print_function, absolute_import
import itertools
from datetime import datetime

# Third party libraries
import pytest
from heroku3.models import BaseResource
from heroku3.helpers import to_python

_TYPES_MAP = {
    "bools": bool,
    "dates": datetime,
    "dicts": dict,
    "ints": int,
    "strs": str,
}


class SubResource(BaseResource):
    _ints = ["count"]


_CLASS_ATTRS = {
    "arrays": {"array_of_subresources": SubResource},
    "bools": ["bool_value"],
    "dates": ["date_value"],
    "dicts": ["dict_value"],
    "ints": ["int_value"],
    "map": {"subresource": SubResource,},
    "strs": ["str_value"],
}


@pytest.mark.parametrize("str_value", (None, "some string"))
@pytest.mark.parametrize(
    "date_value", (None, "2017-11-01T00:00:00Z", "2017-11-01T00:00:00.0Z", "2017-11-01T00:00:00.0+01:00",)
)
@pytest.mark.parametrize("int_value", (None, "10", "-10"))
@pytest.mark.parametrize("dict_value", (None, {}, {"key": "value"}))
@pytest.mark.parametrize("bool_value", (None, True, False))
def test_to_python(str_value, date_value, int_value, dict_value, bool_value):
    arguments = locals()

    Resource = type("Resource", (BaseResource,), dict([("_{0}".format(k), v) for k, v in _CLASS_ATTRS.items()]))
    data = {}
    for attr in itertools.chain(*_CLASS_ATTRS.values()):
        if attr in arguments and arguments[attr] is not None:
            data.update(
                {attr: arguments[attr],}
            )

    result = to_python(
        Resource(), data, **dict([(k if k != "map" else "objects", v) for k, v in _CLASS_ATTRS.items()])
    )

    for attr_type, attrs in _CLASS_ATTRS.items():
        expected_type = _TYPES_MAP.get(attr_type, None)
        for attr in attrs:
            if expected_type is None:
                expected_type = _CLASS_ATTRS[attr_type][attr]
            if attr in data:
                assert isinstance(getattr(result, attr), expected_type)
            else:
                assert getattr(result, attr) is None


def test_to_python_raises_exception_when_given_date_not_a_str():
    Resource = type("Resource", (BaseResource,), dict([("_{0}".format(k), v) for k, v in _CLASS_ATTRS.items()]))
    data = {
        "date_value": list(),
    }

    with pytest.raises(TypeError):
        to_python(Resource(), data, **dict([(k if k != "map" else "objects", v) for k, v in _CLASS_ATTRS.items()]))


def test_to_python_raises_exception_on_invalid_date():
    Resource = type("Resource", (BaseResource,), dict([("_{0}".format(k), v) for k, v in _CLASS_ATTRS.items()]))
    data = {
        "date_value": "201-1-32 25:00:00.0+1:00",
    }

    with pytest.raises(ValueError):
        to_python(Resource(), data, **dict([(k if k != "map" else "objets", v) for k, v in _CLASS_ATTRS.items()]))


def test_to_python_with_sub_resource():
    Resource = type("Resource", (BaseResource,), dict([("_{0}".format(k), v) for k, v in _CLASS_ATTRS.items()]))
    data = {"subresource": {"count": "42",}}

    result = to_python(
        Resource(), data, **dict([(k if k != "map" else "objects", v) for k, v in _CLASS_ATTRS.items()])
    )

    for attr_type, attrs in _CLASS_ATTRS.items():
        expected_type = _TYPES_MAP.get(attr_type, None)
        for attr in attrs:
            if expected_type is None:
                expected_type = _CLASS_ATTRS[attr_type][attr]
            if attr in data:
                assert isinstance(getattr(result, attr), expected_type)
            else:
                assert getattr(result, attr) is None


def test_to_python_with_array_of_sub_resources():
    Resource = type("Resource", (BaseResource,), dict([("_{0}".format(k), v) for k, v in _CLASS_ATTRS.items()]))
    data = {"array_of_subresources": [{"count": "42",}, {"count": "66",},]}

    result = to_python(
        Resource(), data, **dict([(k if k != "map" else "objects", v) for k, v in _CLASS_ATTRS.items()])
    )

    for attr_type, attrs in _CLASS_ATTRS.items():
        expected_type = _TYPES_MAP.get(attr_type, None)
        for attr in attrs:
            if expected_type is None:
                expected_type = _CLASS_ATTRS[attr_type][attr]
            attr_value = getattr(result, attr)
            if attr in data:
                if isinstance(attr_value, list):
                    assert all(isinstance(value, expected_type) for value in attr_value)
                else:
                    assert isinstance(attr_value, expected_type)
            else:
                assert getattr(result, attr) is None


# vim: et:sw=4:syntax=python:ts=4:
