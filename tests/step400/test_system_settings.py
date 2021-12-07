#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Ensure system commands and responses execute successfully."""


from threading import Event

import pytest

from stepseries import commands, responses, step400


@pytest.mark.incremental
class TestSystemSettings:
    # This test MUST run first to enable communication with the device
    @pytest.mark.order(1)
    def test_set_dest_ip(self, device: step400.STEP400, dest_ip_success: Event) -> None:
        try:
            device.set(commands.SetDestIP())
            assert dest_ip_success.wait(timeout=0.5)

            # Verify the device is a STEP400
            firmware: responses.Version = device.get(commands.GetVersion())
            assert firmware.firmware_name == "STEP400"
        except AssertionError:
            dest_ip_success.clear()
            pytest.xfail("hardware not detected")

    def test_get_version(self, device: step400.STEP400) -> None:
        resp = device.get(commands.GetVersion())
        assert isinstance(resp, responses.Version)

    def test_get_config_name(self, device: step400.STEP400) -> None:
        resp = device.get(commands.GetConfigName())
        assert isinstance(resp, responses.ConfigName)

    def test_report_error(self, device: step400.STEP400) -> None:
        device.set(commands.ReportError(enable=1))
        device.set(commands.ReportError(False))
