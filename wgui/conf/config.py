# -*- coding: utf-8 -*-
import functools
import json
import logging
import pathlib
import pkgutil

from flask import g
import jsonschema
import yaml

from wgui.conf.helper import ConfigurationHelper
from wgui.contrib.decorators import deprecated

log = logging.getLogger(__name__)


class Configuration:
    DEFAULT_VALUES = {
        "config":
            {
                "client_folder": "/etc/wireguard/clients",
                "client_template": "/etc/wgui/client.tpl",
                "peer_folder": "/etc/wireguard/peers",
                "peer_template": "/etc/wgui/peer.tpl",
                "database_uri": "sqlite:////etc/wgui/users.db"
            },
        "clients": {}
    }

    def __init__(self, options=None):
        self._options = options
        self.helper = ConfigurationHelper(self)

    @property
    def configuration(self):
        try:
            if g.config is not None:
                return g.config
        except RuntimeError:
            Configuration.validate(self._options.config)
            return Configuration.load_config(self._options.config)

    @staticmethod
    @functools.lru_cache(maxsize=128)
    def get_config_schema():
        """
            Load Configuration JSON Schema

            :return: Validation Schema
        """
        log.debug("Load configuraiton Schema")
        schema = pkgutil.get_data("wgui", "conf/wgui.schema.json")
        return json.loads(schema)

    @staticmethod
    def load_config(path):
        """
            Load configuration File

            :param path: Path to Configuration File
            :return dict: Configuration Dict
        """
        log.debug("Load Config from path: {}".format(path))
        with open(path, "r") as fobj:
            return yaml.load(fobj, Loader=yaml.Loader)

    @staticmethod
    def validate(path):
        """
            Validate Configuration dict via JSON-Schema

            :param path: Path to Configuration file
            :return: Returns True if validation is Successful
        """
        log.debug("Validate Config")
        raw_config = Configuration.load_config(path)
        jsonschema.validate(raw_config, Configuration.get_config_schema())
        return True

    @deprecated
    def get_config(self, name):
        """
        Deprecation
        :param name:
        :return:
        """
        return self.configuration.get("config").get(name)

    def get(self, name_path, mod=None):
        """
            Returns Configuration Item from dot path.
            If no value in configuration is available it use DEFAULT_VALUES

            :param name_path: Dot-Path to config item
            :return:
        """
        default = self.__class__.DEFAULT_VALUES
        conf = self.configuration
        for part in name_path.split("."):
            if default is not None:
                default = default.get(part)
            conf = conf.get(part, default)

        if mod is not None:
            return getattr(self.helper, mod)(conf)
        return conf

    @deprecated
    def get_path_config(self, value):
        p = pathlib.Path(self._options.config).parent.resolve().joinpath(value)
        log.debug("Config-FilePath: {}".format(p))
        return p
