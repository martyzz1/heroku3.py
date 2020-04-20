import copy


class ConfigVars(object):
    """Set of configuration variables of a Heroku application

    This class mutates the settings of the application as you mutate it's
    content:

    .. code-block::

       configuration = app.config()  # Assume app is an application
       configure['SOME_SETTING'] = 'some value'

    That last line of code will synchronously trigger a call to Heroku's
    API to change the setting value. If this is not what you desire, you
    can collect settings in a regular dictionary with::

       import copy
       configuration = app.config()  # Assume app is an application
       safe_configuration = configuration.dict()
       # mutate safe_configuration as you please
       configuration.update(safe_configuration)

    """

    def __init__(self, data, app, h=None, **kwargs):
        # assert app is not None
        # copy: Ensures caller has no way to mutate our internal state outside
        # our control
        self.__data = copy.copy(data)
        self.__app = app
        self._h = h

        super(ConfigVars, self).__init__()

    def __repr__(self):
        return repr(self.__data)

    def __contains__(self, key):
        return key in self.__data

    def __getitem__(self, key):
        return self.__data.get(key)

    def __setitem__(self, key, value):
        # API expects JSON.
        self.__data = self.__patch_config({key: value})

    def __delitem__(self, key):
        data = self.__patch_config({key: None})
        assert key not in data
        self.__data = data

    @property
    def _resource(self):
        return "apps", self.__app.name, "config-vars"

    def __patch_config(self, config):
        payload = self._h._resource_serialize(config)
        r = self._h._http_resource(method="PATCH", resource=self._resource, data=payload)
        r.raise_for_status()
        return self._h._resource_deserialize(r.content.decode("utf-8"))

    def update(self, newconf):
        """Update the configuration

        Note:
          To actually remove a variable from you application configuration, you
          should not just remove the key from the ``newconfg`` but actually set
          it to None. Otherwise Heroku's API will just assume you want to leave
          that variable *as-is*::

              # This won't work:
              configuration = app.config()
              config = configuration.dict()
              del config['SOME_SETTING']  # Wrong
              configuration.update(config)
              assert 'SOME_SETTING' in configuration

              # This will work:
              configuration = app.config()
              config = configuration.dict()
              config['SOME_SETTING'] = None  # Ok
              configuration.update(config)
              assert 'SOME_SETTING' not in configuration

        Args:
          newconf (dict): the new application configuration
        Returns:
          None: mutates the :class:`ConfigVars` instance state.
        """
        self.__data = self.__patch_config(newconf)

    def to_dict(self):
        return copy.copy(self.__data)

    dict = to_dict

    @classmethod
    def new_from_dict(cls, d, h=None, **kwargs):
        # Override normal operation because of crazy api.
        c = cls(d, kwargs.pop("app", None), h=h, **kwargs)
        return c
