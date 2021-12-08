#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Ensure system commands and responses execute successfully."""


import pytest

from stepseries import commands, responses, step400


@pytest.mark.skip_400_disconnected
class TestVoltageCurrentModeSettings:
    def test_set_voltage_mode(self, device: step400.STEP400) -> None:
        device.set(commands.SetVoltageMode(4))

    def test_kval(self, device: step400.STEP400) -> None:
        device.set(commands.SetKval(3, 127, 128, 129, 130))
        resp = device.get(commands.GetKval(3))
        assert isinstance(resp, responses.Kval)
        assert resp.holdKVAL == 127
        assert resp.runKVAL == 128
        assert resp.accKVAL == 129
        assert resp.setDecKVAL == 130
        device.set(commands.SetKval(3, 16, 16, 16, 16))

    def test_bemf_param(self, device: step400.STEP400) -> None:
        device.set(commands.SetBemfParam(2, 1422, 253, 254, 255))
        resp = device.get(commands.GetBemfParam(2))
        assert isinstance(resp, responses.BemfParam)
        assert resp.INT_SPEED == 1422
        assert resp.ST_SLP == 253
        assert resp.FN_SLP_ACC == 254
        assert resp.FN_SLP_DEC == 255
        device.set(commands.SetBemfParam(2, 1032, 25, 41, 41))

    def test_set_current_mode(self, device: step400.STEP400) -> None:
        device.set(commands.SetCurrentMode(1))

    def test_tval(self, device: step400.STEP400) -> None:
        device.set(commands.SetTval(4, 10, 20, 30, 40))
        resp = device.get(commands.GetTval(4))
        assert isinstance(resp, responses.Tval)
        assert resp.holdTVAL == 10
        assert resp.runTVAL == 20
        assert resp.accTVAL == 30
        assert resp.decTVAL == 40
        device.set(commands.SetTval(4, 0, 16, 16, 16))

    def test_get_tval_mA(self, device: step400.STEP400) -> None:
        resp = device.get(commands.GetTval_mA(3))
        assert isinstance(resp, responses.Tval_mA)
        assert resp.holdTVAL_mA == 78.125
        assert resp.runTVAL_mA == 1328.125
        assert resp.accTVAL_mA == 1328.125
        assert resp.decTVAL_mA == 1328.125

    def test_decay_mode_param(self, device: step400.STEP400) -> None:
        device.set(commands.SetDecayModeParam(4, 100, 90, 80))
        resp = device.get(commands.GetDecayModeParam(4))
        assert isinstance(resp, responses.DecayModeParam)
        assert resp.T_FAST == 100
        assert resp.TON_MIN == 90
        assert resp.TOFF_MIN == 80
        device.set(commands.SetDecayModeParam(4, 25, 41, 41))
