#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""OSC message builders to send to the device."""


from dataclasses import asdict, dataclass

from pythonosc.osc_message import OscMessage
from pythonosc.osc_message_builder import OscMessageBuilder


@dataclass
class OSCCommand:
    """An abstract class meant to be implemented by OSC command objects."""

    def build(self) -> OscMessage:
        """Converts the builder to a usable OSC message."""

        # Convert the builder to a dictionary
        builder_dict = asdict(self)

        # Extract the values
        # Code is largely copy-paste from pythonosc.UDPClient
        address = builder_dict.pop("address")

        builder = OscMessageBuilder(address=address)

        # Return as a message string
        for v in builder_dict.values():
            if isinstance(v, bool):
                v = int(v)
            builder.add_arg(v)

        return builder.build()

    def stringify(self) -> str:
        """Converts the builder to an OSC message string."""

        # Convert the builder to a dictionary
        builder_dict = asdict(self)

        # Extract the values
        address: str = builder_dict.pop("address") + " "

        # Return as a message string
        for v in builder_dict.values():
            if isinstance(v, bool):
                v = int(v)
            address += str(v) + " "

        return address[:-1]


# System Settings


@dataclass
class SetDestIP(OSCCommand):
    address: str = "/setDestIp"


@dataclass
class GetVersion(OSCCommand):
    address: str = "/getVersion"


@dataclass
class GetConfigName(OSCCommand):
    address: str = "/getConfigName"


@dataclass
class ReportError(OSCCommand):
    address: str = "/reportError"


# Motor Driver Settings


@dataclass
class SetMicrostepMode(OSCCommand):
    motorID: int
    STEP_SEL: int
    address: str = "/setMicrostepMode"


@dataclass
class GetMicrostepMode(OSCCommand):
    motorID: int
    address: str = "/getMicrostepMode"


@dataclass
class SetLowSpeedOptimizeThreshold(OSCCommand):
    motorID: int
    lowSpeedOptimizationThreshold: float
    address: str = "/setLowSpeedOptimizeThreshold"


@dataclass
class GetLowSpeedOptimizeThreshold(OSCCommand):
    motorID: int
    address: str = "/getLowSpeedOptimizeThreshold"


@dataclass
class EnableBusyReport(OSCCommand):
    motorID: int
    enable: bool
    address: str = "/enableBusyReport"


@dataclass
class GetBusy(OSCCommand):
    motorID: int
    address: str = "/getBusy"


@dataclass
class EnableHiZReport(OSCCommand):
    motorID: int
    enable: bool
    address: str = "/enableHizReport"


@dataclass
class GetHiZ(OSCCommand):
    motorID: int
    address: str = "/getHiZ"


@dataclass
class EnableMotorStatusReport(OSCCommand):
    motorID: int
    enable: bool
    address: str = "/enableMotorStatusReport"


@dataclass
class GetMotorStatus(OSCCommand):
    motorID: int
    address: str = "/getMotorStatus"


@dataclass
class GetAdcVal(OSCCommand):
    motorID: int
    address: str = "/getAdcVal"


@dataclass
class GetStatus(OSCCommand):
    motorID: int
    address: str = "/getStatus"


@dataclass
class GetConfigRegister(OSCCommand):
    motorID: int
    address: str = "/getConfigRegister"


@dataclass
class ResetMotorDriver(OSCCommand):
    motorID: int
    address: str = "/resetMotorDriver"


# Alarm Settings


@dataclass
class EnableUvloReport(OSCCommand):
    motorID: int
    enable: bool
    address: str = "/enableUvloReport"


@dataclass
class GetUvlo(OSCCommand):
    motorID: int
    address: str = "/getUvlo"


@dataclass
class EnableThermalStatusReport(OSCCommand):
    motorID: int
    enable: bool
    address: str = "/enableThermalStatusReport"


@dataclass
class GetThermalStatus(OSCCommand):
    motorID: int
    address: str = "/getThermalStatus"


@dataclass
class EnableOverCurrentReport(OSCCommand):
    motorID: int
    enable: bool
    address: str = "/enableOverCurrentReport"


@dataclass
class SetOverCurrentThreshold(OSCCommand):
    motorID: int
    OCD_TH: int
    address: str = "/setOverCurrentThreshold"


@dataclass
class GetOverCurrentThreshold(OSCCommand):
    motorID: int
    address: str = "/getOverCurrentThreshold"


@dataclass
class EnableStallReport(OSCCommand):
    motorID: int
    enable: bool
    address: str = "/enableStallReport"


@dataclass
class SetStallThreshold(OSCCommand):
    motorID: int
    STALL_TH: int
    address: str = "/setStallThreshold"


