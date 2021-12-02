"""
    Dummy conftest.py for stepseries.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

from threading import Event
from typing import Dict, Tuple

import pytest

from stepseries.commands import SetDestIP
from stepseries.responses import DestIP
from stepseries.step400 import STEP400

# store history of failures per test class name and per index in parametrize (if parametrize used)
_test_failed_incremental: Dict[str, Dict[Tuple[int, ...], str]] = {}


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        # incremental marker is used
        if call.excinfo is not None and call.excinfo.typename != "Skipped":
            # the test has failed
            # retrieve the class name of the test
            cls_name = str(item.cls)
            # retrieve the index of the test
            # (if parametrize is used in combination with incremental)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # retrieve the name of the test function
            test_name = item.originalname or item.name
            # store in _test_failed_incremental the original name of the failed test
            _test_failed_incremental.setdefault(cls_name, {}).setdefault(
                parametrize_index, test_name
            )


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        # retrieve the class name of the test
        cls_name = str(item.cls)
        # check if a previous test has failed for this class
        if cls_name in _test_failed_incremental:
            # retrieve the index of the test
            # (if parametrize is used in combination with incremental)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # retrieve the name of the first test function to fail for this class name and index
            test_name = _test_failed_incremental[cls_name].get(parametrize_index, None)
            # if name found, test has failed for the combination of class name & test name
            if test_name is not None:
                pytest.xfail("previous test failed ({})".format(test_name))


_dest_ip_success = Event()


@pytest.mark.incremental
class HardwareIncremental:

    # This test MUST run first to enable communication with the device
    @pytest.mark.order(1)
    def test_set_dest_ip(self, device: STEP400) -> None:  # noqa
        device.set(SetDestIP())
        try:
            assert _dest_ip_success.wait(timeout=0.5)
        finally:
            _dest_ip_success.clear()


def callback(_: DestIP) -> None:
    _dest_ip_success.set()


@pytest.fixture(scope="session")
def device() -> STEP400:
    dip_switch_id = 0
    local_ip_address = "10.1.21.56"
    local_port = 50000
    server_ip_address = "0.0.0.0"
    server_port = 50100

    device = STEP400(
        dip_switch_id, local_ip_address, local_port, server_ip_address, server_port
    )
    device.on(DestIP, callback)
    return device
