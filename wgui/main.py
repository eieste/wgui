import argparse
from pathlib import Path
import yaml

class WgUiCommand:


    def __init__(self):
        self._parser = self.get_parser()

    def get_parser(self):
        return argparse.ArgumentParser()

    def add_arguments(self, parser):
        parser.add_argument("-c", type=)
        parser.add_argument(
            "--config",
            type=Path,
            default=Path(__file__).absolute().parent / "wgui.yml",
            help="Path to wgui.yml config yml",
        )

    def handle(self, options):
        pass

    def parse(self):
        options = self._parser.parse_args()
        self.handle(options)