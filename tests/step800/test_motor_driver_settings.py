#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Ensure system commands and responses execute successfully."""


from math import isclose  # Due to precision, we cannot compare floats directly
from threading import Event

import pytest

from stepseries import commands, exceptions, responses, step800


@pytest.mark.skip_800_disconnected
class TestMotorDriverSettings:
    def test_microstep_mode(self, device: step800.STEP800) -> None:
        device.set(commands.SetMicrostepMode(1, 5))
        resp = device.get(commands.GetMicrostepMode(1))
        assert isinstance(resp, responses.MicrostepMode)
        assert resp.STEP_SEL == 5
        device.set(commands.SetMicrostepMode(1, 7))

    def test_low_speed_optimize_threshold(self, device: step800.STEP800) -> None:
        device.set(commands.EnableLowSpeedOptimize(4, True))
        device.set(commands.SetLowSpeedOptimizeThreshold(4, 555.5))
        resp = device.get(commands.GetLowSpeedOptimizeThreshold(4))
        assert isinstance(resp, responses.LowSpeedOptimizeThreshold)
        assert isclose(resp.lowSpeedOptimizeThreshold, 555.5, rel_tol=0.1)
        device.set(commands.SetLowSpeedOptimizeThreshold(4, 0.0))
        device.set(commands.EnableLowSpeedOptimize(4, False))

    def test_busy(self, device: step800.STEP800) -> None:
        device.set(commands.EnableBusyReport(2, False))
        resp = device.get(commands.GetBusy(2))
        assert isinstance(resp, responses.Busy)

    def test_hiz(self, device: step800.STEP800) -> None:
        device.set(commands.EnableHiZReport(1, True))
        resp = device.get(commands.GetHiZ(1))
        assert isinstance(resp, responses.HiZ)
        device.set(commands.EnableHiZReport(1, False))

    def test_dir(self, device: step800.STEP800) -> None:
        device.set(commands.EnableDirReport(3, True))
        resp = device.get(commands.GetDir(3))
        assert isinstance(resp, responses.Dir)
        assert resp.direction == 0
        device.set(commands.EnableDirReport(3, False))

    def test_motor_status(self, device: step800.STEP800) -> None:
        device.set(commands.EnableMotorStatusReport(4, False))
        resp = device.get(commands.GetMotorStatus(4))
        assert isinstance(resp, responses.MotorStatus)

    def test_set_position_report_interval(self, device: step800.STEP800) -> None:
        report_received = Event()
        device.on(responses.Position, lambda x: report_received.set())
        device.set(commands.SetPositionReportInterval(3, 1000))
        try:
            assert report_received.wait(timeout=2)
        finally:
            device.set(commands.SetPositionReportInterval(3, 0))

    def test_set_position_list_report_interval(self, device: step800.STEP800) -> None:
        report_received = Event()
        device.on(responses.PositionList, lambda x: report_received.set())
        device.set(commands.SetPositionListReportInterval(1000))
        try:
            assert report_received.wait(timeout=2)
        finally:
            device.set(commands.SetPositionListReportInterval(0))

    def test_get_adc_val(self, device: step800.STEP800) -> None:
        with pytest.raises(exceptions.InvalidCommandError):
            device.get(commands.GetAdcVal(2))

    def test_get_status(self, device: step800.STEP800) -> None:
        resp = device.get(commands.GetStatus(3))
        assert isinstance(resp, responses.Status)

    def test_get_config_register(self, device: step800.STEP800) -> None:
        resp = device.get(commands.GetConfigRegister(1))
        assert isinstance(resp, responses.ConfigRegister)

    def test_reset_motor_driver(self, device: step800.STEP800) -> None:
        device.set(commands.ResetMotorDriver(4))
        device.set(commands.ResetMotorDriver(3))
        device.set(commands.ResetMotorDriver(2))
        device.set(commands.ResetMotorDriver(1))
