#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Ensure get/set actions execute or raise errors as expected."""


import pytest

from stepseries import commands, exceptions, responses, server, step800


def test_get_errors(device: step800.STEP800, monkeypatch) -> None:
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


@pytest.mark.skip_800_disconnected
def test_get_multiple_responses(device: step800.STEP800) -> None:
    resp = device.get(commands.GetMicrostepMode(255))
    assert isinstance(resp, list)
    assert len(resp) == 8
    assert isinstance(resp[0], responses.MicrostepMode)
    assert isinstance(resp[1], responses.MicrostepMode)
    assert isinstance(resp[2], responses.MicrostepMode)
    assert isinstance(resp[3], responses.MicrostepMode)
    assert isinstance(resp[4], responses.MicrostepMode)
    assert isinstance(resp[5], responses.MicrostepMode)
    assert isinstance(resp[6], responses.MicrostepMode)
    assert isinstance(resp[7], responses.MicrostepMode)
