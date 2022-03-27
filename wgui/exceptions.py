# -*- coding: utf-8 -*-
class ConfigurationError(ValueError):
    pass


class AlreadyExists(ValueError):
    pass


class DeviceAlreadyExists(AlreadyExists):
    pass


class PersonAlreadyExists(AlreadyExists):
    pass


class ValidationError(ValueError):
    pass
