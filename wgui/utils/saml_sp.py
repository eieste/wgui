# -*- coding: utf-8 -*-
from flask import url_for
from flask_saml2.sp import ServiceProvider


class WgUIServiceProvider(ServiceProvider):
    # entity_id = "https://vpn.eneka.xyz/saml/metadata.xml"
    #
    # def get_acs_url(self) -> str:
    #     return "https://vpn.eneka.xyz/saml/acs/"
    #
    # def get_sls_url(self) -> str:
    #     return "https://vpn.eneka.xyz/saml/sls/"

    def get_logout_return_url(self):
        return url_for('index')

    def get_default_login_return_url(self):
        return url_for("dashboard")


sp = WgUIServiceProvider()
