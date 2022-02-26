# -*- coding: utf-8 -*-


class Client:

    def __init__(self, person, device_name, filename, ip_address, public_key, private_key):
        self.person = person
        self.device_name = device_name
        self.public_key = public_key
        self.private_key = private_key
        self.filename = filename
        self.ip_address = ip_address

    @staticmethod
    def load(person, data):
        return Client(
            person=person,
            device_name=data.get("device_name"),
            filename=data.get("filename"),
            ip_address=data.get("ip_address"),
            public_key=data.get("public_key"),
            private_key=data.get("private_key"))
