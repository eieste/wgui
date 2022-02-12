import pathlib

import jsonschema
import logging
import pkgutil
import yaml
import json
import functools

log = logging.getLogger(__name__)


class Configuration:

    def __init__(self, options=None):
        self._options = options
        Configuration.validate(options.config)
        self.configuration = Configuration.get_config(options.config)

    @staticmethod
    def get_config_schema():
        log.debug("Load config Schema")
        schema = pkgutil.get_data("wgui", "conf/wgui.schema.json")
        return json.loads(schema)

    @staticmethod
    @functools.cache
    def get_config(path):
        log.debug("Load Config from path: {}".format(path))
        with open(path, "r") as fobj:
            return yaml.load(fobj, Loader=yaml.Loader)

    @staticmethod
    def validate(path):
        log.debug("Validate Config")
        raw_config = Configuration.get_config(path)
        jsonschema.validate(raw_config, Configuration.get_config_schema())

    def config(self, name):
        return self.configuration.get("config").get(name)

    def get_client_ip_addresses(self):
        ip_address_list = []
        for client in self.configuration.get("clients"):
            ip_address_list.append(client.get("ip_address"))
        return ip_address_list

    def get_path_config(self, name):
        p = pathlib.Path(self._options.config).parent.resolve().joinpath(self.config(name))
        log.debug("Config-FilePath: {}".format(p))
        return p

    def add_client(self, ctx):
        clients = self.configuration.get("clients", [])

        clients.append({
            "device": ctx.get("device"),
            "ip_address": ctx.get("ip_address"),
            "email": ctx.get("email"),
            "filename": ctx.get("filename"),
            "public_key": ctx.get("public_key")
        })

        with open(self._options.config, "r") as fobj:

            conf = yaml.load(fobj, Loader=yaml.FullLoader)
            print(conf)
            conf["clients"] = clients
            with open(self._options.config, "w") as fobj:
                yaml.dump(conf, fobj, sort_keys=True, indent=2)
            #fobj.seek(0)
            #yaml.dump(conf, fobj)