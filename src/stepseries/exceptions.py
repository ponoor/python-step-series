#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Custom exceptions raised by this library."""


class ClientNotFound(Exception):
    """The requested client could not be found."""


class ParseError(Exception):
    """Failed to parse the message from the device."""

    response: str
