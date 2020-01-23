# -*- coding: utf-8; -*-
# General libraries
from __future__ import division, print_function, absolute_import
import copy

# Third party libraries
import pytest
import requests
import responses

try:
    from itertools import chain, izip_longest as zip_longest
except ImportError:
    from itertools import chain, zip_longest  # noqa


@responses.activate
def test_update_when_response_ok(
    config_vars, config_dict, extra_config_dict,
):
    final_config = copy.copy(config_dict)
    final_config.update(extra_config_dict)

    responses.add(
        responses.PATCH, config_vars._h._url_for(*config_vars._resource), status=200, json=final_config,
    )

    new_config_vars = config_vars.update(extra_config_dict)

    assert config_vars._ConfigVars__data == final_config
    assert config_vars._ConfigVars__data is not final_config
    assert new_config_vars is None  # To mimic dict.update()


@responses.activate
def test_update_raise_exception_if_response_ko(
    config_vars, extra_config_dict,
):
    responses.add(
        responses.PATCH, config_vars._h._url_for(*config_vars._resource), status=500, json={},
    )

    with pytest.raises(requests.HTTPError):
        config_vars.update(extra_config_dict)


# vim: et:sw=4:syntax=python:ts=4:
