**************
Specifications
**************

====================
Basic Specifications
====================

* Input voltage: 5-48V
* Control channels: 4 channels
* PCB size: 45x56mm

.. note:: When supplying voltage under 12V, the indicator LED may not be
    visible.

---------------
Driving Current
---------------

According the `datasheet`_ of the switching MOSFET, the rating is
60V @ 28A. However, the actual rating is limited to the rating of the
power source terminal block which is 7A. Within this range, you can
control other loads like LEDs or motors.

========
Drawings
========

.. figure:: /img/step400-emb-dimension.png

    `PCB PDF`_

.. figure:: /img/stem400-emb-schematic.png

    `Circuit PDF`_

===========
Accessories
===========

* 3.81mm pitch 2pin Euro-style terminal block x5
* 6 pin ribbon cable


.. _datasheet: https://datasheet.lcsc.com/szlcsc/Winsok-Semicon-WSF28N06_C148431.pdf
.. _データシート: https://datasheet.lcsc.com/szlcsc/Winsok-Semicon-WSF28N06_C148431.pdf
.. _PCB PDF: https://ponoor.com/cms/wp-content/uploads/2021/03/step400-emb-dimension.pdf
.. _基板外形 PDF: https://ponoor.com/cms/wp-content/uploads/2021/03/step400-emb-dimension.pdf
.. _Circuit PDF: https://ponoor.com/cms/wp-content/uploads/2021/03/step400-brakeBoard-schematic.pdf
.. _回路図 PDF: https://ponoor.com/cms/wp-content/uploads/2021/03/step400-brakeBoard-schematic.pdf