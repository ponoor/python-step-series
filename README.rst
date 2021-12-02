==================
python-step-series
==================


    A Python library for OSC communication with the Ponoor Step-series devices.


Welcome to ``python-step-series``, a Python library to stupidly simplify communication
with ponoor's Step-series devices.

To get started, follow the simple example below or read the `documentation`_ to truly
see what this library has to offer.


Installation
============

There are multiple ways to install ``python-step-series``. The easiest way is from PyPI (coming soon):

.. code-block:: shell

    pip install python-step-series

Or you can install from source. See the `Contributing`_ guide for more information
on how to do that.

``python-step-series`` requires Python >=3.7.

First-steps Example
===================

.. code-block:: python

    from stepseries.commands import GetVersion, SetDestIP
    from stepseries.step400 import STEP400
    from stepseries.responses import OSCResponse, Version

    def default_handler(message: OSCResponse) -> None:
        print("Message received:", message)

    def version_handler(message: Version) -> None:
        print("Firmware:")
        print(" - Name:", message.firmware_name)
        print(" - Version:", message.firmware_version)
        print(" - Compiled:", message.compile_date)

    if __name__ == '__main__':
        # Configurations that should be changed
        dip_switch_id = 0  # Should match what is set on the device
        local_ip_address = "10.1.21.56"  # The ip address of the device
        local_port = 50000
        server_address = "0.0.0.0"  # The address of the server; should always be 0.0.0.0 (the local machine)
        server_port = 50100

        # Create a device instance using the configurations above
        # This does two things: creates a communication interface and starts up an OSC endpoint for
        # the device to communicate with
        device = STEP400(dip_switch_id, local_ip_address, local_port, server_address, server_port)

        # Register a default handler for messages
        # Typically, these are used to log events and print to stdout
        # It is recommended to instead register 'filtered' handlers if
        # you want to parse the message (like the one below)
        device.on(None, default_handler)

        # Register a handler just for version info
        device.on(Version, version_handler)

        # Enable communication with the device
        device.set(SetDestIP())

        # Get the current version of the firmware
        version: Version = device.get(GetVersion())


Making Changes & Contributing
=============================

Any ideas on how to improve this library are welcome. Please see the `Contributing`_ guide for
a full run-down on how to contribute to this project as well as some tips for
making sure your idea is added.

We thank you in-advance for your contributions.

Note
====

This project has been set up using PyScaffold 4.1.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.


.. TODO: Point link at RTD
.. _documentation: https://www.google.com/
.. _Contributing: https://github.com/ponoor/python-step-series/blob/main/CONTRIBUTING.rst
