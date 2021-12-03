from threading import Event

import pytest

from stepseries.responses import DestIP
from stepseries.step800 import STEP800

_dest_ip_success = Event()


# Electromagnetic Brake
class BrakePresets:
    brake_connected: bool = False


# Homing
class HomingPresets:
    direction: int = None  # forward: 1; reverse: 0
    speed: float = None  # 0 - 15625; default is 100 steps/secs
    gu_timeout: int = None  # goUntil timeout; 0 - 65535; default is 10000ms
    sw_timeout: int = None  # 0 - 65535; default is 5000ms
    motor: int = None  # 1 - 4
    run_motor: bool = False  # Run the motor with the above presets


def callback(_: DestIP) -> None:
    _dest_ip_success.set()


@pytest.fixture(scope="package")
def device() -> STEP800:
    dip_switch_id = 0
    local_ip_address = "10.1.21.56"
    local_port = 50000
    server_ip_address = "0.0.0.0"
    server_port = 50100

    device = STEP800(
        dip_switch_id, local_ip_address, local_port, server_ip_address, server_port
    )
    device.on(DestIP, callback)
    return device


@pytest.fixture
def dest_ip_success() -> Event:
    return _dest_ip_success


@pytest.fixture(autouse=True)
def skip_if_disconnected(request) -> None:
    if request.node.get_closest_marker("skip_800_disconnected"):
        if not _dest_ip_success.is_set():
            pytest.skip("hardware not detected")


@pytest.fixture
def brake_presets() -> BrakePresets:
    return BrakePresets


@pytest.fixture
def homing_presets() -> HomingPresets:
    return HomingPresets


@pytest.fixture(autouse=True)
def skip_if_brake_disconnected(request) -> None:
    if request.node.get_closest_marker("skip_brake_disconnected"):
        if not BrakePresets.brake_connected:
            pytest.skip("electromagnetic brake not connected")


@pytest.fixture(autouse=True)
def skip_if_homing_preset_unset(request) -> None:
    if request.node.get_closest_marker("skip_homing_malconfigured"):
        if (
            HomingPresets.direction is None
            or HomingPresets.speed is None
            or HomingPresets.gu_timeout is None
            or HomingPresets.sw_timeout is None
            or HomingPresets.motor is None
        ):
            pytest.skip("homing presets not configured")
