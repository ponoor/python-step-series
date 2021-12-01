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
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/system-settings/#setdestip"""  # noqa

    address: str = field(default="/setDestIp", init=False)


@dataclass
class GetVersion(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/system-settings/#getversion"""  # noqa

    address: str = field(default="/getVersion", init=False)


@dataclass
class GetConfigName(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/system-settings/#getconfigname"""  # noqa

    address: str = field(default="/getConfigName", init=False)


@dataclass
class ReportError(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/system-settings/#reporterror_boolenable"""  # noqa

    address: str = field(default="/reportError", init=False)
    enable: bool


# Motor Driver Settings


@dataclass
class SetMicrostepMode(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/motor-driver-settings/#setmicrostepmode_intmotorid_intstep_sel"""  # noqa

    address: str = field(default="/setMicrostepMode", init=False)
    motorID: int
    STEP_SEL: int


@dataclass
class GetMicrostepMode(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/motor-driver-settings/#setmicrostepmode_intmotorid_intstep_sel"""  # noqa

    address: str = field(default="/getMicrostepMode", init=False)
    motorID: int


@dataclass
class EnableLowSpeedOptimize(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/motor-driver-settings/#enablelowspeedoptimize_intmotorid_boolenable"""  # noqa

    address: str = field(default="/enableLowSpeedOptimize", init=False)
    motorID: int
    enable: bool


@dataclass
class SetLowSpeedOptimizeThreshold(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/motor-driver-settings/#setlowspeedoptimizethreshold_intmotorid_floatlowspeedoptimizationthreshold"""  # noqa

    address: str = field(default="/setLowSpeedOptimizeThreshold", init=False)
    motorID: int
    lowSpeedOptimizationThreshold: float


@dataclass
class GetLowSpeedOptimizeThreshold(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/motor-driver-settings/#getlowspeedoptimizethreshold_intmotorid"""  # noqa

    address: str = field(default="/getLowSpeedOptimizeThreshold", init=False)
    motorID: int


@dataclass
class EnableBusyReport(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/motor-driver-settings/#enablebusyreport_intmotorid_boolenable"""  # noqa

    address: str = field(default="/enableBusyReport", init=False)
    motorID: int
    enable: bool


@dataclass
class GetBusy(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/motor-driver-settings/#getbusy_intmotorid"""  # noqa

    address: str = field(default="/getBusy", init=False)
    motorID: int


@dataclass
class EnableHiZReport(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/motor-driver-settings/#enablehizreport_intmotorid_boolenable"""  # noqa

    address: str = field(default="/enableHizReport", init=False)
    motorID: int
    enable: bool


@dataclass
class GetHiZ(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/motor-driver-settings/#gethiz_intmotorid"""  # noqa

    address: str = field(default="/getHiZ", init=False)
    motorID: int


@dataclass
class EnableMotorStatusReport(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/motor-driver-settings/#enablemotorstatusreport_intmotorid_boolenable"""  # noqa

    address: str = field(default="/enableMotorStatusReport", init=False)
    motorID: int
    enable: bool


@dataclass
class GetMotorStatus(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/motor-driver-settings/#getmotorstatus_intmotorid"""  # noqa

    address: str = field(default="/getMotorStatus", init=False)
    motorID: int


@dataclass
class GetAdcVal(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/motor-driver-settings/#getadcval_intmotorid"""  # noqa

    address: str = field(default="/getAdcVal", init=False)
    motorID: int


@dataclass
class GetStatus(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/motor-driver-settings/#getstatus_intmotorid"""  # noqa

    address: str = field(default="/getStatus", init=False)
    motorID: int


@dataclass
class GetConfigRegister(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/motor-driver-settings/#getconfigregister_intmotorid"""  # noqa

    address: str = field(default="/getConfigRegister", init=False)
    motorID: int


@dataclass
class ResetMotorDriver(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/motor-driver-settings/#resetmotordriver_intmotorid"""  # noqa

    address: str = field(default="/resetMotorDriver", init=False)
    motorID: int


# Alarm Settings


@dataclass
class EnableUvloReport(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#enableuvloreport_intmotorid_boolenable"""  # noqa

    address: str = field(default="/enableUvloReport", init=False)
    motorID: int
    enable: bool


@dataclass
class GetUvlo(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#getuvlo_intmotorid"""  # noqa

    address: str = field(default="/getUvlo", init=False)
    motorID: int


@dataclass
class EnableThermalStatusReport(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#enablethermalstatusreport_intmotorid_boolenable"""  # noqa

    address: str = field(default="/enableThermalStatusReport", init=False)
    motorID: int
    enable: bool


@dataclass
class GetThermalStatus(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#getthermalstatus_intmotorid"""  # noqa

    address: str = field(default="/getThermalStatus", init=False)
    motorID: int


@dataclass
class EnableOverCurrentReport(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#enableovercurrentreport_intmotorid_boolenable"""  # noqa

    address: str = field(default="/enableOverCurrentReport", init=False)
    motorID: int
    enable: bool


@dataclass
class SetOverCurrentThreshold(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#setovercurrentthreshold_intmotorid_intocd_th"""  # noqa

    address: str = field(default="/setOverCurrentThreshold", init=False)
    motorID: int
    OCD_TH: int


@dataclass
class GetOverCurrentThreshold(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#getovercurrentthreshold_intmotorid"""  # noqa

    address: str = field(default="/getOverCurrentThreshold", init=False)
    motorID: int


@dataclass
class EnableStallReport(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#enablestallreport_intmotorid_boolenable"""  # noqa

    address: str = field(default="/enableStallReport", init=False)
    motorID: int
    enable: bool


@dataclass
class SetStallThreshold(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#setstallthreshold_intmotorid_intstall_th"""  # noqa

    address: str = field(default="/setStallThreshold", init=False)
    motorID: int
    STALL_TH: int


@dataclass
class GetStallThreshold(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#getstallthreshold_intmotorid"""  # noqa

    address: str = field(default="/getStallThreshold", init=False)
    motorID: int


@dataclass
class SetProhibitMotionOnHomeSw(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#setprohibitmotiononhomesw_intmotorid_boolenable"""  # noqa

    address: str = field(default="/setProhibitMotionOnHomeSw", init=False)
    motorID: int
    enable: bool


@dataclass
class GetProhibitMotionOnHomeSw(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#getprohibitmotiononhomesw_intmotorid"""  # noqa

    address: str = field(default="/getProhibitMotionOnHomeSw", init=False)
    motorID: int


@dataclass
class SetProhibitMotionOnLimitSw(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#setprohibitmotiononlimitsw_intmotorid_boolenable"""  # noqa

    address: str = field(default="/setProhibitMotionOnLimitSw", init=False)
    motorID: int
    enable: bool


@dataclass
class GetProhibitMotionOnLimitSw(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#getprohibitmotiononlimitsw_intmotorid"""  # noqa

    address: str = field(default="/getProhibitMotionOnLimitSw", init=False)
    motorID: int


# Voltage and Current Mode Settings


@dataclass
class SetVoltageMode(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setvoltagemode_intmotorid"""  # noqa

    address: str = field(default="/setVoltageMode", init=False)
    motorID: int


@dataclass
class SetKval(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setkval_intmotorid_intholdkval_intrunkval_intacckval_intsetdeckval"""  # noqa

    address: str = field(default="/setKval", init=False)
    motorID: int
    holdKVAL: int
    runKVAL: int
    accKVAL: int
    setDecKVAL: int


@dataclass
class GetKval(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#getkval_intmotorid"""  # noqa

    address: str = field(default="/getKval", init=False)
    motorID: int


@dataclass
class SetBemfParam(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setbemfparam_intmotorid_intint_speed_intst_slp_intfn_slp_acc_intfn_slp_dec"""  # noqa

    address: str = field(default="/setBemfParam", init=False)
    motorID: int
    INT_SPEED: int
    ST_SLP: int
    FN_SLP_ACC: int
    FN_SLP_DEC: int


@dataclass
class GetBemfParam(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#getbemfparam_intmotorid"""  # noqa

    address: str = field(default="/getBemfParam", init=False)
    motorID: int


@dataclass
class SetCurrentMode(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setcurrentmode_intmotorid"""  # noqa

    address: str = field(default="/setCurrentMode", init=False)
    motorID: int


@dataclass
class SetTval(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#settval_intmotorid_intholdtval_intruntval_intacctval_intsetdectval"""  # noqa

    address: str = field(default="/setTval", init=False)
    motorID: int
    holdTVAL: int
    runTVAL: int
    accTVAL: int
    setDecTVAL: int


@dataclass
class GetTval(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#gettval_intmotorid"""  # noqa

    address: str = field(default="/getTval", init=False)
    motorID: int


@dataclass
class SetDecayModeParam(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setdecaymodeparam_intmotorid_intt_fast_intton_min_inttoff_min"""  # noqa

    address: str = field(default="/setDecayModeParam", init=False)
    motorID: int
    T_FAST: int
    TON_MIN: int
    TOFF_MIN: int


@dataclass
class GetDecayModeParam(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#getdecaymodeparam_intmotorid"""  # noqa

    address: str = field(default="/getDecayModeParam", init=False)
    motorID: int


# Speed Profile


@dataclass
class SetSpeedProfile(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/speed-profile/#setspeedprofile_intmotorid_floatacc_floatdec_floatmaxspeed"""  # noqa

    address: str = field(default="/setSpeedProfile", init=False)
    motorID: int
    acc: float
    dec: float
    maxSpeed: float


@dataclass
class GetSpeedProfile(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/speed-profile/#getspeedprofile_intmotorid"""  # noqa

    address: str = field(default="/getSpeedProfile", init=False)
    motorID: int


@dataclass
class SetFullstepSpeed(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/speed-profile/#setfullstepspeed_intmotorid_floatfullstepspeed"""  # noqa

    address: str = field(default="/setFullstepSpeed", init=False)
    motorID: int
    fullstepSpeed: float


@dataclass
class GetFullstepSpeed(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/speed-profile/#getfullstepspeed_intmotorid"""  # noqa

    address: str = field(default="/getFullstepSpeed", init=False)
    motorID: int


@dataclass
class SetMaxSpeed(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/speed-profile/#setmaxspeed_intmotorid_floatmaxspeed"""  # noqa

    address: str = field(default="/setMaxSpeed", init=False)
    motorID: int
    maxSpeed: float


@dataclass
class SetAcc(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/speed-profile/#setacc_intmotorid_floatacc"""  # noqa

    address: str = field(default="/setAcc", init=False)
    motorID: int
    acc: float


@dataclass
class SetDec(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/speed-profile/#setdec_intmotorid_floatdec"""  # noqa

    address: str = field(default="/setDec", init=False)
    motorID: int
    dec: float


@dataclass
class SetMinSpeed(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/speed-profile/#setminspeed_intmotorid_floatminspeed"""  # noqa

    address: str = field(default="/setMinSpeed", init=False)
    motorID: int
    minSpeed: float


@dataclass
class GetMinSpeed(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/speed-profile/#getminspeed_intmotorid"""  # noqa

    address: str = field(default="/getMinSpeed", init=False)
    motorID: int


@dataclass
class GetSpeed(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/speed-profile/#getspeed_intmotorid"""  # noqa

    address: str = field(default="/getSpeed", init=False)
    motorID: int


# Homing


@dataclass
class Homing(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#homing_intmotorid"""  # noqa

    address: str = field(default="/homing", init=False)
    motorID: int


@dataclass
class GetHomingStatus(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#sethomingdirection_intmotorid_booldirection"""  # noqa

    address: str = field(default="/getHomingStatus", init=False)
    motorID: int


@dataclass
class SetHomingDirection(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#sethomingspeed_intmotorid_floatspeed"""  # noqa

    address: str = field(default="/setHomingDirection", init=False)
    motorID: int
    direction: bool


@dataclass
class GetHomingDirection(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#gethomingdirection_intmotorid"""  # noqa

    address: str = field(default="/getHomingDirection", init=False)
    motorID: int


@dataclass
class SetHomingSpeed(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#sethomingspeed_intmotorid_floatspeed"""  # noqa

    address: str = field(default="/setHomingSpeed", init=False)
    motorID: int
    speed: float


@dataclass
class GetHomingSpeed(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#gethomingspeed_intmotorid"""  # noqa

    address: str = field(default="/getHomingSpeed", init=False)
    motorID: int


@dataclass
class GoUntil(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#gountil_intmotorid_boolact_floatspeed"""  # noqa

    address: str = field(default="/goUntil", init=False)
    motorID: int
    ACT: bool
    speed: float


@dataclass
class SetGoUntilTimeout(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#setgountiltimeout_intmotorid_inttimeout"""  # noqa

    address: str = field(default="/setGoUntilTimeout", init=False)
    motorID: int
    timeOut: int


@dataclass
class GetGoUntilTimeout(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#getgountiltimeout_intmotorid"""  # noqa

    address: str = field(default="/getGoUntilTimeout", init=False)
    motorID: int


@dataclass
class ReleaseSw(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#releasesw_intmotorid_boolact_booldir"""  # noqa

    address: str = field(default="/releaseSw", init=False)
    motorID: int
    ACT: bool
    DIR: bool


@dataclass
class SetReleaseSwTimeout(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#setreleaseswtimeout_intmotorid_inttimeout"""  # noqa

    address: str = field(default="/setReleaseSwTimeout", init=False)
    motorID: int
    timeOut: int


@dataclass
class GetReleaseSwTimeout(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#setreleaseswtimeout_intmotorid_inttimeout"""  # noqa

    address: str = field(default="/getReleaseSwTimeout", init=False)
    motorID: int


# Home and Limit Sensors


@dataclass
class EnableHomeSwReport(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/home-and-limit-sensers/#enablehomeswreport_intmotorid_boolenable"""  # noqa

    address: str = field(default="/enableHomeSwReport", init=False)
    motorID: int
    enable: bool


@dataclass
class EnableSwEventReport(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/home-and-limit-sensers/#enablesweventreport_intmotorid_boolenable"""  # noqa

    address: str = field(default="/enableSwEventReport", init=False)
    motorID: int
    enable: bool


@dataclass
class GetHomeSw(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/home-and-limit-sensers/#gethomesw_intmotorid"""  # noqa

    address: str = field(default="/getHomeSw", init=False)
    motorID: int


@dataclass
class EnableLimitSwReport(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/home-and-limit-sensers/#enablelimitswreport_intmotorid_boolenable"""  # noqa

    address: str = field(default="/enableLimitSwReport", init=False)
    motorID: int
    enable: bool


@dataclass
class GetLimitSw(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/home-and-limit-sensers/#getlimitsw_intmotorid"""  # noqa

    address: str = field(default="/getLimitSw", init=False)
    motorID: int


@dataclass
class SetHomeSwMode(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/home-and-limit-sensers/#sethomeswmode_intmotorid_boolsw_mode"""  # noqa

    address: str = field(default="/setHomeSwMode", init=False)
    motorID: int
    SW_MODE: bool


@dataclass
class GetHomeSwMode(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/home-and-limit-sensers/#gethomeswmode_intmotorid"""  # noqa

    address: str = field(default="/getHomeSwMode", init=False)
    motorID: int


@dataclass
class SetLimitSwMode(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/home-and-limit-sensers/#setlimitswmode_intmotorid_boolsw_mode"""  # noqa

    address: str = field(default="/setLimitSwMode", init=False)
    motorID: int
    SW_MODE: bool


@dataclass
class GetLimitSwMode(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/home-and-limit-sensers/#getlimitswmode_intmotorid"""  # noqa

    address: str = field(default="/getLimitSwMode", init=False)
    motorID: int


# Position Management


@dataclass
class SetPosition(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/position-management/#setposition_intmotorid_intnewposition"""  # noqa

    address: str = field(default="/setPosition", init=False)
    motorID: int
    newPosition: int


@dataclass
class GetPosition(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/position-management/#getposition_intmotorid"""  # noqa

    address: str = field(default="/getPosition", init=False)
    motorID: int


@dataclass
class ResetPos(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/position-management/#resetpos_intmotorid"""  # noqa

    address: str = field(default="/resetPos", init=False)
    motorID: int


@dataclass
class SetMark(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/position-management/#setmark_intmotorid_intmark"""  # noqa

    address: str = field(default="/setMark", init=False)
    motorID: int
    MARK: int


@dataclass
class GetMark(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/position-management/#getmark_intmotorid"""  # noqa

    address: str = field(default="/getMark", init=False)
    motorID: int


@dataclass
class GoHome(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/position-management/#gohome_intmotorid"""  # noqa

    address: str = field(default="/goHome", init=False)
    motorID: int


@dataclass
class GoMark(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/position-management/#gomark_intmotorid"""  # noqa

    address: str = field(default="/goMark", init=False)
    motorID: int


# Motor Control


@dataclass
class Run(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/motor-control/#run_intmotorid_floatspeed"""  # noqa

    address: str = field(default="/run", init=False)
    motorID: int
    speed: float


@dataclass
class Move(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/motor-control/#move_intmotorid_intstep"""  # noqa

    address: str = field(default="/move", init=False)
    motorID: int
    step: int


@dataclass
class GoTo(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/motor-control/#goto_intmotorid_intposition"""  # noqa

    address: str = field(default="/goTo", init=False)
    motorID: int
    position: int


@dataclass
class GoToDir(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/motor-control/#gotodir_intmotorid_booldir_intposition"""  # noqa

    address: str = field(default="/goToDir", init=False)
    motorID: int
    DIR: bool
    position: int


@dataclass
class SoftStop(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/motor-control/#softstop_intmotorid"""  # noqa

    address: str = field(default="/softStop", init=False)
    motorID: int


@dataclass
class HardStop(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/motor-control/#hardstop_intmotorid"""  # noqa

    address: str = field(default="/hardStop", init=False)
    motorID: int


@dataclass
class SoftHiZ(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/motor-control/#softhiz_intmotorid"""  # noqa

    address: str = field(default="/softHiZ", init=False)
    motorID: int


@dataclass
class HardHiZ(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/motor-control/#hardhiz_intmotorid"""  # noqa

    address: str = field(default="/hardHiZ", init=False)
    motorID: int


# Electromagnetic Brake


@dataclass
class EnableElectromagnetBrake(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/brake/#enableelectromagnetbrake_intmotorid_boolenable"""  # noqa

    address: str = field(default="/enableElectromagnetBrake", init=False)
    motorID: int
    enable: bool


@dataclass
class Activate(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/brake/#activate_intmotorid_boolstate"""  # noqa

    address: str = field(default="/activate", init=False)
    motorID: int
    state: bool


@dataclass
class Free(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/brake/#free_intmotorid_boolstate"""  # noqa

    address: str = field(default="/free", init=False)
    motorID: int
    state: bool


@dataclass
class SetBrakeTransitionDuration(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/brake/#setbraketransitionduration_intmotorid_intduration"""  # noqa

    address: str = field(default="/setBrakeTransitionDuration", init=False)
    motorID: int
    duration: int


@dataclass
class GetBrakeTransitionDuration(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/brake/#getbraketransitionduration_intmotorid"""  # noqa

    address: str = field(default="/getBrakeTransitionDuration", init=False)
    motorID: int


# Servo Mode


@dataclass
class EnableServoMode(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/servo-mode/#enableservomode_intmotorid_boolenable"""  # noqa

    address: str = field(default="/enableServoMode", init=False)
    motorID: int
    enable: bool


@dataclass
class SetServoParam(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/servo-mode/#setservoparam_intmotorid_floatkp_floatki_floatkd"""  # noqa

    address: str = field(default="/setServoParam", init=False)
    motorID: int
    kP: float
    kI: float
    kD: float


@dataclass
class GetServoParam(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/servo-mode/#getservoparam_intmotorid"""  # noqa

    address: str = field(default="/getServoParam", init=False)
    motorID: int


@dataclass
class SetTargetPosition(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/servo-mode/#settargetposition_intmotorid_intposition"""  # noqa

    address: str = field(default="/setTargetPosition", init=False)
    motorID: int
    position: int


@dataclass
class SetTargetPositionList(OSCCommand):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/servo-mode/#settargetpositionlist_intposition1_intposition2_intposition3_intposition4"""  # noqa

    address: str = field(default="/setTargetPositionList", init=False)
    position1: int
    position2: int
    position3: int
    position4: int
