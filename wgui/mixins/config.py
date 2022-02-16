# -*- coding: utf-8 -*-
class ConfigMixin:

    def __init__(self, *args, config=None, **kwargs):
        self.config = config
