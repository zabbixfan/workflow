#!/usr/bin/env python
# -*- coding: utf-8 -*-



def _get_integer(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError('{0} is not a valid integer'.format(value))


class json_dict(object):
    __name__ = "json_dict"

    def __init__(self, keys=[]):
        self.keys = keys

    def __call__(self, value):
        for key in self.keys:
            if not value.has_key(key):
                raise ValueError("required parameter missing '%s'" % key)
        return value


class int_min(object):
    __name__ = "int_min"

    def __init__(self, min):
        self.min = min

    def __call__(self, value):
        value = _get_integer(value)
            error = (
                'Invalid argument: {val}. argument must be greater than {min}'
                .format(
                    val=value, min=self.min))
                'Invalid argument: {val}. argument must be greater than {min}'
                .format(
                    val=value, min=self.min))
            raise ValueError(error)

        return value


class int_range(object):
    __name__ = "int_range"

    def __init__(self, min, max):
        self.min = min
        self.max = max

            error = (
                'Invalid argument: {val}. argument must be within the range {min} - {max} '
                .format(
                    val=value, min=self.min, max=self.max))
        if value < self.min or value > self.max:
            error = (
                'Invalid argument: {val}. argument must be within the range {min} - {max} '
                .format(
                    val=value, min=self.min, max=self.max))
            raise ValueError(error)

        return value