@dataclass
class GetStallThreshold(OSCCommand):
    motorID: int
    address: str = "/getStallThreshold"


@dataclass
class SetProhibitMotionOnHomeSw(OSCCommand):
    motorID: int
    enable: bool
    address: str = "/setProhibitMotionOnHomeSw"


@dataclass
class GetProhibitMotionOnHomeSw(OSCCommand):
    motorID: int
    address: str = "/getProhibitMotionOnHomeSw"


@dataclass
class SetProhibitMotionOnLimitSw(OSCCommand):
    motorID: int
    enable: bool
    address: str = "/setProhibitMotionOnLimitSw"


@dataclass
class GetProhibitMotionOnLimitSw(OSCCommand):
    motorID: int
    address: str = "/getProhibitMotionOnLimitSw"


# Voltage and Current Mode Settings


@dataclass
class SetVoltageMode(OSCCommand):
    motorID: int
    address: str = "/setVoltageMode"


@dataclass
class SetKval(OSCCommand):
    motorID: int
    holdKVAL: int
    runKVAL: int
    accKVAL: int
    setDecKVAL: int
    address: str = "/setKval"


@dataclass
class GetKval(OSCCommand):
    motorID: int
    address: str = "/getKval"


@dataclass
class SetBemfParam(OSCCommand):
    motorID: int
    INT_SPEED: int
    ST_SLP: int
    FN_SLP_ACC: int
    FN_SLP_DEC: int
    address: str = "/setBemfParam"


@dataclass
class GetBemfParam(OSCCommand):
    motorID: int
    address: str = "/getBemfParam"


@dataclass
class SetCurrentMode(OSCCommand):
    motorID: int
    address: str = "/setCurrentMode"


@dataclass
class SetTval(OSCCommand):
    motorID: int
    holdTVAL: int
    runTVAL: int
    accTVAL: int
    setDecTVAL: int
    address: str = "/setTval"


@dataclass
class GetTval(OSCCommand):
    motorID: int
    address: str = "/getTval"


@dataclass
class SetDecayModeParam(OSCCommand):
    motorID: int
    T_FAST: int
    TON_MIN: int
    TOFF_MIN: int
    address: str = "/setDecayModeParam"


@dataclass
class GetDecayModeParam(OSCCommand):
    motorID: int
    address: str = "/getDecayModeParam"


# Speed Profile


@dataclass
class SetSpeedProfile(OSCCommand):
    motorID: int
    acc: float
    dec: float
    maxSpeed: float
    address: str = "/setSpeedProfile"


@dataclass
class GetSpeedProfile(OSCCommand):
    motorID: int
    address: str = "/getSpeedProfile"


@dataclass
class SetFullstepSpeed(OSCCommand):
    motorID: int
    fullstepSpeed: float
    address: str = "/setFullstepSpeed"


@dataclass
class GetFullstepSpeed(OSCCommand):
    motorID: int
    address: str = "/getFullstepSpeed"


@dataclass
class SetMaxSpeed(OSCCommand):
    motorID: int
    maxSpeed: float
    address: str = "/setMaxSpeed"


@dataclass
class SetAcc(OSCCommand):
    motorID: int
    acc: float
    address: str = "/setAcc"


@dataclass
class SetDec(OSCCommand):
    motorID: int
    dec: float
    address: str = "/setDec"


@dataclass
class GetSpeed(OSCCommand):
    motorID: int
    address: str = "/getSpeed"


# Homing


@dataclass
class Homing(OSCCommand):
    motorID: int
    address: str = "/homing"


@dataclass
class GetHomingStatus(OSCCommand):
    motorID: int
    address: str = "/getHomingStatus"


@dataclass
class SetHomingDirection(OSCCommand):
    motorID: int
    direction: bool
    address: str = "/setHomingDirection"


@dataclass
class GetHomingDirection(OSCCommand):
    motorID: int
    address: str = "/getHomingDirection"


@dataclass
class SetHomingSpeed(OSCCommand):
    motorID: int
    speed: float
    address: str = "/setHomingSpeed"


@dataclass
class GetHomingSpeed(OSCCommand):
    motorID: int
    address: str = "/getHomingSpeed"


@dataclass
class GoUntil(OSCCommand):
    motorID: int
    ACT: bool
    speed: float
    address: str = "/goUntil"


@dataclass
class SetGoUntilTimeout(OSCCommand):
    motorID: int
    timeOut: int
    address: str = "/setGoUntilTimeout"


@dataclass
class GetGoUntilTimeout(OSCCommand):
    motorID: int
    address: str = "/getGoUntilTimeout"


@dataclass
class ReleaseSw(OSCCommand):
    motorID: int
    ACT: bool
    DIR: bool
    address: str = "/releaseSw"


