from . import BaseResource, BuildPack


class BuildpackInstallation(BaseResource):
    """Heroku Buildpack Insallation."""

    _map = {'buildpack': Buildpack}
    _ints = ['ordinal']
    _pks = ['ordinal']

    def __repr__(self):
        return "<buildpack-installation '{}'>".format(self.buildpack)
