# -*- coding: utf-8; -*-
# General libraries
from __future__ import division, print_function, absolute_import

# Third party libraries
import pytest

# Project libraries
from . import CONFIG_VAR_KEYS

try:
    from itertools import chain, izip_longest as zip_longest
except ImportError:
    from itertools import chain, zip_longest  # noqa


@pytest.mark.parametrize(
    "key, expected", chain(zip_longest(CONFIG_VAR_KEYS, tuple(), fillvalue=True,), [("Inexsitant", False)])
)
def test___contains__(config_vars, key, expected):
    assert (key in config_vars) is expected


# vim: et:sw=4:syntax=python:ts=4:
