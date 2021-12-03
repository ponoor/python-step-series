#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Ensure system commands and responses execute successfully."""


import pytest

from stepseries import commands, responses, step800


@pytest.mark.skip_800_disconnected
@pytest.mark.incremental
class TestElectromagneticBrakeSettings:
    @pytest.mark.skip_brake_disconnected
    def test_enable_electromagnet_brake(self, device: step800.STEP800) -> None:
        device.set(commands.EnableElectromagnetBrake(1, True))

    @pytest.mark.skip_brake_disconnected
    def test_activate(self, device: step800.STEP800) -> None:
        device.set(commands.Activate(1, True))

    @pytest.mark.skip_brake_disconnected
    def test_free(self, device: step800.STEP800) -> None:
        device.set(commands.Free(1, True))

    def test_brake_transition_duration(self, device: step800.STEP800) -> None:
        device.set(commands.SetBrakeTransitionDuration(1, 1250))
        resp = device.get(commands.GetBrakeTransitionDuration(1))
        assert isinstance(resp, responses.BrakeTransitionDuration)
        assert resp.duration == 1250
