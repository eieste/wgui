=======================
Configuration Templates
=======================

Client Template
===============

This template is used to generate a configuration which is loaded on "User".

See also: :ghr:`sample/client.tpl`.

In the template Jinja2 :doc:`jinja2:templates` variables can be used.
What context is available is in this article

This generated file can be downloaded by user and added to Wireguard app

Example
-------

See :ref:`admin/template-ctx:Template Context`

See :doc:`Template Language <jinja2:templates>`

.. code-block:: cfg

   [Interface]
   Address = {{ip_address}}/32
   PrivateKey = {{private_key}}
   DNS = 172.16.246.1

   [Peer]
   PublicKey = {{ wireguard.public_key }}
   Endpoint = {{ wireguard.endpoint }}
   AllowedIPs = 10.0.0.0/19,{{ wireguard.ip_range}}
   PersistentKeepalive = 21





Peer Template
=============

This template is used to generate a configuration which is loaded on "Server" side in Wireguard.
See also: :ghr:`sample/peer.tpl`.
In the template Jinja2 :doc:`jinja2:templates` variables can be used.
What context is available is in this article


wgui generates and autoloads this config into wireguard

Example
-------

See :ref:`admin/template-ctx:Template Context`

See :doc:`Template Language <jinja2:templates>`

.. code-block:: cfg

   [Peer]
   PublicKey = {{public_key}}
   AllowedIPs = {{ip_address}}/32
