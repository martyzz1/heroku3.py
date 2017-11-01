# -*- coding: utf-8; -*-
from __future__ import absolute_import, division, print_function

import pytest

from heroku3.helpers import is_collection


@pytest.mark.parametrize("candidate,expected",
                         [('', False),
                          ({}, True),
                          ([], True),
                          ])
def test_is_collection(candidate, expected):
    actual = is_collection(candidate)
    assert actual is expected


# vim: et:sw=4:syntax=python:ts=4:
