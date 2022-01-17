#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""4 axis stepper motor driver with Ethernet interface."""


from queue import Empty
from typing import List, Union

from .commands import OSCGetCommand, OSCSetCommand, ReportError, SetDestIP
from .exceptions import StepSeriesException
from .responses import OSCResponse, ErrorCommand, ErrorOSC
from .server import DEFAULT_SERVER
from .stepXXX import STEPXXX


class STEP400(STEPXXX):
    """Send and receive data from a STEP400 motor driver.

    Note:
        It is recommended to create a default message handler for this
        driver. Here is an example:

            >>> from stepseries.step400 import STEP400
            >>>
            >>> def default_handler(message) -> None:
            ...     print(message)
            ...
            >>> driver = STEP400(0, '192.168.1.100')
            >>> driver.on(None, default_handler)

    Args:
        id (`int`):
            The id set by the DIP switches on the device.
        address (`str`):
            The ip address of the device. Defaults to `10.0.0.100`.
        port (`int`):
            The local port the device is listening on. Defaults to
            `50000`.
        server_address (`str`):
            The ip address of the server (this machine). Should always
            be `0.0.0.0`. Defaults to `0.0.0.0`.
        server_port (`int`):
            The port the server is listening on. Defaults to `50100`.
        add_id_to_args (`bool`):
            Whether to add `id` to `address` and `server_port`
            (the default behavior on the device). Defaults to `True`.
    """

    def get(
        self, command: OSCGetCommand, with_callback: bool = True
    ) -> Union[OSCResponse, List[OSCResponse]]:
        """Send a 'get' command to the device and return the response.

        Note:
            The responses are also sent to each applicable callback.

            If a `ParseError` is received, then it will be raised. The
            raw response can be retrieved via the `response` attribute
            of the error.

        Args:
            command (`OSCGetCommand`):
                The completed command template (`stepseries.commands`).
            with_callback (`bool`):
                Send the response to callbacks as well
                (defaults to `True`).

        Raises:
            `TypeError`:
                `command` is not an `OSCSetCommand`.
        """

        if not isinstance(command, OSCGetCommand):
            raise TypeError(
                "argument 'command' expected to be 'OSCGetCommand', "
                f"'{type(command).__name__}' found"
            )

        self._check_status()

        # Prepare for get request
        s: str = command.address.replace("get", "")
        self._get_request = s.lower()
        self._get_with_callback = with_callback
        if hasattr(command, "motorID"):
            if command.motorID == 255:
                self._is_multiple_response = True

        # Send the request
        DEFAULT_SERVER.send(self, command)

        # Wait for data and reset
        try:
            resp = self._get_queue.get(timeout=2)
            self._get_queue.task_done()
        except Empty:
            raise TimeoutError("timed-out waiting for a response from the device")
        finally:
            self._get_request = None
            self._get_with_callback = True
            self._multiple_responses = list()
            self._is_multiple_response = False

        if isinstance(resp, Exception):
            if isinstance(resp, StepSeriesException):
                if resp.original_exc is not None:
                    raise resp from resp.original_exc
            raise resp

        return resp

    def set(self, command: OSCSetCommand) -> None:
        """Send a 'set' command to the device.

        Args:
            command (`OSCCommand`):
                The completed command template (`stepseries.commands`).

        Raises:
            `TypeError`:
                `command` is not an `OSCSetCommand`.
        """

        if not isinstance(command, OSCSetCommand):
            raise TypeError(
                "argument 'command' expected to be 'OSCSetCommand', "
                f"'{type(command).__name__}' found"
            )

        if not isinstance(command, SetDestIP):
            self._check_status()

        if command.__dict__.get("callback", None):
            if isinstance(command, ReportError):
                self.on(ErrorCommand, command.callback)
                self.on(ErrorOSC, command.callback)
            else:
                self.on(command.response_cls, command.callback)

        DEFAULT_SERVER.send(self, command)
