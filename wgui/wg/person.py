# -*- coding: utf-8 -*-
import logging

from wgui.exceptions import ConfigurationError
from wgui.wg.device import PersonDevice
from wgui.wg.inizialize import PersonInitialize

log = logging.getLogger(__name__)


class Person(PersonInitialize):
    PERSON_LIST = []

    @staticmethod
    def load(client_config):
        for client_item in client_config:
            Person.init_person(client_item)

    @staticmethod
    def load_into_person(client_item):
        person = Person.get_person_by_email(client_item.get("email"))
        if person is None:
            person = Person(client_item.get("email"))
        person.add_device(client_item)
        Person.PERSON_LIST.append(person)

    def __init__(self, wg_client):
        self._email = wg_client.get("email")
        self.devices = []

    def add_device(self, wg_client):
        already_exists = False
        for device in self.devices:
            if device.device_name == wg_client.get("device"):
                already_exists = True

        if not already_exists:
            device = PersonDevice(wg_client)
            self.devices.append(device)
        else:
            raise ConfigurationError("Device already Exists name {} already exists".format(wg_client.get("device")))

        return device

    @staticmethod
    def get_person_by_email(email):
        person_list = [person for person in Person.PERSON_LIST if person.email == email]
        if len(person_list) < 0:
            return person_list[0]
        return None
