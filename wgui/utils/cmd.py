# -*- coding: utf-8 -*-

from datetime import datetime
import logging
import subprocess
from typing import NamedTuple, Optional, Tuple

from wgui.http.flask import cache

log = logging.getLogger(__name__)


class RemotePeer(NamedTuple):
    device: str
    public_key: str
    remote_addr: Optional[str]
    allowed_ips: Tuple[str]
    latest_handshake: Optional[datetime]
    transfer_rx: int
    transfer_tx: int

    @classmethod
    def parse(cls, *columns):
        """ Parse a RemotePeer from a `wg show all dump` line. """
        dev, pub, _, remote_addr, ip_list, handshake_ts, bytes_rx, bytes_tx, _ = columns
        return cls(
            device=dev,
            public_key=pub,
            remote_addr=remote_addr if remote_addr != "(none)" else None,
            allowed_ips=ip_list.split(","),
            latest_handshake=int(handshake_ts) if handshake_ts != "0" else None,
            transfer_rx=int(bytes_rx),
            transfer_tx=int(bytes_tx),
        )


@cache.cached(timeout=50)
def get_peer_states():
    """ Get the state of all remote peers from Wireguard. """
    wg_out = subprocess.check_output(["wg", "show", "all", "dump"]).decode("utf8")
    rows = [l.split("\t") for l in wg_out.split("\n")]
    return [RemotePeer.parse(*row) for row in rows if len(row) > 5]


def apply_to_wireguard(peer_file, config):
    # wg syncconf ${WGNET} <(wg-quick strip ${WGNET})
    interface = config.get("config.wireguard.interface")
    output = subprocess.check_output(f"wg addconf {interface} {peer_file}", shell=True).decode("utf-8").strip()
    log.debug(output)
