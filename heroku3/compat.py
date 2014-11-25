# -*- coding: utf-8 -*-

"""
heroku3.compat
~~~~~~~~~~~~~

Compatiblity for heroku3.py.
"""

try:
    import json
except ImportError:
    import simplejson as json
