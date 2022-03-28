=============
Configuration
=============

.. contents::
   :depth: 2

Example
=======


Content of /etc/wgui/wgui.yml

.. parsed-literal::

   config:
     :ref:`client_template<admin/config:config.client_template>`: string
     :ref:`peer_template<admin/config:config.peer_template>`: string
     :ref:`client_folder<admin/config:config.client_folder>`: string
     :ref:`peer_folder<admin/config:config.peer_folder>`: string
     :ref:`person_file<admin/config:config.person_file>`: string
     :ref:`allow_signup<admin/config:config.allow_signup>`: string
     :ref:`secret_key<admin/config:config.secret_key>`: string
     :ref:`app_url<admin/config:config.app_url>`: string
     wireguard:
       :ref:`interface<admin/config:config.wireguard.interface>`: string
       :ref:`public_key<admin/config:config.wireguard.public_key>`: string
       :ref:`ip_range<admin/config:config.wireguard.ip_range>`: string
       :ref:`endpoint<admin/config:config.wireguard.endpoint>`: string
       :ref:`reserved_ip<admin/config:config.wireguard.reserved_ip>`:
         - string
     saml:
       :ref:`saml_key<admin/config:config.saml.saml_key>`: string
       :ref:`saml_crt<admin/config:config.saml.saml_crt>`: string
       id_providers:
         - :ref:`provider<admin/config:provider>`



config.client_template
~~~~~~~~~~~~~~~~~~~~~~
+--------------------+---------------------------------------------------------+
| **Datatype**       | string                                                  |
+--------------------+---------------------------------------------------------+
| **Type**           | Path (to File)                                          |
+--------------------+---------------------------------------------------------+
| **Default**        | /etc/wgui/client.tpl                                    |
+--------------------+---------------------------------------------------------+
| **Path**           | config.client_template                                  |
+--------------------+---------------------------------------------------------+


**Description:**

Path to the Wireguard :ref:`admin/template:Client Template`.
The client template is then fed with :ref:`admin/template-ctx:Template Context` and rendered.
The rendered Template file will be stored under :ref:`admin/config:config.client_folder`.
This configuration is then added to the user in Wireguard.


config.peer_template
~~~~~~~~~~~~~~~~~~~~
+--------------------+---------------------------------------------------------+
| **Datatype**       | string                                                  |
+--------------------+---------------------------------------------------------+
| **Type**           | Path (to File)                                          |
+--------------------+---------------------------------------------------------+
| **Default**        | /etc/wgui/peer.tpl                                      |
+--------------------+---------------------------------------------------------+
| **Path**           | config.peer_template                                    |
+--------------------+---------------------------------------------------------+


**Description:**

Path to the Wireguard :ref:`admin/template:Peer Template`.
The peer template is then fed with :ref:`admin/template-ctx:Template Context` and rendered.
The rendered Template file will be stored under :ref:`admin/config:config.peer_folder`.
This configuration is then added to the Wireguard server and defines the connection with :ref:`admin/config:config.client_template`

config.client_folder
~~~~~~~~~~~~~~~~~~~~
+--------------------+---------------------------------------------------------+
| **Datatype**       | string                                                  |
+--------------------+---------------------------------------------------------+
| **Type**           | Path (to Folder)                                        |
+--------------------+---------------------------------------------------------+
| **Default**        | /etc/wireguard/clients                                  |
+--------------------+---------------------------------------------------------+
| **Path**           | config.client_folder                                    |
+--------------------+---------------------------------------------------------+


**Description:**

The generated :ref:`admin/config:config.client_template` Configurations will be stored here.
Each Configuration has its own generated :ref:`admin/template-ctx:filename`

config.peer_folder
~~~~~~~~~~~~~~~~~~
+--------------------+---------------------------------------------------------+
| **Datatype**       | string                                                  |
+--------------------+---------------------------------------------------------+
| **Type**           | Path (to Folder)                                        |
+--------------------+---------------------------------------------------------+
| **Default**        | /etc/wireguard/peers                                    |
+--------------------+---------------------------------------------------------+
| **Path**           | config.peer_folder                                      |
+--------------------+---------------------------------------------------------+

**Description:**

The generated :ref:`admin/config:config.peer_folder` Configurations will be stored here.
Each Configuration has its own generated :ref:`admin/template-ctx:filename`


config.person_file
~~~~~~~~~~~~~~~~~~
+--------------------+---------------------------------------------------------+
| **Datatype**       | string                                                  |
+--------------------+---------------------------------------------------------+
| **Type**           | Path (to File)                                          |
+--------------------+---------------------------------------------------------+
| **Default**        | /etc/wgui/person.yml                                    |
+--------------------+---------------------------------------------------------+
| **Path**           | config.person_file                                      |
+--------------------+---------------------------------------------------------+

**Description:**

All users and their devices are stored in the :ref:`admin/person:Person File`.

If :ref:`admin/config:config.allow_signup` in config.yml is set to false then entries with the allowed E-Mail addresses must be created here.
The authentication is still done via an external SAML service.

config.allow_signup
~~~~~~~~~~~~~~~~~~~
+--------------------+---------------------------------------------------------+
| **Datatype**       | boolean                                                 |
+--------------------+---------------------------------------------------------+
| **Default**        | false                                                   |
+--------------------+---------------------------------------------------------+
| **Path**           | config.allow_signup                                     |
+--------------------+---------------------------------------------------------+

**Description:**

This flag prevents automatic creation of new users after successful SAML authentication.
If this flag is false, an entry must be created in the :ref:`admin/person:Person File` file for each allowed user.

As an example:

.. code-block:: yaml
   :caption: :ref:`person.yml<admin/person:Person File>`

   person:
     - email: user@example.com
     - email: anotheruser@example.com



config.secret_key
~~~~~~~~~~~~~~~~~

.. note::
   This is an required value

+--------------------+---------------------------------------------------------+
| **Datatype**       | string                                                  |
+--------------------+---------------------------------------------------------+
| **Path**           | config.secret_key                                       |
+--------------------+---------------------------------------------------------+
| **Reference**      | Flask :external+flask:py:data:`SECRET_KEY`              |
+--------------------+---------------------------------------------------------+

**Description:**

A random string used for hashing in Flask

config.app_url
~~~~~~~~~~~~~~

.. note::
   This is an required value


+--------------------+---------------------------------------------------------+
| **Datatype**       | string                                                  |
+--------------------+---------------------------------------------------------+
| **Path**           | config.app_url                                          |
+--------------------+---------------------------------------------------------+

**Description:**

Url under which the application can be reached

config.wireguard
================

Describes the subscrtion wireguard at config file

config.wireguard.interface
~~~~~~~~~~~~~~~~~~~~~~~~~~
+-----------------------+------------------------------------------------------+
| **Datatype**          | string                                               |
+-----------------------+------------------------------------------------------+
| **Path**              | config.wireguard.interface                           |
+-----------------------+------------------------------------------------------+
| **Most Common Value** | wg0                                                  |
+-----------------------+------------------------------------------------------+

**Description:**

The interface name of the wireguard connection.
Normally the interface is named like the wireguard configuration file.
In most common setups the following file exists in the Wireguard setup: ``/etc/wireguard/wg0.conf``
This means that the wireguard interface is called ``wg0``

config.wireguard.public_key
~~~~~~~~~~~~~~~~~~~~~~~~~~~
+-----------------------+------------------------------------------------------+
| **Datatype**          | string                                               |
+-----------------------+------------------------------------------------------+
| **Path**              | config.wireguard.public_key                          |
+-----------------------+------------------------------------------------------+

**Description:**

This is generated together with a private key within the Wireguard setup.
In most cases this is done with the following command:

.. code-block:: bash

   wg genkey | tee privatekey | wg pubkey > publickey


config.wireguard.ip_range
~~~~~~~~~~~~~~~~~~~~~~~~~
+-----------------------+------------------------------------------------------+
| **Datatype**          | string                                               |
+-----------------------+------------------------------------------------------+
| **Type**              | IP-Network                                           |
+-----------------------+------------------------------------------------------+
| **Path**              | config.wireguard.ip_range                            |
+-----------------------+------------------------------------------------------+

**Description:**

Defines which IP-Netowrk (IPv4) is available for Peer IP Addresses.
Define a IPv4 Network in CIDR Annotation like ``192.168.0.0/24``


config.wireguard.endpoint
~~~~~~~~~~~~~~~~~~~~~~~~~
+-----------------------+------------------------------------------------------+
| **Datatype**          | string                                               |
+-----------------------+------------------------------------------------------+
| **Type**              | Domain with Port                                     |
+-----------------------+------------------------------------------------------+
| **Path**              | config.wireguard.endpoint                            |
+-----------------------+------------------------------------------------------+

**Description:**

Contains the address or the name of the Wireguard VPN server.
The address must include the port of the wireguard setup.
Example Value: ``vpn.example.com:51820``

config.wireguard.reserved_ip
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
+-----------------------+------------------------------------------------------+
| **Datatype**          | list                                                 |
+-----------------------+------------------------------------------------------+
| **Type**              | list with string items                               |
+-----------------------+------------------------------------------------------+
| **Path**              | config.wireguard.reserved_ip                         |
+-----------------------+------------------------------------------------------+


**Description:**

It is possible to define here which IP addresses should be excluded from the automatic allocation.
It is recommended to exclude about 5-10 addresses from the automatic allocation to allow the later addition of sites or "static" servers.

**Example usecase:**

Wireguard uses subnet 192.168.0.0/22. The Public Available server has IP 192.168.0.1 and a second Server at Organization Site has 192.168.0.2
Both IP Addresses has been created without wgui and both IP-Adresses has no User-Binding.
Now you should define

.. code-block:: yaml

   config:
     wireguard:
       reserved_ips:
         - 192.168.0.1
         - 192.168.0.2g
       ...


config.saml
================

Describes the subscrtion saml at config file


config.saml.saml_key
~~~~~~~~~~~~~~~~~~~~

config.saml.saml_crt
~~~~~~~~~~~~~~~~~~~~

config.saml.id_providers
~~~~~~~~~~~~~~~~~~~~~~~~~



provider
========

.. parsed-literal::

   :ref:`display_name<admin/config:provider.display_name>`: string
   :ref:`button_style<admin/config:provider.button_style>`: string
   :ref:`slug<admin/config:provider.slug>`: string
   :ref:`entity_id<admin/config:provider.entity_id>`: string
   :ref:`sso_url<admin/config:provider.sso_url>`: string
   :ref:`slo_url<admin/config:provider.slo_url>`: string
   :ref:`certificate_path<admin/config:provider.certificate_path>`: string

provider.display_name
~~~~~~~~~~~~~~~~~~~~~

provider.button_style
~~~~~~~~~~~~~~~~~~~~~

provider.slug
~~~~~~~~~~~~~~~~~~

provider.entity_id
~~~~~~~~~~~~~~~~~~

provider.sso_url
~~~~~~~~~~~~~~~~

provider.slo_url
~~~~~~~~~~~~~~~~

provider.certificate_path
~~~~~~~~~~~~~~~~~~~~~~~~~

