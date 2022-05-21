"""Messages received from the device."""


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
            # Concat split string args
            if all([isinstance(x, str) for x in args]):
                args = (" ".join(args),)

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

                # Now add all to kwargs
                field_names = [
                    k
                    for k in self.__annotations__.keys()
                    if k not in kwargs and not k.endswith("_re")
                ]
                for i, arg in enumerate(args):
                    field_name = field_names[i]
                    kwargs[field_name] = arg
                args = tuple()
                kwargs.pop("address", None)

            # Remove unnecessary address identifier
            args = list(args)
            if args and args[0] == self.address:
                args.pop(0)

            # Eval positional args
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
class OSCResponse(object):
    """An abstract class meant to be implemented by OSC resp objects."""

    address: str


# Automatic Messages


@dataclass
class Booted(OSCResponse):
    """Sent when the device (re)starts.

    This message is sent regardless if
    :py:class:`stepseries.commands.SetDestIP` has been recieved. By
    watching for this message, you can determine when the device
    restarts even if unexpectedly.

    When the firmware has started and an ethernet uplink is confirmed,
    this message will be sent.

    This is a broadcast message meaning it is sent to all devices on the
    subnet (address ``255.255.255.255``). If this is unacceptable for
    your network, you can disable it via the `Config Tool`_.

    .. _Config Tool: http://ponoor.com/tools/step400-config/
    """

    address: str = field(default="/booted", init=False)
    deviceID: int
    """
    ===== ===================================
    Range Description
    ===== ===================================
    0-255 The device ID set by the DIP switch
    ===== ===================================
    """


@dataclass
class ErrorCommand(OSCResponse, Exception):
    """Sent if an error is detected while executing a command.

    Can be enabled or disabled with
    :py:class:`stepseries.commands.ReportError`.
    """

    address: str = field(default="/error/command", init=False)
    errorText: str
    """
    ================= ===============================================================================
    errorText	      Description
    ================= ===============================================================================
    CommandIgnored	  The command is currently not executable. Also refer Timing section.
    MotorIdNotMatch	  Motor ID is not appropriate.
    BrakeEngaging	  A motion command was sent while the electromagnet brake was active.
    HomeSwActivating  Movement from home sensor position towards the origin point.
    LimitSwActivating Movement from limit sensor position towards the opposite direction from origin.
    GoUntilTimeout    Timeout while executing /goUntil command.
    ReleaseSwTimeout  Timeout while executing /releaseSw command.
    InServoMode       Received a command which can not be executed while servo mode.
    ================= ===============================================================================
    """
    motorID: int = None
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """


@dataclass
class ErrorOSC(OSCResponse, Exception):
    """Sent if any error is detected in the OSC command."""

    address: str = field(default="/error/osc", init=False)
    errorText: str
    """
    =============== =================================
    errorText	    Description
    =============== =================================
    messageNotMatch	There is no corresponding command
    oscSyntaxError	The OSC format is out of standard
    WrongDataType	Wrong datatype of in argument(s)
    =============== =================================
    """
    motorID: int = None
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """


