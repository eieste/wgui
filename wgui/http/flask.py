# -*- coding: utf-8 -*-
from flask import Flask
from flask_caching import Cache
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__, static_folder="../static", template_folder="../templates")
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)
