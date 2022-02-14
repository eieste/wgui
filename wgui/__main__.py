# -*- coding: utf-8 -*-

from wgui.cli import WgUiCommand

if __name__ in "__main__":
    parser = WgUiCommand()
    options = parser.parse()
    parser.handle(parser.get_parser(), options)
