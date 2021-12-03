#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Ensure system commands and responses execute successfully."""


import pytest

from stepseries import commands, exceptions, responses, step800


@pytest.mark.skip_800_disconnected
class TestVoltageCurrentModeSettings:
    def test_set_voltage_mode(self, device: step800.STEP800) -> None:
        with pytest.raises(exceptions.InvalidCommandError):
            device.set(commands.SetVoltageMode(4))

    def test_kval(self, device: step800.STEP800) -> None:
        device.set(commands.SetKval(3, 127, 128, 129, 130))
        resp = device.get(commands.GetKval(3))
        assert isinstance(resp, responses.Kval)
        assert resp.holdKVAL == 127
        assert resp.runKVAL == 128
        assert resp.accKVAL == 129
        assert resp.setDecKVAL == 130
        device.set(commands.SetKval(3, 16, 16, 16, 16))

    def test_bemf_param(self, device: step800.STEP800) -> None:
        device.set(commands.SetBemfParam(2, 1422, 253, 254, 255))
        resp = device.get(commands.GetBemfParam(2))
        assert isinstance(resp, responses.BemfParam)
        assert resp.INT_SPEED == 1422
        assert resp.ST_SLP == 253
        assert resp.FN_SLP_ACC == 254
        assert resp.FN_SLP_DEC == 255
        device.set(commands.SetBemfParam(2, 1032, 25, 41, 41))

    def test_set_current_mode(self, device: step800.STEP800) -> None:
        with pytest.raises(exceptions.InvalidCommandError):
            device.set(commands.SetCurrentMode(1))

    def test_tval(self, device: step800.STEP800) -> None:
        with pytest.raises(exceptions.InvalidCommandError):
            device.set(commands.SetTval(4, 10, 20, 30, 40))

        with pytest.raises(exceptions.InvalidCommandError):
            device.get(commands.GetTval(4))

    def test_decay_mode_param(self, device: step800.STEP800) -> None:
        with pytest.raises(exceptions.InvalidCommandError):
            device.set(commands.SetDecayModeParam(4, 100, 90, 80))

        with pytest.raises(exceptions.InvalidCommandError):
            device.get(commands.GetDecayModeParam(4))
