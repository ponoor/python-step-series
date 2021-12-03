#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Ensure system commands and responses execute successfully."""


import pytest

from stepseries import commands, responses, step800


@pytest.mark.skip_800_disconnected
@pytest.mark.skip_homing_malconfigured
@pytest.mark.incremental
class TestHomingSettings:
    def test_homing_direction(self, device: step800.STEP800, homing_presets) -> None:
        device.set(
            commands.SetHomingDirection(homing_presets.motor, homing_presets.direction)
        )
        resp = device.get(commands.GetHomingDirection(homing_presets.motor))
        assert isinstance(resp, responses.HomingDirection)
        assert resp.homingDirection == homing_presets.direction

    def test_homing_speed(self, device: step800.STEP800, homing_presets) -> None:
        device.set(commands.SetHomingSpeed(homing_presets.motor, homing_presets.speed))
        resp = device.get(commands.GetHomingSpeed(homing_presets.motor))
        assert isinstance(resp, responses.HomingSpeed)
        assert resp.homingSpeed == homing_presets.speed

    def test_go_until_timeout(self, device: step800.STEP800, homing_presets) -> None:
        device.set(
            commands.SetGoUntilTimeout(homing_presets.motor, homing_presets.gu_timeout)
        )
        resp = device.get(commands.GetGoUntilTimeout(homing_presets.motor))
        assert isinstance(resp, responses.GoUntilTimeout)
        assert resp.timeout == homing_presets.gu_timeout

    def test_release_sw_timeout(self, device: step800.STEP800, homing_presets) -> None:
        device.set(
            commands.SetReleaseSwTimeout(
                homing_presets.motor, homing_presets.sw_timeout
            )
        )
        resp = device.get(commands.GetReleaseSwTimeout(homing_presets.motor))
        assert isinstance(resp, responses.ReleaseSwTimeout)
        assert resp.timeout == homing_presets.sw_timeout

    def test_homing(self, device: step800.STEP800, homing_presets) -> None:
        if homing_presets.run_motor:
            device.set(commands.Homing(4))
        else:
            pytest.skip("preset 'run_motor' is not set")
