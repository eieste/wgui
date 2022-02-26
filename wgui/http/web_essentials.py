# -*- coding: utf-8 -*-
from datetime import datetime

from flask import g

import wgui
from wgui.conf.config import Configuration
from wgui.wireguard.person import Person


def apply_essential(config, app):

    @app.before_request
    def load_user():
        Configuration.validate(config._options.config)
        g.config = Configuration.load_config(config._options.config)
        g.person_list = Person.load(config)

    @app.context_processor
    def inject_version():
        return {"version": wgui.__version__}

    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}
