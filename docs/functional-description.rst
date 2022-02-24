.. _step_series:

######################
Functional Description
######################

*****************************
Voltage mode and current mode
*****************************

==========================================================
The difference between voltage control and current control
==========================================================

There are two types of stepping motor control methods: constant voltage
control (**voltage mode**) and constant current control (**current
mode**). STEP800 can be used in voltage mode, while STEP400 can switch
between both voltage and current modes. The difference between these
modes is well-explained in `this presentation
PDF <https://www.st.com/content/dam/AME/2019/developers-conference-2019/presentations/STDevCon19_3.6_Using%20Powerstep01.pdf>`__
by STMicroelectronics.

The differences for the users can be described as follows;

-  Voltage mode is quiet and smooth, but can only drive at low speed.
-  Current mode is noisy, but can drive to higher speed.

Test with the STEP400
---------------------

Here is a video about: - The difference between constant voltage control
and constant current control - The difference between full-step and
micro-stepping drive

.. container:: embed-video

   .. raw:: html

      <iframe width="560" height="315" src="https://www.youtube.com/embed/ydPHQfc22kQ" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>

   .. raw:: html

      </iframe>

First, the motor runs under constant voltage control (hereinafter
referred to as “**voltage mode**”). After around 800 step/sec, the motor
cannot run properly and starts to vibrate, then it stalls at about 1,400
step/sec and stops completely. The motor runs quietly until the
vibration starts, but in this video, a microphone is attached to the
motor so that we can capture the smallest noise.

Next, the motor is switched to constant current control (hereinafter
referred to as “**current mode**”). It is noisy, but it can drive to
higher speed. In this setting, we were able to achieve more than 11,000
steps/sec.

KVAL and TVAL
-------------

**KVAL** register values are applied to control the drive voltage in the
voltage mode, and **TVAL** registers are used to control the drive
current in the current mode. Although they are actually same registers
in the driver, our firmware keeps them separated, rewrites them when
mode changes to avoid unintended values to be set.

Voltage mode setting
--------------------

In the voltage mode of the STEP400 or STEP800, registers called KVAL is
used to set what percentage of the power supply voltage should be
applied to the motor. Also if a high voltage power source is used,
excessive current may flow when the motor is spinning at lower speed. To
compensate this current imbalance, there is a group of registers to
lower the drive voltage at low speed and supply higher voltage at higher
speed. The calculation of these register values is described in the
`STMicroelectronics application
note <https://www.st.com/resource/en/application_note/dm00061093-voltage-mode-control-operation-and-parameter-optimization-stmicroelectronics.pdf>`__.
In STEP400, these registers can be set with
```/setBemfParam`` <https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setbemfparam_intmotorid_intint_speed_intst_slp_intfn_slp_acc_intfn_slp_dec>`__
command, and from the `Config
Tool <http://ponoor.com/tools/step400-config/>`__ as well.

We have calculated the register values for some motors based on our
actual measurements and have made them available as `configuration
files <https://ponoor.com/en/docs/step-series/settings/example-parameter-values-for-example-steppers/>`__.
We have only a small numbers of configuration files at the moment, but
we are planning to add more in the future.

Current mode setting
--------------------

In the current mode which available in STEP400, the TVAL registers are
used to set the target current value. The current can be set up to 5A in
increments of 78mA in the STEP400. Yo need a high voltage power supply
to deliver the target current when the motor is running at high speed.
Although the PowerSTEP01’s actual current drive capability is 10A, the
STEP400 has the upper rating limit of 5A due to the power rating
limitation of the current sensing resistor. At 5A phase current, the
torque is considerably strong, and the tiniest mistake may lead to great
physical danger. In such situations we recommend to use use an
industrial grade motor drivers.

Switching modes
---------------

These commands are available for switching between modes; -
```/setVoltageMode`` <https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setvoltagemode_intmotorid>`__
- switch to the voltage mode. -
```/setCurrentMode`` <https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setcurrentmode_intmotorid>`__
- switch to the current mode.

The motor must be in the high impedance (High Z) state before switching
the mode. For example, if you are going to switch the Motor 1 to current
mode, the command sequence is in the following order; 1. ``/hardHiZ 1``
1. ``/setCurrentMode 1``

The microstepping is limited to minimum 1/16 in current mode. Any lower
value than 1/16 will be regarded as 1/16. When you change the
microstepping mode, the coordinate system will also change. For example
one rotation in 1/128 microstepping mode is 200x128=25600 steps for a
200steps/round motor, but one rotation in 1/16 microstepping mode is
200x16=3200 steps.

***************************************
Speed profile and types of motor motion
***************************************

=============
Speed profile
=============

Overview
--------

The speed profile sets the acceleration, deceleration, and maximum speed values of the motion prior to the motor operation in advance. This depends on the following:

- Motor Specifications
- Power supply voltage
- Load (e.g. on a load cell)
- Voltage control or current control

You need to set these values according to your actual environment.

Values to be set
----------------

The three values, Acceleration(acc),deceleration(dec), and maxSpeed need
to be set. You can also set the minimum speed (minSpeed) as a function
of the motor driver, but it is fixed at 0 on the firmware because it is
unlikely to be used for the actual application.

