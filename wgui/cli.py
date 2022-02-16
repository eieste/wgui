# -*- coding: utf-8 -*-
import argparse
import logging
from pathlib import Path
import re
import sys

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

import wgui
from wgui.conf.config import Configuration
from wgui.conf.initializer import ConfigurationInitializer
from wgui.utils.saml import apply_saml
from wgui.utils.tunnel import Tunnel
from wgui.utils.web import apply_routes

log = logging.getLogger(__name__)


class Validator(object):

    def __init__(self, pattern):
        self._pattern = re.compile(pattern)

    def __call__(self, value):
        if not self._pattern.match(value):
            raise argparse.ArgumentTypeError("Argument has to match '{}'".format(self._pattern.pattern))
        return value


class WgUiCommand:

    def __init__(self, parser=None):
        """
            Initialize an Arg-Parser and apply automaticly arguments
        """
        self._parser = parser or argparse.ArgumentParser()
        self._add_arguments(self._parser)

    def _add_arguments(self, parser):
        """
            Parser add Arguments
        """
        parser.add_argument("-c", "--config", type=Path, help="File get_config path")
        parser.add_argument("-d", "--debug", action="store_true", help="Enable Debug mode")
        parser.add_argument("-v", "--version", action="store_true", help="Display Version")
        parser.add_argument("-i", "--initialize", action="store_true", help="Default Configuration initialize")

        submod = parser.add_subparsers(title="subcommands", dest="cmd")
        tunnel_parser = submod.add_parser("tunnel-create")
        tunnel_parser.add_argument("--email", type=Validator(r"^[^@]+@[^@]+\.[^@]+$"), required=True)
        tunnel_parser.add_argument("--device", type=Validator(r"^[a-z0-9]+(?:-[a-z0-9]+)*$"), required=True)

        server_parser = submod.add_parser("server")
        server_parser.add_argument("--start", action="store_true", required=False)
        server_parser.add_argument("--host", type=str, default="0.0.0.0", required=False)
        server_parser.add_argument("--port", type=int, default=80, required=False)

    def get_parser(self):
        """
            Get initialized Parser from current object instance
        """
        return self._parser

    def parse(self, *args, **kwargs):
        """
            Start resolving arguments of cli
        """
        options = self._parser.parse_args(*args, **kwargs)
        return options

    def handle(self, parser, options):

        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)

        if options.version is True:
            print("wgui: {}".format(wgui.__version__))
            sys.exit(0)

        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)

        if options.debug is True:
            logging.basicConfig(level=logging.DEBUG)
            logging.debug("Enable Debug-Mode")
            logging.debug("Input Options {}".format(options.__dict__))

        if options.config is None:
            raise ValueError("--config is required")

        if options.initialize is True:
            ConfigurationInitializer(parser, options)
            log.info("Exit")
            sys.exit(0)

        self.start(parser, options)

    def start(self, parser, options):
        config = Configuration(options)

        if options.cmd == "tunnel-create":
            t = Tunnel(config)
            t.create(email=options.email, device=options.device)
            # t.create(email=options)

        if options.cmd == "server":
            app = Flask(__name__)
            app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)
            app.config["SECRET_KEY"] = config.get("config.secret_key")
            app.config["APP_URL"] = config.get("config.app_url")
            apply_saml(config, app)
            apply_routes(config, app)
            app.run(
                debug=options.debug,
                host=options.host,
                port=options.port,
            )


def main():
    parser = WgUiCommand()
    options = parser.parse()
    parser.handle(parser.get_parser(), options)


if __name__ == "__main__":
    main()
