# -*- coding: utf-8; -*-
# General libraries
from __future__ import division, print_function, absolute_import


def test__url_for(heroku_core):
    assert heroku_core._heroku_url is not None
    path = "a", "b", "c"

    url = heroku_core._url_for(*path)
    url_path = url.replace(heroku_core._heroku_url, "")

    assert url.startswith(heroku_core._heroku_url)
    assert url_path == "/{0}".format("/".join(path))


# vim: et:sw=4:syntax=python:ts=4:
