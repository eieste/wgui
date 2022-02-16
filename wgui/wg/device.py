# -*- coding: utf-8 -*-
from wgui.wg.client import TunnelClient
from wgui.wg.peer import TunnelPeer


class PersonDevice:

    def __init__(self, wg_client):
        self.device_name = wg_client.get("device")
        self.peer = TunnelPeer(wg_client)
        self.client = TunnelClient(wg_client)
