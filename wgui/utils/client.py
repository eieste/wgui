# -*- coding: utf-8 -*-
from ipaddress import IPv4Network
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import logging
import os

from wgui.mixins.wireguard import WireguardConfigMixin
from wgui.utils.cmd import apply_to_wireguard

log = logging.getLogger(__name__)


class Client(WireguardConfigMixin):

    def __init__(self, person, device_name, filename, ip_address, public_key, private_key):
        self.person = person
        self.device_name = device_name
        self.public_key = public_key
        self.private_key = private_key
        self.filename = filename
        self.ip_address = ip_address

    def as_dict(self):
        return {
            "device_name": self.device_name,
            "public_key": self.public_key,
            "private_key": self.private_key,
            "filename": self.filename,
            "ip_address": str(self.ip_address)
        }

    @staticmethod
    def load(person, data):
        return Client(
            person=person,
            device_name=data.get("device_name"),
            filename=data.get("filename"),
            ip_address=data.get("ip_address"),
            public_key=data.get("public_key"),
            private_key=data.get("private_key"))

    @classmethod
    def create(cls, person, device_name):
        used_ips = person.get_used_ips(person.config) + person.config.get("config.wireguard.reserved_ip")
        ip_address = cls.find_available_ip(person.config.get("config.wireguard.ip_range"), used_ips)
        keypair = cls.generate_wireguard_keys()
        filename = cls.generate_filename()

        client = cls(person, device_name, filename, ip_address, keypair.public_key, keypair.private_key)

        ctx = {
            "person": person,
            "device_name": device_name,
            "private_key": keypair[0],
            "public_key": keypair[1],
            "filename": filename,
            "ip_address": str(ip_address),
            "wireguard":
                {
                    "public_key": person.config.get("config.wireguard.public_range"),
                    "ip_range": person.config.get("config.wireguard.ip_range"),
                    "endpoint": person.config.get("config.wireguard.endpoint")
                },
            "config": person.config,
        }

        peer_target_path = os.path.join(person.config.get("config.peer_folder", mod="get_relative_path"), "{}.conf".format(filename))

        peer_source_path = person.config.get("config.peer_template", mod="get_relative_path")

        cls.generate_config(peer_source_path, peer_target_path, ctx)

        client_target_path = os.path.join(person.config.get("config.client_folder", mod="get_relative_path"), "{}.conf".format(filename))

        client_source_path = person.config.get("config.client_template", mod="get_relative_path")

        cls.generate_config(client_source_path, client_target_path, ctx)

        apply_to_wireguard(peer_target_path, person.config)
        return client

    @classmethod
    def find_available_ip(cls, network, occupied_ip_addresses):
        for possible_host in IPv4Network(network).hosts():
            if str(possible_host) not in occupied_ip_addresses:
                return possible_host
