# -*- coding: utf-8 -*-
from datetime import datetime

from flask import flash, redirect, url_for

import wgui


def apply_essential(config, app):

    @app.context_processor
    def inject_version():
        return {"version": wgui.__version__}

    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    @app.errorhandler(403)
    def page_forbidden(error):
        flash("You have performed a prohibited action and have therefore been logged off ")
        return redirect(url_for("index"))
