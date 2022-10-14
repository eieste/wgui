============
Install wgui
============

Docker Setup
============

comming Soon



Manual Setup
============

There should be python > 3.8 on the system

.. code-block::

   apt install python3 python3-virtualenv python3-pip

You should have an existing  :ref:`Wireguard Setup <admin/wg-install:Install Wireguard>>`.

For installation you can use pip.
Its nessesary to use an virtual environment

.. code-block:: python

   virtualenv venv/
   source venv/bin/activate
   pip install wgui

Create required Configuration files and Templates
The following Command create configuration and Template at ``/etc/wgui``

.. code-block:: bash

   wgui -i
   (venv) root@vpn:/opt/venv# WGUI_APP_URL=example.com wgui -i
   Wireguard Endpoint domain (with port) [vpn.local:58120]:
   Wireguard Server Public Key [None]:
   IP-Range used for Peers [192.168.0.0/24]:
   Wireguard Interface [wg0]:
   Wireguard Gateway IP:  [192.168.0.1,192.168.0.2,192.168.0.3,192.168.0.4,192.168.0.5]:
   Path Prefix where the wgui configuration should be stored [/etc/wgui/]:

wgui -i has two different modes.
 - interactive. wgui asks for the necessary settings interactively.
 - via environment variables

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

+--------------------+----------------------------------------------------------------+---------------------------------------+
| ENV-Variable       | config-path                                                    | Question                              |
+====================+================================================================+=======================================+
| WGUI_APP_URL       | :ref:`admin/config:config.app_url`                             | URL of used for Webinterface          |
+--------------------+----------------------------------------------------------------+---------------------------------------+
| WGUI_WG_ENDPOINT   | :ref:`admin/config:config.wireguard.endpoint`                  | Wireguard Endpoint domain (with port) |
+--------------------+----------------------------------------------------------------+---------------------------------------+
| WGUI_WG_PUBLIC_KEY | :ref:`admin/config:config.wireguard.public_key`                |Wireguard Server Public Key            |
+--------------------+----------------------------------------------------------------+---------------------------------------+
| WGUI_IP_RANGE      | :ref:`admin/config:config.wireguard.ip_range`                  | IP-Range used for Peers               |
+--------------------+----------------------------------------------------------------+---------------------------------------+
| WGUI_INTERFACE     | :ref:`admin/config:config.wireguard.interface`                 | Wireguard Interface                   |
+--------------------+----------------------------------------------------------------+---------------------------------------+
| WGUI_CONFIG_PREFIX | -/-                                                            | Path Prefix where the wgui config...  |
+--------------------+----------------------------------------------------------------+---------------------------------------+

Setup web-UI
============

Its possible to use wgui only for cli command usage.
But if you like the full experience you should setup the web-ui.
