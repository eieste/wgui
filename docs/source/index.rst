.. wgui documentation master file, created by
sphinx-quickstart on Sat Feb 12 19:40:31 2022.
You can adapt this file completely to your liking, but it should at least
contain the root `toctree` directive.

Welcome to wgui's documentation!
================================
wgui is an simple to use interface for Wireguard Servers.
wgui allows users to create Wireguard tunnel clients on their own.
Users are authenticated via SAML.
Users can easily download the complete configuration file

Example for usage:
An organization or group that manages members via auth0, okta, google, microsoft etc. and wants to give certain groups access to a wireguard VPN. The members should do this themselves to minimize the effort for IT.

---------
Features:
---------

 - Login via SAML
 - Multiple SAML Provider Support
 - Uses simple YAML files as "database"
 - Has an CLI interface
 - Simple Configuration-File Download
 - Determines a free IP by itself
 - Templates for peer and client configuration
 - no intervention in wireguard itself
   - it does only what defined by user in peer/client templates
   - no magic ( it uses simple wireguard owned commands )
  - fully automated peer generation ( including private key )


---------------------
What wgui does not do
---------------------


 - It does not provide a wireguard setup
 - no iptables, routing magic

----
ToDo
----

 - Allow Configuration with local create private/public keypair


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   ./developer/index
   ./admin/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
