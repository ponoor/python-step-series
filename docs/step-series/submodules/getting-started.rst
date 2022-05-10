***************
Getting Started
***************

=============
Example Files
=============

The STEP400 and STEP800 both communicate via the ``Open Sound Control`` (OSC) `protocol`_.
Beyond just ``python-step-series``, a myriad of applications can also communicate with these
devices, so example configuration and setup files are provided in the list below:

- `Max`_ (recommended, `download`_)
- `Processing`_ (thanks `@yuskegoto`_)
- `openFrameworks`_ (thanks `@niimi`_)
- `Unity`_ (thanks `@niimi`_)
- `Touch Designer`_ (thanks `@loveandsheep`_, `@yuskegoto`_)
- `Node-RED`_ (thanks `@yuskegoto`_)

======
Wiring
======

-------------
Communication
-------------

Both devices communicate via Ethernet, meaning your computer must have an ethernet port or a
USB-ethernet converter. This tutorial will assume you have connected the device directly to your
PC (peer-to-peer); however, if this is not possible for you, then plugging the device into a network
switch is also viable.

Please plug the ethernet cable in now.

.. warning:: Ensure your switch is actually a switch. Do not plug these devices into a router as
    router ports behave differently than switch ports do.

.. note:: Please do not power the device until directed to do so later in the tutorial. You will be
    asked to connect the power supply in the upcoming sections, but make sure it is **not** on.

--------------
Stepper Motors
--------------

Only 4-wire, bipolar stepper motors can be used with these devices. As an example, a highly
accessible and inexpensive stepper motor is Mercury Motor's ``SM-42BYG011-25``. This tutorial
assumes you are using this motor, so, if you are not, you may need to watch out for specific
settings that may need to be changed to match the motor you have. The ``SM-42BYG011-25`` can be
purchased from one the (unaffiliated) recommended sites below:

- `Sparkfun`_
- `Strawberry Linux`_
- `Akizuki Denshi`_

.. image:: /img/09238-01.jpg


From the wiring diagram found in the `datasheet`_ for this motor, we can see that the wiring pairs
are ``Red - Green`` and ``Yellow - Blue``.

.. image:: /img/motor-wiring-diagram-sample.png

The wiring to the terminal block should look like this:

.. image:: /img/SM-42BYG-wiring-700x525.jpg

We've calculated register values for some motors and made them available as `configuration files`_.

------------
Power Supply
------------

The STEP400 and STEP800 both have differing power ratings. These devices also have two different
power input terminals. While the USB-C jack can be considered a power input terminal, it's primary,
and arguably sole purpose, is to provide USB communication. By design, the USB protocol can only
supply of maximum of 5V which is not enough to fully power the board. It is, however, safe to power
both devices through either primary input (4 and 5 in the picture below) and have USB connected,
but **do not** connect power to both primary inputs.

.. note:: Again, make sure not to power the device. You may connect the supply, but make sure it is
    not on.

.. image:: /img/step400_connectors_numbering.jpg

====== ========================================
Number Description
====== ========================================
1      Electromagnetic brake terminal (STEP400)
2      Ethernet Port
3      USB-C Port
4      (Primary Power Input) DC Barrel Plug
5      (Primary Power Input) Screw Terminal
====== ========================================

.. warning:: Again, **do NOT** connect both 4 and 5. This will damage your controller.

As stated above, both devices have different power ratings and different ratings for each primary
input.

========== ====================== =========== ==============
Controller Board Max Power Rating Barrel Jack Screw Terminal
========== ====================== =========== ==============
STEP400    12V-76V @ 20A          24V @ 5A    76V @ 20A
STEP800    9V-36V @ 16A           24V @ 5A    36V @ 16A
========== ====================== =========== ==============

The amps listed here reflect the cumulative maximum phase current draw of all motors, not the
maximum current capacity of the power supply. Look at :ref:`Current Capacity` for more information.
The STEP800 has a maximum phase current draw of 2A per motor whereas the STEP400 has a maximum of
5A. Please keep these limits in mind when choosing your motor.

