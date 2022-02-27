# -*- coding: utf-8 -*-
from ipaddress import IPv4Network
# -*- coding: utf-8 -*-
import logging

from wgui.mixins.wireguard import WireguardConfigMixin

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
            "ip_address": self.ip_address
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

        ctx = {
            "person": person,
            "device_name": device_name,
            "private_key": keypair[0],
            "public_key": keypair[1],
            "filename": filename,
            "ip_address": str(ip_address),
            "config": person.config,
        }
        cls.generate_config("client", ctx)
        cls.generate_config("peer", ctx)
        # apply_to_wireguard(filename)

    @classmethod
    def find_available_ip(cls, network, occupied_ip_addresses):
        for possible_host in IPv4Network(network).hosts():
            if str(possible_host) not in occupied_ip_addresses:
                return possible_host
