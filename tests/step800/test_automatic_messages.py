#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Verify alarm-related commands execute successfully."""


import pytest

from stepseries import commands, responses
from stepseries.step800 import STEP800


@pytest.mark.order(1)
@pytest.mark.skip_800_disconnected
class TestAutomaticMessages:
    def test_booted(self, device: STEP800, wait_for) -> None:
        # Request the device reset and then wait for the response
        wait_for(device, commands.ResetDevice(), responses.Booted)

        # Make sure to re-initialize the device
        device.set(commands.SetDestIP())

    def test_osc_errors(self, device: STEP800) -> None:
        # Create a dummy command
        from dataclasses import dataclass

        @dataclass
        class GetDummy(commands.OSCGetCommand):
            address: str = "/getDummy"

        # Send the command
        # There exists no such command as this, so the device should
        # return a "messageNotMatch" error, which the API raises
        with pytest.raises(responses.ErrorOSC):
            device.get(GetDummy())

    def test_command_errors(self, device: STEP800) -> None:
        # Request data about a motor that doesn't exist on the board
        # The device will raise a "MotorIdNotMatch" error which the
        # API raises
        with pytest.raises(responses.ErrorCommand):
            device.get(commands.GetStatus(200))
