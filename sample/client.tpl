[Interface]
Address = {{ip_address}}/32
PrivateKey = {{private_key}}
DNS = 10.0.0.12

[Peer]
PublicKey = {{ wireguard.public_key }}
Endpoint = {{ wireguard.endpoint }}
AllowedIPs = 10.0.0.0/19,{{address_range}}
PersistentKeepalive = 21
