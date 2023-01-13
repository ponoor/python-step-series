******
Wiring
******

=======================
Wiring the Power Source
=======================

--------------------
Power Source Voltage
--------------------

Supply power for the electromagnetic brake. Many EM brakes use 24V, but
please refer to the datasheet of your motor.

----------------------
Power Supply Terminals
----------------------

There are two types of power supply terminals: the DC barrel jack and
the Euro-style terminal block.

.. warning:: As these are connected on the PCB, **DO NOT SUPPLY BOTH AT
    THE SAME TIME**

^^^^^^^
DC Jack
^^^^^^^

* Outer diameter 5.5mm
* Inner diameter 2.1mm
* Center positive

^^^^^^^^^^^^^^^^^^^^^^^^^
Euro-style Terminal Block
^^^^^^^^^^^^^^^^^^^^^^^^^

A 3.81mm pitch, 2pin Euro-style terminal block is built-in. Refer to the
polarity described on the PC for connecting your DC supply correctly.

.. image:: /img/brake-power-700x525.jpg

====================
Connecting the Motor
====================

Connect the wires from the EM brake's terminal block to the
corresponding motor. Note how each terminal on the brake is numbered
just like the STEP400--make sure these match in terms of wiring.

Like most EM brakes, this brake has a polarity requirement, so wire your
motor as stated on the PCB.

======================
Connecting the STEP400
======================

Connect the STEP400 using the provided 6-pin ribbon cable.

.. image:: /img/brake-riboncable-700x525.jpg
