# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import logging
import pathlib

log = logging.getLogger(__name__)


class ConfigurationHelper:

    def __init__(self, config):
        self.config = config

    def get_saml_idp_by_slug(self, slug):
        for saml in self.config.get("config.saml.id_providers"):
            if saml.get("slug") == slug:
                return saml

    def get_relative_path(self, target_path):
        return get_relative_path(self.config._options.config, target_path)


def get_relative_path(origin_path, target_path):
    p = pathlib.Path(origin_path).parent.resolve().joinpath(target_path)
    log.debug("Config-FilePath: {}".format(p))
    return p
