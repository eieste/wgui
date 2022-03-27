=============
Configuration
=============

Example
=======

.. code-block:: yaml

   config:
     client_template: string
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
         id_providers: string
           - display_name: string
             button_style: string
             slug: string
             entity_id: string
             sso_url: string
             slo_url: string
             certificate_path: string


config.client_template
======================

Type: string
Default: "/etc/wgui/client.tpl"
Description: