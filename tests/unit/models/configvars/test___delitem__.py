# -*- coding: utf-8; -*-
# General libraries
from __future__ import division, print_function, absolute_import
import copy

# Third party libraries
import pytest
import responses


@responses.activate
def test__delitem__when_key_exists(config_vars, config_dict):
    key = list(config_dict.keys())[0]
    original_config = config_vars._ConfigVars__data
    final_config = copy.copy(config_dict)
    del final_config[key]

    responses.add(
        responses.PATCH, config_vars._h._url_for(*config_vars._resource), status=200, json=final_config,
    )

    del config_vars[key]

    assert config_vars._ConfigVars__data == final_config
    assert config_vars._ConfigVars__data is not final_config
    assert config_vars._ConfigVars__data is not original_config


@responses.activate
def test__delitem__when_key_not_removed(config_vars, config_dict):
    key = list(config_dict.keys())[0]
    original_config = config_vars._ConfigVars__data

    responses.add(
        responses.PATCH, config_vars._h._url_for(*config_vars._resource), status=200, json=config_dict,
    )

    with pytest.raises(AssertionError):
        del config_vars[key]

    assert config_vars._ConfigVars__data == original_config
    assert config_vars._ConfigVars__data is original_config


# vim: et:sw=4:syntax=python:ts=4:
