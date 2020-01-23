# Project libraries
from . import BaseResource
from .app import App
from .build import Build


class PostDeploy(BaseResource):
    _strs = ["output"]
    _ints = ["exit_code"]

    def __init__(self):
        super(PostDeploy, self).__init__()


class AppSetup(BaseResource):
    _strs = ["id", "failure_message", "postdeploy:exit_code", "postdeploy:output", "resolved_success_url", "status"]
    _map = {"app": App, "build": Build, "postdeploy": PostDeploy}
    _dates = ["created_at", "updated_at"]
    _pks = ["id"]

    def __init__(self):
        super(AppSetup, self).__init__()

    def __repr__(self):
        return "<appsetup '{0}' - '{1}'>".format(self.id, self.status)