@dataclass
class Busy(OSCResponse):
    """The BUSY state of a motor."""

    address: str = field(default="/busy", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    state: int
    """
    ===== ====================
    Range Description
    ===== ====================
    0-1   1: BUSY, 0: Not BUSY
    ===== ====================
    """


@dataclass
class HiZ(OSCResponse):
    """The high-impedance (HiZ) state of a motor."""

    address: str = field(default="/HiZ", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    state: int
    """
    ===== ==================
    Range Description
    ===== ==================
    0-1   1: HiZ, 0: Not HiZ
    ===== ==================
    """


@dataclass
class MotorStatus(OSCResponse):
    """The operating status of a motor."""

    address: str = field(default="/motorStatus", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    MOT_STATUS: int
    """
    ===== ==============
    Range Description
    ===== ==============
    0     Stopped
    1     Acceleration
    2     Deceleration
    3     Constant Speed
    ===== ==============
    """


@dataclass
class HomingStatus(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/automatically-sent-messages-from-step-400/#homingstatus"""  # noqa

    address: str = field(default="/homingStatus", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    homingStatus: int


@dataclass
class Uvlo(OSCResponse):
    """The current state of undervoltage lockout of a motor."""

    address: str = field(default="/uvlo", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    state: int
    """
    ===== ===================
    Range Description
    ===== ===================
    0-1   1: UVLO, 0: No UVLO
    ===== ===================
    """


@dataclass
class ThermalStatus(OSCResponse):
    """The thermal status of a motor.

    The thresholds between the STEP400 and STEP800 do vary.
    """

    address: str = field(default="/thermalStatus", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    thermalStatus: int
    """
    **STEP400**:

    ===== =============== ============= =================
    Range Description     Set Threshold Release Threshold
    ===== =============== ============= =================
    0     Normal          N/A           N/A
    1     Warning         135°C         125°C
    2     Bridge Shutdown 155°C         145°C
    3     Device Shutdown 170°C         130°C
    ===== =============== ============= =================

    **STEP800**:

    ===== =============== ============= =================
    Range Description     Set Threshold Release Threshold
    ===== =============== ============= =================
    0     Normal          N/A           N/A
    1     Warning         130°C         130°C
    2     Bridge Shutdown 160°C         130°C
    ===== =============== ============= =================
    """


@dataclass
class OverCurrent(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/automatically-sent-messages-from-step-400/#overcurrent"""  # noqa

    address: str = field(default="/overCurrent", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """


@dataclass
class Stall(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/automatically-sent-messages-from-step-400/#stall"""  # noqa

    address: str = field(default="/stall", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """


# System Settings


@dataclass
class DestIP(OSCResponse):
    """Confirmation :py:class:`stepseries.commands.SetDestIP` has been
    recieved.
    """

    address: str = field(default="/destIp", init=False)
    destIp0: int
    """The first octet of the IP address set."""
    destIp1: int
    """The second octet of the IP address set."""
    destIp2: int
    """The third octet of the IP address set."""
    destIp3: int
    """The fourth octet of the IP address set."""
    isNewDestIp: int
    """Indicates if the IP address has changed from what is already set."""


@dataclass
class Version(OSCResponse):
    """The firmware version burnt onto the chip."""

    address: str = field(default="/version", init=False)
    firmware_name: str
    """Name of the firmware."""
    firmware_version: str
    """Version of the firmware."""
    compile_date: str
    """Compile date of the firmware"""

    # Custom regex to breakout
    compile_date_re: re.Pattern = field(
        default=re.compile(r"\w+ ? \d{1,2} \d{4} .+"),
        init=False,
        repr=False,
    )


@dataclass
class ConfigName(OSCResponse):
    """Metadata about the configuration file."""

    address: str = field(default="/configName", init=False)
    configName: str
    """Name of the configuration."""
    sdInitializeSucceeded: int
    """If the microSD card was successfully read."""
    configFileOpenSucceeded: int
    """If the device could open the configuration file."""
    configFileParseSucceeded: int
    """If the configuration was successfully parsed."""


# Motor Driver Settings


@dataclass
class MicrostepMode(OSCResponse):
    """The microstep mode of the motor."""

    address: str = field(default="/microstepMode", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    STEP_SEL: int
    """
    ===== ===========
    Range Description
    ===== ===========
    0     Full-step
    1     Half-step
    2     1/4 step
    3     1/8 step
    4     1/16 step
    5     1/32 step
    6     1/64 step
    7     1/128 step
    ===== ===========
    """


@dataclass
class LowSpeedOptimizeThreshold(OSCResponse):
    """The threshold to enable low speed optimization."""

    address: str = field(default="/lowSpeedOptimizeThreshold", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    lowSpeedOptimizeThreshold: float
    """0.0 - 976.3 steps/s"""
    optimizationEnabled: int
    """
    ===== =======================
    Range Description
    ===== =======================
    0-1   1: Enabled, 0: Disabled
    ===== =======================
    """


@dataclass
class Dir(OSCResponse):
    """The direction of a motor."""

    address: str = field(default="/dir", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    direction: int
    """
    ===== ======================
    Range Description
    ===== ======================
    0-1   1: Forward, 0: Reverse
    ===== ======================
    """


@dataclass
class AdcVal(OSCResponse):
    """The ADC_OUT register value from the PowerSTEP01 chip."""

    address: str = field(default="/adcVal", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    ADC_OUT: int
    """
    ===== ======================================
    Range Description
    ===== ======================================
    0-31  5-bit read out of the ADC_OUT register
    ===== ======================================
    """


@dataclass
class Status(OSCResponse):
    """The STATUS of a motor.

    Refer to STATUS in the datasheet for the information contained in
    the registers. Some bits are latched and reset when the STATUS
    registers are read out. Because the firmware constantly reads these
    registers, they are immediately reset. It is possible to setup event
    to be reported depending on the data read, so please use those
    commands.

    ================ ======================== =========================================================
    STEP400 Bits     STEP800 Bits             Configuration Command
    ================ ======================== =========================================================
    UVLO             UVLO                     :py:class:`stepseries.commands.EnableUvloReport`
    UVLO_ADC         N/A                      Not implemented
    OCD              OCD                      :py:class:`stepseries.commands.EnableOverCurrentReport`
    STALL_A, STALL_B STEP_LOSS_A, STEP_LOSS_B :py:class:`stepseries.commands.EnableStallReport`
    CMD_ERROR        WRONG_CMD, NOTPREF_CMD   :py:class:`stepseries.commands.EnableCommandErrorReport`
    TH_STATUS        TH_WRN, TH_SD            :py:class:`stepseries.commands.EnableThermalStatusReport`
    SW_EVN           SW_EVN                   :py:class:`stepseries.commands.EnableHomeSwReport`
    MOT_STATUS       MOT_STATUS               :py:class:`stepseries.commands.EnableMotorStatusReport`
    SW_F             SW_F                     :py:class:`stepseries.commands.EnableHomeSwReport`
    BUSY             BUSY                     :py:class:`stepseries.commands.EnableBusyReport`
    HIZ              HIZ                      :py:class:`stepseries.commands.EnableHiZReport`
    ================ ======================== =========================================================
    """

    address: str = field(default="/status", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    status: int
    """
    ===== ======================================
    Range Description
    ===== ======================================
    0-31  5-bit read out of the ADC_OUT register
    ===== ======================================
    """


@dataclass
class ConfigRegister(OSCResponse):
    """The 16-bit CONFIG register value from the motor driver."""

    address: str = field(default="/configRegister", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    CONFIG: int
    """0-65535 (0xFFFF)"""


# Alarm Settings


@dataclass
class OverCurrentThreshold(OSCResponse):
    """The threshold of over current in mA."""

    address: str = field(default="/overCurrentThreshold", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    overCurrentThreshold: float
    """
    ========== =============
    Controller Range
    ========== =============
    STEP400    312.5-10000.0
    STEP800    375.0-6000.0
    ========== =============
    """


@dataclass
class StallThreshold(OSCResponse):
    """The stall detection threshold in mA."""

    address: str = field(default="/stallThreshold", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    stallThreshold: float
    """
    ========== =============
    Controller Range
    ========== =============
    STEP400    312.5-10000.0
    STEP800    31.25-4000.0
    ========== =============
    """


@dataclass
class ProhibitMotionOnHomeSw(OSCResponse):
    """Whether motion towards origin is permitted when HomeSw is active."""

    address: str = field(default="/prohibitMotionOnHomeSw", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    enable: int
    """
    ===== =========================
    Range Description
    ===== =========================
    0-1   1: Prohibited, 0: Allowed
    ===== =========================
    """


@dataclass
class ProhibitMotionOnLimitSw(OSCResponse):
    """
    Whether motion away from origin is permitted when LimitSw is active.
    """

    address: str = field(default="/prohibitMotionOnLimitSw", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    enable: int
    """
    ===== =========================
    Range Description
    ===== =========================
    0-1   1: Prohibited, 0: Allowed
    ===== =========================
    """


# Voltage and Current Mode Settings


@dataclass
class Kval(OSCResponse):
    """All four KVALs together."""

    address: str = field(default="/kval", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    holdKVAL: int
    """
    ===== =================
    Range Description
    ===== =================
    0-255 KVAL when stopped
    ===== =================
    """
    runKVAL: int
    """
    ===== =================
    Range Description
    ===== =================
    0-255 KVAL when stopped
    ===== =================
    """
    accKVAL: int
    """
    ===== =================
    Range Description
    ===== =================
    0-255 KVAL when stopped
    ===== =================
    """
    decKVAL: int
    """
    ===== =================
    Range Description
    ===== =================
    0-255 KVAL when stopped
    ===== =================
    """


@dataclass
class BemfParam(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#getbemfparam_intmotorid"""  # noqa

    address: str = field(default="/bemfParam", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    INT_SPEED: int
    ST_SLP: int
    FN_SLP_ACC: int
    FN_SLP_DEC: int


@dataclass
class Tval(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#gettval_intmotorid"""  # noqa

    address: str = field(default="/tval", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    holdTVAL: int
    runTVAL: int
    accTVAL: int
    decTVAL: int


@dataclass
class Tval_mA(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#gettval_ma_intmotorid"""  # noqa

    address: str = field(default="/tval_mA", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    holdTVAL_mA: float
    runTVAL_mA: float
    accTVAL_mA: float
    decTVAL_mA: float


@dataclass
class DecayModeParam(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#getdecaymodeparam_intmotorid"""  # noqa

    address: str = field(default="/decayModeParam", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    T_FAST: int
    TON_MIN: int
    TOFF_MIN: int


# Speed Profile


@dataclass
class SpeedProfile(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/speed-profile/#getspeedprofile_intmotorid"""  # noqa

    address: str = field(default="/speedProfile", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    acc: float
    dec: float
    maxSpeed: float


@dataclass
class FullstepSpeed(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/speed-profile/#getfullstepspeed_intmotorid"""  # noqa

    address: str = field(default="/fullstepSpeed", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    fullstepSpeed: float


@dataclass
class MinSpeed(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/speed-profile/#getminspeed_intmotorid"""  # noqa

    address: str = field(default="/minSpeed", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    minSpeed: float


@dataclass
class Speed(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/speed-profile/#getspeed_intmotorid"""  # noqa

    address: str = field(default="/speed", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    speed: float


# Homing


@dataclass
class HomingDirection(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#gethomingdirection_intmotorid"""  # noqa

    address: str = field(default="/homingDirection", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    homingDirection: int


@dataclass
class HomingSpeed(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#gethomingspeed_intmotorid"""  # noqa

    address: str = field(default="/homingSpeed", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    homingSpeed: float


@dataclass
class GoUntilTimeout(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#getgountiltimeout_intmotorid"""  # noqa

    address: str = field(default="/goUntilTimeout", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    timeout: int


@dataclass
class ReleaseSwTimeout(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#setreleaseswtimeout_intmotorid_inttimeout"""  # noqa

    address: str = field(default="/releaseSwTimeout", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    timeout: int


# Home and Limit Sensors


@dataclass
class SwEvent(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/home-and-limit-sensers/#enablesweventreport_intmotorid_boolenable"""  # noqa

    address: str = field(default="/swEvent", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """


@dataclass
class HomeSw(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/home-and-limit-sensers/#gethomesw_intmotorid"""  # noqa

    address: str = field(default="/homeSw", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    swState: int
    direction: int


@dataclass
class LimitSw(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/home-and-limit-sensers/#getlimitsw_intmotorid"""  # noqa

    address: str = field(default="/limitSw", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    swState: int
    direction: int


@dataclass
class HomeSwMode(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/home-and-limit-sensers/#gethomeswmode_intmotorid"""  # noqa

    address: str = field(default="/homeSwMode", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    swMode: int


@dataclass
class LimitSwMode(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/home-and-limit-sensers/#getlimitswmode_intmotorid"""  # noqa

    address: str = field(default="/limitSwMode", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    swMode: int


# Position Management


@dataclass
class Position(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/position-management/#getposition_intmotorid"""  # noqa

    address: str = field(default="/position", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    ABS_POS: int


@dataclass
class PositionList(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/position-management/#getpositionlist"""  # noqa

    address: str = field(default="/positionList", init=False)
    position1: int
    position2: int
    position3: int
    position4: int
    position5: int = None
    position6: int = None
    position7: int = None
    position8: int = None


@dataclass
class ElPos(OSCResponse):
    """Documentation https://ponoor.com/en/docs/step-series/osc-command-reference/position-management/#getelpos_intmotorid"""  # noqa

    address: str = field(default="/elPos", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    fullstep: int
    microstep: int


@dataclass
class Mark(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/position-management/#getmark_intmotorid"""  # noqa

    address: str = field(default="/mark", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    MARK: int


# Electromagnetic Brake


@dataclass
class BrakeTransitionDuration(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/brake/#getbraketransitionduration_intmotorid"""  # noqa

    address: str = field(default="/brakeTransitionDuration", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    duration: int


# Servo Mode


@dataclass
class ServoParam(OSCResponse):
    """Documentation: https://ponoor.com/en/docs/step-series/osc-command-reference/servo-mode/#getservoparam_intmotorid"""  # noqa

    address: str = field(default="/servoParam", init=False)
    motorID: int
    """
    ========== ===========
    Controller Motor Range
    ========== ===========
    STEP400    1-4
    STEP800    1-8
    ========== ===========
    """
    kP: float
    kI: float
    kD: float