Setting command
---------------

With
```/setSpeedProfile`` <https://ponoor.com/en/docs/step400/osc-command-reference/speed-profile/#setspeedprofile_intmotorid_floatacc_floatdec_floatmaxspeed>`__
command you can set above three values. The acc and dec cannot be set
unless the motor is stopped, the maxSpeed parameter can be set at
anytime.

=======================
Type of motor operation
=======================

Constant speed
--------------

This is the command to drive the the motor with the
acceleration/deceleration rate set by the speed profile, then maintains
constant speed. It continues to rotate until speed 0 is set, or stop
command is sent. The range of speed that can be set is limited to the
maximum speed of the speed profile. It will keep BUSY state during the
acceleration and deceleration. A representative command for the constant
speed drive is
```/run`` <https://ponoor.com/en/docs/step400/osc-command-reference/motor-control/#run_intmotorid_floatspeed>`__.
There are also
```/goUntil`` <https://ponoor.com/en/docs/step400/osc-command-reference/homing/#gountil_intmotorid_boolact_floatspeed>`__
and
```/releaseSw`` <https://ponoor.com/en/docs/step400/osc-command-reference/homing/#releasesw_intmotorid_boolact_booldir>`__
commands are available.

Positioning
-----------

The trapezoidal drive towards the specified position is performed
according to the speed profile. In other words, it accelerates according
to the acceleration rate of the speed profile, then drives at constant
speed when it reaches the maximum speed, and then decelerates at
specified deceleration rate at the timing calculated backwards to stop
at the specified position. It may start decelerating before it reaches
the maximum speed, especially when you want to accelerate / decelerate
relatively slow rate. It remains in the BUSY state until the motor
stops. It’s not possible to interrupt the current positioning motion
with another positioning motion.

Servo mode
----------

This is not a function of the motor driver, but a mode of driving
implemented in the firmware. It constantly updates the constant speed
operation to follow a given target position. This mode is similar to tje
radio controlled servo motor. No other motor motion commands can be sent
while the motor is operating in this mode.

Types of stops
--------------

There are two options with a total of four different commands, as
follows;

-  Decelerate according to the speed profile or stop instantly.
-  Keep magnetized / excited or goes to the high impedance(High Z) state
   after stop.

================ ================= ==============
State after stop Deceleration stop Immediate stop
================ ================= ==============
Excitation       SoftStop          HardStop
HiZ              SoftHiZ           HardHiZ
================ ================= ==============

The excited state is the state in which the torque is applied to hold
the motor position according to ``KVAL_HOLD``\ voltage, or current set
by the ``TVAL_HOLD`` value. The high impedance state is the state where
the current is cut off and there is no holding torque.

******************************
Homing and position management
******************************

========================
Stepper motor and homing
========================

When the system powers up, it doesn’t know where the motor is currently
positioned. It could be pointing to various directions depending on the
timing of the last time the system was shut off.

Also, if the stepper motor receives exceeding external force, the step
will slip out of alignment (**stall**). If this happens, the motor will
continue to work with offset between the programmed and its physical
position.

Therefore, applications that have position or orientation must use
sensors to detect a reference position on startup or periodically. This
action is called **homing**.

=================
Sensor and switch
=================

.. figure:: http://ponoor.com/manage/wp-content/uploads/2020/10/two-homing-sensors.png
   :alt: Two configuration of homing sensor

   Two configuration of homing sensor

Photointerrupters are often used as home sensors. On the left, a white
piece of plastic attached to the slider blocks the photointerrupter’s
light-emitting and receiving parts. The right side is an example of a
rotary table, where the photo interrupter responds to the black screw.

Other devices such as microswitches, or photoelectric sensors are also
used for the sensing.

============================
HOME sensor and LIMIT sensor
============================

Each axis of STEP400/STEP800 has HOME connector which can connect
sensors or switches. STEP400 has LIMIT sensor inputs in addition to HOME
inputs. 5V is supplied to each connector for the sensing power source.

HOME
----

This input is connected directly to the motor driver chip and can be
used in conjunction with the driver’s homing function. Usually, this
connector is used for the home sensor.

LIMIT (Only in STEP400)
-----------------------

Some applications may require two sensors. For example, a slider has a
limited operating range, and if it stalls during the operation, it may
collide with one of either end. In such cases, installing sensors on
both ends of the slider will prevent collisions.

The motor can be set to force-stop when these sensors respond, but these
can also be used as simple switch inputs separated from the motor
operation. For example, you can connect a push button to one of them and
press to send an OSC message.

Collision prevention setting
----------------------------

You can limit the motor rotate direction when HOME or LIMIT sensors are
active. With the
command\ ```/setProhibitMotionOnHomeSw`` <https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#setprohibitmotiononhomesw_intmotorid_boolenable>`__\ and\ ```/setProhibitMotionOnLimitSw`` <https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#setprohibitmotiononlimitsw_intmotorid_boolenable>`__\ you
can prohibit the actuator to move towards\ ``homingDirection``\ when the
HOME sensor is active, or the reverse direction
towards\ ``homingDirection``\ when the LIMIT sensor is active. With
this, you can prevent mechanism from collision.

