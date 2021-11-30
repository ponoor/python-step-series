#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""OSC message builders to send to the device."""


from dataclasses import asdict, dataclass, field

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
    address: str = field(default="/setDestIp", init=False)


@dataclass
class GetVersion(OSCCommand):
    address: str = field(default="/getVersion", init=False)


@dataclass
class GetConfigName(OSCCommand):
    address: str = field(default="/getConfigName", init=False)


@dataclass
class ReportError(OSCCommand):
    address: str = field(default="/reportError", init=False)
    enable: bool


# Motor Driver Settings


@dataclass
class SetMicrostepMode(OSCCommand):
    motorID: int
    STEP_SEL: int
    address: str = field(default="/setMicrostepMode", init=False)


@dataclass
class GetMicrostepMode(OSCCommand):
    motorID: int
    address: str = field(default="/getMicrostepMode", init=False)


@dataclass
class SetLowSpeedOptimizeThreshold(OSCCommand):
    motorID: int
    lowSpeedOptimizationThreshold: float
    address: str = field(default="/setLowSpeedOptimizeThreshold", init=False)


@dataclass
class GetLowSpeedOptimizeThreshold(OSCCommand):
    motorID: int
    address: str = field(default="/getLowSpeedOptimizeThreshold", init=False)


@dataclass
class EnableBusyReport(OSCCommand):
    motorID: int
    enable: bool
    address: str = field(default="/enableBusyReport", init=False)


@dataclass
class GetBusy(OSCCommand):
    motorID: int
    address: str = field(default="/getBusy", init=False)


@dataclass
class EnableHiZReport(OSCCommand):
    motorID: int
    enable: bool
    address: str = field(default="/enableHizReport", init=False)


@dataclass
class GetHiZ(OSCCommand):
    motorID: int
    address: str = field(default="/getHiZ", init=False)


@dataclass
class EnableMotorStatusReport(OSCCommand):
    motorID: int
    enable: bool
    address: str = field(default="/enableMotorStatusReport", init=False)


@dataclass
class GetMotorStatus(OSCCommand):
    motorID: int
    address: str = field(default="/getMotorStatus", init=False)


@dataclass
class GetAdcVal(OSCCommand):
    motorID: int
    address: str = field(default="/getAdcVal", init=False)


@dataclass
class GetStatus(OSCCommand):
    motorID: int
    address: str = field(default="/getStatus", init=False)


@dataclass
class GetConfigRegister(OSCCommand):
    motorID: int
    address: str = field(default="/getConfigRegister", init=False)


@dataclass
class ResetMotorDriver(OSCCommand):
    motorID: int
    address: str = field(default="/resetMotorDriver", init=False)


# Alarm Settings


@dataclass
class EnableUvloReport(OSCCommand):
    motorID: int
    enable: bool
    address: str = field(default="/enableUvloReport", init=False)


@dataclass
class GetUvlo(OSCCommand):
    motorID: int
    address: str = field(default="/getUvlo", init=False)


@dataclass
class EnableThermalStatusReport(OSCCommand):
    motorID: int
    enable: bool
    address: str = field(default="/enableThermalStatusReport", init=False)


@dataclass
class GetThermalStatus(OSCCommand):
    motorID: int
    address: str = field(default="/getThermalStatus", init=False)


@dataclass
class EnableOverCurrentReport(OSCCommand):
    motorID: int
    enable: bool
    address: str = field(default="/enableOverCurrentReport", init=False)


@dataclass
class SetOverCurrentThreshold(OSCCommand):
    motorID: int
    OCD_TH: int
    address: str = field(default="/setOverCurrentThreshold", init=False)


@dataclass
class GetOverCurrentThreshold(OSCCommand):
    motorID: int
    address: str = field(default="/getOverCurrentThreshold", init=False)


@dataclass
class EnableStallReport(OSCCommand):
    motorID: int
    enable: bool
    address: str = field(default="/enableStallReport", init=False)


@dataclass
class SetStallThreshold(OSCCommand):
    motorID: int
    STALL_TH: int
    address: str = field(default="/setStallThreshold", init=False)


@dataclass
class GetStallThreshold(OSCCommand):
    motorID: int
    address: str = field(default="/getStallThreshold", init=False)


@dataclass
class SetProhibitMotionOnHomeSw(OSCCommand):
    motorID: int
    enable: bool
    address: str = field(default="/setProhibitMotionOnHomeSw", init=False)


@dataclass
class GetProhibitMotionOnHomeSw(OSCCommand):
    motorID: int
    address: str = field(default="/getProhibitMotionOnHomeSw", init=False)


@dataclass
class SetProhibitMotionOnLimitSw(OSCCommand):
    motorID: int
    enable: bool
    address: str = field(default="/setProhibitMotionOnLimitSw", init=False)


@dataclass
class GetProhibitMotionOnLimitSw(OSCCommand):
    motorID: int
    address: str = field(default="/getProhibitMotionOnLimitSw", init=False)


