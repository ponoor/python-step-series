#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""4 axis stepper motor driver with Ethernet interface."""


from queue import Empty

from .commands import OSCGetCommand, OSCSetCommand
from .exceptions import StepSeriesException
from .responses import OSCResponse
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

    def get(self, command: OSCGetCommand) -> OSCResponse:
        """Send a 'get' command to the device and return the response.

        Note:
            The responses are also sent to each applicable callback.

            If a `ParseError` is received, then it will be raised. The
            raw response can be retrieved via the `response` attribute
            of the error.

        Args:
            command (`OSCGetCommand`):
                The completed command template (`stepseries.commands`).

        Raises:
            `TypeError`:
                `command` is not an `OSCSetCommand`.
        """

        if not isinstance(command, OSCGetCommand):
            raise TypeError(
                "argument 'command' expected to be 'OSCGetCommand', "
                f"'{type(command).__name__}' found"
            )

        # Prepare for get request
        s: str = command.address.replace("get", "")
        self._get_request = s.lower()

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

        DEFAULT_SERVER.send(self, command)
