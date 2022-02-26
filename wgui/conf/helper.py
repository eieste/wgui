# -*- coding: utf-8 -*-
from ipaddress import IPv4Network
# -*- coding: utf-8 -*-
import logging
import pathlib

import yaml

from wgui.contrib.decorators import deprecated

log = logging.getLogger(__name__)


class ConfigurationHelper:

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

    def find_available_ip_address(self):
        for possible_host in IPv4Network(self.config.get("config.wireguard.ip_range")).hosts():
            if str(possible_host) not in self.config.helper.get_client_ip_addresses() and str(possible_host) not in self.config.get(
                    "config.wireguard.reserved_ip"):
                return possible_host

    @deprecated
    def get_path_config(self, value):
        p = pathlib.Path(self.config._options.config).parent.resolve().joinpath(value)
        log.debug("Config-FilePath: {}".format(p))
        return p

    def get_relative_path(self, target_path):
        return get_relative_path(self.config._options.config, target_path)

    def update(self):
        log.info("re-Write config ")


def get_relative_path(origin_path, target_path):
    p = pathlib.Path(origin_path).parent.resolve().joinpath(target_path)
    log.debug("Config-FilePath: {}".format(p))
    return p
