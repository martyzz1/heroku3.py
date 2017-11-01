# -*- coding: utf-8; -*-
from __future__ import absolute_import, division, print_function

from backports import unittest_mock
import pytest
import requests

from heroku3.api import Heroku, HerokuCore


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
