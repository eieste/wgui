# -*- coding: utf-8 -*-
from flask import flash, redirect, url_for

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
            return redirect(url_for("index"))
            message = '<p>You are logged out.</p>'

            login_url = url_for('flask_saml2_sp.login')
            link = f'<p><a href="{login_url}">Log in to continue</a></p>'

            return message + link

    @app.route("/", methods=["GET"])
    def index():
        flash("WooopWooop", "info")
        handler = sp.get_default_idp_handler()
        login_next = sp.get_login_return_url()
        if handler:
            return redirect(url_for('.login_idp', entity_id=handler.entity_id, next=login_next, _scheme=sp.get_scheme(), _external=True))
        return sp.render_template('pages/login/index.jinja2', login_next=login_next, handlers=sp.get_idp_handlers())
