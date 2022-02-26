# -*- coding: utf-8 -*-
import subprocess


def get_peer_states():
    """ Get the state of all remote peers from Wireguard. """
    wg_out = subprocess.check_output(["wg", "show", "all", "dump"]).decode("utf8")
    rows = [l.split("\t") for l in wg_out.split("\n")]
    print(rows)
    #  return [RemotePeer.parse(name_map, *row) for row in rows if len(row) > 5]
