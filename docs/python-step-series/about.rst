.. _python_step_series:

#################
API Documentation
#################

Welcome to the documentation for ``python-step-series``! Read this page to learn how to install and
develop your first application to configure and control a STEP-series device.

.. note:: Before you begin, please make sure to read the STEP400/STEP800 tutorial on the side!

********
Overview
********

``python-step-series`` is a library built to provide an easy-to-use programmatic interface for
configuring and controlling motors using the STEP400 or STEP800. As stated in the
``STEP400/STEP800`` tutorial, there are other third-party applications that can be used to perform
the same actions that this library does.

By the end of this tutorial, you'll have installed the library and learned how to properly use it.

************
Installation
************

.. note:: This section is only applicable for end-users of this library. Aspiring contributors
    should review the CONTRIBUTING guide found on the Github for this library.

The recommended method of installing ``python-step-series`` is using Python's ``pip`` in a
``virtualenv``:

.. code-block:: shell

    pip install virtualenv
    virtualenv -v my-venv
    source my-venv/bin/activate
    # Windows users: .\my-venv\Scripts\activate

    pip install python-step-series

And that is it! You can verify the installation by merely importing the library:

.. code-block:: python

    import stepseries

.. note:: New terminals will not have your virtualenv active. You'll need to rerun the `activate`
    command above in order to reactivate the environment.

To deactivate the environment, simply run the command:

.. code-block:: shell

    deactivate

***********
First-Steps
***********

As stated before, ``python-step-series`` strives to be as easy-to-use as possible. For example, it
takes four lines of code to establish communication with either device:

.. code-block:: python

    # Import the commands module. Commands are essentially templates
    # that need to be filled with data. This ensures you only have to
    # worry about WHAT to send, not how.
    from stepseries import commands

    # Import the interface class. This class is what is used to send and
    # receive data with the physical device.
    from stepseries.step400 import STEP400  # Replace "400" with "800" if you have a STEP800

    # Set-up and configure the library for communication with the device
    device = STEP400(1, "10.0.0.101")

    # Establish communication with the device
    device.set(commands.SetDestIP())

Sending ``commands.SetDestIP()`` is required each time you establish communication with the device.

************************************
Understanding Commands and Responses
************************************

``Commands`` are used to control the device whereas ``Responses`` are
returned by the device. The library presents both as dataclass objects
to give you what is essentially a template to fill or a structured
response.

Commands exist in the ``commands`` module of the library, hence why we had to import it above.
Likewise, responses exist in the ``responses`` module.

***************
Using Callbacks
***************

``python-step-series`` provides support for a callback architectured application. You can "bind"
callbacks, or multiple callbacks, to a response which will then be called when it is sent by a
device.

For example:

.. code-block:: python

    from stepseries import commands, responses, step400

    def version_handler(message: responses.Version) -> None:
        print("Firmware:")
        print(" - Name:", message.firmware_name)
        print(" - Version:", message.firmware_version)
        print(" - Compiled:", message.compile_date)

    device = step400.STEP400(1, "10.0.0.101")
    device.set(commands.SetDestIP())

    # Call 'version_handler' when a 'Version' response is sent
    device.on(responses.Version, version_handler)

    # Get the current version of the firmware
    # Notice that the code in 'version_handler' will be printed to your
    # console
    # Also note that the response is returned by the function call while
    # being sent to the handler
    version = device.get(commands.GetVersion())

You can also bind all responses to a callback:

.. code-block:: python

    from stepseries import commands, responses, step400

    def default_handler(message: OSCResponse) -> None:
        print("Message received:", message)

    device = step400.STEP400(1, "10.0.0.101")
    device.set(commands.SetDestIP())

    # Call 'default_handler' when any response is sent by the device
    device.on(None, default_handler)  # None means send everything

    device.get(commands.GetVersion())
    device.get(commands.GetStatus(motor_id=1))

The callback API of ``python-step-series`` allows you to be as simple or complex as you need. The
possibilities are virtually endless.

We hope this short tutorial has given you a nice overview of what the library offers. We recommend
you check out the Modules page to see what commands and responses you have available to you.
