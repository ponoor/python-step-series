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
* Occasionally, the Arduino Zero may fail to write. In case this
  happens, try double-clicking the RESET switch and putting the board in
  bootloader mode. Then try uploading again. In this mode, the sketch
  will not boot and the LED ``L`` will begin to fade. You also have to
  reselect a different serial port.


==================
Diagnosing via USB
==================

Apart from uploading new firmware, the USB-C port on the device is also
used to debug and monitor.

.. note:: The USB-C port only powers the Arduino portion of the device.
  If you wish to run any motors, be sure to also connect (only) one of
  the primary power inputs.

.. note:: If providing supplemental power, be sure to connect the USB-C
  cable last (or press RESET after doing so). Because the motor
  controllers will be in an unknown state if this process is flipped,
  you may encounter undefined behavior.

--------------
Serial Monitor
--------------

This portion of the tutorial assumes you're using the Arduino IDE. Any
serial port terminal client that can send and receive text strings can
also be used.

^^^^^^^^^^^^^^^^^^
Selecting the Port
^^^^^^^^^^^^^^^^^^

**Tools** > **Port** > **COMXXX (Arduino Zero (Native USB Port))**

.. image:: /img/selecting-the-port.png


^^^^^^^^^^^^^^^^^^^
Open Serial Monitor
^^^^^^^^^^^^^^^^^^^

The Serial Monitor is what you use to communicate the with device.
Opening this tool can be done in a few ways.

First way: Click the magnifying glass

.. image:: /img/openserialmonitor-486x525.png

Second way: **Tools** > **Serial Monitor**

Third way: **CTRL + SHIFT + M**

^^^^^^^^^^^^^^
Diagnosis Menu
^^^^^^^^^^^^^^

With the Serial Monitor now open, ensure that the baud rate is set to
115200. Changing the baud rate may cause the board to reset, so keep
that in mind if a load is connected to your board--it may fall.

Next, type the letter *m* and press *Enter* or click **Send**. You
should now see something like the following:

.. image:: /img/diagnosis-menu.png


^^^^^^
Status
^^^^^^

Sending *s* allows you to retrieve it's hardware status.

The first output block you will see is the firmware information on the
MCU.

.. code-block:: text

  ============== Current Status ==============
  -------------- Firmware --------------
  Firmware name : STEP400
  Firmware version : 1.0.0
  Compile date : Mar 19 2021, 10:27:55
  Applicable config version : 1.0
  Loaded config version : 1.0 [CONFIG_VERSION_APPLICABLE]

``Loaded config version`` shows the config.txt version number read
from the microSD card. Depending on the version of the config and the
firmware, you'll get one of the following messages:

========================= ==========================================================================
Message                   Description
========================= ==========================================================================
CONFIG_VERSION_UNDEFINED  Unknown config version
CONFIG_VERSION_NOTLOADED  The config could not be read from the microSD card
CONFIG_VERSION_NOTLOADED  The config version is old
CONFIG_VERSION_APPLICABLE The config and firmware versions matched
CONFIG_VERSION_NEW        The config file's version is newer than the firmware (the firmware is old)
========================= ==========================================================================

Next output is the DIP Switch.

.. code-block:: text

  -------------- DIP Switch --------------
  BIN : 0000 0001
  DEC : 1

- ``BIN``: The current positions of all switches on the board. Please note
  that on the board, the left-most position is the right-most position
  here in tool.
- ``DEC``: The decimal representation of the switch.

Ethernet status is shown next.

.. code-block:: text

  -------------- Ethernet --------------
  Ethernet hardware status: 3 -EthernetW5500
  Ethernet link status: 2 -LinkOff
  isDestIpSet : No

- ``Ethernet hardare status``: The status of the built-in ethernet
  controller. If everything is worker, ``EthernetW5500`` will be shown.
  ``EthernetNoHardware`` indicates an issue is present.
- ``Ethernet link status``: The status of the ethernet cable. ``LinkOn``
  and ``LinkOff`` are self-explanatory. If ``Unknown`` is present, that
  indicates an issue with the controller is likely present.
