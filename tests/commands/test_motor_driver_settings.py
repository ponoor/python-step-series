#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Ensure OSC commands for motor driver settings build properly."""


from stepseries import commands


def test_set_microstep_mode() -> None:
    builder = commands.SetMicrostepMode(0, 3)
    osc_message = builder.build()
    params = osc_message.params

    assert osc_message.address == builder.address
    assert len(params) == 2
    assert params[0] == builder.motorID
    assert params[1] == builder.STEP_SEL


def test_get_microstep_mode() -> None:
    builder = commands.GetMicrostepMode(0)
    osc_message = builder.build()
    params = osc_message.params

    assert osc_message.address == builder.address
    assert len(params) == 1
    assert params[0] == builder.motorID


def test_set_low_speed_optimize_threshold() -> None:
    builder = commands.SetLowSpeedOptimizeThreshold(0, 0.5)
    osc_message = builder.build()
    params = osc_message.params

    assert osc_message.address == builder.address
    assert len(params) == 2
    assert params[0] == builder.motorID
    assert params[1] == builder.lowSpeedOptimizationThreshold


def test_get_low_speed_optimize_threshold() -> None:
    builder = commands.GetLowSpeedOptimizeThreshold(1)
    osc_message = builder.build()
    params = osc_message.params

    assert osc_message.address == builder.address
    assert len(params) == 1
    assert params[0] == builder.motorID
