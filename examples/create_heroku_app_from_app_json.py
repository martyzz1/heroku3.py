#! /usr/bin/env python
#
######################################################################################################################
#
#  Script that will create and deploy an app to Heroku
#  requirements:-
#  An app in its own repo   "example-app"
#  valid app.json  "example-app" repo  - see heroku button for more information
#  an existing app running on heroku - "reference-app"  which contains any number of personalised config vars
#  you would like to copy over to your new app.   Useful for things like api keys.
#  a "type" of app. This can be any string you want, but best to stick to your own naming conventions.
#  'production', 'staging' 'test'  are good examples
#
#  YOU WILL NEED TO EDIT THIS CODE TO WORK WITH YOUR OWN PROJECTS. ITS JUST HERE TO GIVE YOU SOME POINTERS
######################################################################################################################


import os
import sys
import time
import itertools
from pprint import pprint

# Third party libraries
import heroku3
from requests.exceptions import Timeout, ConnectionError

HEROKU_API_KEY = os.environ["HEROKU_API_KEY"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
heroku_conn = heroku3.from_key(os.environ["HEROKU_API_KEY"])

app = {
    "region": "eu",
}
source_blob = {}
overrides = {"env": {}}

POPULATE_FROM_HEROKU_ENV_VARS = [
    "DJANGO_GOOGLE_API_KEY",
    "PIP_EXTRA_INDEX_URL",
    "SENTRY_AUTH_TOKEN",
    "SENTRY_DSN",
]

spinner = itertools.cycle(["-", "\\", "|", "/"])


def get_configuration(app_name, app_type):

    if app_type == "production":
        domain = ".example.com"
        reference_app = "reference-app"
        app["name"] = "example-{0}".format(app_name)
        git_name = "heroku_live"
    else:
        domain = ".{0}example.com".format(app_type)
        reference_app = "{0}reference-app".format(app_type)
        app["name"] = "{0}example-{1}".format(app_type, app_name)
        overrides["env"]["DJANGO_CONFIGURATION"] = app_type.capitalize()
        overrides["env"]["DJANGO_SETTINGS_MODULE"] = "config.settings.{0}".format(app_type)
        git_name = "heroku_{0}".format(app_type)

    overrides["env"]["DJANGO_HOSTNAME"] = "{0}{1}".format(app_name, domain)

    heroku_app = heroku_conn.app(reference_app)
    config = heroku_app.config()

    for k in POPULATE_FROM_HEROKU_ENV_VARS:
        if config[k]:
            overrides["env"][k] = config[k]

    source_blob["url"] = "https://api.github.com/repos/example/{0}/tarball/master?access_token={1}".format(
        app_name, GITHUB_TOKEN
    )

    data = {
        "app": app,
        "source_blob": source_blob,
        "overrides": overrides,
    }

    return data, git_name


def wait_for_status_event(appsetup_id, time_checkpoint):
    time_check = time.time()
    if (time_check - time_checkpoint) > 5:
        time_checkpoint = time_check
        print("checking status", end="\r")
        appsetup = heroku_conn.get_appsetup(appsetup_id)
        if appsetup.build:
            print("Build Available", appsetup.build)
            return True, time_checkpoint
        if appsetup.status in ["failed", "succeeded"]:
            return True, time_checkpoint
    return False, time_checkpoint


def stream_build_logs(appsetup_id):
    appsetup = heroku_conn.get_appsetup(appsetup_id)
    build_iterator = appsetup.build.stream(timeout=5)
    try:
        for line in build_iterator:
            if line:
                print("{0}".format(line.decode("utf-8")))
    except Timeout:
        appsetup = heroku_conn.get_appsetup(appsetup_id)
        if appsetup.build.status == "pending":
            return stream_build_logs(appsetup_id)
        else:
            return
    except ConnectionError:
        appsetup = heroku_conn.get_appsetup(appsetup_id)
        if appsetup.build.status == "pending":
            return stream_build_logs(appsetup_id)
        else:
            return


def stream_app_logs(appsetup_id, app_id):
    app = heroku_conn.app(app_id)
    iterator = app.stream_log(timeout=5)
    try:
        for line in iterator:
            if line:
                print("{0}".format(line.decode("utf-8")))
    except ConnectionError:
        appsetup = heroku_conn.get_appsetup(appsetup_id)
        if appsetup.status == "pending":
            return stream_app_logs(appsetup_id, app_id)
        else:
            return


if __name__ == "__main__":

    if len(sys.argv) > 2:
        app_name = sys.argv[1]  # example-app
        app_type = sys.argv[2]  # staging | production
    else:
        print(
            "Please specify the app name and the type of heroku app to create e.g.\n",
            "./create_heroku_app.py example-app production\n or\n./create_heroku_app.py example-app staging",
        )  # noqa
        exit(1)

    data, git_name = get_configuration(app_name, app_type)
    pprint(data)
    heroku_appsetup = heroku_conn.create_appsetup(**data)
    pprint(vars(heroku_appsetup))

    app = heroku_conn.app(heroku_appsetup.app.id)
    time_checkpoint = time.time()
    waiting = True
    while True:
        next(spinner)
        print("{0}\r".format(next(spinner)), end="\r")

        success, time_checkpoint = wait_for_status_event(heroku_appsetup.id, time_checkpoint)
        if success:
            break

    stream_build_logs(heroku_appsetup.id)
    stream_app_logs(heroku_appsetup.id, heroku_appsetup.app.id)

    appsetup = heroku_conn.get_appsetup(heroku_appsetup.id)
    if appsetup.status == "succeeded":
        print("Enabling heroku labs runtime dyno metrics")
        app.enable_feature("runtime-dyno-metadata")

        print("Don't forget to add your git remotes in your local repo directory\n\n")
        print("git remote add {0} {1}\n\n".format(git_name, app.git_url))
