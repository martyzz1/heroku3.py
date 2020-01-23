# -*- coding: utf-8; -*-
# General libraries
from __future__ import division, print_function, absolute_import


def test_to_dict(config_vars, config_dict):
    assert config_vars._ConfigVars__data == config_dict
    assert config_vars._ConfigVars__data is not config_dict

    new_dict = config_vars.to_dict()

    assert config_vars._ConfigVars__data == new_dict
    assert config_vars._ConfigVars__data is not new_dict


# vim: et:sw=4:syntax=python:ts=4:
