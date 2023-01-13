****************
Sending Commands
****************

==========
Brake Mode
==========

To use the electromagnetic brake, brake mode must first be activated. To
do this, send the command ``/enableElectromagnetBrake`` or from the
config tool under ``Electromagnetic brake enable``.

If the mode is enabled, the brake will be controlled according to the
motors' excitation state.

================
Switching States
================

With the command ``/activate``, you can switch the excitation state of
the motor. The brake will be released when the motor is excited and
engage when the motor is not excited.

The overlapping time ``Brake Transition Duration`` can be set from
``/setBrakeTransitionDuration`` or from the config tool under ``Brake
transition duration``.

==================
Releasing the Hold
==================

Any load will be releasing when the holding torque on it is lost.
However, there are cases where this behavior is desired. To do this,
the command ``/free`` can be sent.

.. warning:: Be very careful when sending this command. It is dangerous
    while any load is still attached to the motor! Ensure the load is
    safed before sending this command!

=================
Command Behaviors
=================

While the EM brake is engaged, the motion commands ``/run``, ``/goTo``,
and ``/move`` are not executed. Instead, the error
``ERROR_BRAKE_ENGAGED`` message will be raised.

.. note:: Python users: This message will raise an error!

Commands that put the motor into a non-excited state (torque hold
released) will behave as follows:

* ``/softHiZ``: Decelerate the motor to a stop, engage the brake, then release the motor (HiZ state).
* ``/hardHiZ``: Stop the motor immediately, engage the brake, thenrelease the motor (HiZ state).

``/softStop`` and ``/hardStop`` have no change in behavior and will
operate like normal. The brake is not engaged when these commands are
sent and the motor is kept excited.
