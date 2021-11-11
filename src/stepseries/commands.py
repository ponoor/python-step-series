#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""OSC message builders to send to the device."""


from dataclasses import asdict, dataclass

from pythonosc.osc_message import OscMessage
from pythonosc.osc_message_builder import OscMessageBuilder


@dataclass
class AbstractBuilder:
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
class SetDestIP(AbstractBuilder):
    address: str = "/setDestIp"


@dataclass
class GetVersion(AbstractBuilder):
    address: str = "/getVersion"


@dataclass
class GetConfigName(AbstractBuilder):
    address: str = "/getConfigName"


@dataclass
class ReportError(AbstractBuilder):
    address: str = "/reportError"


# Motor Driver Settings


@dataclass
class SetMicrostepMode(AbstractBuilder):
    motorID: int
    STEP_SEL: int
    address: str = "/setMicrostepMode"


@dataclass
class GetMicrostepMode(AbstractBuilder):
    motorID: int
    address: str = "/getMicrostepMode"


@dataclass
class SetLowSpeedOptimizeThreshold(AbstractBuilder):
    motorID: int
    lowSpeedOptimizationThreshold: float
    address: str = "/setLowSpeedOptimizeThreshold"


@dataclass
class GetLowSpeedOptimizeThreshold(AbstractBuilder):
    motorID: int
    address: str = "/getLowSpeedOptimizeThreshold"


@dataclass
class EnableBusyReport(AbstractBuilder):
    motorID: int
    enable: bool
    address: str = "/enableBusyReport"


@dataclass
class GetBusy(AbstractBuilder):
    motorID: int
    address: str = "/getBusy"


@dataclass
class EnableHiZReport(AbstractBuilder):
    motorID: int
    enable: bool
    address: str = "/enableHizReport"


@dataclass
class GetHiZ(AbstractBuilder):
    motorID: int
    address: str = "/getHiZ"


@dataclass
class EnableMotorStatusReport(AbstractBuilder):
    motorID: int
    enable: bool
    address: str = "/enableMotorStatusReport"


@dataclass
class GetMotorStatus(AbstractBuilder):
    motorID: int
    address: str = "/getMotorStatus"


@dataclass
class GetAdcVal(AbstractBuilder):
    motorID: int
    address: str = "/getAdcVal"


@dataclass
class GetStatus(AbstractBuilder):
    motorID: int
    address: str = "/getStatus"


@dataclass
class GetConfigRegister(AbstractBuilder):
    motorID: int
    address: str = "/getConfigRegister"


@dataclass
class ResetMotorDriver(AbstractBuilder):
    motorID: int
    address: str = "/resetMotorDriver"


# Alarm Settings


@dataclass
class EnableUvloReport(AbstractBuilder):
    motorID: int
    enable: bool
    address: str = "/enableUvloReport"


@dataclass
class GetUvlo(AbstractBuilder):
    motorID: int
    address: str = "/getUvlo"


@dataclass
class EnableThermalStatusReport(AbstractBuilder):
    motorID: int
    enable: bool
    address: str = "/enableThermalStatusReport"


@dataclass
class GetThermalStatus(AbstractBuilder):
    motorID: int
    address: str = "/getThermalStatus"


@dataclass
class EnableOverCurrentReport(AbstractBuilder):
    motorID: int
    enable: bool
    address: str = "/enableOverCurrentReport"


@dataclass
class SetOverCurrentThreshold(AbstractBuilder):
    motorID: int
    OCD_TH: int
    address: str = "/setOverCurrentThreshold"


@dataclass
class GetOverCurrentThreshold(AbstractBuilder):
    motorID: int
    address: str = "/getOverCurrentThreshold"


@dataclass
class EnableStallReport(AbstractBuilder):
    motorID: int
    enable: bool
    address: str = "/enableStallReport"


@dataclass
class SetStallThreshold(AbstractBuilder):
    motorID: int
    STALL_TH: int
    address: str = "/setStallThreshold"


@dataclass
class GetStallThreshold(AbstractBuilder):
    motorID: int
    address: str = "/getStallThreshold"


@dataclass
class SetProhibitMotionOnHomeSw(AbstractBuilder):
    motorID: int
    enable: bool
    address: str = "/setProhibitMotionOnHomeSw"


@dataclass
class GetProhibitMotionOnHomeSw(AbstractBuilder):
    motorID: int
    address: str = "/getProhibitMotionOnHomeSw"


@dataclass
class SetProhibitMotionOnLimitSw(AbstractBuilder):
    motorID: int
    enable: bool
    address: str = "/setProhibitMotionOnLimitSw"


@dataclass
class GetProhibitMotionOnLimitSw(AbstractBuilder):
    motorID: int
    address: str = "/getProhibitMotionOnLimitSw"


# Voltage and Current Mode Settings


@dataclass
class SetVoltageMode(AbstractBuilder):
    motorID: int
    address: str = "/setVoltageMode"


@dataclass
class SetKval(AbstractBuilder):
    motorID: int
    holdKVAL: int
    runKVAL: int
    accKVAL: int
    setDecKVAL: int
    address: str = "/setKval"


@dataclass
class GetKval(AbstractBuilder):
    motorID: int
    address: str = "/getKval"


@dataclass
class SetBemfParam(AbstractBuilder):
    motorID: int
    INT_SPEED: int
    ST_SLP: int
    FN_SLP_ACC: int
    FN_SLP_DEC: int
    address: str = "/setBemfParam"


@dataclass
class GetBemfParam(AbstractBuilder):
    motorID: int
    address: str = "/getBemfParam"


@dataclass
class SetCurrentMode(AbstractBuilder):
    motorID: int
    address: str = "/setCurrentMode"


@dataclass
class SetTval(AbstractBuilder):
    motorID: int
    holdTVAL: int
    runTVAL: int
    accTVAL: int
    setDecTVAL: int
    address: str = "/setTval"


@dataclass
class GetTval(AbstractBuilder):
    motorID: int
    address: str = "/getTval"


@dataclass
class SetDecayModeParam(AbstractBuilder):
    motorID: int
    T_FAST: int
    TON_MIN: int
    TOFF_MIN: int
    address: str = "/setDecayModeParam"


@dataclass
class GetDecayModeParam(AbstractBuilder):
    motorID: int
    address: str = "/getDecayModeParam"


# Speed Profile


@dataclass
class SetSpeedProfile(AbstractBuilder):
    motorID: int
    acc: float
    dec: float
    maxSpeed: float
    address: str = "/setSpeedProfile"


@dataclass
class GetSpeedProfile(AbstractBuilder):
    motorID: int
    address: str = "/getSpeedProfile"


@dataclass
class SetFullstepSpeed(AbstractBuilder):
    motorID: int
    fullstepSpeed: float
    address: str = "/setFullstepSpeed"


@dataclass
class GetFullstepSpeed(AbstractBuilder):
    motorID: int
    address: str = "/getFullstepSpeed"


@dataclass
class SetMaxSpeed(AbstractBuilder):
    motorID: int
    maxSpeed: float
    address: str = "/setMaxSpeed"


@dataclass
class SetAcc(AbstractBuilder):
    motorID: int
    acc: float
    address: str = "/setAcc"


@dataclass
class SetDec(AbstractBuilder):
    motorID: int
    dec: float
    address: str = "/setDec"


@dataclass
class GetSpeed(AbstractBuilder):
    motorID: int
    address: str = "/getSpeed"


# Homing


@dataclass
class Homing(AbstractBuilder):
    motorID: int
    address: str = "/homing"


@dataclass
class GetHomingStatus(AbstractBuilder):
    motorID: int
    address: str = "/getHomingStatus"


@dataclass
class SetHomingDirection(AbstractBuilder):
    motorID: int
    direction: bool
    address: str = "/setHomingDirection"


@dataclass
class GetHomingDirection(AbstractBuilder):
    motorID: int
    address: str = "/getHomingDirection"


@dataclass
class SetHomingSpeed(AbstractBuilder):
    motorID: int
    speed: float
    address: str = "/setHomingSpeed"


@dataclass
class GetHomingSpeed(AbstractBuilder):
    motorID: int
    address: str = "/getHomingSpeed"


@dataclass
class GoUntil(AbstractBuilder):
    motorID: int
    ACT: bool
    speed: float
    address: str = "/goUntil"


@dataclass
class SetGoUntilTimeout(AbstractBuilder):
    motorID: int
    timeOut: int
    address: str = "/setGoUntilTimeout"


@dataclass
class GetGoUntilTimeout(AbstractBuilder):
    motorID: int
    address: str = "/getGoUntilTimeout"


@dataclass
class ReleaseSw(AbstractBuilder):
    motorID: int
    ACT: bool
    DIR: bool
    address: str = "/releaseSw"


@dataclass
class SetReleaseSwTimeout(AbstractBuilder):
    motorID: int
    timeOut: int
    address: str = "/setReleaseSwTimeout"


