# -*- coding: utf-8 -*-
import logging
import pathlib

import yaml

from wgui.contrib.decorators import deprecated

log = logging.getLogger(__name__)


class ConfiguraitonHelper:

    def __init__(self, config):
        self.config = config

    def get_clients_by_user(self, email):
        client_list = []
        for client in self.config.get("clients"):
            if client.get("email") == email:
                client_list.append(client)
        return client_list

    def get_saml_idp_by_slug(self, slug):
        for saml in self.config.get("config.saml.id_providers"):
            if saml.get("slug") == slug:
                return saml

    def add_client(self, ctx):
        clients = self.config.get("clients", [])

        clients.append(
            {
                "device": ctx.get("device"),
                "ip_address": ctx.get("ip_address"),
                "email": ctx.get("email"),
                "filename": ctx.get("filename"),
                "public_key": ctx.get("public_key")
            })

        with open(self.config._options.config, "r") as fobj:
            conf = yaml.load(fobj, Loader=yaml.FullLoader)

            conf["clients"] = clients
            with open(self.config._options.config, "w") as fobj:
                yaml.dump(conf, fobj, sort_keys=True, indent=2)
            # fobj.seek(0)
            # yaml.dump(conf, fobj)

    def get_client_ip_addresses(self):
        ip_address_list = []
        for client in self.config.get("clients"):
            ip_address_list.append(client.get("ip_address"))
        return ip_address_list

    @deprecated
    def get_path_config(self, value):
        p = pathlib.Path(self.config._options.config).parent.resolve().joinpath(value)
        log.debug("Config-FilePath: {}".format(p))
        return p

    def get_relative_path(self, path):
        p = pathlib.Path(self.config._options.config).parent.resolve().joinpath(path)
        log.debug("Config-FilePath: {}".format(p))
        return p
