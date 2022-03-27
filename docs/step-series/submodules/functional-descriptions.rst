**********************
Functionality Overview
**********************

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

To better illustrate this point, here is a demostration video to show
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

You can also set the minimum speed (minSpeed) as a function of the motor
driver, but it is fixed at 0 in the firmware because it is unlikely to
be used for any actual application.

-------------------
Setting the Profile
-------------------

Use `/setSpeedProfile`_ to set the above three values. Acc and dec
cannot be set unless the motor is stopped; however, maxSpeed can be set
at any time.


.. _this presentation PDF: https://www.st.com/content/dam/AME/2019/developers-conference-2019/presentations/STDevCon19_3.6_Using%20Powerstep01.pdf
.. _STMicroelectronic's application notes: https://www.st.com/resource/en/application_note/dm00061093-voltage-mode-control-operation-and-parameter-optimization-stmicroelectronics.pdf
.. _/setBemfParam: https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setbemfparam_intmotorid_intint_speed_intst_slp_intfn_slp_acc_intfn_slp_dec
.. _Config Tool: http://ponoor.com/tools/step400-config/
.. _configuration files: https://ponoor.com/en/docs/step-series/settings/example-parameter-values-for-example-steppers/
.. _/setVoltageMode: https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setvoltagemode_intmotorid
.. _/setCurrentMode: https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setcurrentmode_intmotorid

.. _/setSpeedProfile: https://ponoor.com/en/docs/step400/osc-command-reference/speed-profile/#setspeedprofile_intmotorid_floatacc_floatdec_floatmaxspeed
.. _/run: https://ponoor.com/en/docs/step400/osc-command-reference/motor-control/#run_intmotorid_floatspeed
.. _/goUntil: https://ponoor.com/en/docs/step400/osc-command-reference/homing/#gountil_intmotorid_boolact_floatspeed
.. _/releaseSw: https://ponoor.com/en/docs/step400/osc-command-reference/homing/#releasesw_intmotorid_boolact_booldir

.. _/setProhibitMotionOnHomeSw: https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#setprohibitmotiononhomesw_intmotorid_boolenable
.. _/setProhibitMotionOnLimitSw: https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#setprohibitmotiononlimitsw_intmotorid_boolenable
.. _/setHomingDirection: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#sethomingdirection_intmotorid_booldirection
.. _/homing: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#homing_intmotorid
.. _/goUntil: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#gountil_intmotorid_boolact_floatspeed
.. _/releaseSw: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#releasesw_intmotorid_boolact_booldir
.. _/setHomeSwMode: https://ponoor.com/en/docs/step-series/osc-command-reference/home-limit-sensors/#sethomeswmode_intmotorid_boolsw_mode
.. _EE-SX671A: http://www.ia.omron.com/product/item/2219/
.. _/enableHomeSwReport: https://ponoor.com/en/docs/step-series/osc-command-reference/home-limit-sensors/#enablehomeswreport_intmotorid_boolenable

.. _/enableServoMode: https://ponoor.com/docs/step-series/osc-command-reference/servo-mode/#enableservomode_intmotorid_boolenable
.. _/setTargetPosition: https://ponoor.com/docs/step-series/osc-command-reference/servo-mode/#settargetposition_intmotorid_intposition
.. _/setTargetPositionList: https://ponoor.com/docs/step-series/osc-command-reference/servo-mode/#settargetpositionlist_intposition1_intposition2_intposition3_intposition4
.. _/setServoParam: https://ponoor.com/docs/step-series/osc-command-reference/servo-mode/#setservoparam_intmotorid_floatkp_floatki_floatkd
