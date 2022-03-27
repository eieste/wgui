# -*- coding: utf-8 -*-
from wgui.contrib.avatar import get_initial_sign


def test_mail_variants():
    assert get_initial_sign("foo.bar@test.de") == "fb"
    assert get_initial_sign("jan-foo.bar@test.de") == "jb"
    assert get_initial_sign("foo-bar@test.de") == "fb"
    assert get_initial_sign("fbar@test.de") == "fb"
    assert get_initial_sign("foo.1bar@test.de") == "fb"
    assert get_initial_sign("2an-foo.bar@test.de") == "ab"
    assert get_initial_sign("f4o-bar@test.de") == "fb"
    assert get_initial_sign("432fbar@test.de") == "fb"
