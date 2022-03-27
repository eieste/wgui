# -*- coding: utf-8 -*-
from wgui.contrib.validators import validate_email


def test_mail_validator_decorator():
    assert validate_email()("foo.bar@test.de") == True
    assert validate_email()("foo.bar-hello@test.de") == True
