# -*- coding: utf-8 -*-
import logging

from flask import session, url_for
from flask_saml2.sp import ServiceProvider

log = logging.getLogger(__name__)


class WgUIServiceProvider(ServiceProvider):

    def get_logout_return_url(self):
        return url_for('index')

    def get_default_login_return_url(self):
        return url_for("dashboard")

    def login_successful(self, auth_data, redirect_to):
        flask_response = super().login_successful(auth_data, redirect_to)
        session["user"] = auth_data.nameid
        return flask_response


sp = WgUIServiceProvider()