# Voltage and Current Mode Settings


@dataclass
class SetVoltageMode(OSCCommand):
    motorID: int
    address: str = field(default="/setVoltageMode", init=False)


@dataclass
class SetKval(OSCCommand):
    motorID: int
    holdKVAL: int
    runKVAL: int
    accKVAL: int
    setDecKVAL: int
    address: str = field(default="/setKval", init=False)


@dataclass
class GetKval(OSCCommand):
    motorID: int
    address: str = field(default="/getKval", init=False)


@dataclass
class SetBemfParam(OSCCommand):
    motorID: int
    INT_SPEED: int
    ST_SLP: int
    FN_SLP_ACC: int
    FN_SLP_DEC: int
    address: str = field(default="/setBemfParam", init=False)


@dataclass
class GetBemfParam(OSCCommand):
    motorID: int
    address: str = field(default="/getBemfParam", init=False)


@dataclass
class SetCurrentMode(OSCCommand):
    motorID: int
    address: str = field(default="/setCurrentMode", init=False)


@dataclass
class SetTval(OSCCommand):
    motorID: int
    holdTVAL: int
    runTVAL: int
    accTVAL: int
    setDecTVAL: int
    address: str = field(default="/setTval", init=False)


@dataclass
class GetTval(OSCCommand):
    motorID: int
    address: str = field(default="/getTval", init=False)


@dataclass
class SetDecayModeParam(OSCCommand):
    motorID: int
    T_FAST: int
    TON_MIN: int
    TOFF_MIN: int
    address: str = field(default="/setDecayModeParam", init=False)


@dataclass
class GetDecayModeParam(OSCCommand):
    motorID: int
    address: str = field(default="/getDecayModeParam", init=False)


# Speed Profile


@dataclass
class SetSpeedProfile(OSCCommand):
    motorID: int
    acc: float
    dec: float
    maxSpeed: float
    address: str = field(default="/setSpeedProfile", init=False)


@dataclass
class GetSpeedProfile(OSCCommand):
    motorID: int
    address: str = field(default="/getSpeedProfile", init=False)


@dataclass
class SetFullstepSpeed(OSCCommand):
    motorID: int
    fullstepSpeed: float
    address: str = field(default="/setFullstepSpeed", init=False)


@dataclass
class GetFullstepSpeed(OSCCommand):
    motorID: int
    address: str = field(default="/getFullstepSpeed", init=False)


@dataclass
class SetMaxSpeed(OSCCommand):
    motorID: int
    maxSpeed: float
    address: str = field(default="/setMaxSpeed", init=False)


@dataclass
class SetAcc(OSCCommand):
    motorID: int
    acc: float
    address: str = field(default="/setAcc", init=False)


@dataclass
class SetDec(OSCCommand):
    motorID: int
    dec: float
    address: str = field(default="/setDec", init=False)


@dataclass
class GetSpeed(OSCCommand):
    motorID: int
    address: str = field(default="/getSpeed", init=False)


# Homing


@dataclass
class Homing(OSCCommand):
    motorID: int
    address: str = field(default="/homing", init=False)


@dataclass
class GetHomingStatus(OSCCommand):
    motorID: int
    address: str = field(default="/getHomingStatus", init=False)


@dataclass
class SetHomingDirection(OSCCommand):
    motorID: int
    direction: bool
    address: str = field(default="/setHomingDirection", init=False)


@dataclass
class GetHomingDirection(OSCCommand):
    motorID: int
    address: str = field(default="/getHomingDirection", init=False)


@dataclass
class SetHomingSpeed(OSCCommand):
    motorID: int
    speed: float
    address: str = field(default="/setHomingSpeed", init=False)


@dataclass
class GetHomingSpeed(OSCCommand):
    motorID: int
    address: str = field(default="/getHomingSpeed", init=False)


@dataclass
class GoUntil(OSCCommand):
    motorID: int
    ACT: bool
    speed: float
    address: str = field(default="/goUntil", init=False)


@dataclass
class SetGoUntilTimeout(OSCCommand):
    motorID: int
    timeOut: int
    address: str = field(default="/setGoUntilTimeout", init=False)


@dataclass
class GetGoUntilTimeout(OSCCommand):
    motorID: int
    address: str = field(default="/getGoUntilTimeout", init=False)


@dataclass
class ReleaseSw(OSCCommand):
    motorID: int
    ACT: bool
    DIR: bool
    address: str = field(default="/releaseSw", init=False)


@dataclass
class SetReleaseSwTimeout(OSCCommand):
    motorID: int
    timeOut: int
    address: str = field(default="/setReleaseSwTimeout", init=False)


@dataclass
class GetReleaseSwTimeout(OSCCommand):
    motorID: int
    address: str = field(default="/getReleaseSwTimeout", init=False)


# Home and Limit Sensors


