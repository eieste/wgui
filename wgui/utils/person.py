# -*- coding: utf-8 -*-
import logging

import yaml

from wgui.utils.client import Client

log = logging.getLogger(__name__)


def load_person_file(config):
    with open(config.get("config.person_file"), "r") as fobj:
        return yaml.load(fobj, Loader=yaml.SafeLoader)


def get_person(config, email):
    person_data = load_person_file(config)

    for person in person_data.get("persons"):
        if person.get("email") == email:
            return Person.load(person)


class Person:

    def __init__(self, email):
        self.email = email
        self.clients = []

    def add_client(self, client):
        self.clients.append(client)

    @staticmethod
    def load(data):
        person = Person(data.get("email"))
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
