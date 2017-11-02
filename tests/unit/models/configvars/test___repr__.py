# -*- coding: utf-8; -*-
from __future__ import absolute_import, division, print_function

from heroku3.models.configvars import ConfigVars

import pytest


@pytest.mark.parametrize("settings", [None, {}, {'VARIABLE': 'value'}, ])
def test___repr__(settings, app):
    config_vars = ConfigVars(settings, app)

    assert repr(config_vars) == repr(config_vars._ConfigVars__data)


# vim: et:sw=4:syntax=python:ts=4:
