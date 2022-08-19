#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Ensure the internal server executes its operations successfully."""


import pytest

from stepseries import commands, exceptions, server, step400


@pytest.mark.order(-1)
class TestServerOperation:

    def test_shutdown(self) -> None:
        server.DEFAULT_SERVER.shutdown()
        assert len(server.DEFAULT_SERVER._bound_devices) == 0

    def test_send_errors(self) -> None:
        with pytest.raises(exceptions.ClientClosedError):
            device = step400.STEP400(0)
            server.DEFAULT_SERVER.remove_device(device)
            device.get(commands.GetVersion())
