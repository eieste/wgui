# -*- coding: utf-8 -*-

import io
import os

from flask import flash, redirect, render_template, request, url_for
import qrcode
import qrcode.image.svg

from wgui.utils.forms import CreateDeviceForm
from wgui.utils.saml import sp
from wgui.utils.tunnel import Tunnel


def apply_routes(config, app):

    @app.route("/tunnel/detail/<filename>", methods=["GET"])
    def tunnel_detail(filename):
        context = {}
        try:
            auth_data = sp.get_auth_data_in_session()
        except:
            return redirect(url_for("index"))

        for client in config.configuration.get("clients"):
            if client.get("email") == auth_data.nameid:
                if client.get("filename") == filename:
                    context["client"] = client

        client_dir = config.get_path_config(config.get_config("client_folder"))
        peer_dir = config.get_path_config(config.get_config("peer_folder"))

        with open(os.path.join(client_dir, "{}.conf".format(filename))) as fobj:
            context["client_config"] = fobj.read()

        with open(os.path.join(peer_dir, "{}.conf".format(filename))) as fobj:
            context["peer_config"] = fobj.read()

        img = qrcode.make(context["client_config"], image_factory=qrcode.image.svg.SvgImage)
        stream = io.BytesIO()
        img.save(stream)
        stream.seek(0)
        context["qrcode"] = stream.getvalue().decode()
        return render_template('pages/tunnel/detail.jinja2', **context)

    @app.route("/tunnel/create", methods=["GET", "POST"])
    def tunnel_create():
        try:
            auth_data = sp.get_auth_data_in_session()
        except:
            return redirect(url_for("index"))
        form = CreateDeviceForm(request.form)
        if request.method == 'POST' and form.validate():
            tun = Tunnel(config)
            client = tun.create(email=auth_data.nameid, device=form.device.data)
            flash('New device created')
            return redirect(url_for('tunnel_detail', filename=client.get("filename")))
        return render_template('pages/tunnel/new.jinja2', form=form)

    @app.route("/dashboard")
    def dashboard():
        try:
            auth_data = sp.get_auth_data_in_session()
            sp.is_user_logged_in()
        except:
            return redirect(url_for("index"))
        return render_template("pages/dashboard/index.jinja2", clients=config.get_clients_by_user(auth_data.nameid))

    @app.route("/", methods=["GET"])
    def index():
        handler = sp.get_default_idp_handler()
        login_next = sp.get_login_return_url()
        if handler:
            return redirect(
                url_for('flask_saml2_sp.login_idp', entity_id=handler.entity_id, next=login_next,
                        _external=True))  # _scheme=sp.get_scheme(),
        return sp.render_template('pages/login/index.jinja2', login_next=login_next, handlers=sp.get_idp_handlers())