@dataclass
class EnableHomeSwReport(OSCCommand):
    motorID: int
    enable: bool
    address: str = field(default="/enableHomeSwReport", init=False)


@dataclass
class EnableSwEventReport(OSCCommand):
    motorID: int
    enable: bool
    address: str = field(default="/enableSwEventReport", init=False)


@dataclass
class GetHomeSw(OSCCommand):
    motorID: int
    address: str = field(default="/getHomeSw", init=False)


@dataclass
class EnableLimitSwReport(OSCCommand):
    motorID: int
    enable: bool
    address: str = field(default="/enableLimitSwReport", init=False)


@dataclass
class GetLimitSw(OSCCommand):
    motorID: int
    address: str = field(default="/getLimitSw", init=False)


@dataclass
class SetHomeSwMode(OSCCommand):
    motorID: int
    SW_MODE: bool
    address: str = field(default="/setHomeSwMode", init=False)


@dataclass
class GetHomeSwMode(OSCCommand):
    motorID: int
    address: str = field(default="/getHomeSwMode", init=False)


@dataclass
class SetLimitSwMode(OSCCommand):
    motorID: int
    SW_MODE: bool
    address: str = field(default="/setLimitSwMode", init=False)


@dataclass
class GetLimitSwMode(OSCCommand):
    motorID: int
    address: str = field(default="/getLimitSwMode", init=False)


# Position Management


@dataclass
class SetPosition(OSCCommand):
    motorID: int
    newPosition: int
    address: str = field(default="/setPosition", init=False)


@dataclass
class GetPosition(OSCCommand):
    motorID: int
    address: str = field(default="/getPosition", init=False)


@dataclass
class ResetPos(OSCCommand):
    motorID: int
    address: str = field(default="/resetPos", init=False)


@dataclass
class SetMark(OSCCommand):
    motorID: int
    MARK: int
    address: str = field(default="/setMark", init=False)


@dataclass
class GetMark(OSCCommand):
    motorID: int
    address: str = field(default="/getMark", init=False)


@dataclass
class GoHome(OSCCommand):
    motorID: int
    address: str = field(default="/goHome", init=False)


@dataclass
class GoMark(OSCCommand):
    motorID: int
    address: str = field(default="/goMark", init=False)


# Motor Control


@dataclass
class Run(OSCCommand):
    motorID: int
    speed: float
    address: str = field(default="/run", init=False)


@dataclass
class Move(OSCCommand):
    motorID: int
    step: int
    address: str = field(default="/move", init=False)


@dataclass
class GoTo(OSCCommand):
    motorID: int
    position: int
    address: str = field(default="/goTo", init=False)


@dataclass
class GoToDir(OSCCommand):
    motorID: int
    DIR: bool
    position: int
    address: str = field(default="/goToDir", init=False)


@dataclass
class SoftStop(OSCCommand):
    motorID: int
    address: str = field(default="/softStop", init=False)


@dataclass
class HardStop(OSCCommand):
    motorID: int
    address: str = field(default="/hardStop", init=False)


@dataclass
class SoftHiZ(OSCCommand):
    motorID: int
    address: str = field(default="/softHiZ", init=False)


@dataclass
class HardHiZ(OSCCommand):
    motorID: int
    address: str = field(default="/hardHiZ", init=False)


# Electromagnetic Brake


@dataclass
class EnableElectromagnetBrake(OSCCommand):
    motorID: int
    enable: bool
    address: str = field(default="/enableElectromagnetBrake", init=False)


@dataclass
class Activate(OSCCommand):
    motorID: int
    state: bool
    address: str = field(default="/activate", init=False)


@dataclass
class Free(OSCCommand):
    motorID: int
    state: bool
    address: str = field(default="/free", init=False)


@dataclass
class SetBrakeTransitionDuration(OSCCommand):
    motorID: int
    duration: int
    address: str = field(default="/setBrakeTransitionDuration", init=False)


@dataclass
class GetBrakeTransitionDuration(OSCCommand):
    motorID: int
    address: str = field(default="/getBrakeTransitionDuration", init=False)


# Servo Mode


@dataclass
class EnableServoMode(OSCCommand):
    motorID: int
    enable: bool
    address: str = field(default="/enableServoMode", init=False)


@dataclass
class SetServoParam(OSCCommand):
    motorID: int
    kP: float
    kI: float
    kD: float
    address: str = field(default="/setServoParam", init=False)


@dataclass
class GetServoParam(OSCCommand):
    motorID: int
    address: str = field(default="/getServoParam", init=False)


@dataclass
class SetTargetPosition(OSCCommand):
    motorID: int
    position: int
    address: str = field(default="/setTargetPosition", init=False)


@dataclass
class SetTargetPositionList(OSCCommand):
    position1: int
    position2: int
    position3: int
    position4: int
    address: str = field(default="/setTargetPositionList", init=False)
