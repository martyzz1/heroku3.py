#! /usr/bin/env python
########################################################################
#
#  Script to simple stream the progress of a app thats been created.
#  Useful if the create_heroku_app.py is terminated early
#
########################################################################

import os
import sys
from pprint import pprint

# Third party libraries
import heroku3
from urllib3.exceptions import ReadTimeoutError
from requests.exceptions import Timeout, ConnectionError

HEROKU_API_KEY = os.environ["HEROKU_API_KEY"]


def stream_build_logs(appsetup_id):
    appsetup = heroku_conn.get_appsetup(appsetup_id)
    build_iterator = appsetup.build.stream(timeout=2)
    try:
        for line in build_iterator:
            if line:
                print("{0}".format(line.decode("utf-8")))
    except Timeout:
        print("\n\n\nTimeout occurred\n\n\n")
        appsetup = heroku_conn.get_appsetup(appsetup_id)
        if appsetup.build.status == "pending":
            return stream_build_logs(appsetup_id)
        else:
            return
    except ReadTimeoutError:
        print("\n\n\nReadTimeoutError occurred\n\n\n")
        appsetup = heroku_conn.get_appsetup(appsetup_id)
        if appsetup.build.status == "pending":
            return stream_build_logs(appsetup_id)
        else:
            return


def stream_app_logs(appsetup_id, app_id):
    app = heroku_conn.app(app_id)
    iterator = app.stream_log(timeout=2)
    try:
        for line in iterator:
            if line:
                print("{0}".format(line.decode("utf-8")))
    except ConnectionError:
        print("\n\n\nConnectionError occurred\n\n\n")
        appsetup = heroku_conn.get_appsetup(appsetup_id)
        if appsetup.status == "pending":
            return stream_app_logs(appsetup_id, app_id)
        else:
            return


if __name__ == "__main__":

    if len(sys.argv) > 1:
        app_id = sys.argv[1]  # example-app
    else:
        print(
            "Please specify the app name and the type of heroku app to create e.g.\n",
            "./get_app_status.py.py hg4kjgl34hg4-23kj23khg2k3j23-kj23h4k23k4-23423423md-rdfdfmo32r2r34r",
        )  # noqa
        exit(1)

    heroku_conn = heroku3.from_key(os.environ["HEROKU_API_KEY"])
    appsetup = heroku_conn.get_appsetup(app_id)
    pprint(vars(appsetup))
    pprint(vars(appsetup.build))
    if appsetup.build:
        stream_build_logs(appsetup.id)
        stream_app_logs(appsetup.id, appsetup.app.id)
