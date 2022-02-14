# -*- coding: utf-8 -*-

import argparse
import os
import pathlib
import secrets

import yaml

from wgui.conf.config import Configuration


class ConfigurationInitializer:

    def __init__(self, parser, options):
        self._parser = parser
        self._options = options

        if not os.path.exists(self._options.config):
            self.create_config_yaml(self._options.config)

        config = Configuration(self._options)
        self.initialize_config_files(config)

    def initialize_config_files(self, config):
        pathlib.Path(config.get("config.client_folder", mod="get_relative_path")).mkdir(parents=True)
        pathlib.Path(config.get("config.peer_folder", mod="get_relative_path")).mkdir(parents=True)
        pathlib.Path(config.get("config.client_template", mod="get_relative_path")).parent.mkdir(parents=True)
        pathlib.Path(config.get("config.peer_template", mod="get_relative_path")).parent.mkdir(parents=True)
        pathlib.Path(config.get("config.client_template", mod="get_relative_path")).touch()
        pathlib.Path(config.get("config.peer_template", mod="get_relative_path")).touch()

    def create_config_yaml(self, config_file):
        config_data = self.get_new_configuration_data()
        with open(config_file, "r+") as fobj:
            yaml.dump(config_data, fobj)

    def get_new_configuration_data(self):
        question = {
            "app_url": "URL of used for Webinterface: ",
            "wg_endpoint": "Wireguard Endpoint domain (with port): ",
            "wg_public_key": "Wireguard Server Public Key: ",
            "wg_ip_range": "IP-Range used for Peers: "
        }
        user_config = {}
        for slug, prompt in question.items():
            user_config[slug] = ConfigurationInitializer.user_input(prompt)

        config_data = {
            "config":
                {
                    "wireguard":
                        {
                            "endpoint": user_config.get("wg_endpoint"),
                            "ip_range": user_config.get("wg_ip_range"),
                            "public_key": user_config.get("wg_public_key")
                        },
                    "secret_key": secrets.token_urlsafe(32),
                    "app_url": user_config.get("app_url")
                }
        }
        return config_data

    @staticmethod
    def user_input(prompt):
        data = ""
        retry = 0
        while data == "" and retry <= 3:
            data = input(prompt).strip()
            retry = retry + 1
        if retry >= 3:
            raise ValueError("too many invalid inputs")
        return data


a = ConfigurationInitializer(None, argparse.Namespace(config="foooo"))
a.create_config_yaml("x")
