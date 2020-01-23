# -*- coding: utf-8; -*-
# General libraries
from __future__ import division, print_function, absolute_import

# Third party libraries
import pytest

# Project libraries
from . import CONFIG_VAR_KEYS


@pytest.mark.parametrize("key", CONFIG_VAR_KEYS + ("INEXISTANT",))
def test___getitem__(key, config_vars, config_dict):
    value = config_vars[key]

    assert value == config_dict.get(key)


# vim: et:sw=4:syntax=python:ts=4:
