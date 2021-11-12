#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""OSC message responses sent from the device."""


import ast
import re
from dataclasses import dataclass as _dataclass
from dataclasses import field
from typing import Any, Callable, Dict, Tuple, TypeVar, Union

# Pylance custom dataclass work around
_T = TypeVar("_T")


def __dataclass_transform__(
    *,
    eq_default: bool = True,
    order_default: bool = False,
    kw_only_default: bool = False,
    field_descriptors: Tuple[Union[type, Callable[..., Any]], ...] = (()),
) -> Callable[[_T], _T]:
    return lambda a: a


# Implement a custom dataclass to parse raw strings
@__dataclass_transform__(field_descriptors=(field,))
def dataclass(*args: Tuple[Any], **kwargs: Dict[str, Any]):
    def wrapper(cls):
        cls = _dataclass(cls, **kwargs)
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            # Break down the args
            if len(args) == 1 and isinstance(args[0], str):
                # First look for custom regex strings
                # These will be <field_name>_re
                for i, field_name in enumerate(self.__annotations__.keys()):
                    if field_name.endswith("_re"):
                        match: re.Match = getattr(self, field_name).search(args[0])
                        kwargs[field_name[:-3]] = match[0]
                        args = (
                            (args[0][: match.start()] + args[0][match.end() :]).strip(),
                        )
                args = args[0].split()

            # Eval positional args
            args = list(args)
            for i, arg in enumerate(args):
                try:
                    args[i] = ast.literal_eval(arg.capitalize())
                except (AttributeError, ValueError, SyntaxError, NameError):
                    # Catch errors for non-strings, bad strings (i.e. ture instead of true)
                    # or non-evalable strings (i.e. class name)
                    pass

            # Eval named args
            for k, v in kwargs.items():
                try:
                    kwargs[k] = ast.literal_eval(v.capitalize())
                except (AttributeError, ValueError, SyntaxError, NameError):
                    # Catch errors for non-strings, bad strings (i.e. ture instead of true)
                    # or non-evalable strings (i.e. class name)
                    pass

            # Now call the generated dataclass init
            original_init(self, *args, **kwargs)

        cls.__init__ = __init__
        return cls

    return wrapper(args[0]) if args else wrapper


@dataclass
class AbstractResponse:
    """An abstract class meant to be implemented by OSC resp objects."""

    address: str


# Automatic Messages


@dataclass
class Booted(AbstractResponse):
    deviceID: int


@dataclass
class Error(AbstractResponse):
    errorText: str
    motorID: int = None


@dataclass
class Busy(AbstractResponse):
    motorID: int


@dataclass
class HiZ(AbstractResponse):
    motorID: int
    state: bool


@dataclass
class MotorStatus(AbstractResponse):
    motorID: int
    MOT_STATUS: int


@dataclass
class HomingStatus(AbstractResponse):
    motorID: int
    homingStatus: int


@dataclass
class Uvlo(AbstractResponse):
    motorID: int
    state: bool


@dataclass
class ThermalStatus(AbstractResponse):
    motorID: int
    thermalStatus: int


@dataclass
class OverCurrent(AbstractResponse):
    motorID: int


@dataclass
class Stall(AbstractResponse):
    motorID: int


# System Settings


@dataclass
class DestIP(AbstractResponse):
    destIp0: int
    destIp1: int
    destIp2: int
    destIp3: int
    isNewDestIp: bool


@dataclass
class Version(AbstractResponse):
    firmware_name: str
    firmware_version: str
    compile_date: str

    # Custom regex to breakout
    compile_date_re: re.Pattern = re.compile(r"\w+  .+")


@dataclass
class ConfigName(AbstractResponse):
    configName: str
    sdInitializeSucceeded: bool
    configFileOpenSucceeded: bool


# Motor Driver Settings


@dataclass
class MicrostepMode(AbstractResponse):
    motorID: int
    STEP_SEL: int


@dataclass
class LowSpeedOptimizeThreshold(AbstractResponse):
    motorID: int
    lowSpeedOptimizeThreshold: float


@dataclass
class AdcVal(AbstractResponse):
    motorID: int
    ADC_OUT: int


@dataclass
class Status(AbstractResponse):
    motorID: int
    status: int


@dataclass
class ConfigRegister(AbstractResponse):
    motorID: int
    CONFIG: int


# Alarm Settings


@dataclass
class OverCurrentThreshold(AbstractResponse):
    motorID: int
    overCurrentThreshold: float


@dataclass
class StallThreshold(AbstractResponse):
    motorID: int
    stallThreshold: float


@dataclass
class ProhibitMotionOnHomeSw(AbstractResponse):
    motorID: int
    enable: bool


@dataclass
class ProhibitMotionOnLimitSw(AbstractResponse):
    motorID: int
    enable: bool


# Voltage and Current Mode Settings


@dataclass
class Kval(AbstractResponse):
    motorID: int
    holdKVAL: int
    runKVAL: int
    accKVAL: int
    setDecKVAL: int


@dataclass
class BemfParam(AbstractResponse):
    motorID: int
    INT_SPEED: int
    ST_SLP: int
    FN_SLP_ACC: int
    FN_SLP_DEC: int


@dataclass
class Tval(AbstractResponse):
    motorID: int
    holdTVAL: int
    runTVAL: int
    accTVAL: int
    decTVAL: int


@dataclass
class DecayModeParam(AbstractResponse):
    motorID: int
    T_FAST: int
    TON_MIN: int
    TOFF_MIN: int


# Speed Profile


@dataclass
class SpeedProfile(AbstractResponse):
    motorID: int
    acc: float
    dec: float
    maxSpeed: float


@dataclass
class FullstepSpeed(AbstractResponse):
    motorID: int
    fullstepSpeed: float


@dataclass
class Speed(AbstractResponse):
    motorID: int
    speed: float


# Homing


@dataclass
class HomingDirection(AbstractResponse):
    motorID: int
    homingDirection: bool


@dataclass
class HomingSpeed(AbstractResponse):
    motorID: int
    homingSpeed: float


@dataclass
class GoUntilTimeout(AbstractResponse):
    motorID: int
    timeout: int


@dataclass
class ReleaseSwTimeout(AbstractResponse):
    motorID: int
    timeout: int


# Home and Limit Sensors


@dataclass
class SwEvent(AbstractResponse):
    motorID: int


@dataclass
class HomeSw(AbstractResponse):
    motorID: int
    swState: bool
    direction: bool


@dataclass
class LimitSw(AbstractResponse):
    motorID: int
    swState: bool
    direction: bool


@dataclass
class HomeSwMode(AbstractResponse):
    motorID: int
    swMode: bool


@dataclass
class LimitSwMode(AbstractResponse):
    motorID: int
    swMode: bool


# Position Management


@dataclass
class Position(AbstractResponse):
    motorID: int
    ABS_POS: int


@dataclass
class Mark(AbstractResponse):
    motorID: int
    MARK: int


# Electromagnetic Brake


@dataclass
class BrakeTransitionDuration(AbstractResponse):
    motorID: int
    duration: int


# Servo Mode


@dataclass
class ServoParam(AbstractResponse):
    motorID: int
    kP: float
    kI: float
    kD: float