^^^^^^^^^^^^^^
DC Barrel Plug
^^^^^^^^^^^^^^

The DC barrel has the following specifications beyond its power rating:

- 5.5mm outer diameter
- 2.1mm inner diameter
- Center positive

^^^^^^^^^^^^^^
Screw Terminal
^^^^^^^^^^^^^^

The screw terminal has the following specifications beyond its power rating:

- Negative left side, positive right side
- M3 screw diameter
- Use a wire terminal like the ``NICHIFU TMEX1.25-3N`` for a more secure connection

------------------------------------
Power Supply & Stepper Motor Ratings
------------------------------------

^^^^^^^^^^^^^^^^^^
Current vs Voltage
^^^^^^^^^^^^^^^^^^

The copper windings inside a stepper motor behave as an inductor. When power is supplied to the
inductor, current rises gradually--it is not instant. Stepper motors that operate through the ON/OFF
cycle see decreased current the faster they move because the current cannot reach its maximum.
Because the motor's torque is virtually proportional to it's phase current, that means higher speeds
means lower torque.

^^^^^^^^^^^^^^^^^^^^^^^
Overcoming the Tradeoff
^^^^^^^^^^^^^^^^^^^^^^^

To overcome this tradeoff, you need to use a power supply with a high voltage rating. Remember, both
boards have their maximum voltages, so keep that in mind when choosing a supply. To better
articulate this point, see the following graph and note the correlation between a higher voltage
providing higher current (aka torque) and a higher maximum speed.

.. image:: /img/motor_current_example_graph-800x570.png

The required voltage varies greatly depending on the motor's rating, required speed, and required
torque. But, in general, the required voltage is roughly as follows:

- NEMA17 and under: 24V
- NEMA23 and bigger: 48V (or 72V for high speed)

This means the STEP800 may not be suitable for driving larger motors; however, some motors may
produce high torque in a small form factor and vice versa with a large form factor. **It's
imperative you review your motor's voltage and current ratings.**

The STEP400 does work with a minimum of 12V; however, since that is its on-board DC-DC converter's
minimum required voltage, there may be cases where the STEP400 resets on a slight voltage drop. This
is especially the case during a motor's inrush current, therefore we do not recommend a 12V power
supply unless if you are driving a small motor at a low load.

.. figure:: /img/update-48V-configuration-800x533.jpg

    A STEP400 being supplied 48V through two 24V power supplies in series.

^^^^^^^^^^^^^^^^
Current Capacity
^^^^^^^^^^^^^^^^

The current capacity of the power supply is as equally important as its voltage. If a motor stalls
it may draw a high amount of current that may exceed the capacity of the power supply. This will
cause the overload protection circuit on the supply to trigger (if there is one) forcing the supply
to shut down. Typically, you will likely need to only supply a few amps to drive small motors at low
speeds. But large motors at high speeds often do require high voltage with high current (especially
if they are under load). Depending on the quantity of motors, their usecases, as well as your
circuit protection settings, we recommend a supply with at least 10A-20A capacity.

==========
Networking
==========

------------------
Configuration Tool
------------------

Both devices do have a microSD card slot included on the board. Using this slot, you can just about
completely configure the device using our convenient `Configuration Tool`_. This tool is a webpage,
that can be accessed through your browser--so no third party software is required.

This tutorial uses default settings, so we will not be using the microSD card. Just leave the slot
empty.

.. note:: If you are connecting the board through a network switch that is connected to an existing
    VLAN, you may need to use the configuration tool to pre-configure the device's network settings
    and override those that will be set by the DIP switches as described below.


------------
Dip Switches
------------

The DIP switches on the board must be set to 1. This means only the left-most switch is ON and the
rest are OFF. With this configuration, the board has the following network settings:

============== ========== ======================================================
Name           Value      Description
============== ========== ======================================================
IP Address     10.0.0.101 The IP address of the device
Server Address 10.0.0.10  The IP address of the server (i.e. your PC)
Local Port     50000      The port the device is listening on
Server Port    50101      The port on the server that the server is listening on
============== ========== ======================================================

