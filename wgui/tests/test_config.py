# -*- coding: utf-8 -*-
import argparse

from wgui.conf.config import Configuration


def test_configuration_get(monkeypatch, mocker):
    sample_config = {"key": "value", "subobj": {"a": "b", "subsubobj": {"c": "d"}}}
    monkeypatch.setattr(Configuration, "validate", lambda x: True)
    monkeypatch.setattr(Configuration, "load_config", lambda x: sample_config)
    conf = Configuration(argparse.Namespace(config={"saml_key": "foo"}))

    assert conf.get("key") == "value"
    assert conf.get("subobj.a") == "b"
    assert conf.get("subobj.subsubobj.c") == "d"


def test_configuration_get_default(monkeypatch, mocker):
    sample_config = {"config": {"peer_folder": "asdf"}}
    monkeypatch.setattr(Configuration, "validate", lambda x: True)
    monkeypatch.setattr(Configuration, "load_config", lambda x: sample_config)
    conf = Configuration(argparse.Namespace(config={"saml_key": "foo"}))

    assert conf.get("config.peer_folder") == "asdf"
    assert conf.get("config.client_folder") == "/etc/wireguard/clients"
