******************************
Other Connections and Settings
******************************

====================
Sensors and Switches
====================

Each axis of the STEP400 and STEP800 has a ``HOME`` connector which allows for you to plug-in some
form of limit switch or equivalent sensor. Additionally, the STEP400 has ``LIMIT`` inputs for each
axis in addition to the ``HOME`` inputs.

----
HOME
----

Since the stepper motor cannot track its own position, a dedicated sensor is required to return to
the home position on boot-up. It is directly connected to the motor driver IC and can be used for
position management. The pin is pulled up to 3v3 (3.3V) inside the driver IC.

-----
LIMIT
-----

``STEP400 Only``

As stated above, the STEP400 has an additional ``LIMIT`` switch input that can be used to limit the
operational range of each motor. You can configure these inputs to halt the motor, or to be used as
another input for another purpose. Like the ``HOME`` input, this input is also pulled up to 3v3.

--------------------
Connection Terminals
--------------------

We use the XA series connectors from JST (J.S.T.MFG.CO., LTD.). For compatible connectors, please
refer to the following:

==================== ==================== =======================================
Name                 Model Number         Description
==================== ==================== =======================================
(Reference) PCB Post B03B-XASK-1 (LF)(SN) Female connector on the PCB
Housing              XAP-03V-1            Male plastic housing
Contact              BXA-001T-P0.6        Crimp contact inserted into the housing
==================== ==================== =======================================

.. tip:: We also sell pre-crimped sensor cables for your convenience. These are available here:
    https://ponoor.com/en/products/sensor-cable/

---------------
Pin Assignments
---------------

The pin assignments for both inputs are the same. The order of these pins are relative to how you
are looking at your board. We assume you are viewing the board with the board's name at the bottom
and the power/ethernet ports at the top. This table is for the left-side ports; the right-side ports
will be inverted as they are upside-down.

=================== ==================
Pin (left-to-right) Function
=================== ==================
1                   5V Output
2                   3v3 (Switch Input)
3                   GND
=================== ==================

.. tip:: They are also printed on the bottom of the boards for your convenience.

The driver responds when the input falls from ``HIGH (3v3)`` to ``LOW (0V)``. Therefore, the switch
must behave as "normally open".

======================
Network and DIP Switch
======================

-------------------
Dip Switch Settings
-------------------

.. figure:: /img/step400-dipSw.jpg

    The DIP switch specifies the ID that is used to reply to OSC messages and is also reflected in
    the local IP address and expected server port number. The ID is set in binary with more
    information provided by `Soundhouse's Documentation`_.

----------------
Network Settings
----------------

^^^^^^^^^^^^^^^^
Initial Settings
^^^^^^^^^^^^^^^^

==================== =====================================
Item                 Initial Value
==================== =====================================
IP Address           10.0.0.100+ID
MAC Address          0x60, 0x95, 0xCE, 0x10, 0x02, 0x00+ID
Server IP Address    10.0.0.10
Local Port           50000
Expected Server Port 50100+ID
==================== =====================================

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
IP Address and Expected Server Port
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In its initial state, an ID will be added to IP address's final octet and the expected server port.
With this mechanism, you are able to operate multiple devices with the same firmware and settings
file. On the server, if you are able to retrieve the IP address of the device, you can configure the
device to not add its ID to the expected server port.

This feature can be disabled via the microSD card configuration.

^^^^^^^^^^^
MAC Address
^^^^^^^^^^^

A unique MAC address is assigned to the device; however, its initial value is set as seen in the
table above. The unique MAC address is printed on the sticker on the bottom of the device beneath
another sticker that should contain the device's serial number. To use the assigned MAC address,
please generate the settings file from the `Configuration Tool`_ and load it onto the microSD card.

.. tip:: A variety of settings can be preconfigured on the microSD card. See
    :ref:`microSD Card Setup`.


.. _Configuration Tool: http://ponoor.com/tools/step400-config/
.. _Soundhouse's Documentation: https://www.soundhouse.co.jp/howto/light/dmx-dip/
