# WGUI

A config generator for Wireguard

## Configuration

Create a folder eg. `/etc/wgui/` and create Certificats for SAML usage and a configuration file

### Generate SAML Certificats

```
openssl req -x509 -newkey rsa:4096 -keyout saml.key -out saml.crt -sha256 -days 365
```

### wgui.yml

```yaml
config:
  range: 172.16.246.0/12
  client_template: /etc/wgui/client.tpl
  peer_template: ./sample/peer.tpl
  client_folder: /etc/wireguard/clients
  peer_folder: /etc/wireguard/peers
  saml_crt: /etc/wgui/saml.crt
  saml_key: /etc/wgui/saml.key
  idp_meta_url: ""
  secret_key: "c346e4fa76925518349d3489a471994d"

clients:




```
