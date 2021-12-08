#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Ensure get/set actions execute or raise errors as expected."""


import pytest

from stepseries import commands, exceptions, server, step400


def test_get_errors(device: step400.STEP400, monkeypatch) -> None:
    # Mocked device get to replace server.send
    # and STEP400._handle_incoming_message
    # Always fill the STEP400._get_queue with an errored response
    def mockget(*_) -> None:
        exc = TypeError("this is a dummy error")
        resp = exceptions.ParseError("parsing failed to deconstruct response")
        resp.response = "/dummy 0 1 2 3"
        resp.original_exc = exc

        device._get_queue.put(resp)

    # Application of the monkeypatch to replace server.send and
    # STEP400._handle_incoming_message
    monkeypatch.setattr(server.DEFAULT_SERVER, "send", mockget)

    # Verify the exception returned from the mocked function is raised
    # in device.get
    with pytest.raises(exceptions.ParseError):
        device.get(commands.GetVersion())
