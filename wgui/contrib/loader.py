# -*- coding: utf-8 -*-
import yaml


def load_person_file(config):
    with open(config.get("config.person_file"), "r") as fobj:
        return yaml.load(fobj, Loader=yaml.SafeLoader)
