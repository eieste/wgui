# -*- coding: utf-8 -*-
import yaml


def load_person_file(config):
    with open(config.get("config.person_file"), "r") as fobj:
        person_data = yaml.load(fobj, Loader=yaml.SafeLoader)
        if person_data is None:
            person_data = {"persons": []}
        return person_data
