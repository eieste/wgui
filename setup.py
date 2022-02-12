# -*- coding: utf-8 -*-
import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="wgui",
    version="0.0.1",
    author="Stefan Eiermann",
    author_email="foss@ultraapp.de",
    description=("Simple WG UI"),
    license="AGPL",
    keywords="wireguard ui flask",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["jsonschema==4.4.0", "pyyaml==6.0"],
    package_data={'': ['conf/wgui.schema.json']},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console"
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    entry_points={'console_scripts': ['wgui = wgui.main:main']},
)
