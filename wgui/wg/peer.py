# -*- coding: utf-8 -*-
import os
import subprocess

from wgui.mixins.config import ConfigMixin
from wgui.mixins.wireguard import WireguardConfigMixin


class TunnelPeer(ConfigMixin, WireguardConfigMixin):

    def __init__(self, *args, person=None, config=None, filename=None, **kwargs):
        self.person = person
        self.config = config
        self.filename = filename
        super().__init__(*args, **kwargs)

    def apply_config(self):
        peer_file = os.path.join(self.config.get("config.peer_folder", mod="get_relative_path"), "{}.conf".format(self.filename))
        subprocess.check_output(f"wg addconf wg0 {peer_file}; wg syncconf wg0 <(wq-quick strip wg0)", shell=True).decode("utf-8").strip()

    def create_peer_config(self):
        pass
