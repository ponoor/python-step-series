#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Ensure system commands and responses execute successfully."""


from threading import Event

import pytest

from stepseries import commands, responses, step800


@pytest.mark.incremental
class TestSystemSettings:
    # This test MUST run first to enable communication with the device
    @pytest.mark.order(1)
    def test_set_dest_ip(self, device: step800.STEP800, dest_ip_success: Event) -> None:
        device.set(commands.SetDestIP())
        assert dest_ip_success.wait(timeout=0.5), "hardware not detected"

        # Verify the device is a STEP400
        firmware: responses.Version = device.get(commands.GetVersion())
        try:
            assert firmware.firmware_name == "STEP800"
        except AssertionError:
            dest_ip_success.clear()
            raise

    def test_get_version(self, device: step800.STEP800) -> None:
        resp = device.get(commands.GetVersion())
        assert isinstance(resp, responses.Version)

    def test_get_config_name(self, device: step800.STEP800) -> None:
        resp = device.get(commands.GetConfigName())
        assert isinstance(resp, responses.ConfigName)

    def test_report_error(self, device: step800.STEP800) -> None:
        device.set(commands.ReportError(enable=1))
        device.set(commands.ReportError(False))
