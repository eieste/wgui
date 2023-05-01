# -*- coding: utf-8 -*-
import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="wgui",
    version="1.0.0",
    author="Stefan Eiermann",
    author_email="foss@ultraapp.de",
    description=("Simple WG UI"),
    license="AGPL",
    keywords="wireguard ui flask",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "jsonschema==4.4.0", "qrcode==7.3.1", "pyyaml==6.0", "Jinja2==3.0.3", "flask==2.3.2", "Flask-WTF==1.0.0",
        "flask-saml2@git+https://github.com/eieste/flask-saml2.git@0.4.0#egg=flask-saml2", "flask-caching==1.10.1"
    ],
    package_data={
        '':
            [
                'conf/wgui.schema.json', "sample/*", 'templates/*', 'templates/*/*', 'templates/*/*/*', 'static/*', 'static/*/*',
                'static/*/*/*'
            ],
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console"
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: Unix",
    ],
    entry_points={'console_scripts': ['wgui = wgui.main:main']},
)
