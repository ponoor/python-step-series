#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Ensure the internal server executes its operations successfully."""


import pytest

from stepseries import commands, exceptions, server, step400


@pytest.mark.order(-1)
class TestServerOperation:
    def test_add_device(self) -> None:
        device = step400.STEP400(0)
        assert server.DEFAULT_SERVER._bound_devices[-1][0] == device
        assert server.DEFAULT_SERVER._bound_devices[-1][-1] is None

        device2 = step400.STEP400(0, "10.1.21.56")
        assert server.DEFAULT_SERVER._bound_devices[-1][0] == device2
        assert server.DEFAULT_SERVER._bound_devices[-1][-1] is None

        device3 = step400.STEP400(0, server_port=5000)
        assert server.DEFAULT_SERVER._bound_devices[-1][0] == device3
        assert server.DEFAULT_SERVER._bound_devices[-1][-1] is not None

    def test_remove_device(self) -> None:
        device = step400.STEP400(0)
        length = len(server.DEFAULT_SERVER._bound_devices)
        assert length > 1

        server.DEFAULT_SERVER.remove_device(device)
        assert (length - len(server.DEFAULT_SERVER._bound_devices)) == 1

    def test_shutdown(self) -> None:
        server.DEFAULT_SERVER.shutdown()
        assert len(server.DEFAULT_SERVER._bound_devices) == 0

    def test_send_errors(self) -> None:
        with pytest.raises(exceptions.ClientNotFoundError):
            device = step400.STEP400(0)
            server.DEFAULT_SERVER.remove_device(device)
            device.get(commands.GetVersion())
