# Project libraries
from . import BuildPack, BaseResource  # noqa


class BuildpackInstallation(BaseResource):
    """Heroku Buildpack Insallation."""

    _map = {"buildpack": Buildpack}  # noqa
    _ints = ["ordinal"]
    _pks = ["ordinal"]

    def __repr__(self):
        return "<buildpack-installation '{}'>".format(self.buildpack)
