# -*- coding: utf-8; -*-
# General libraries
from __future__ import division, print_function, absolute_import

# Third party libraries
import pytest
from heroku3.api import MaxRangeExceeded


@pytest.mark.parametrize("limit", [None, 100])
@pytest.mark.parametrize("order_by", [None, "other"])
@pytest.mark.parametrize("sort", ["asc", "desc"])
@pytest.mark.parametrize("valrange", [None, "some valrange"])
def test__get_headers_for_request_with_legacy(
    heroku_core, limit, order_by, sort, valrange,
):
    expected_header = "Accept"
    expected_value = "application/json"

    headers = heroku_core._get_headers_for_request(legacy=True,)

    assert len(headers) == 1
    assert expected_header in headers
    assert headers[expected_header] == expected_value


@pytest.mark.parametrize("limit", [None, 100])
@pytest.mark.parametrize("order_by", [None, "other"])
@pytest.mark.parametrize("sort", [None, "asc", "desc"])
@pytest.mark.parametrize("valrange", [None, "some valrange"])
def test__get_headers_for_request(
    heroku_core, limit, order_by, sort, valrange,
):
    expected_header = "Range"

    headers = heroku_core._get_headers_for_request(limit=limit, order_by=order_by, sort=sort, valrange=valrange,)
    args = (
        limit,
        order_by,
        sort,
        valrange,
    )
    _all_args_none = all([arg is None for arg in args])
    assert _all_args_none or len(headers) == 1
    assert _all_args_none or expected_header in headers
    if valrange is not None:
        assert headers[expected_header] == valrange
    if valrange is None and sort is not None:
        assert "order={0}".format(sort) in headers[expected_header]
    if valrange is None and limit is not None:
        assert "max={0}".format(limit) in headers[expected_header]
    if valrange is None and order_by is not None:
        assert "{0} ..;".format(order_by) in headers[expected_header]


def test__get_headers_for_request_with_wrong_limit(heroku_core):
    limit = 1500
    with pytest.raises(MaxRangeExceeded):
        heroku_core._get_headers_for_request(limit=limit)


# vim: et:sw=4:syntax=python:ts=4:
