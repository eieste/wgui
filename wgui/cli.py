# -*- coding: utf-8 -*-
import argparse
import logging
from pathlib import Path
import re
import sys

import wgui
from wgui.conf.config import Configuration
from wgui.utils.tunnel import Tunnel

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
        parser.add_argument("-c", "--config", type=Path, required=True, help="File config path")
        parser.add_argument("-r", "--run", action="store_true", help="Start Webserver")
        parser.add_argument("-d", "--debug", action="store_true", help="Enable Debug mode")
        parser.add_argument("-v", "--version", action="store_true", help="Display Version")

        submod = parser.add_subparsers(title="subcommands", dest="cmd")
        tunnel_parser = submod.add_parser("create")
        tunnel_parser.add_argument("--email", type=Validator(r"^[^@]+@[^@]+\.[^@]+$"), required=True)
        tunnel_parser.add_argument("--device", type=Validator(r"^[a-z0-9]+(?:-[a-z0-9]+)*$"), required=True)

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

        self.start(parser, options)

    def start(self, parser, options):
        config = Configuration(options)

        if options.cmd == "create":
            t = Tunnel(config)
            t.create(email=options.email, device=options.device)
            # t.create(email=options)


def main():
    parser = WgUiCommand()
    options = parser.parse()
    parser.handle(parser.get_parser(), options)


if __name__ == "__main__":
    main()
