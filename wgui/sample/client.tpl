[Interface]
Address = {{ip_address}}/32
PrivateKey = {{private_key}}
DNS = 8.8.8.8

[Peer]
PublicKey = {{ wireguard.public_key }}
Endpoint = {{ wireguard.endpoint }}
AllowedIPs = {{address_range}}
PersistentKeepalive = 21
