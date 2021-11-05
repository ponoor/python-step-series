#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Ensure OSC commands for system settings build properly."""


from stepseries import commands


def test_set_dest_ip() -> None:
    builder = commands.SetDestIP()
    osc_message = builder.build()

    assert osc_message.address == builder.address
    assert len(osc_message.params) == 0


def test_get_version() -> None:
    builder = commands.GetVersion()
    osc_message = builder.build()

    assert osc_message.address == builder.address
    assert len(osc_message.params) == 0


def test_get_config_name() -> None:
    builder = commands.GetConfigName()
    osc_message = builder.build()

    assert osc_message.address == builder.address
    assert len(osc_message.params) == 0


def test_report_error() -> None:
    builder = commands.ReportError()
    osc_message = builder.build()

    assert osc_message.address == builder.address
    assert len(osc_message.params) == 0
