# -*- coding: utf-8; -*-
from __future__ import absolute_import, division, print_function

import pytest
import requests

from heroku3.api import Heroku, HerokuCore
from heroku3.models.configvars import ConfigVars


class __App():
    def __init__(self):
        self.name = "mock-application"
        self.id = "12345678-90ab-cdef-1234-567890abcdef"


@pytest.fixture
def app():
    return __App()


@pytest.fixture
def config_dict():
    # Because the ``unit`` package will only be added to ``sys.path`` during
    # discovery.
    from unit.models.configvars import CONFIG_VAR_KEYS, CONFIG_VAR_VALUES
    return dict(zip(CONFIG_VAR_KEYS, CONFIG_VAR_VALUES))


@pytest.fixture
def config_vars(config_dict, app, heroku_core):
    # Not using new_from_dict() to not spoil coverage
    cfg = ConfigVars(config_dict, app, h=heroku_core)
    cfg.data = config_dict
    cfg.app = app
    return cfg


@pytest.fixture
def extra_config_dict():
    # Because the ``unit`` package will only be added to ``sys.path`` during
    # discovery.
    from unit.models.configvars import (EXTRA_CONFIG_VAR_KEYS,
                                        EXTRA_CONFIG_VAR_VALUES,
                                        )
    return dict(zip(EXTRA_CONFIG_VAR_KEYS, EXTRA_CONFIG_VAR_VALUES))


@pytest.fixture
def heroku_api_key():
    return "some-heroku-api-key"


@pytest.fixture
def heroku_core():
    return HerokuCore()


@pytest.fixture
def heroku_core_w_session():
    return HerokuCore(session=requests.session())


@pytest.fixture
def login_name():
    return "some login name"


@pytest.fixture
def login_secret():
    return "some login secret"


# vim: et:sw=4:syntax=python:ts=4:
