# -*- coding: utf-8 -*-
import re

from wgui.exceptions import ValidationError


def validate_email():
    email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    def wrapper(value):
        if re.fullmatch(email_regex, value):
            return True
        raise ValidationError("Given value isnt an valid E-Mail")

    return wrapper
