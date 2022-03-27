# -*- coding: utf-8 -*-

import os

from flask import (
    abort,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
import qrcode
import qrcode.image.svg

from wgui.contrib.decorators import login_required
from wgui.http.forms import CreateDeviceForm
from wgui.saml.saml import sp
from wgui.utils.cmd import get_peer_states


def apply_routes(config, app):

    @app.route("/tunnel/delete/<filename>", methods=["GET", "POST"])
    @login_required
    def tunnel_delete(filename, person=None):
        if person is None:
            raise RuntimeError("Impossible error")
        context = {}
        client = person.get_client_by_filename(filename)
        context["person"] = person
        context["client"] = client
        if request.method == 'POST':
            client = person.get_client_by_filename(filename)
            client.delete()
            flash("Device successfully deleted")
            return redirect(url_for("dashboard"))

        return render_template("pages/tunnel/delete.jinja2", **context)

    @app.route("/tunnel/download/<filename>", methods=["GET"])
    @login_required
    def tunnel_download(filename, person=None):
        if person is None:
            raise RuntimeError("Impossible error")
        context = {}
        client = person.get_client_by_filename(filename)
        if not client:
            raise abort(403, description="Insufficient Permission")
        client_file = os.path.join(config.get("config.client_folder", mod="get_relative_path"), "{}.conf".format(filename))
        return send_file(client_file, as_attachment=True)

    @app.route("/tunnel/detail/<filename>", methods=["GET"])
    @login_required
    def tunnel_detail(filename, person=None):
        if person is None:
            raise RuntimeError("Impossible error")
        context = {}
        client = person.get_client_by_filename(filename)

        context["person"] = person
        context["client"] = client

        with open(os.path.join(config.get("config.client_folder", mod="get_relative_path"), "{}.conf".format(filename))) as fobj:
            context["client_config"] = fobj.read()

        with open(os.path.join(config.get("config.peer_folder", mod="get_relative_path"), "{}.conf".format(filename))) as fobj:
            context["peer_config"] = fobj.read()

        qr = qrcode.QRCode(image_factory=qrcode.image.svg.SvgImage)
        qr.add_data(context["client_config"])
        qr.make(fit=True)
        img = qr.make_image(svgclass="asdf")
        context["qrcode"] = img.to_string().decode("utf-8")
        return render_template('pages/tunnel/detail.jinja2', **context)

    @app.route("/tunnel/create", methods=["GET", "POST"])
    @login_required
    def tunnel_create(person=None):
        context = {"person": person}
        if person is None:
            raise RuntimeError("Impossible error")
        form = CreateDeviceForm(request.form)
        context["form"] = form
        if request.method == 'POST' and form.validate():
            client = person.create_device(form.device.data)
            return redirect(url_for("tunnel_detail", filename=client.filename))
        return render_template('pages/tunnel/new.jinja2', **context)

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
        request_data = request.json
        if type(dict) is not request_data and len(request_data.items()) != 1:
            raise abort(400, description="Invalid Request Body")
        requested_clients = request_data.get("clients", [])

        if not person.has_clients(*requested_clients):
            return redirect(url_for("logout"))

        peers = get_peer_states()
        clients = {}
        if len(peers) <= 0:
            return {"clients": clients, "max_rx": 0, "max_tx": 0}
        max_values = {"rx": [max(peer.transfer_rx for peer in peers)], "tx": [max(peer.transfer_tx for peer in peers)]}

        for client in person.clients:
            result = [peer for peer in peers if client.public_key == peer.public_key]
            if len(result) == 1 and client.filename in requested_clients:
                remote_peer = result[0]
                clients[client.filename] = remote_peer._asdict()
        return {"clients": clients, "max_rx": max_values["rx"], "max_tx": max_values["tx"]}

    @app.route("/", methods=["GET"])
    def index():
        # handler = sp.get_default_idp_handler()
        login_next = sp.get_login_return_url()
        # if handler:
        #     return redirect(
        #         url_for('flask_saml2_sp.login_idp', entity_id=handler.entity_id, next=login_next,
        #                 _external=True))  # _scheme=sp.get_scheme(),
        return sp.render_template('pages/login/index.jinja2', login_next=login_next, handlers=sp.get_idp_handlers())
