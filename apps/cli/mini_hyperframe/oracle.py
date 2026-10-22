#!/usr/bin/env python3
"""Runs data/jobs.tsv through hyperframe and prints expected.out.

Each job prints "== " and its fields joined by " | ", then two spaces and the
result. A build job prints three lines of result (hex=, repr=, rt=) or one
err= line; a parse job prints the parsed frame's repr or one err= line.
"""
import sys

sys.path.insert(0, "vendor")
from hyperframe.frame import (  # noqa: E402
    AltSvcFrame, ContinuationFrame, DataFrame, Frame, GoAwayFrame,
    HeadersFrame, PingFrame, PriorityFrame, PushPromiseFrame, RstStreamFrame,
    SettingsFrame, WindowUpdateFrame,
)


def unhex(s):
    return b"" if s == "-" else bytes.fromhex(s)


def flaglist(s):
    return () if s == "-" else tuple(s.split(","))


def build(f):
    typ = f[1]
    sid = int(f[2])
    flags = flaglist(f[3])
    if typ == "data":
        fr = DataFrame(sid, data=unhex(f[4]), flags=flags)
        fr.pad_length = int(f[5])
    elif typ == "headers":
        fr = HeadersFrame(sid, data=unhex(f[7]), flags=flags,
                          depends_on=int(f[4]), stream_weight=int(f[5]),
                          exclusive=f[6] == "1")
        fr.pad_length = int(f[8])
    elif typ == "priority":
        fr = PriorityFrame(sid, flags=flags, depends_on=int(f[4]),
                           stream_weight=int(f[5]), exclusive=f[6] == "1")
    elif typ == "rststream":
        fr = RstStreamFrame(sid, error_code=int(f[4]), flags=flags)
    elif typ == "settings":
        settings = {}
        if f[4] != "-":
            for pair in f[4].split(";"):
                k, v = pair.split(":")
                settings[int(k)] = int(v)
        fr = SettingsFrame(sid, settings=settings, flags=flags)
    elif typ == "pushpromise":
        fr = PushPromiseFrame(sid, promised_stream_id=int(f[4]),
                              data=unhex(f[5]), flags=flags)
        fr.pad_length = int(f[6])
    elif typ == "ping":
        fr = PingFrame(sid, opaque_data=unhex(f[4]), flags=flags)
    elif typ == "goaway":
        fr = GoAwayFrame(sid, last_stream_id=int(f[4]), error_code=int(f[5]),
                         additional_data=unhex(f[6]), flags=flags)
    elif typ == "windowupdate":
        fr = WindowUpdateFrame(sid, window_increment=int(f[4]), flags=flags)
    elif typ == "continuation":
        fr = ContinuationFrame(sid, data=unhex(f[4]), flags=flags)
    elif typ == "altsvc":
        fr = AltSvcFrame(sid, origin=unhex(f[4]), field=unhex(f[5]),
                         flags=flags)
    else:
        raise SystemExit("unknown build type: " + typ)

    ser = fr.serialize()
    out = ["hex=" + ser.hex(), "repr=" + repr(fr)]
    frame2, length = Frame.parse_frame_header(memoryview(ser[:9]))
    frame2.parse_body(memoryview(ser[9:9 + length]))
    out.append("rt=" + repr(frame2))
    return out


def parse(f):
    data = unhex(f[1])
    strict = f[2] == "1"
    frame, length = Frame.parse_frame_header(memoryview(data[:9]), strict=strict)
    frame.parse_body(memoryview(data[9:9 + length]))
    return [repr(frame)]


def run(f):
    k = f[0]
    try:
        if k == "build":
            return build(f)
        if k == "parse":
            return parse(f)
    except Exception as e:  # noqa: BLE001
        return ["err=" + str(e)]
    raise SystemExit("unknown job: " + k)


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().splitlines():
        f = line.split("\t")
        out.append("== " + " | ".join(f))
        for r in run(f):
            out.append("  " + r)
sys.stdout.write("\n".join(out) + "\n")