- ``isDestIpSet``: Shows if ``/setDestIp`` has been recieved.

And finally, the status for the microSD card is shown.

.. code-block:: text

  -------------- microSD --------------
  SD library initialize succeeded : Yes
  SD config file open succeeded : Yes
  SD config JSON parse succeeded : Yes

- ``SD library initialize succeeded``: ``No`` if the card is not
  inserted.
- ``SD config file open succeeded``: Shows if ``config.txt`` was
  successfully opened on the card.
- ``SD config JSON parse succeeded``: Shows if the content of
  ``config.txt`` (JSON) was read correctly.

We now move into status information for the motor driver chips.

``STEP400 Only``

.. code-block:: text

  -------------- Motor Driver --------------
  PowerSTEP01 SPI connection established : Yes
  PowerSTEP01 ID#1
      STATUS: 0xE603
      High impedance state : Yes
      BUSY : No
      Motor direction : Reverse
      Motor status : Stopped
      UVLO (Undervoltage lock out) : No
      Thermal status : Normal
      OCD (Overcurent detection) : No
      Stalled : No
      SW_F: 0 -HOME senser input open.
      ADC_OUT: 31 -LIMIT senser input open.
  PowerSTEP01 ID#2
      ...
  PowerSTEP01 ID#3
      ...
  PowerSTEP01 ID#4
      ...

If communication with the PowerSTEP01 driver chips is unsuccessful
because the chips are unpowered, for example, ``PowerSTEP01 ID#<1-4>``
will not be shown.

``STEP800 Only``

.. code-block:: text

  -------------- Motor Driver --------------
  L6470 SPI connection established : Yes
  L6470 ID#1
      STATUS: 0x7E03
      High impedance state : Yes
      BUSY : No
      Motor direction : Reverse
      Motor status : Stopped
      UVLO (Undervoltage lock out) : No
      Thermal status : Stopped
      OCD (Overcurent detection) : No
      Stalled : No
      SW_F: 0 -HOME senser input open.
  L6470 ID#2
      ...
  L6470 ID#3
      ...
  L6470 ID#4
      ...
  L6470 ID#5
      ...
  L6470 ID#6
      ...
  L6470 ID#7
      ...
  L6470 ID#8
      ...

Like the STEP800 above, ``L6470 ID#<1-8>`` will only be shown if
connection to the driver chips was successful.

Next are the modes and electromagnetic brake and homing statuses.

.. code-block:: text

  -------------- Modes --------------
  Servo Mode :  No, No, No, No
  Current Mode :  No, No, No, No
  Electromagnetic Brake Enable :  No, No, No, No
  Brake status :
  #1 : BRAKE_ENGAGED
  #2 : BRAKE_ENGAGED
  #3 : BRAKE_ENGAGED
  #4 : BRAKE_ENGAGED
  Homing status : 0, 0, 0, 0

======================= ==============================
Brake status	          Description
======================= ==============================
BRAKE_ENGAGED	          Brake is engaged
BRAKE_DISENGAGE_WAITING	In transition to brake release
BRAKE_DISENGAGED	      Brake released
BRAKE_MOTORHIZ_WAITING	In transition to brake engage
======================= ==============================

== ================ ==================================
ID Homing status    Description
== ================ ==================================
0  HOMING_UNDEFINED Not homing yet
1  HOMING_GOUNTIL   Moving towards sensor
2  HOMING_RELEASESW Leaving from sensor active area
3  HOMING_COMPLETED Homing completed
4  HOMING_TIMEOUT   Time out was detected while homing
== ================ ==================================

^^^^^^
Config
^^^^^^

By entering the letter *c*, you are able to retrieve the current
configurations of the board. Note that the output reflects the current
settings on the device, not what is loaded on the microSD card if you
have one inserted.

For example, the following output may shown if the STEP400 is booted
without a microSD card:

.. code-block:: text

  ============== Configurations ==============
  -------------- Config file --------------
  SD config file open succeeded : No
  SD config file parse succeeded : No
  configTargetProduct : ---
  configName : Default
  config version : -1.0 [CONFIG_VERSION_NOTLOADED]
  -------------- Network --------------
  My Ip : 10.0.0.101
  isMyIpAddId : Yes
  Dest Ip : 10.0.0.10
  DNS : 10.0.0.1
  Gateway : 10.0.0.1
  Subnet mask : 255.255.255.0
  MAC address : 60:95:CE:10:05:01
  isMacAddId : Yes
  inPort : 50000
  outPort : 50101
  isOutPortAddId : Yes
  bootedMsgEnable : Yes
  isDestIpSet : No
  reportErrors : Yes
  -------------- Report & Alarm --------------
  reportBUSY :  No, No, No, No
  reportBUSY :  No, No, No, No
  reportHiZ :  No, No, No, No
  reportHomeSwStatus :  No, No, No, No
  reportLimitSwStatus :  No, No, No, No
  reportDir :  No, No, No, No
  reportMotorStatus :  No, No, No, No
  reportSwEvn :  No, No, No, No
  reportUVLO :  Yes, Yes, Yes, Yes
  reportThermalStatus :  Yes, Yes, Yes, Yes
  reportOCD :  Yes, Yes, Yes, Yes
  reportStall :  Yes, Yes, Yes, Yes
  reportOCD :  Yes, Yes, Yes, Yes
  OCThreshold : 15, 15, 15, 15
  -------------- driverSettings --------------
  homingAtStartup :  No, No, No, No
  homingDirection(1:FWD,0:REV) : 0, 0, 0, 0
  homingSpeed : 50.00, 50.00, 50.00, 50.00
  homeSwMode : 1, 1, 1, 1
  prohibitMotionOnHomeSw :  No, No, No, No
  limitSwMode : 1, 1, 1, 1
  prohibitMotionOnLimitSw :  No, No, No, No
  goUntilTimeout : 10000, 10000, 10000, 10000
  releaseSwTimeout : 10000, 10000, 10000, 10000
  microStepMode : 7, 7, 7, 7
  isCurrentMode :  No, No, No, No
  slewRate : 5, 5, 5, 5
  electromagnetBrakeEnable :  No, No, No, No
  brakeTransitionDuration : 100, 100, 100, 100
  -------------- speedProfile --------------
  acc : 1000.00, 1000.00, 1000.00, 1000.00
  dec : 1000.00, 1000.00, 1000.00, 1000.00
  maxSpeed : 650.00, 650.00, 650.00, 650.00
  fullStepSpeed : 15610.00, 15610.00, 15610.00, 15610.00
  -------------- Voltage mode --------------
  kvalHold : 0, 0, 0, 0
  kvalRun : 16, 16, 16, 16
  kvalAcc : 16, 16, 16, 16
  kvalDec : 16, 16, 16, 16
  intersectSpeed : 1032, 1032, 1032, 1032
  startSlope : 25, 25, 25, 25
  accFinalSlope : 41, 41, 41, 41
  decFinalSlope : 41, 41, 41, 41
  stallThreshold : 31, 31, 31, 31
  lowSpeedOptimize : 20.00, 20.00, 20.00, 20.00
  -------------- Current mode --------------
  tvalHold : 0, 0, 0, 0
  tvalRun : 16, 16, 16, 16
  tvalAcc : 16, 16, 16, 16
  tvalDec : 16, 16, 16, 16
  fastDecaySetting : 25, 25, 25, 25
  minOnTime : 41, 41, 41, 41
  minOffTime : 41, 41, 41, 41
  -------------- Servo mode --------------
  kP : 0.06, 0.06, 0.06, 0.06
  kI : 0.00, 0.00, 0.00, 0.00
  kD : 0.00, 0.00, 0.00, 0.00


^^^^^^^^^^^
Test Motion
^^^^^^^^^^^

Motors can also be tested via the Serial Monitor by entering the letter
*t*. All motors will rotate 25600 steps, or one rotation at 200 steps
with 1/128 microstepping enabled.


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
