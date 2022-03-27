=============
Configuration
=============

.. contents::
   :depth: 2

Example
=======

.. code-block:: yaml

   config:
     admin/config:client_template: string
     peer_template: string
     client_folder: string
     peer_folder: string
     person_file: string
     allow_signup: string
     secret_key: string
     app_url: string
     wireguard:
       interface: string
       public_key: string
       ip_range: string
       endpoint: string
       reserved_ip:
         - string
       saml:
         saml_key: string
         saml_crt: string
         id_providers:
           - display_name: string
             button_style: string
             slug: string
             entity_id: string
             sso_url: string
             slo_url: string
             certificate_path: string


config.client_template
======================
+--------------------+---------------------------------------------------------+
| **Datatype**       | string                                                  |
+--------------------+---------------------------------------------------------+
| **Type**           | Path                                                    |
+--------------------+---------------------------------------------------------+
| **Default**        | /etc/wgui/config.tpl                                    |
+--------------------+---------------------------------------------------------+
| **Path**           | config.client_template                                  |
+--------------------+---------------------------------------------------------+
**Description:**

Defines


config.peer_template
====================

config.client_folder
====================

config.peer_folder
==================

config.person_file
==================

config.allow_signup
===================

config.secret_key
=================

config.app_url
==============

config.allow_signup
===================

config.wireguard.interface
==========================

config.wireguard.public_key
===========================

config.wireguard.ip_range
=========================

config.wireguard.endpoint
=========================

config.wireguard.reserved_ip
============================

config.wireguard.saml.saml_key
==============================

config.wireguard.saml.saml_key
==============================

config.wireguard.saml.saml_crt
==============================

config.wireguard.saml.id_providers
==================================
