# -*- coding: utf-8 -*-

import io
import os

from flask import redirect, render_template, request, url_for
import qrcode
import qrcode.image.svg

from wgui.contrib.decorators import login_required
from wgui.http.forms import CreateDeviceForm
from wgui.saml.saml import sp
from wgui.utils.cmd import get_peer_states


def apply_routes(config, app):

    @app.route("/tunnel/detail/<filename>", methods=["GET"])
    @login_required
    def tunnel_detail(filename, person=None):
        if person is None:
            raise RuntimeError("Impossible error")
        context = {}
        client = person.get_client_by_filename(filename)

        context["client"] = client

        with open(os.path.join(config.get("config.client_folder", mod="get_relative_path"), "{}.conf".format(filename))) as fobj:
            context["client_config"] = fobj.read()

        with open(os.path.join(config.get("config.peer_folder", mod="get_relative_path"), "{}.conf".format(filename))) as fobj:
            context["peer_config"] = fobj.read()

        img = qrcode.make(context["client_config"], image_factory=qrcode.image.svg.SvgImage)
        stream = io.BytesIO()
        img.save(stream)
        stream.seek(0)
        context["qrcode"] = stream.getvalue().decode()
        return render_template('pages/tunnel/detail.jinja2', **context)

    @app.route("/tunnel/create", methods=["GET", "POST"])
    @login_required
    def tunnel_create(person=None):
        if person is None:
            raise RuntimeError("Impossible error")
        form = CreateDeviceForm(request.form)
        if request.method == 'POST' and form.validate():
            print("OK")

        return render_template('pages/tunnel/new.jinja2', form=form)

    @app.route("/dashboard")
    @login_required
    def dashboard(person=None):
        if person is None:
            raise RuntimeError("Impossible Error")

        return render_template("pages/dashboard/index.jinja2", person=person)

    @app.route("/logout")
    def logout():
        sp.clear_auth_data_in_session()
        return redirect(url_for("flask_saml2_sp.logout"))

    @app.route("/api/wireguard", methods=["POST"])
    @login_required
    def api_wireguard(person=None):
        if person is None:
            raise RuntimeError("Impossible Error")

        requested_clients = request.json.get("clients")
        if not person.has_clients(*requested_clients):
            return redirect(url_for("logout"))

        peers = get_peer_states()
        clients = {}
        for client in person.clients:
            result = [peer for peer in peers if client.public_key == peer.public_key]
            if len(result) == 1 and client.filename in requested_clients:
                remote_peer = result[0]
                clients[client.filename] = remote_peer._asdict()
        return {"clients": clients}

    @app.route("/", methods=["GET"])
    def index():
        # handler = sp.get_default_idp_handler()
        login_next = sp.get_login_return_url()
        # if handler:
        #     return redirect(
        #         url_for('flask_saml2_sp.login_idp', entity_id=handler.entity_id, next=login_next,
        #                 _external=True))  # _scheme=sp.get_scheme(),
        return sp.render_template('pages/login/index.jinja2', login_next=login_next, handlers=sp.get_idp_handlers())
