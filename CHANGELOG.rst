=========
Changelog
=========


Development version
===================

Version 0.0.2, 2021-12-XX
-------------------------

- Added support for the STEP800 motor controller
- Added the following commands:
    - GetPositionList (``/getPositionList``)
    - GetTval_mA (``/getTval_mA``)
    - GetDir (``/getDir``)
    - EnableDirReport (``/enableDirReport``)
    - SetPositionReportInterval (``/setPositionReportInterval``)
    - SetPositionListReportInterval (``/setPositionListReportInterval``)
    - GetElPos (``/getElPos``)
    - SetElPos (``/setElPos``)
    - ResetDevice (``/resetDevice``)

- Fixed an issue with ``get`` only returning 1 response when there are multiple (`#1`_)


Current versions
================

Version 0.0.1, 2021-12-03
-------------------------

- First release


.. _#1: https://github.com/ponoor/python-step-series/issues/1