.. figure:: /img/IMG_0704.jpg

    Configured DIP switches on the STEP400.

Now with the motor, power supply, and ethernet cord connected; and the DIP switches set, you may now
power-on the device. Please remember the bottom side of the board does have high-voltage and
high-current pins, so either place the board on non-conductive material or attach spacers to avoid
damaging the board or hurting yourself.

----------------
PC Configuration
----------------

As seen in the table above, the device will expect your PC (server) to exist at a certain IP
address. If you need to, you can set it statically by reviewing the guides linked below:

=============== =============
Name            Value
=============== =============
IP Address      10.0.0.10
Subnet Mask     255.255.255.0
DNS             <Leave Empty>
Default Gateway <Leave Empty>
=============== =============

- `Windows`_
- `Mac`_
- `Linux`_

======================
Running Basic Commands
======================

------------------------
Verifying the Connection
------------------------

After configuring the above settings, you can verify your connection by running ``ping 10.0.0.101``
from your terminal (Command Prompt on Windows).

From this point forward, how you send commands to the device will completely depend on if you're
using ``python-step-series`` or one of the programs listed in :ref:`Example Files`. This tutorial
will describe each command and provide the code for ``python-step-series``; however, it will be up
to you to determine how to send the commands through your program of choice.

Before sending configuration commands to the device, you must first send the command ``/setDestIp``.
This tells the device where response messages will be sent. Until this command is received by the
device, it will not send any OSC messages beyond ``/booted``. This is because operation may become
unstable if the device continues to send OSC messages to a non-existent destination. You will
receive the following response from the device if ``/setDestIp`` was received without issue:
``/destIp octet1 octet2 octet3 octet4 isNewDestIp`` where ``octet<N>`` corresponds to each number
between the dots in your PC's IP address and ``isNewDestIp`` will indicate if the dest ip has
changed (``1``) or not (``0``).

For ``python-step-series``, the code may look like this:

.. code-block:: python

    from stepseries import commands
    from stepseries.step400 import STEP400

    device = STEP400(1, "10.0.0.101", 50000, "0.0.0.0", 50101)
    device.on(None, lambda x: print(x))

    device.set(commands.SetDestIP())

    >>> DestIP(address="/destIp", destIp0="10", destIp1="0", destIp2="0", destIp3="10")

We are now ready to configure and control the device.

---------------------
Get the Motor Running
---------------------

Let's send the command to run the motor at a desired speed: ``/run (int)motorID (float)speed``.

``motorID`` specifies which motor to run (1-4 on the STEP400, 1-8 on the STEP800). Each ID is
printed on the board for your convenience. Specifying ``255`` will indicate to run all motors at
your desired speed and is a valid parameter for almost every command requiring ``motorID``.

``speed`` specifies the speed and direction of the motor. The range you can set is from -15625.0 to
15625.0 steps/second. If you're using a motor with 200 steps per revolution, specifying ``200.0``
will run the motor at 1 revolution per second (RPS). Negative values will run the motor backwards.

For example, to run an ``SM-42BYG011-25`` at 1 RPS, the command ``/run 1 200`` can be sent.

.. code-block:: python

    # For python-step-series
    device.set(commands.Run(1, 200))

Is the motor now slowly spinning? If there is an issue, or you would like to stop it, set the speed
to 0 using the ``/run`` command or send  ``/hardHiZ 255``:

.. code-block:: python

    # For python-step-series
    device.set(commands.HardHiZ(255))

.. warning:: Do **not** disconnect the motor while it is active and running. This will damage your
    board.


If everything succeeded, then congratulations! You've successfully ran your first motor. But, you
may have noticed the motor ran a little rough--lots of vibration and possibly noisy. This is where
``KVAL`` and ``TVAL`` come in.

------------
Setting KVAL
------------

In most cases, the reason for rough operation of a motor is insufficient, or excessive, drive
voltage. The KVAL register sets this voltage on a scale of 0-255 where 0 means no voltage
(cannot move) and 255 is the same as your supply voltage. So, if you have a 24V supply, the motor
will run on 24V at 255, or 12V for 128, and so-on.

Each parameter in the ``/setKVAL`` command has a unique function.

======== =================== =============
Name     Description         Initial Value
======== =================== =============
holdKVAL Holding KVAL        0
runKVAL  Constant speed KVAL 16
accKVAL  Acceleration KVAL   16
decKVAL  Deceleration KVAL   16
======== =================== =============

Let's adjust these values while the motor is running. Send the command ``/run 1 200``.

.. code-block:: python

    # For python-step-series
    device.set(commands.Run(1, 200))

You can set individual KVAL parameters using commands like ``/setRunKval``, but we are going to set
all 4 parameters at once. Let's set ``holdKVAL`` to ``0`` and then gradually increase each of the
other three simultaneously. To do this, send the command ``/setKval 1 0 24 24 24``. The syntax of
the command is ``/setKval (int)motorID (int)holdKVAL (int)runKVAL (int)accKVAL (int)decKVAL``.

.. code-block:: python

    # For python-step-series
    device.set(commands.SetKval(1, 0, 24, 24, 24))

This message specifies the first motor's ``holdKval`` as 0 and the rest at 24 (approximately 9% of
your power supply voltage). Gradually increase the values until the motor begins to turn quietly.
For example: ``/setKval 1 0 32 32 32``, then ``/setKval 1 0 40 40 40``, etc.

.. code-block:: python

    # For python-step-series
    device.set(commands.SetKval(1, 0, 32, 32, 32))

    # then
    device.set(commands.SetKval(1, 0, 40, 40, 40))

    # etc...

As you increase each parameter, the motor's torque will also increase; however, the motor will also
begin to vibrate more and produce more heat. Be sure to set the parameters appropriately for your
load.

.. tip:: Remember: we've already calculated `configuration files`_ for a variety of motors for you
    if you would like to use them.


.. _protocol: http://opensoundcontrol.org/
.. _プロトコル: http://opensoundcontrol.org/

.. _datasheet: https://www.sparkfun.com/datasheets/Robotics/SM-42BYG011-25.pdf
.. _データシート: https://www.sparkfun.com/datasheets/Robotics/SM-42BYG011-25.pdf


.. _Max: https://github.com/ponoor/step-series-example-Max
.. _Processing: https://github.com/yuskegoto/STEP400_Processing
.. _openFrameworks: https://github.com/ponoor/step-series-example-openFrameworks
.. _Unity: https://github.com/ponoor/step-series-example-Unity
.. _Touch Designer: https://github.com/ponoor/step-series-example-TouchDesigner
.. _Node-RED: https://github.com/yuskegoto/STEP400_Node-RED

.. _download: https://cycling74.com/downloads

.. _@yuskegoto: https://github.com/yuskegoto
.. _@niimi: https://github.com/niimi
.. _@loveandsheep: https://github.com/loveandsheep

.. _Sparkfun: https://www.sparkfun.com/products/9238
.. _Strawberry Linux: http://strawberry-linux.com/catalog/items?code=12026
.. _Akizuki Denshi: https://akizukidenshi.com/catalog/g/gP-05372/
.. _秋月電子通商: https://akizukidenshi.com/catalog/g/gP-05372/

.. _configuration files: https://ponoor.com/en/docs/step-series/settings/example-parameter-values-for-example-steppers/
.. _設定ファイル: https://ponoor.com/en/docs/step-series/settings/example-parameter-values-for-example-steppers/

.. _Configuration Tool: http://ponoor.com/tools/step400-config/
.. _設定ツール: http://ponoor.com/tools/step400-config/

.. _Windows: https://support.microsoft.com/en-us/windows/change-tcp-ip-settings-bd0a07af-15f5-cd6a-363f-ca2b6f391ace
.. _Mac: https://support.apple.com/en-us/HT202480
.. _Linux: https://www.youtube.com/watch?v=Yr6qI6v1QCY

.. _Soundhouse's Documentation: https://www.soundhouse.co.jp/howto/light/dmx-dip/
.. _ディップスイッチによるチャンネル設定: https://www.soundhouse.co.jp/howto/light/dmx-dip/
