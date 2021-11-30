#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""4 axis stepper motor driver with Ethernet interface."""


from queue import Queue
from typing import Any, Callable, Dict, List, Tuple, Union

from .commands import OSCCommand
from .exceptions import ParseError
from .responses import OSCResponse
from .server import DEFAULT_SERVER


class STEP400:
    """Send and receive data from a STEP400 motor driver.

    Note:
        It is recommended to create a default message handler for this
        driver. This driver will not be 'registered' with the server
        until `on()` is called. Here is an example:

            >>> from stepseries.step400 import STEP400
            >>>
            >>> def default_handler(message) -> None:
            ...     print(message)
            ...
            >>> driver = STEP400(0, '192.168.1.100')
            >>> driver.on(None, default_handler)

    Args:
        id (`int`):
            The ID set with the DIP switches on the motor driver.
        address (`str`):
            The IP address of the motor driver.
        port (`int`, optional):
            The port set on the device. If not provided, then it is
            assumed that the port on the device is set with the equation
            `default_port + id` where `default_port` is `50100`.
            If `-1`, then `50100` is assumed.
    """

    _id: int
    _address: str
    _port: int
    _server_address: str
    _server_port: int

    _registered_callbacks: Dict[
        Union[OSCResponse, None], List[Callable[[OSCResponse], None]]
    ]
    _get_request: str
    _get_queue: Queue

    def __init__(
        self,
        id: int,
        address: str = "10.0.0.100",
        port: int = 50000,
        server_address: str = "10.0.0.10",
        server_port: int = 50100,
        add_id_to_args: bool = True,
    ) -> None:
        self._id = id
        self._address = address
        self._port = port
        self._server_address = server_address
        self._server_port = server_port

        if add_id_to_args:
            # Add id to address
            address_split = self._address.split(".")
            last_octet = int(address_split[-1])
            address_split[-1] = str(last_octet + id)
            self._address = ".".join(address_split)

            # Add id to server port
            self._server_port += id

        self._registered_callbacks = {}
        self._get_request = None
        self._get_queue = Queue()

        # Bind this device
        DEFAULT_SERVER.add_device(self)

    def __enter__(self):
        return self

    def __exit__(self, *args) -> None:
        pass

    @property
    def address(self) -> str:
        """The local IP address of the client."""
        return self._address

    @property
    def port(self) -> int:
        """The local port on the client."""
        return self._port

    @property
    def server_address(self) -> str:
        """The remote IP address of the server."""
        return self._server_address

    @property
    def server_port(self) -> int:
        """The remote port on the server."""
        return self._server_port

    def _handle_incoming_message(
        self, message_address: str, *osc_args: Tuple[Any]
    ) -> None:
        # Reconstruct message as an object
        resp = None
        for cls in OSCResponse.__subclasses__():
            if cls.address == message_address:
                resp = cls(*(message_address, *osc_args))
                break
        else:
            # Flatten the response
            raw_resp = message_address + " ".join([str(x) for x in osc_args])
            resp = ParseError("no response object matched this message")
            resp.response = raw_resp

        # Return the get request
        if self._get_request:
            if message_address == self._get_request:
                self._get_queue.put(resp)
                self._get_queue.join()

        # Send the message to all required callbacks
        # TODO: Look at thread pooling this process
        for resp_type, callbacks in self._registered_callbacks.items():
            if resp.__class__ == resp_type or resp_type is None:
                for callback in callbacks:
                    callback(resp)

    def on(
        self, message_type: Union[OSCResponse, None], fn: Callable[[OSCResponse], None]
    ) -> None:
        """Register `fn` to be executed when `message_type` is received.

        Args:
            message_type (`OSCResponse`):
                The message type to filter for. If `None`, then all
                messages received will be sent to `fn`. Note multiple
                `fn`s can be registered to the same type, or multiple
                types.
            fn (`callable`):
                The callable to be executed when `message_type` is
                received.
                    Note:
                        `fn` should accept one and only one argument
                        being the message received.
        """

        try:
            if fn not in self._registered_callbacks[message_type]:
                self._registered_callbacks[message_type].append(fn)
        except KeyError:
            self._registered_callbacks[message_type] = [fn]

    def remove(self, fn: Callable[[OSCResponse], None]) -> None:
        """Remove `fn` from the registered callbacks."""

        for k, callbacks in self._registered_callbacks.items():
            for callback in callbacks:
                if callback == fn:
                    self._registered_callbacks[k].remove(fn)

    def get(self, command: OSCCommand) -> OSCResponse:
        """Send a 'get' command to the device and return the response.

        The responses are also sent to each applicable callback.

        Note:
            If a `ParseError` is received, then it will be raised. The
            raw response can be retrieved via the `response` attribute
            of the error.

        Args:
            command (`OSCCommand`):
                The builder of the command (`stepseries.commands`).
        """

        # Prepare for get request
        s = command.address.replace("get", "")
        self._get_request = s[0] + s[1].lower() + s[2:]

        # Send the request
        DEFAULT_SERVER.send(self, command)

        # Wait for data and reset
        resp = self._get_queue.get()
        self._get_request = None
        self._get_queue.task_done()

        if resp is ParseError:
            raise resp

        return resp

    def set(self, command: OSCCommand) -> None:
        """Send a 'set' command to the device."""

        DEFAULT_SERVER.send(self, command)
