# -*- coding: utf-8 -*-
from ipaddress import IPv4Network
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
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
            "address_range": self._config.get("config.wireguard.ip_range"),
            "wireguard":
                {
                    "endpoint": self._config.get("config.wireguard.endpoint"),
                    "public_key": self._config.get("config.wireguard.public_key")
                }
        }
        self.generate_config("client", ctx)
        self.generate_config("peer", ctx)
        self._config.helper.add_client(ctx)
        self.apply_config_to_server(filename)
        return ctx

    def apply_config_to_server(self, filename):
        peer_file = os.path.join(self._config.get("config.peer_folder", mod="get_relative_path"), "{}.conf".format(filename))
        subprocess.check_output(f"wireguard addconf wg0 {peer_file}", shell=True).decode("utf-8").strip()

    def generate_config(self, name, ctx):
        tpl = self.load_tpl(name)
        conf = tpl.render(ctx)
        log.debug(conf)
        folder_path = self._config.get("config.{}_folder".format(name))
        target_path = os.path.join(self._config.helper.get_path_config(folder_path), "{}.conf".format(ctx.get("filename")))
        log.debug("Write {}".format(target_path))

        with open(target_path, "w+") as fobj:
            fobj.write(conf)

    def load_tpl(self, name):
        template_path = self._config.get("config.{}_template".format(name), mod="get_relative_path")
        with open(template_path, "r") as fobj:
            template = Template(fobj.read())
            return template

    def generate_filename(self):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(10))
        return result_str

    def find_available_ip_address(self):
        for possible_host in IPv4Network(self._config.get("config.wireguard.ip_range")).hosts():
            if str(possible_host) not in self._config.helper.get_client_ip_addresses() and str(possible_host) not in self._config.get(
                    "config.reserved_ip"):
                log.debug(possible_host)
                return possible_host

    def generate_wireguard_keys(self):
        """
            Generate a WireGuard private & public key
            Requires that the 'wireguard' command is available on PATH
            Returns (private_key, public_key), both strings
        """
        privkey = subprocess.check_output("wireguard genkey", shell=True).decode("utf-8").strip()
        pubkey = subprocess.check_output(f"echo '{privkey}' | wireguard pubkey", shell=True).decode("utf-8").strip()
        return (privkey, pubkey)
