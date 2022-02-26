# -*- coding: utf-8 -*-
import yaml


def load_person_file(config):
    with open(config.person_file, "r") as fobj:
        return yaml.load(fobj)


def get_person(config, email):
    person_data = load_person_file(config)

    for person in person_data.get("persons"):
        if person.get("email") == email:
            return person
