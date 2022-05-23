*********
Operation
*********

=================================
What is an electromagnetic brake?
=================================

Some stepper motors have an EM brake built-in. In operation, stepper
motors maintain a holding torque even when stopped. However, if power is
lost, then that torque is lost and any suspended load will move or drop.

The brake is a device to lock the shaft when power is lost--or when
commanded--and releases when power is regained--or when commanded. This
device is especially necessary in situations of vertically suspended
loads.

===============
Response Timing
===============

The EM brake locks the axis when the power to the brake is lost.
However, this mechanism is not instant and requires a slight amount of
time to engage. This means there must be a duration of time in which the
brake and the motor are both engaged.

This transition duration, as it is called, does not affect how long it
takes for the brake to engage. This duration instead affects how long to
wait before releasing or engaging the motor after the brake. The initial
value of this overlap time is set to 100ms in the STEP400. It can also
be configured using the command ``/setBrakeTransitionDuration`` or from
the config tool.

.. image:: /img/brakeTransition.png

==========================
Built-in EM Brake Examples
==========================

.. figure:: /img/nema-23-stepper-19nm269ozin-w-brake-friction-torque-20nm283ozin-52372-1000x1000-1.jpg

    `STEPPER ONLINE`_

.. figure:: /img/pkp243d-700x525.jpg

    `OrientalMotor`_ PKP243D23M2


.. _STEPPER ONLINE: https://www.omc-stepperonline.com/stepper-motor-brake/nema-23-stepper-19nm269ozin-w-brake-friction-torque-20nm283ozin-23hs30-2804d-b200.html
.. _OrientalMotor: https://www.orientalmotor.co.jp/