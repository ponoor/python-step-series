#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""4 axis stepper motor driver with Ethernet interface."""


from queue import Queue
from typing import Any, Callable, Dict, List, Tuple, Union

from .commands import OSCGetCommand, OSCSetCommand, ResetDevice
from .exceptions import ParseError
from .responses import OSCResponse
from .server import DEFAULT_SERVER


class STEPXXX:
    """Send and receive data from a STEP-series motor driver.

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

    _id: int
    _address: str
    _port: int
    _server_address: str
    _server_port: int

    _boards_to_n_motors: Dict[str, int]
    _registered_callbacks: Dict[
        Union[OSCResponse, None], List[Callable[[OSCResponse], None]]
    ]
    _get_request: str
    _get_queue: Queue
    _is_multiple_response: bool
    _multiple_responses: List[OSCResponse]

    def __init__(
        self,
        id: int,
        address: str = "10.0.0.100",
        port: int = 50000,
        server_address: str = "0.0.0.0",
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

        self._boards_to_n_motors = {"STEP400": 4, "STEP800": 8}
        self._registered_callbacks = dict()
        self._get_request = None
        self._get_queue = Queue()
        self._is_multiple_response = False
        self._multiple_responses = list()

        # Bind this device
        DEFAULT_SERVER.add_device(self)

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
        raw_resp = message_address + " " + " ".join([str(x) for x in osc_args])
        for cls in OSCResponse.__subclasses__():
            if cls.address == message_address:
                try:
                    resp = cls(raw_resp)
                except (IndexError, TypeError) as exc:
                    resp = ParseError("parsing failed to deconstruct response")
                    resp.response = raw_resp
                    resp.original_exc = exc
                break
        else:
            resp = ParseError("no response object matched this message")
            resp.response = raw_resp

        # Support multiple responses
        if self._is_multiple_response:
            if not isinstance(resp, Exception):
                if resp.address.lower() == self._get_request:
                    self._multiple_responses.append(resp)
                    if (
                        len(self._multiple_responses)
                        < self._boards_to_n_motors[self.__class__.__name__]
                    ):
                        return
            else:
                if self._get_request:
                    if resp.address.lower() == self._get_request:
                        self._get_queue.put(resp)
                        self._get_queue.join()

        # Send the message to all required callbacks
        # TODO: Look at thread pooling this process
        for resp_type, callbacks in self._registered_callbacks.items():
            if resp.__class__ == resp_type or resp_type is None:
                for callback in callbacks:
                    if self._multiple_responses:
                        callback(self._multiple_responses)
                    else:
                        callback(resp)

        # Return the get request
        if self._get_request:
            if resp.address.lower() == self._get_request or isinstance(resp, Exception):
                if self._multiple_responses:
                    self._get_queue.put(self._multiple_responses)
                else:
                    self._get_queue.put(resp)
                self._get_queue.join()

    def on(
        self, message_type: Union[OSCResponse, None], fn: Callable[[OSCResponse], None]
    ) -> None:
        """Register `fn` to be executed when `message_type` is received.

        Args:
            message_type (`OSCResponse`, `None`):
                The message type to filter for. If `None`, then all
                messages received will be sent to `fn`. Note multiple
                `fn`s can be registered to the same type or multiple
                types.
            fn (`callable`):
                The callable to be executed when `message_type` is
                received.
                    Note:
                        `fn` should accept one and only one argument
                        being the message received.

        Raises:
            `TypeError`:
                `message_type` is not an `OSCResponse`.
                `fn` is not a callable.
        """

        if message_type is not None and message_type.__base__ is not OSCResponse:
            raise TypeError(
                "argument 'message_type' expected to be 'OSCResponse', "
                f"'{type(message_type).__name__}' found"
            )
        if not callable(fn):
            raise TypeError(
                "argument 'fn' expected to be callable, " f"'{type(fn).__name__}' found"
            )

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

    def reset(self) -> None:
        """Resets the device.

        Note: This function may return before the device is ready.
        """
        self.set(ResetDevice())

    def get(self, command: OSCGetCommand) -> Union[OSCResponse, List[OSCResponse]]:
        """Send a 'get' command to the device and return the response."""
        raise NotImplementedError

    def set(self, command: OSCSetCommand) -> None:
        """Send a 'set' command to the device."""
        raise NotImplementedError
