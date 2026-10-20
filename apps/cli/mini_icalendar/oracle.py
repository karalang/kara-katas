# Reads each calendar in data/ with icalendar 7.3.0 (the copy in
# icalendar/, unchanged), as an importer would, and prints what
# mini_icalendar prints: the components with each property's value and
# its type, the errors icalendar collected, the file written back out,
# and whether reading that again gives the same text.
import datetime
import os
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import mk  # noqa: E402
import icalendar  # noqa: E402
from icalendar import prop  # noqa: E402

DATA = os.path.join(HERE, "data")
warnings.simplefilter("ignore")


def tz_label(tz):
    return getattr(tz, "key", None) or getattr(tz, "_tzid", None) or str(tz)


def td_str(td):
    return str(td)


def dt_str(x):
    if isinstance(x, tuple):
        return "(" + dt_str(x[0]) + ", " + dt_str(x[1]) + ")"
    if isinstance(x, datetime.datetime):
        s = x.strftime("%Y-%m-%d %H:%M:%S")
        if x.tzinfo is not None:
            s += " " + tz_label(x.tzinfo)
        return s
    if isinstance(x, datetime.date):
        return x.strftime("%Y-%m-%d")
    if isinstance(x, datetime.time):
        s = x.strftime("%H:%M:%S")
        if x.tzinfo is not None:
            s += " " + tz_label(x.tzinfo)
        return s
    if isinstance(x, datetime.timedelta):
        return td_str(x)
    raise TypeError(type(x))


def recur_val(v):
    if isinstance(v, (datetime.date, datetime.time)):
        return dt_str(v)
    if isinstance(v, prop.vMonth):
        return str(v)
    if isinstance(v, int):
        return str(int(v))
    return repr(str(v))


def show_value(v):
    t = type(v).__name__
    if isinstance(v, prop.vBroken):
        return f"vBroken (expected {v.expected_type}) {str(v)!r}"
    if isinstance(v, prop.vDDDLists):
        return t + " [" + ", ".join(dt_str(x.dt) for x in v.dts) + "]"
    if isinstance(v, (prop.vDDDTypes, prop.vPeriod, prop.vTime)):
        return t + " " + dt_str(v.dt)
    if isinstance(v, prop.vUTCOffset):
        return t + " " + td_str(v.td)
    if isinstance(v, prop.vRecur):
        parts = [k + "=[" + ", ".join(recur_val(x) for x in vals) + "]" for k, vals in v.items()]
        return t + " " + "; ".join(parts)
    if isinstance(v, prop.vCategory):
        return t + " " + repr([str(c) for c in v.cats])
    if isinstance(v, prop.vGeo):
        return t + " " + repr((v.latitude, v.longitude))
    if isinstance(v, prop.vBinary):
        return f"{t} {len(v.bytes)} bytes {v.bytes[:24]!r}"
    if isinstance(v, prop.vBoolean):
        return t + " " + repr(bool(v))
    if isinstance(v, (prop.vInt, prop.vFloat)):
        return t + " " + repr(v.ical_value)
    if isinstance(v, str):
        return t + " " + repr(str(v))
    raise TypeError(t)


def show(comp, depth):
    pad = "  " * depth
    print(pad + comp.name)
    for name, value in comp.items():
        for v in value if isinstance(value, list) else [value]:
            params = dict(v.params)
            ps = " " + repr(params) if params else ""
            print(f"{pad}  {name}{ps} {show_value(v)}")
    if comp.errors:
        print(f"{pad}  errors: {comp.errors!r}")
    for sub in comp.subcomponents:
        show(sub, depth + 1)


def run(rel):
    print("== " + rel)
    with open(os.path.join(DATA, "calendars", rel), "rb") as f:
        raw = f.read()
    try:
        cals = icalendar.Calendar.from_ical(raw, multiple=True)
    except Exception as e:
        print(f"error: {type(e).__name__}: {e}")
        return
    print(f"calendars: {len(cals)}")
    for cal in cals:
        show(cal, 0)
        text = cal.to_ical()
        print("written:")
        for line in text.decode("utf-8").split("\r\n")[:-1]:
            print("| " + line)
        try:
            again = icalendar.Calendar.from_ical(text).to_ical()
            print("read back: " + ("same" if again == text else "differs"))
        except Exception as e:
            print(f"read back: error: {type(e).__name__}: {e}")


def main():
    mk.main()
    with open(os.path.join(DATA, "calendars.txt"), encoding="utf-8") as f:
        names = [l for l in f.read().split("\n") if l]
    for rel in names:
        run(rel)


if __name__ == "__main__":
    main()
