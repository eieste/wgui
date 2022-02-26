# -*- coding: utf-8 -*-
from datetime import datetime

import wgui


def apply_essential(config, app):

    @app.context_processor
    def inject_version():
        return {"version": wgui.__version__}

    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}
