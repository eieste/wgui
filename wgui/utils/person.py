# -*- coding: utf-8 -*-
import logging

import yaml

from wgui.contrib.loader import load_person_file
from wgui.utils.client import Client

log = logging.getLogger(__name__)


def get_person(config, email):
    person_data = load_person_file(config)

    for person in person_data.get("persons"):
        if person.get("email") == email:
            return Person.load(config, person)


class Person:

    def __init__(self, config, email):
        self.config = config
        self.email = email
        self.clients = []

    def add_client(self, client):
        self.clients.append(client)

    @staticmethod
    def load(config, data):
        person = Person(config, data.get("email"))
        [person.add_client(Client.load(person, client)) for client in data.get("clients")]
        return person

    def get_client_by_filename(self, filename):
        for client in self.clients:
            if filename == client.filename:
                return client
        return False

    def has_clients(self, *clients):
        for client in clients:
            exist = False
            if self.get_client_by_filename(client):
                exist = True
            if not exist:
                log.error(f"Cant find client {client} at logged in Person {self.email}")
                return False
        return True

    def create_device(self, device_name):
        client = Client.create(self, device_name)
        self.add_client(client)
        self._save()

    def as_dict(self):
        return {"email": self.email, "clients": [client.as_dict() for client in self.clients]}

    def _save(self):
        with open(self.config.get("config.person_file"), "r+") as fobj:
            data = yaml.load(fobj, Loader=yaml.SafeLoader)
            person_data = []
            for person in data.get("persons"):
                if person.get("email") == self.email:
                    person_data.append(self.as_dict())
                else:
                    person_data.append(person)
            fobj.seek(0)
            yaml.dump({"persons": person_data}, fobj, indent=4)
            fobj.truncate()

    @classmethod
    def get_used_ips(cls, config):
        used_ip = []
        data = load_person_file(config)
        for person in data.get("persons"):
            used_ip = used_ip + [client.get("ip_address") for client in person.get("clients")]
        return used_ip