@dataclass
class SetReleaseSwTimeout(OSCCommand):
    motorID: int
    timeOut: int
    address: str = "/setReleaseSwTimeout"


@dataclass
class GetReleaseSwTimeout(OSCCommand):
    motorID: int
    address: str = "/getReleaseSwTimeout"


# Home and Limit Sensors


@dataclass
class EnableHomeSwReport(OSCCommand):
    motorID: int
    enable: bool
    address: str = "/enableHomeSwReport"


@dataclass
class EnableSwEventReport(OSCCommand):
    motorID: int
    enable: bool
    address: str = "/enableSwEventReport"


@dataclass
class GetHomeSw(OSCCommand):
    motorID: int
    address: str = "/getHomeSw"


@dataclass
class EnableLimitSwReport(OSCCommand):
    motorID: int
    enable: bool
    address: str = "/enableLimitSwReport"


@dataclass
class GetLimitSw(OSCCommand):
    motorID: int
    address: str = "/getLimitSw"


@dataclass
class SetHomeSwMode(OSCCommand):
    motorID: int
    SW_MODE: bool
    address: str = "/setHomeSwMode"


@dataclass
class GetHomeSwMode(OSCCommand):
    motorID: int
    address: str = "/getHomeSwMode"


@dataclass
class SetLimitSwMode(OSCCommand):
    motorID: int
    SW_MODE: bool
    address: str = "/setLimitSwMode"


@dataclass
class GetLimitSwMode(OSCCommand):
    motorID: int
    address: str = "/getLimitSwMode"


# Position Management


@dataclass
class SetPosition(OSCCommand):
    motorID: int
    newPosition: int
    address: str = "/setPosition"


@dataclass
class GetPosition(OSCCommand):
    motorID: int
    address: str = "/getPosition"


@dataclass
class ResetPos(OSCCommand):
    motorID: int
    address: str = "/resetPos"


@dataclass
class SetMark(OSCCommand):
    motorID: int
    MARK: int
    address: str = "/setMark"


@dataclass
class GetMark(OSCCommand):
    motorID: int
    address: str = "/getMark"


@dataclass
class GoHome(OSCCommand):
    motorID: int
    address: str = "/goHome"


@dataclass
class GoMark(OSCCommand):
    motorID: int
    address: str = "/goMark"


# Motor Control


@dataclass
class Run(OSCCommand):
    motorID: int
    speed: float
    address: str = "/run"


@dataclass
class Move(OSCCommand):
    motorID: int
    step: int
    address: str = "/move"


@dataclass
class GoTo(OSCCommand):
    motorID: int
    position: int
    address: str = "/goTo"


@dataclass
class GoToDir(OSCCommand):
    motorID: int
    DIR: bool
    position: int
    address: str = "/goToDir"


@dataclass
class SoftStop(OSCCommand):
    motorID: int
    address: str = "/softStop"


@dataclass
class HardStop(OSCCommand):
    motorID: int
    address: str = "/hardStop"


@dataclass
class SoftHiZ(OSCCommand):
    motorID: int
    address: str = "/softHiZ"


@dataclass
class HardHiZ(OSCCommand):
    motorID: int
    address: str = "/hardHiZ"


# Electromagnetic Brake


@dataclass
class EnableElectromagnetBrake(OSCCommand):
    motorID: int
    enable: bool
    address: str = "/enableElectromagnetBrake"


@dataclass
class Activate(OSCCommand):
    motorID: int
    state: bool
    address: str = "/activate"


@dataclass
class Free(OSCCommand):
    motorID: int
    state: bool
    address: str = "/free"


@dataclass
class SetBrakeTransitionDuration(OSCCommand):
    motorID: int
    duration: int
    address: str = "/setBrakeTransitionDuration"


@dataclass
class GetBrakeTransitionDuration(OSCCommand):
    motorID: int
    address: str = "/getBrakeTransitionDuration"


# Servo Mode


@dataclass
class EnableServoMode(OSCCommand):
    motorID: int
    enable: bool
    address: str = "/enableServoMode"


@dataclass
class SetServoParam(OSCCommand):
    motorID: int
    kP: float
    kI: float
    kD: float
    address: str = "/setServoParam"


@dataclass
class GetServoParam(OSCCommand):
    motorID: int
    address: str = "/getServoParam"


@dataclass
class SetTargetPosition(OSCCommand):
    motorID: int
    position: int
    address: str = "/setTargetPosition"


@dataclass
class SetTargetPositionList(OSCCommand):
    position1: int
    position2: int
    position3: int
    position4: int
    address: str = "/setTargetPositionList"
