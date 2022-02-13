# -*- coding: utf-8 -*-
from flask import render_template, url_for

from wgui.utils.saml import sp


def apply_routes(config, app):

    @app.route("/dashboard")
    def dashboard():

        if sp.is_user_logged_in():
            auth_data = sp.get_auth_data_in_session()

            message = f'''
            <p>You are logged in as <strong>{auth_data.nameid}</strong>.
            The IdP sent back the following attributes:<p>
            '''

            attrs = '<dl>{}</dl>'.format(''.join(f'<dt>{attr}</dt><dd>{value}</dd>' for attr, value in auth_data.attributes.items()))

            logout_url = url_for('flask_saml2_sp.logout')
            logout = f'<form action="{logout_url}" method="POST"><input type="submit" value="Log out"></form>'

            return message + attrs + logout
        else:
            message = '<p>You are logged out.</p>'

            login_url = url_for('flask_saml2_sp.login')
            link = f'<p><a href="{login_url}">Log in to continue</a></p>'

            return message + link

        return "<p>Hello, DASHBOARD World!</p>"

    @app.route("/login")
    def login():
        message = "The Flask Shop"
        return render_template('pages/login/index.jinja2', message=message)
