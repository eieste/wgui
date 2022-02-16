# -*- coding: utf-8 -*-
from wgui.mixins.config import ConfigMixin
from wgui.mixins.wireguard import WireguardConfigMixin


class TunnelClient(ConfigMixin, WireguardConfigMixin):
    pass
