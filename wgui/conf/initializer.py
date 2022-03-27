# -*- coding: utf-8 -*-

import logging
import os
import pathlib
import pkgutil
import secrets

import yaml

from wgui.conf.config import Configuration
from wgui.exceptions import ValidationError

log = logging.getLogger(__name__)


def str_validator():

    def wrapper(value):
        return str(value)

    return wrapper


class ConfigQuestion:

    def __init__(self, slug, question, validator, default=None, only_from_env=False):
        self.slug = slug
        self.question = question
        self.validator = validator
        self.only_from_env = only_from_env
        self.default = default
        self.value = None

    def get_value(self):
        if self.value is None:
            self.value = self.acquire_value()
        return self.value

    def acquire_value(self):
        data = ""
        retry = 0
        env_name = "WGUI_" + self.slug.upper()
        if os.environ.get(env_name) is not None:
            return os.environ.get(env_name)

        while (data == "" or data is None) and retry <= 3:
            raw_data = input(f"{self.question} [{self.default}]: ").strip()
            if raw_data == "":
                raw_data = self.default
            try:
                data = self.validator(raw_data)
            except ValidationError:
                log.info("Value {} cant be validated")
            retry = retry + 1
        if retry >= 3:
            raise ValueError("too many invalid inputs")
        return data


class ConfigurationInitializer:

    DEFAULT_CONFIG_PATH = "/etc/wgui/wgui.yml"

    def __init__(self, parser, options):
        self._parser = parser
        self._options = options

        if self._options.config is None or not os.path.exists(self._options.config):
            config_path = self.create_config_yaml()

        config = Configuration(self._options.config or config_path)
        self.initialize_config_files(config)

    def initialize_config_files(self, config):
        log.debug("Create client_folder")
        pathlib.Path(config.get("config.client_folder", mod="get_relative_path")).mkdir(parents=True, exist_ok=True)
        log.debug("Create peer_folder")
        pathlib.Path(config.get("config.peer_folder", mod="get_relative_path")).mkdir(parents=True, exist_ok=True)
        log.debug("Create client_template")
        pathlib.Path(config.get("config.client_template", mod="get_relative_path")).parent.mkdir(parents=True, exist_ok=True)
        log.debug("Create peer_template")
        pathlib.Path(config.get("config.peer_template", mod="get_relative_path")).parent.mkdir(parents=True, exist_ok=True)

        if not pathlib.Path(config.get("config.client_template", mod="get_relative_path")).exists():
            log.debug("Create client_template")
            with pathlib.Path(config.get("config.client_template", mod="get_relative_path")).open("w+") as fobj:
                fobj.write(pkgutil.get_data("wgui", "sample/client.tpl").decode('utf8'))

        log.debug("Create peer_template")

        if not pathlib.Path(config.get("config.peer_template", mod="get_relative_path")).exists():
            log.debug("Create peer_template")
            with pathlib.Path(config.get("config.peer_template", mod="get_relative_path")).open("w+") as fobj:
                fobj.write(pkgutil.get_data("wgui", "sample/peer.tpl").decode('utf8'))

    def create_config_yaml(self):
        config_data, user_config = self.get_new_configuration_data()

        config_path = pathlib.Path(user_config.get("config_prefix"))
        config_path.mkdir(parents=True, exist_ok=True)
        with config_path.joinpath("wgui.yml").open("w+") as fobj:
            yaml.dump(config_data, fobj)
        return config_path.joinpath("wgui.yml").as_posix()

    def get_new_configuration_data(self):
        config_option = [
            ConfigQuestion("app_url", "URL of used for Webinterface", str_validator(), default="vpn.local"),
            ConfigQuestion("wg_endpoint", "Wireguard Endpoint domain (with port)", str_validator(), default="vpn.local:58120"),
            ConfigQuestion("wg_public_key", "Wireguard Server Public Key", str_validator()),
            ConfigQuestion("wg_ip_range", "IP-Range used for Peers", str_validator(), default="192.168.0.0/24"),
            ConfigQuestion("wg_interface", "Wireguard Interface", str_validator(), default="wg0"),
            ConfigQuestion(
                "wg_reserved_ip",
                "Wireguard Gateway IP: ",
                str_validator(),
                default="192.168.0.1,192.168.0.2,192.168.0.3,192.168.0.4,192.168.0.5"),
            ConfigQuestion(
                "config_prefix",
                "Path Prefix where the wgui configuration should be stored",
                str_validator(),
                default="/etc/wgui/",
                only_from_env=True)
        ]

        user_config = {}
        for option in config_option:
            user_config[option.slug] = option.acquire_value()

        config_data = {
            "config":
                {
                    "wireguard":
                        {
                            "endpoint": user_config.get("wg_endpoint"),
                            "ip_range": user_config.get("wg_ip_range"),
                            "public_key": user_config.get("wg_public_key"),
                            "reserved_ip": user_config.get("wg_reserved_ip").split(","),
                            "interface": user_config.get("wg_interface")
                        },
                    "client_folder": "/etc/wireguard/clients",
                    "peer_folder": "/etc/wireguard/peers",
                    "client_template": "/etc/wgui/client.tpl",
                    "peer_template": "/etc/wgui/peer.tpl",
                    "secret_key": secrets.token_urlsafe(32),
                    "app_url": user_config.get("app_url"),
                    "person_file": "/etc/wgui/person.yml"
                }
        }
        return config_data, user_config
