#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Verify automatic messages parse successfully."""


import pytest

from stepseries import commands, responses
from stepseries.step800 import STEP800


@pytest.mark.order(1)
@pytest.mark.skip_800_disconnected
def test_booted(device: STEP800, wait_for) -> None:
    # Request the device reset and then wait for the response
    wait_for(device, commands.ResetDevice(), responses.Booted)

    # Make sure to re-initialize the device
    device.set(commands.SetDestIP())
