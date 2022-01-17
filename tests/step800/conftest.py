import random
import time

import pytest

from stepseries import commands
from stepseries.step800 import STEP800


# Test configurations
# Please configure these presets before running the tests. Ensure to set
# "is_configured" to True, otherwise these tests will be skipped.
# The defaults for these tests assume you are using an SM-42BYG011-25
# 12V stepper motor. Change the configurations as needed to match your
# motor. Examples for a variety of steppers can be found here:
# https://github.com/ponoor/step-series-support/tree/main/configGenerator
class TestPresets:
    is_configured: bool = False

    # Device networking settings
    id: int = 0
    address: str = "10.1.16.20"
    port: int = 50000
    server_address: str = "0.0.0.0"
    server_port: int = 50100
    add_id_to_args: bool = True

    # The singular motor ID to test on (1 - 8, 255)
    # 255 means run the command on all motors
    # Keep at None to randomize per test
    motor_id: int = None

    # Allow motors to be physically ran
    # Do not make True if you have no motor(s) connected
    enable_motors: bool = False


@pytest.fixture(scope="package")
def device() -> STEP800:
    device = STEP800(
        TestPresets.id,
        TestPresets.address,
        TestPresets.port,
        TestPresets.server_address,
        TestPresets.server_port,
        TestPresets.add_id_to_args
    )

    # Send the start-up command
    device.set(commands.SetDestIP())

    # Allow the device to start
    time.sleep(3)

    return device


@pytest.fixture
def motor_id() -> int:
    if not TestPresets.motor_id:
        valid_ids = list(range(1, 9)) + [255]
        return valid_ids[random.randint(0, len(valid_ids) - 1)]

    return TestPresets.motor_id


@pytest.fixture(autouse=True)
def skip_if_disconnected(request, device: STEP800):
    if request.node.get_closest_marker("skip_800_disconnected"):
        if device.is_closed:
            pytest.skip("hardware not detected")


@pytest.fixture(autouse=True)
def skip_if_motors_disabled(request):
    if request.node.get_closest_marker("skip_motors_disabled"):
        if not TestPresets.enable_motors:
            pytest.skip("motors are disabled")
