*********************
Technical Information
*********************

Advanced information regarding firmware and the actual hardware around
the boards is contained here. A basic understanding of programming
Arduinos and the Arduino IDE or PlatformIO with VSCode is assumed.

========
Firmware
========

Because the main control unit (MCU) is an Arduino Zero, the firmware is
actually an Arduino sketch. This means uploading the firmware is done
using the Arduino IDE or PlatformIO in VSCode.

The latest firware version can be viewed at this `GitHub Releases`_
page. The code itself lives in this `GitHub Repository`_ where it can be
downloaded for use throughout this module.

--------------------
Checking the Version
--------------------

Two methods exist to check the current version of the firmware:

* Using the OSC command ``/getVersion``
* Connecting a USB cable to the board and typing ``s`` in the
  Serial Monitor

^^^^^^^^^^^^^^^^^^^^^
Method 1: OSC Command
^^^^^^^^^^^^^^^^^^^^^

This method only requires you to send the ``/getVersion`` command to the
board. The resulting response will tell you the current version of the
firmware.

For example:

.. code-block:: shell

    /version "STEP800_R1_UNIVERSAL 1.0.1 Mar 24 2022 11:17:29"

^^^^^^^^^^^^^^^^^^
Method 2: Over USB
^^^^^^^^^^^^^^^^^^

Connect the USB-C cable to the board and to your PC. Then open Serial
Monitor in the IDE you're using. Send the command ``s`` and you should
receive a response containing the version.

For example:

.. code-block:: shell

    -------------- Firmware --------------
    Firmware name : STEP800_R1_UNIVERSAL
    Firmware version : 1.0.1
    Compile date : Mar 24 2022, 11:17:29

----------------------
Uploading New Versions
----------------------

^^^^^^^^^^^^^^^^^^^^^^^^^
Compiling with PlatformIO
^^^^^^^^^^^^^^^^^^^^^^^^^

The firmware is primarily developed using `PlatformIO`_. Each repository
has a dedicated directory you can open using the "Open Project" menu of
PlatformIO. All dependencies are automatically installed when you
compile the project for the first-time.

^^^^^^^^^^^^^^^^^^^^^^
Compiling with Arduino
^^^^^^^^^^^^^^^^^^^^^^

Using the Arduino IDE requires a bit of manual setup than PlatformIO. To
begin, the Arduino Zero board must be first installed in the IDE using
the Board Manager. This `Quickstart Page`_ is a great resource for how
to do this procedure.

Next, the following libraries need to be installed. Here's a page
describing how to `install libraries`_.

* `OSC Library`_
* `ArduinoJSON`_
* `Adafruit SleepyDog Arduino Library`_
* STEP400 only: `Ponoor PowerSTEP01 Library`_
* STEP800 only: `Ponoor L6470 Library`_

.. note:: There many OSC libraries that may be listed in the Library
    Manager. This project uses the library made by CNMAT and is listed
    as **OSC**. Note that the creators are listed as Adrian Freed and
    Yotam Mann, not CNMAT.

    .. image:: /img/OSC_library_manager.png


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Compiling/Uploading the Sketch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before compiling, ensure the ``.ino`` file is open and the board
"Arduino Zero (Native USB Port)" in Tools **>** Boards is selected for
the Arduino IDE.

PlatformIO should already be configured for this project, so no action
should be taken.

Now the firmware can be compiled and uploaded using either IDE.

^^^^^^^^^^^
Extra Notes
^^^^^^^^^^^

* As a safety precaution, the electromagnetic brake should be
  disconnected from the board. While uploading the firmware, defaults
  are sometimes reset which may lead to the load being held by the brake
  to be dropped.
* Connecting just the USB-C cable is not enough to power the motor
  driver chips on either board. So, while you can upload sketches and
  perform some basic commands on the board, no movement will be possible
  unless additional power is provided.
* Ocassionally, the Arduino Zero may fail to write. In case this
  happens, try double-clicking the RESET switch and putting the board in
  bootloader mode. Then try uploading again. In this mode, the sketch
  will not boot and the LED ``L`` will begin to fade. You also have to
  reselect a different serial port.


.. _GitHub Releases: https://github.com/ponoor/step-series-universal-firmware/releases/
.. _GitHub Repository: https://github.com/ponoor/step-series-universal-firmware
.. _PlatformIO: https://platformio.org/
.. _Quickstart Page: https://docs.arduino.cc/hardware/zero
.. _install libraries: https://docs.arduino.cc/software/ide-v1/tutorials/installing-libraries

.. _OSC Library: https://github.com/CNMAT/OSC
.. _ArduinoJSON: https://arduinojson.org/
.. _Adafruit SleepyDog Arduino Library: https://github.com/adafruit/Adafruit_SleepyDog
.. _Ponoor PowerSTEP01 Library: https://github.com/ponoor/Ponoor_PowerSTEP01_Library
.. _Ponoor L6470 Library: https://github.com/ponoor/Ponoor_L6470_Library
