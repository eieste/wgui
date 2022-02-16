# -*- coding: utf-8 -*-
import logging
import os
import random
import string
import subprocess
from typing import NamedTuple

from jinja2 import Template

log = logging.getLogger(__name__)


class WireguardKeys(NamedTuple):
    private_key: str
    public_key: str


class WireguardConfigMixin:

    def generate_config(self, name, ctx):
        tpl = self.load_tpl(name)
        conf = tpl.render(ctx)
        log.debug(conf)
        folder_path = self.config.get("config.{}_folder".format(name))
        target_path = os.path.join(self.config.helper.get_path_config(folder_path), "{}.conf".format(ctx.get("filename")))
        log.debug("Write {}".format(target_path))

        with open(target_path, "w+") as fobj:
            fobj.write(conf)

    def load_tpl(self, name):
        template_path = self.config.get("config.{}_template".format(name), mod="get_relative_path")
        with open(template_path, "r") as fobj:
            template = Template(fobj.read())
            return template

    def generate_filename(self):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(10))
        return result_str

    def generate_wireguard_keys(self) -> WireguardKeys:
        """
            Generate a WireGuard private & public key
            Requires that the 'wg' command is available on PATH
            Returns (private_key, public_key), both strings
        """
        privkey = subprocess.check_output("wg genkey", shell=True).decode("utf-8").strip()
        pubkey = subprocess.check_output(f"echo '{privkey}' | wg pubkey", shell=True).decode("utf-8").strip()
        return WireguardKeys(private_key=privkey, public_key=pubkey)
