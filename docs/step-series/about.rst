.. _step_series:

###############
STEP400/STEP800
###############

.. image:: ../img/step400_step800-1600x1067.jpg

*****
About
*****


Both the STEP400 and STEP800 are multi-axis stepper motor controllers which can be controlled via
Ethernet. While both devices use an `Arduino Zero`_ as the main control unit (MCU), the STEP400 uses
STMicroelectronics's `powerSTEP01`_ as its stepper driver chip whereas the STEP800 uses
STMicroelectronics's `L6470`_. It is recommended to review the datasheets for both chips to better
understand how they work and what each command is doing.

Both devices use the exact same commands save for a select few which are marked in the API
Reference. So, unless you see ``STEP400 Only`` or ``STEP800 Only``, assume the command is compatible
with both devices.


.. _powerSTEP01: https://www.st.com/en/motor-drivers/powerstep01.html
.. _L6470: https://www.st.com/en/motor-drivers/l6470.html

.. _protocol: http://opensoundcontrol.org/
.. _Arduino Zero: https://www.arduino.cc/en/Guide/ArduinoZero

.. include:: submodules/getting-started.rst
.. include:: submodules/other-connections-settings.rst
.. include:: submodules/functionality-descriptions.rst
.. include:: submodules/technical-information.rst
