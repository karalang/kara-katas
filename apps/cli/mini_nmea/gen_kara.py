"""Writes the generated parts of mini_nmea.kara to stdout: with the argument
`tables`, the sentence classes of the copy of pynmea2 in pynmea2/ (their
field names and converters, mixins and properties, and the SeaTalk command
names); with none, the files under data/."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
os.chdir(HERE)

from decimal import Decimal  # noqa: E402

import pynmea2  # noqa: E402
from pynmea2 import nmea, nmea_utils  # noqa: E402
from pynmea2.seatalk_utils import SeaTalk  # noqa: E402
from pynmea2.types.proprietary import ubx  # noqa: E402


def lit(s):
    out = []
    for ch in s:
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\t":
            out.append("\\t")
        elif ord(ch) < 32 or ord(ch) > 126:
            out.append("\\u{%x}" % ord(ch))
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


def conv_code(f):
    if f is nmea_utils.timestamp:
        return "ts"
    if f is nmea_utils.datestamp:
        return "ds"
    if f is int:
        return "int"
    if f is float:
        return "float"
    if f is Decimal:
        return "dec"
    if f is str:
        return "str"
    if getattr(f, "__name__", "") == "<lambda>" and "utcfromtimestamp" in f.__code__.co_names:
        return "utc"
    raise SystemExit("unknown converter %r" % f)


GROUPS = {"ASH", "GRM", "KWD", "MGN", "RDI", "SRF", "SXN", "TNL", "UBX", "VTX", "NOR"}

# Attributes a sentence object has besides its fields; a field may not
# share a name with one, since normal lookup would find it first.
PROPS = {"latitude", "longitude", "latitude_minutes", "longitude_minutes", "latitude_seconds",
         "longitude_seconds", "datetime", "is_valid", "datestamp", "tzinfo", "localdatetime",
         "waypoint_list", "num_transducers", "command_name", "satellite_list"}


def flags(cls):
    out = []
    if issubclass(cls, nmea_utils.LatLonFix):
        out.append("latlon")
    if issubclass(cls, nmea_utils.DatetimeFix):
        out.append("dt")
    if issubclass(cls, nmea_utils.ValidRMCStatusFix):
        out.append("vrmc")
    elif issubclass(cls, nmea_utils.ValidStatusFix):
        out.append("vstatus")
    if issubclass(cls, nmea_utils.ValidGSAFix):
        out.append("vgsa")
    if issubclass(cls, nmea_utils.ValidGGAFix):
        out.append("vgga")
    if issubclass(cls, nmea_utils.ValidVBWFix):
        out.append("vvbw")
    if cls is pynmea2.ZDA:
        out.append("zda")
    if cls is pynmea2.RTE:
        out.append("rte")
    if cls is pynmea2.R00:
        out.append("r00")
    if cls is pynmea2.XDR:
        out.append("xdr")
    if issubclass(cls, SeaTalk):
        out.append("seatalk")
    if cls is ubx.UBX03:
        out.append("ubx03")
    return out


def class_line(cls, base):
    props = set()
    for k in dir(cls):
        if isinstance(getattr(cls, k, None), property):
            props.add(k)
    if not props <= PROPS:
        raise SystemExit("%s has properties %r" % (cls.__name__, props - PROPS))
    fs = []
    for f in cls.fields:
        name = f[1]
        if (cls.__name__, name) == ("SRF103", "checksum"):
            # Normal lookup finds the checksum static method, whose repr
            # carries an address; the data has no SRF103 sentence.
            fs.append(name + "!")
            continue
        if name in props or hasattr(cls, name):
            raise SystemExit("%s field %s is also an attribute" % (cls.__name__, name))
        fs.append(name + (":" + conv_code(f[2]) if len(f) >= 3 else ""))
    return "%s|%s|%s|%s|%s" % (cls.__name__, base, ",".join(flags(cls)), ",".join(sorted(props)), ";".join(fs))


def tables():
    lines = []
    for name, cls in sorted(nmea.TalkerSentence.sentence_types.items()):
        assert name == cls.__name__
        lines.append(class_line(cls, "T"))
    for name, cls in sorted(nmea.ProprietarySentence.sentence_types.items()):
        assert name in GROUPS and name == cls.__name__ and cls.fields == ()
        lines.append(class_line(cls, "P"))
        for sub, scls in sorted(cls.sentence_types.items()):
            assert sub == scls.__name__
            lines.append(class_line(scls, name))
    assert {n for n in nmea.ProprietarySentence.sentence_types} == GROUPS
    print("// ------------------------------------------------------------ classes")
    print()
    print("// pynmea2's sentence classes, one per line: name | base (T for")
    print("// TalkerSentence, P for a manufacturer class under ProprietarySentence,")
    print("// else the manufacturer class it is registered with) | mixins | the")
    print("// properties the class has | fields as name[:converter], in order.")
    print("fn class_lines() -> Vec[String] {")
    print("    let mut v: Vec[String] = Vec.new();")
    for l in lines:
        print("    v.push(%s.to_string());" % lit(l))
    print("    v")
    print("}")
    print()
    print("// SeaTalk.byte_to_command")
    print("fn seatalk_command(cmd: ref String) -> String {")
    print("    let s = match cmd.as_str() {")
    for k, v in SeaTalk.byte_to_command.items():
        print("        %s => %s," % (lit(k), lit(v)))
    print('        _ => "Unknown Command",')
    print("    };")
    print("    s.to_string()")
    print("}")


def datafiles():
    names = []
    for root, dirs, files in os.walk("data"):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), "data")
            if not rel.startswith("out" + os.sep):
                names.append(rel)
    names.sort()
    print("// ------------------------------------------------------------ data")
    print()
    print("// The files under data/, in path order.")
    print("fn data_files() -> Vec[(String, String)] {")
    print("    let mut v: Vec[(String, String)] = Vec.new();")
    for k in range(len(names)):
        print("    v.push(data_%d());" % k)
    print("    v")
    print("}")
    for k, n in enumerate(names):
        text = open(os.path.join("data", n), encoding="utf-8", newline="").read()
        print()
        print("fn data_%d() -> (String, String) {" % k)
        print("    let mut t = String.new();")
        parts = text.split("\n")
        for i, line in enumerate(parts):
            piece = line + ("\n" if i < len(parts) - 1 else "")
            if piece:
                print("    t.push_str(%s);" % lit(piece))
        print("    (%s.to_string(), t)" % lit(n))
        print("}")


if sys.argv[1:] == ["tables"]:
    tables()
else:
    datafiles()
