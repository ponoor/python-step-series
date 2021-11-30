#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Manages IO with multiple STEP-series devices."""


import atexit
from threading import Thread
from typing import Any, List, Tuple

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

from stepseries.commands import OSCCommand
from stepseries.exceptions import ClientNotFound

# Work around for this circular import; allows annotations while
# writing code and doesn't break when running it.
try:
    from .step400 import STEP400
except ImportError:
    STEP400 = Any


class Manager:

    _bound_devices: List[Tuple[STEP400, SimpleUDPClient, ThreadingOSCUDPServer, Thread]]

    def __init__(self) -> None:
        self._bound_devices = list()

        # Shutdown hook to ensure servers are properly closed
        atexit.register(self.shutdown)

    def add_device(self, device: STEP400) -> None:
        """
        For internal use only. Add a device to send data to when it is
        received.
        """
        if not any([device == c[0] for c in self._bound_devices]):
            # Create a new server and client, then bind them to the
            # device
            dispatcher = Dispatcher()
            dispatcher.set_default_handler(device._handle_incoming_message)
            server = ThreadingOSCUDPServer(
                (device.server_address, device.server_port), dispatcher
            )
            client = SimpleUDPClient(device.address, device.port)
            thread = Thread(target=server.serve_forever, daemon=True)
            thread.start()
            self._bound_devices.append((device, client, server, thread))

    def remove_device(self, device: STEP400) -> None:
        """
        For internal use only. Remove a tracked device to stop sending
        data to it.
        """
        for i, (d, _, s, _) in enumerate(self._bound_devices):
            if d == device:
                self._bound_devices.pop(i)
                s.shutdown()
                break

    def shutdown(self) -> None:
        """Shuts down all tracked servers."""

        for _, _, s, _ in self._bound_devices:
            s.shutdown()
        self._bound_devices = list()

    def send(self, device: STEP400, message: OSCCommand) -> None:
        """Send `message` to the `device`."""

        # Get the client bound to this device
        client = None
        for d, c, _, _ in self._bound_devices:
            if d == device:
                client = c
                break
        else:
            raise ClientNotFound("device is not registered with a server")

        client.send(message.build())


DEFAULT_SERVER = Manager()
