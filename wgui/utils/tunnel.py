# -*- coding: utf-8 -*-
from ipaddress import IPv4Network
import logging
import os
import random
import string
import subprocess

from jinja2 import Template

log = logging.getLogger(__name__)


class Tunnel:

    def __init__(self, config):
        self._config = config

    def create(self, email, device):
        available_ip = self.find_available_ip_address()
        filename = self.generate_filename()
        keypair = self.generate_wireguard_keys()
        ctx = {
            "email": email,
            "device": device,
            "private_key": keypair[0],
            "public_key": keypair[1],
            "filename": filename,
            "ip_address": str(available_ip),
            "address_range": self._config.config("range")
        }
        self.generate_config("client", ctx)
        self.generate_config("peer", ctx)

        self._config.add_client(ctx)

    def generate_config(self, name, ctx):
        tpl = self.load_tpl(name)
        conf = tpl.render(ctx)
        log.debug(conf)
        target_path = os.path.join(self._config.get_path_config("{}_folder".format(name)), "{}.conf".format(ctx.get("filename")))
        log.debug("Write {}".format(target_path))

        with open(target_path, "w+") as fobj:
            fobj.write(conf)

    def load_tpl(self, name):
        with open(os.path.join(self._config.get_path_config(name + "_template"))) as fobj:
            template = Template(fobj.read())
            return template

    def generate_filename(self):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(10))
        return result_str

    def find_available_ip_address(self):
        for possible_host in IPv4Network(self._config.config("range")).hosts():
            if str(possible_host) not in self._config.get_client_ip_addresses():
                log.debug(possible_host)
                return possible_host

    def generate_wireguard_keys(self):
        """
            Generate a WireGuard private & public key
            Requires that the 'wg' command is available on PATH
            Returns (private_key, public_key), both strings
        """
        privkey = subprocess.check_output("wg genkey", shell=True).decode("utf-8").strip()
        pubkey = subprocess.check_output(f"echo '{privkey}' | wg pubkey", shell=True).decode("utf-8").strip()
        return (privkey, pubkey)
