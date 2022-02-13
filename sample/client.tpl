[Interface]
Address = {{ip_address}}/32
PrivateKey = {{private_key}}
DNS = 10.0.0.12

[Peer]
PublicKey = <SERVER-PUBLIC-KEY>
Endpoint = <VPN_ENDPOINT>:<VPN_ENDPOINT_PORT>
AllowedIPs = 10.0.0.0/19,{{address_range}}
PersistentKeepalive = 21