# Home and Limit Sensors


@dataclass
class EnableHomeSwReport(AbstractBuilder):
    motorID: int
    enable: bool
    address: str = "/enableHomeSwReport"


@dataclass
class EnableSwEventReport(AbstractBuilder):
    motorID: int
    enable: bool
    address: str = "/enableSwEventReport"


@dataclass
class GetHomeSw(AbstractBuilder):
    motorID: int
    address: str = "/getHomeSw"


@dataclass
class EnableLimitSwReport(AbstractBuilder):
    motorID: int
    enable: bool
    address: str = "/enableLimitSwReport"


@dataclass
class GetLimitSw(AbstractBuilder):
    motorID: int
    address: str = "/getLimitSw"


@dataclass
class SetHomeSwMode(AbstractBuilder):
    motorID: int
    SW_MODE: bool
    address: str = "/setHomeSwMode"


@dataclass
class GetHomeSwMode(AbstractBuilder):
    motorID: int
    address: str = "/getHomeSwMode"


@dataclass
class SetLimitSwMode(AbstractBuilder):
    motorID: int
    SW_MODE: bool
    address: str = "/setLimitSwMode"


@dataclass
class GetLimitSwMode(AbstractBuilder):
    motorID: int
    address: str = "/getLimitSwMode"


# Position Management


@dataclass
class SetPosition(AbstractBuilder):
    motorID: int
    newPosition: int
    address: str = "/setPosition"


@dataclass
class GetPosition(AbstractBuilder):
    motorID: int
    address: str = "/getPosition"


@dataclass
class ResetPos(AbstractBuilder):
    motorID: int
    address: str = "/resetPos"


@dataclass
class SetMark(AbstractBuilder):
    motorID: int
    MARK: int
    address: str = "/setMark"


@dataclass
class GetMark(AbstractBuilder):
    motorID: int
    address: str = "/getMark"


@dataclass
class GoHome(AbstractBuilder):
    motorID: int
    address: str = "/goHome"


@dataclass
class GoMark(AbstractBuilder):
    motorID: int
    address: str = "/goMark"


# Motor Control


@dataclass
class Run(AbstractBuilder):
    motorID: int
    speed: float
    address: str = "/run"


@dataclass
class Move(AbstractBuilder):
    motorID: int
    step: int
    address: str = "/move"


@dataclass
class GoTo(AbstractBuilder):
    motorID: int
    position: int
    address: str = "/goTo"


@dataclass
class GoToDir(AbstractBuilder):
    motorID: int
    DIR: bool
    position: int
    address: str = "/goToDir"


@dataclass
class SoftStop(AbstractBuilder):
    motorID: int
    address: str = "/softStop"


@dataclass
class HardStop(AbstractBuilder):
    motorID: int
    address: str = "/hardStop"


@dataclass
class SoftHiZ(AbstractBuilder):
    motorID: int
    address: str = "/softHiZ"


@dataclass
class HardHiZ(AbstractBuilder):
    motorID: int
    address: str = "/hardHiZ"


# Electromagnetic Brake


@dataclass
class EnableElectromagnetBrake(AbstractBuilder):
    motorID: int
    enable: bool
    address: str = "/enableElectromagnetBrake"


@dataclass
class Activate(AbstractBuilder):
    motorID: int
    state: bool
    address: str = "/activate"


@dataclass
class Free(AbstractBuilder):
    motorID: int
    state: bool
    address: str = "/free"


@dataclass
class SetBrakeTransitionDuration(AbstractBuilder):
    motorID: int
    duration: int
    address: str = "/setBrakeTransitionDuration"


@dataclass
class GetBrakeTransitionDuration(AbstractBuilder):
    motorID: int
    address: str = "/getBrakeTransitionDuration"


# Servo Mode


@dataclass
class EnableServoMode(AbstractBuilder):
    motorID: int
    enable: bool
    address: str = "/enableServoMode"


@dataclass
class SetServoParam(AbstractBuilder):
    motorID: int
    kP: float
    kI: float
    kD: float
    address: str = "/setServoParam"


@dataclass
class GetServoParam(AbstractBuilder):
    motorID: int
    address: str = "/getServoParam"


@dataclass
class SetTargetPosition(AbstractBuilder):
    motorID: int
    position: int
    address: str = "/setTargetPosition"


@dataclass
class SetTargetPositionList(AbstractBuilder):
    position1: int
    position2: int
    position3: int
    position4: int
    address: str = "/setTargetPositionList"
