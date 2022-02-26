# -*- coding: utf-8 -*-
import logging
import random
import string
import subprocess
from typing import NamedTuple

from jinja2 import Template

log = logging.getLogger(__name__)


class WireguardKeypair(NamedTuple):
    private_key: str
    public_key: str


class WireguardConfigMixin:

    @staticmethod
    def generate_config(self, source_path, target_path, ctx):
        tpl = self.load_tpl(source_path)
        conf = tpl.render(ctx)
        log.debug("Write {}".format(target_path))
        with open(target_path, "w+") as fobj:
            fobj.write(conf)

    @staticmethod
    def load_tpl(template_path):
        with open(template_path, "r") as fobj:
            template = Template(fobj.read())
            return template

    @staticmethod
    def generate_filename():
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(10))
        return result_str

    @staticmethod
    def generate_wireguard_keys() -> WireguardKeypair:
        """
            Generate a WireGuard private & public key
            Requires that the 'wireguard' command is available on PATH
            Returns (private_key, public_key), both strings
        """
        privkey = subprocess.check_output("wireguard genkey", shell=True).decode("utf-8").strip()
        pubkey = subprocess.check_output(f"echo '{privkey}' | wireguard pubkey", shell=True).decode("utf-8").strip()
        return WireguardKeypair(private_key=privkey, public_key=pubkey)
