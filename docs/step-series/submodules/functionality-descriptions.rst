**************************
Functionality Descriptions
**************************

This section delves deeper into what the different functionalities
offered by both boards are and what they do. Please refer to the
:ref:`Command Reference` for what commands to send to control these
different functionalities.

========================
Voltage vs. Current Mode
========================

There are two types of stepping control methods: constant voltage
control (**voltage mode**) and constant current control (**current
mode**). Only the STEP400 can switch between both voltage and current
modes. The difference between these modes is well-explained in
`this presentation PDF`_ by STMicroelectronics.

The differences can be described as follows:

-  Voltage mode is quiet and smooth, but is limited to lower speeds
-  Current mode is noisy, but can reach higher speeds

To better illustrate this point, here is a demonstration video to show
the differences between these two modes.

.. container:: voltage-vs-current-mode-video

    .. raw:: html

        <iframe width="560" height="315" src="https://www.youtube.com/embed/ydPHQfc22kQ" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

First, the motor runs under constant voltage mode. After around 800
steps/sec, the motor cannot run properly and starts to vibrate and
stalls at about 1,400 steps/sec. Overall, the motor runs quietly until
the vibration starts. A microphone is attached to the motor so that we
can capture the smallest noises.

Next, the motor is switched to constant current mode. It is noisy, but
can drive to a higher speed. In this mode, we were able to achieve more
than 11,000 steps/sec before the motor started to vibrate and stall.

=============
KVAL and TVAL
=============

**KVAL** register values are applied to control the drive voltage in
voltage mode; likewise, **TVAL** registers are used to control the drive
current in current mode. Both act as percentage multipliers to dictate
what percentage of the power supply voltage or current is sent to the
motors. Although they are the same registers internally in the driver,
our firmware keeps them separated and rewrites them when the modes are
changed.

=====================
Notes on Voltage Mode
=====================

In voltage mode, KVAL is used to set what percentage of the power supply
voltage should be applied to the motor. If a high voltage power source
is used, excessive current may flow when the motor is spinning at lower
speeds. To compensate this current imbalance, there is a group of
registers to lower the supplied drive voltage at low speeds and supply
higher voltages at higher speeds. The calculation of these register
values is described in `STMicroelectronic's application notes`_. In the
STEP400, these registers can be set with `/setBemfParam`_ command or
with the `Config Tool`_.

Additionally, we have calculated the register values for some motors
based on our actual measurements and have made them available as
`configuration files`_. We have only a small numbers of configuration
files at the moment, but we are planning to add more in the future. If
you have a motor that is not listed in the example files and have
determined these configurations on your own, we would deeply appreciate
you sharing your configurations with us and the community.

=====================
Notes on Current Mode
=====================

In current mode, which is only available on the STEP400, TVAL registers
are used to set the target current value. The current can be set up to
5A in increments of 78mA on the STEP400. You'll need a high voltage
power supply to deliver the target current when the motor is running at
high speed. Although the powerSTEP01's actual current drive capability
is 10A, the STEP400 has the upper rating limit of 5A due to the power
rating limitation of the current sensing resistor. At 5A phase current,
the torque is considerably strong, and the tiniest mistake may lead to
great physical danger. In such situations we recommend to use use an
industrial grade motor driver.

===========================
Switching Between the Modes
===========================

Use the following commands to switch between the modes:

- `/setVoltageMode`_ - switch to voltage mode
- `/setCurrentMode`_ - switch to current mode

The motor must be in the high impedance (High Z) state before switching
the mode. For example, if you are going to switch the Motor 1 to current
mode, send these commands in the following order:

1. ``/hardHiZ 1``
2. ``/setCurrentMode 1``

Microstepping is limited to a minimum of 1/16 in current mode. Any lower
value than 1/16 will be regarded as 1/16. When you change microstep
value, the coordinate system will also change. For example, for one full
shaft rotation of a 200 step motor in 1/128 microstepping mode,
200x128=25600 steps are made; but one rotation in 1/16 microstepping
mode is 200x16=3200 steps.

=============
Speed Profile
=============

--------
Overview
--------

Speed profile sets the acceleration (acc), deceleration (dec), and
maximum speed (maxSpeed) values of the motor prior to the motor moving.
These values depend on the following:

-  Motor Specifications
-  Power supply voltage
-  Load
-  Voltage mode or current mode

