# -*- coding: utf-8 -*-
import re

from wgui.exceptions import ValidationError


def validate_email():
    email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    def wrapper(value):
        if re.fullmatch(email_regex, value):
            return email_regex
        raise ValidationError("Given value isnt an valid E-Mail")

    return wrapper
