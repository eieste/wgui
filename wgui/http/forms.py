# -*- coding: utf-8 -*-
from wtforms import Form, StringField, validators


class CreateDeviceForm(Form):
    device = StringField("Device", [validators.Length(min=4, max=25)])