While we provide some example defaults, you need to set these values
according to your actual environment. This requires some trial and error
on your part.

-------------------
Setting the Profile
-------------------

Use `/setSpeedProfile`_ to set the above three values. Acc and dec
cannot be set unless the motor is stopped; however, maxSpeed can be set
at any time.

You can also set the minimum speed (minSpeed) with ``/setMinSpeed``. 
It is unlikely to be used for any actual application, but this speed 
will be used for ``/releaseSw`` speed as a part of the homing procedure.

========================
Types of Motor Operation
========================

--------------
Constant Speed
--------------

The `/run`_ command is used to drive the motor at a constant speed. The
acceleration, deceleration, and maximum speed curves set by
`/setSpeedProfile`_ are adhered to by this command. The motor runs
perpetually until speed 0 (``/run 0``) or a stop command is sent. The
motor will not run faster than the maximum speed set in the speed
profile. Sending a speed to run faster than this profile setting will
cause the motor's speed to be truncated to that setting. The motor will
be kept in the BUSY state during the acceleration and deceleration.

`/goUntil`_ and `/releaseSw`_ are also considered constant speed
commands.

-----------
Positioning
-----------

The trapezoidal drive towards the specified position is performed
according to the speed profile. In other words, it accelerates according
to the acceleration rate of the speed profile, then drives at constant
speed when it reaches the maximum speed, and then decelerates at
specified deceleration rate at the timing calculated backwards to stop
at the specified position. It may start decelerating before it reaches
the maximum speed, especially when you want to accelerate / decelerate
at a relatively slow rate. It remains in the BUSY state until the motor
stops. It's not possible to interrupt the current positioning motion
with another positioning motion.

Typical commands for positioning operation are ``/goTo`` and ``/move``. 
Other commands include ``/goHome``, ``/goMark``, and ``/goToDir``.

NOTE: With `STEP-series Universal Firmware`_, positioning motions 
(except /move) can interrupt another positioning motions.


----------
Servo Mode
----------

This is not a function of the motor driver, but a mode of driving
implemented in the firmware. It constantly updates the constant speed
operation to follow a given target position. This mode is similar to a
radio controlled servo motor. No other motor motion commands can be sent
while the motor is operating in this mode.

--------------
Types of Stops
--------------

There are two options with a total of four different commands, as
follows:

-  Decelerating according to the speed profile or stop instantly
-  Keeping magnetized/excited or entering a high impedance (High Z)
   state after stopping

================ ================= ==============
State after stop Deceleration stop Immediate stop
================ ================= ==============
Excited          SoftStop          HardStop
HiZ              SoftHiZ           HardHiZ
================ ================= ==============

The excited state is the state in which voltage or current (torque) is
maintained to hold the motor's position according to ``KVAL_HOLD`` or
``TVAL_HOLD``, respectively. The high impedance (HiZ) state is when
the current is cut off and no holding torque is maintained. **Any loads
the motor is moving may fall or lose their positioning during HiZ.**

======
Homing
======

When the system powers up, it doesn't know where the motor is currently
positioned. It could be pointing to various directions depending on the
timing of the last time the system was shut off.

Also, if the stepper motor receives exceeding external force, the step
will slip out of alignment (**stall**). If this happens, the motor will
continue to work with an unknown offset between the expected position
and its actual.

Therefore, applications that have position or orientation must use
sensors to detect a reference position on startup or periodically while
it is active. This action is called **homing**.

====================
Switches and Sensors
====================

.. figure:: /img/two-homing-sensors.png
   :alt: Two different configurations of a homing sensor

   Two different configurations of a homing sensor

Photointerrupters are often used as home sensors. On the left, a white
piece of plastic attached to the slider blocks the photointerrupter's
light-emitting and receiving parts. The right side is an example of a
rotary table where the photo interrupter responds to the black screw.

Other devices such as microswitches or photoelectric sensors are also
used for the sensing.

To make interfacing with these sensors and switches from the controller,
we provide `pre-made connection cables`_
(scroll all the way down to the bottom of the page when you click
"BUY").

======================
HOME and LIMIT Sensors
======================

Each axis of both the STEP400 and STEP800 has a HOME connector which can
connect sensors or switches. The STEP400 has LIMIT sensor inputs in
addition to HOME inputs. 5V is supplied to each connector for the
sensing power source.

----
HOME
----

This input is connected directly to the motor driver chip and can be
used in conjunction with the driver's homing function. Usually, this
connector is used for the home sensor.

--------------------
LIMIT (STEP400 Only)
--------------------

Some applications may require two sensors. For example, a slider has a
limited operating range and if it stalls during operation, it may
collide with one of either end. In such cases, installing sensors on
both ends of the slider will prevent collisions.

The motor can be set to force-stop when these sensors respond, but these
can also be used as simple switch inputs separated from the motor
operation. For example, you can connect a push button to one of them and
press to send an OSC message.

-----------------------------
Collision Prevention Settings
-----------------------------

You can limit the motor's rotate direction when the HOME or LIMIT
sensors are activated. With the commands `/setProhibitMotionOnHomeSw`_
and `/setProhibitMotionOnLimitSw`_, you can prohibit the actuator from
moving towards ``homingDirection`` when the HOME sensor is active, or
the reverse direction towards ``homingDirection`` when the LIMIT sensor
is active. With this, you can prevent the mechanism from colliding with
its bounds.

``homingDirection`` can be set with `/setHomingDirection`_ or
with the `Config Tool`_. This setting is also used for the `/homing`_
command.

.. figure:: /img/homingDirection-800x533.jpg
   :alt: Homing Direction

   Homing Direction

===============
Homing Commands
===============

The homing command is `/homing`_. This command consists
of two commands, ``/goUntil`` and ``/releaseSw``, which are inherited
from the powerSTEP01/L6470 motor driver chip. Let's look closer at those
commands.

------------
`/goUntil`_
------------

First, use this command to move towards the home sensor. The motor will
decelerate and then stop when the home sensor activates (if it has been
set up as such).

--------------
`/releaseSw`_
--------------

This command slowly moves the motor in the opposite direction from the
current position and stops immediately when the HOME sensor reading is
no longer active. The position where the motor stops is the origin/home
position! However, strictly speaking, the ``/goUntil`` command does not
stop immediately, but stop after deceleration. Its current position has
a slight negative offset from the point where the sensor actually
responded. This is not accounted for in the firmware as every
environment is different.

Both commands can be configured to reset the current position to zero
the moment the sensor responds with `/setHomeSwMode`_.

To better illustrate this interaction, here is a demo video.

.. container:: homing-demo-video

   .. raw:: html

      <iframe width="560" height="315" src="https://www.youtube.com/embed/AydxbL6-a_g" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

----------
`/homing`_
----------

It is possible to send above two commands over OSC one after another,
however, the ``/homing`` command executes this sequence in single
operation. It will automatically complete the home sequence according to
the homing direction and homing speed which are pre-configured with the
`Config Tool`_ or with the commands `/setHomingDirection`_ and
`/setHomingSpeed`_, respectively.

---------------
Homing Timeouts
---------------

Both ``/goUntil`` and ``/releaseSw`` have pre-configured timeouts. When
either command times out--that is, the HOME sensor's state has not
changed after a period of time--the controller will halt the movement of
the motor. This is to prevent the moving part from being pushed against
other mechanical objects endlessly and for safety.

=================================
Normally Open and Normally Closed
=================================

----------------------
Electrical Connections
----------------------

Let's explore "sensor reaction” a little bit more in detail. The pin
assignments of HOME and LIMIT connectors are as follows.

========== ===================
Pin number Function
========== ===================
1          GND
2          Switch/Sensor input
3          5V Power Output
========== ===================

Each sensor pin (2) on HOME and LIMIT is pulled up to 3.3V. To connect
the switch, connect the GND (1) and the sensor terminal (2). When the
switch is pressed, it is connected to the GND pin and the voltage drops
from 3.3V to 0V. When the voltage changes from HIGH level to LOW level
(a.k.a. **Falling Edge**), the sensor is considered to have activated.

Let's take photo interrupter `EE-SX671A`_ as an example, where the
connection is as follows:

.. figure:: /img//ee-sx67.jpeg
   :alt: EE-SX671A Diagram

   EE-SX671A Diagram

========== =================== ==========
Pin number Function            Sensor pin
========== =================== ==========
1          GND                 -
2          Switch/Sensor input OUT
3          5V Power Output     +
========== =================== ==========

----------------------------
Light or No Light Activation
----------------------------

This is the part you need to consider carefully before ordering a
sensor.

.. figure:: /img/sensor_dark_light.png
   :alt: Dark on or Light on

   Dark activated or light activated

In the case of the left picture, the light enters into the sensor at the
home position, but in the picture on the right, the light is blocked at
the home position.

There are two types of sensors, one that turns on when light enters and
one that turns on when light is interrupted. In the case of the above
Omron sensor, the action is toggled by connecting the "L" and "+""
terminals.

The mechanism and sensor must be combined in such a way that the sensor
pin goes from HIGH to LOW at the home position.

-------------
Rotary Tables
-------------

In the left example on the picture above, the response position of the
home sensor will differ between clockwise and counterclockwise,
depending on the size of the hole. The controller can notify both HIGH to
LOW and LOW to HIGH changes of the home sensor by OSC messages. The
message also includes the rotation direction, so you can align the home
position if you write a conditional sequence for each rotation
direction. This reporting can be configured with `/enableHomeSwReport`_.

====================
Servo Mode Explained
====================

As stated above, servo mode is not a function native to the motor driver
chip on the board. While seemingly similar to positional commands, servo
mode commands allow you to define a new target position *while the motor
is moving*. This is not possible with positional commands which require
the position to be set in advance of the motor's movements. New
positional targets are not updated until after the current target is
reached. While this mode is active, other functional commands cannot be
sent.

.. container:: servo-mode-demo-video

   .. raw:: html

      <iframe width="560" height="315" src="https://www.youtube.com/embed/1dd_bBqWpMQ" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

*Example Behavior of Servo Mode*

---------------------------------
Initializing Steps for Servo Mode
---------------------------------

^^^^^^^^^^^^^^^^^
Toggling the Mode
^^^^^^^^^^^^^^^^^

The command `/enableServoMode`_ enables or disables Servo Mode. Upon
starting Servo Mode, the driver must not be in the BUSY state.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Updating the Target Position
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The target position can be updated by the `/setTargetPosition`_ command.
When the Arduino Sketch receives a new target position, it will compare
the new position with the current one and change the rotation speed of
the motor. Additionally, you can send target positions to all four
motors at the same time with `/setTargetPositionList`_.

===========================
Types of Control Parameters
===========================

The motor's rotation speed is calculated by a technique called "PID
Control". To better illustrate the purpose of PID, refer to the
following graph:

.. image:: /img/pid-control.jpg


Please refer to this graph when the control parameters are discussed
below. These parameters can be set with the command `/setServoParam`_.

----------------------
Proportional Gain (kP)
----------------------

PID control uses differences of current position and target position
(deviation) for the control. That is, it approaches the target position
by rotating faster when the deviation is large, and rotates slower when
the deviation is small. The proportional gain defines how much influence
to the speed will be given from the deviation. If the value is too
small, it will take time to approach the target position, and if the
value is too large, an "overshoot" may occur in which case the target
position is passed.

------------------
Integral Gain (kI)
------------------

If there is only the proportional control, the rotation speed will get
slower and takes very long time to compensate the offset when
approaching to the target position. In this case, adding the time
integral of the deviation to the control value will effectively
compensate the offset. By applying large integral gain, you could
compensate the offset quickly; however, it may cause the overshoot, or
even the continuous oscillation by trying to compensate the overshoot.

----------------------
Differential Gain (kD)
----------------------

In case an overshoot or oscillation related errors occurs, this
parameter is used to eliminate steep changes in deviation--that is to
say, it acts like a damper that continually decreases each oscillation.

======================================
Methods for Determining PID Parameters
======================================

-----------------------
Step by Step Procedures
-----------------------

PID Control Parameters must be determined from the actual acceleration,
deceleration, and the maximum rotation speed (speed profile). Determine
the control parameters by following these steps:

1. Decide the KVAL (in case of current mode, TVAL) that is matched to
   the rated value and load.
2. Decide the operational acceleration, deceleration, and the maximum
   rotation speed (speed profile).
3. Adjust the PID control gains.

---------------------------------
The Decisions of PID Control Gain
---------------------------------

There are multiple methods for deciding the optimal PID Control Gain.
However, it may also depend on the factors like the objective of
movement, or the frequency of target position change. Therefore we
determine the values by steps described as follows and do trial and
error on the actual set up.

-----
1. kP
-----

Set all kP, kI, kD, to 0.0 and gradually raise the kP until the motor
starts to oscillate around its target position. When the target
position changes only sometimes, we often set only kP while keeping
other kI and kD values at 0.0.

-----
2. kI
-----

In case when the target position only changing once every couple of
seconds, you set the movement to quick and responsive by raising the kI
value. Yet for example, when the target position is sent at 60fps, the
acceleration towards the each new target position would cause the
vibration and loose smooth transition. Depending on the priority of the
quickly response to the target position or smooth movement for the whole
operation, the preferable values may change.

-----
3. kD
-----

We gradually raise the kD if oscillation or overshoot is observed when
approaching the target.


.. _this presentation PDF: https://www.st.com/content/dam/AME/2019/developers-conference-2019/presentations/STDevCon19_3.6_Using%20Powerstep01.pdf
.. _プレゼンテーション資料: https://www.st.com/content/dam/AME/2019/developers-conference-2019/presentations/STDevCon19_3.6_Using%20Powerstep01.pdf

.. _フォーラム: https://github.com/ponoor/step-series-support/discussions

.. _STMicroelectronic's application notes: https://www.st.com/resource/en/application_note/dm00061093-voltage-mode-control-operation-and-parameter-optimization-stmicroelectronics.pdf
.. _アプリケーションノート: https://www.st.com/resource/en/application_note/dm00061093-voltage-mode-control-operation-and-parameter-optimization-stmicroelectronics.pdf

.. _/setBemfParam: https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setbemfparam_intmotorid_intint_speed_intst_slp_intfn_slp_acc_intfn_slp_dec
.. _Config Tool: http://ponoor.com/tools/step400-config/
.. _configuration files: https://ponoor.com/en/docs/step-series/settings/example-parameter-values-for-example-steppers/
.. _/setVoltageMode: https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setvoltagemode_intmotorid
.. _/setCurrentMode: https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setcurrentmode_intmotorid

.. _/setSpeedProfile: https://ponoor.com/en/docs/step400/osc-command-reference/speed-profile/#setspeedprofile_intmotorid_floatacc_floatdec_floatmaxspeed
.. _/run: https://ponoor.com/en/docs/step400/osc-command-reference/motor-control/#run_intmotorid_floatspeed
.. _/goUntil: https://ponoor.com/en/docs/step400/osc-command-reference/homing/#gountil_intmotorid_boolact_floatspeed
.. _/releaseSw: https://ponoor.com/en/docs/step400/osc-command-reference/homing/#releasesw_intmotorid_boolact_booldir
.. _STEP-series Universal Firmware: https://github.com/ponoor/step-series-universal-firmware
.. _pre-made connection cables: https://ponoor.com/en/products/sensor-cable/
.. _コネクタ取り付け済みケーブル: https://ponoor.com/en/products/sensor-cable/

.. _/setProhibitMotionOnHomeSw: https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#setprohibitmotiononhomesw_intmotorid_boolenable
.. _/setProhibitMotionOnLimitSw: https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#setprohibitmotiononlimitsw_intmotorid_boolenable
.. _/setHomingDirection: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#sethomingdirection_intmotorid_booldirection
.. _/setHomingSpeed: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#sethomingspeed_intmotorid_floatspeed
.. _/homing: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#homing_intmotorid
.. _/setHomeSwMode: https://ponoor.com/en/docs/step-series/osc-command-reference/home-limit-sensors/#sethomeswmode_intmotorid_boolsw_mode
.. _EE-SX671A: http://www.ia.omron.com/product/item/2219/
.. _/enableHomeSwReport: https://ponoor.com/en/docs/step-series/osc-command-reference/home-limit-sensors/#enablehomeswreport_intmotorid_boolenable

.. _/enableServoMode: https://ponoor.com/docs/step-series/osc-command-reference/servo-mode/#enableservomode_intmotorid_boolenable
.. _/setTargetPosition: https://ponoor.com/docs/step-series/osc-command-reference/servo-mode/#settargetposition_intmotorid_intposition
.. _/setTargetPositionList: https://ponoor.com/docs/step-series/osc-command-reference/servo-mode/#settargetpositionlist_intposition1_intposition2_intposition3_intposition4
.. _/setServoParam: https://ponoor.com/docs/step-series/osc-command-reference/servo-mode/#setservoparam_intmotorid_floatkp_floatki_floatkd