``homingDirection``\ can be set
from\ ```/setHomingDirection`` <https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#sethomingdirection_intmotorid_booldirection>`__\ or
from the configTool. This setting is also used for following ``/homing``
command.

.. figure:: https://ponoor.com/cms/wp-content/uploads/2020/08/homingDirection-800x533.jpg
   :alt: Homing Direction

   Homing Direction

===============
Homing commands
===============

The homing command in the STEP400 system
is\ ```/homing`` <https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#homing_intmotorid>`__.
This command consists from two commands,
``/goUntil``\ and\ ``/releaseSw`` which are inherited from the Motor
Driver Chip PowerSTEP01. Let’s look closer to those commands.

``/goUnitl``
------------

First, use this command to move towards the home sensor. The motor will
decelerate and then stop when the home sensor reacts (if it has been set
up as such). ->
```/goUntil`` <https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#gountil_intmotorid_boolact_floatspeed>`__

``/releaseSw``
--------------

The position where the motor stops is the origin / home position!
However, strictly speaking, the ``/goUnitl`` command does not stop
immediately, but stop after deceleration, so it’s current position has
negative offset from the point where the sensor have actually responded.
This command slowly moves in the opposite direction from the current
position and stops immediately when the sensor reading is no longer
positive. ->
```/releaseSw`` <https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#releasesw_intmotorid_boolact_booldir>`__

Both commands can be set to reset the current position to zero on the
moment when the sensor responds. ->
```/setHomeSwMode`` <https://ponoor.com/en/docs/step-series/osc-command-reference/home-limit-sensors/#sethomeswmode_intmotorid_boolsw_mode>`__

See this video for these commands in operation.

.. container:: embed-video

   .. raw:: html

      <iframe width="560" height="315" src="https://www.youtube.com/embed/AydxbL6-a_g" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>

   .. raw:: html

      </iframe>

``/homing``
-----------

It is possible to send above two commands over OSC one after another,
the\ ```/homing`` <https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#homing_intmotorid>`__
command executes this sequence in single operation. It will
automatically complete the home sequence according to the homing
direction and homing speed which are pre-configured from the configTool
or over OSC commands.

Time-out
--------

The time-out duration can be set for each of
``/goUntil``\ and\ ``/releaseSw`` commands. The controller will halts
the actuator movement as the Time-out, if no change in the sensor
reading is detected within this time frame. This is to prevent the
moving part to be pushed against other mechanical object endlessly, by
giving up the homing sequence and stops at the specified timing.

============================
Normal open and Normal close
============================

Electrical connection
---------------------

Let’s determine the “sensor reaction” a little more in detail. The pin
assignments of HOME and LIMIT connectors are as follows.

========== ===================
Pin number Function
========== ===================
1          GND
2          Switch/Sensor input
3          5V Power Output
========== ===================

Each sensor pin on HOME and LIMIT is pulled up to 3.3V. To connect the
switch, connect the GND (#1) and the sensor terminal (#2). When the
switch is pressed, it is connected to the GND pin and the voltage drops
from 3.3V to 0V. When the voltage changes from HIGH level to LOW level
(a.k.a. **Falling Edge**), the sensor is considered to have responded.

Let’s take an photo interrupter
`EE-SX671A <http://www.ia.omron.com/product/item/2219/>`__ as an
example, where the connection is as follows:

.. figure:: http://ponoor.com/manage/wp-content/uploads/2020/10/ee-sx67.jpeg
   :alt: EE-SX671A Diagram

   EE-SX671A Diagram

========== =================== ==========
Pin number Function            Sensor pin
========== =================== ==========
1          GND                 -
2          Switch/Sensor input OUT
3          5V Power Output     +
========== =================== ==========

Whether light should enter or be blocked upon the sensor detection
------------------------------------------------------------------

This is the part you need to consider carefully before ordering a
sensor.

.. figure:: http://ponoor.com/manage/wp-content/uploads/2020/10/sensor_dark_light.png
   :alt: Dark on or Light on

   Dark on or Light on

In the case of the left picture, the light enters into the sensor at the
home position, but in the picture on the right, the light is blocked at
the home position.

There are two types of sensors, one that turns on when light enters and
one that turns on when light is interrupted. In the case of the above
Omron sensor, the action is toggled by connecting “L” and “+” terminals.

The mechanism and sensor must be combined in such a way that the sensor
pin goes from HIGH to LOW at the home position.

=================
For rotary tables
=================

In the example on the picture above left, the response position of the
home sensor will differ between clockwise and counterclockwise,
depending on the size of the hole. The STEP400 can notify both HIGH to
LOW and LOW to HIGH changes of the home sensor by OSC messages. The
message also includes the rotation direction, so you can align the home
position if you write a conditional sequence for each rotation
direction. ->
```/enableHomeSwReport`` <https://ponoor.com/en/docs/step-series/osc-command-reference/home-limit-sensors/#enablehomeswreport_intmotorid_boolenable>`__
