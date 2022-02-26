# -*- coding: utf-8 -*-
import functools
import logging
import warnings

from flask import abort, current_app

from wgui.contrib.validators import validate_email
from wgui.saml.saml import sp
from wgui.utils.person import get_person

log = logging.getLogger(__name__)


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__), category=DeprecationWarning, stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)

    return new_func


def login_required(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        config = current_app.config["wgui"]
        try:
            sp.login_required()
            auth_data = sp.get_auth_data_in_session()
            log.debug(f"Auth-Data: {auth_data} ")
            validate_email()(auth_data.attributes.get("email"))
        except Exception as e:
            log.exception(e)
            abort(403, description="Resource not found")
        else:
            person = get_person(config, auth_data.attributes.get("email"))
            return func(*args, person=person, **kwargs)

    return wrapper
