# -*- coding: utf-8; -*-
# General libraries
from __future__ import division, print_function, absolute_import

# Third party libraries
from heroku3.models.configvars import ConfigVars

try:
    from itertools import chain, izip_longest as zip_longest
except ImportError:
    from itertools import chain, zip_longest  # noqa


def test_new_from_dict(config_dict, app):
    config_vars = ConfigVars.new_from_dict(config_dict, app=app)

    assert config_vars._ConfigVars__data == config_dict
    assert config_vars._ConfigVars__app is app


# vim: et:sw=4:syntax=python:ts=4:
