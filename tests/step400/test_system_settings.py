#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Ensure system commands and responses execute successfully."""


from stepseries import commands, responses, step400
from tests.conftest import HardwareIncremental


class TestSystemSettings(HardwareIncremental):
    def test_get_version(self, device: step400.STEP400) -> None:
        resp = device.get(commands.GetVersion())
        assert isinstance(resp, responses.Version)

    def test_get_config_name(self, device: step400.STEP400) -> None:
        resp = device.get(commands.GetConfigName())
        assert isinstance(resp, responses.ConfigName)

    def test_report_error(self, device: step400.STEP400) -> None:
        device.set(commands.ReportError(enable=1))
        device.set(commands.ReportError(False))
