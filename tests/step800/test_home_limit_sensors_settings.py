#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Ensure system commands and responses execute successfully."""


import pytest

from stepseries import commands, exceptions, responses, step800


@pytest.mark.skip_800_disconnected
class TestHomeLimitSensorsSettings:
    def test_home_sw(self, device: step800.STEP800) -> None:
        device.set(commands.EnableHomeSwReport(3, True))
        device.set(commands.EnableSwEventReport(3, True))
        resp = device.get(commands.GetHomeSw(3))
        assert isinstance(resp, responses.HomeSw)

    def test_limit_sw(self, device: step800.STEP800) -> None:
        with pytest.raises(exceptions.InvalidCommandError):
            device.get(commands.GetLimitSw(3))

    def test_home_sw_mode(self, device: step800.STEP800) -> None:
        device.set(commands.SetHomeSwMode(3, 1))
        resp = device.get(commands.GetHomeSwMode(3))
        assert isinstance(resp, responses.HomeSwMode)
        assert resp.swMode == 1

    def test_limit_sw_mode(self, device: step800.STEP800) -> None:
        with pytest.raises(exceptions.InvalidCommandError):
            device.get(commands.GetLimitSwMode(3))
