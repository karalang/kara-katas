# Writes data/: the jobs mini_mido runs (data/jobs.jsonl) and the MIDI,
# SysEx and text files its programs read. The .mid and .syx files are
# put together byte by byte here, not written by mido, so that running
# status, odd headers and broken files can be made on purpose.
# Run with `python3 mk.py`.
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

JOBS = []


def job(name, *steps):
    JOBS.append({"name": name, "steps": [list(s) for s in steps]})


def T(*xs):
    """A tuple in a job (JSON has only lists)."""
    return {"tuple": list(xs)}


# ------------------------------------------------------------ MIDI bytes

def vlq(n):
    out = [n & 0x7F]
    n >>= 7
    while n:
        out.append(0x80 | (n & 0x7F))
        n >>= 7
    return bytes(reversed(out))


def chunk(name, data):
    return name + len(data).to_bytes(4, "big") + data


def header(fmt, ntracks, division, extra=b""):
    return chunk(b"MThd", fmt.to_bytes(2, "big") + ntracks.to_bytes(2, "big")
                 + division.to_bytes(2, "big") + extra)


def track(events):
    """events: (delta, bytes) pairs, written as they are."""
    return chunk(b"MTrk", b"".join(vlq(d) + b for d, b in events))


def meta(kind, data):
    return bytes([0xFF, kind]) + vlq(len(data)) + data


EOT = meta(0x2F, b"")


def tempo(us):
    return meta(0x51, us.to_bytes(3, "big"))


def text(kind, s, enc="latin1"):
    return meta(kind, s.encode(enc))


NAMES = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def pitch(n):
    """'G4' or 'F#5' -> MIDI note number (C4 = 60)."""
    p = NAMES[n[0]]
    rest = n[1:]
    if rest[0] == "#":
        p += 1
        rest = rest[1:]
    return p + 12 * (int(rest) + 1)


def melody(channel, tune, tpb, vel=80, running=True, off_vel0=True):
    """A track body for (note, beats) pairs; 'R' is a rest. With running
    status the status byte is written once; notes end with a note_on of
    velocity 0, or with a note_off when off_vel0 is False."""
    events = []
    rest = 0
    last = None
    for name, beats in tune:
        ticks = int(beats * tpb)
        if name == "R":
            rest += ticks
            continue
        n = pitch(name)
        on = 0x90 | channel
        events.append((rest, (bytes([on]) if not running or last != on else b"") + bytes([n, vel])))
        last = on
        if off_vel0:
            events.append((ticks, (bytes([on]) if not running or last != on else b"") + bytes([n, 0])))
        else:
            off = 0x80 | channel
            events.append((ticks, (bytes([off]) if not running or last != off else b"") + bytes([n, 64])))
            last = off
        rest = 0
    return events


MINUET_TUNE = [
    ("D5", 1), ("G4", 0.5), ("A4", 0.5), ("B4", 0.5), ("C5", 0.5),
    ("D5", 1), ("G4", 1), ("G4", 1),
    ("E5", 1), ("C5", 0.5), ("D5", 0.5), ("E5", 0.5), ("F#5", 0.5),
    ("G5", 1), ("G4", 1), ("G4", 1),
    ("C5", 1), ("D5", 0.5), ("C5", 0.5), ("B4", 0.5), ("A4", 0.5),
    ("B4", 1), ("C5", 0.5), ("B4", 0.5), ("A4", 0.5), ("G4", 0.5),
    ("F#4", 1), ("G4", 0.5), ("A4", 0.5), ("B4", 0.5), ("G4", 0.5),
    ("A4", 3),
]

MINUET_BASS = [
    ("G3", 2), ("A3", 1), ("B3", 3), ("C4", 3), ("B3", 3),
    ("A3", 3), ("G3", 3), ("D4", 1), ("B3", 1), ("G3", 1), ("D4", 1), ("D3", 1), ("C4", 1),
]


def minuet():
    tpb = 480
    conductor = [
        (0, text(0x03, "Minuet in G")),
        (0, text(0x02, "public domain")),
        (0, meta(0x58, bytes([3, 2, 24, 8]))),
        (0, meta(0x59, bytes([1, 0]))),
        (0, tempo(500000)),
        (tpb * 12, text(0x06, "slower")),
        (0, tempo(600000)),
        (tpb * 12, EOT),
    ]
    right = [(0, text(0x03, "Harpsichord RH")), (0, bytes([0xC0, 6]))] + melody(0, MINUET_TUNE, tpb) + [(0, EOT)]
    left = ([(0, text(0x03, "Harpsichord LH")), (0, bytes([0xC1, 6])), (0, bytes([0xB1, 7, 90]))]
            + melody(1, MINUET_BASS, tpb, vel=64, off_vel0=False) + [(0, EOT)])
    return header(1, 3, tpb) + track(conductor) + track(right) + track(left)


def drums():
    tpb = 96
    ev = [
        (0, bytes([0xF0, 5, 0x7E, 0x7F, 0x09, 0x01, 0xF7])),
        (0, text(0x03, "Drums")),
        (0, tempo(461538)),
        (0, bytes([0xB9, 0x07, 100])),
    ]
    pattern = [36, 42, 38, 42, 36, 36, 38, 42]
    first = True
    for bar in range(2):
        for i, n in enumerate(pattern):
            ev.append((0 if first else tpb // 2 - 4, (bytes([0x99]) if first else b"") + bytes([n, 100 if i % 2 == 0 else 70])))
            first = False
            ev.append((4, bytes([n, 0])))
    ev.append((0, bytes([0xE9, 0x00, 0x48])))
    ev.append((tpb, EOT))
    return header(0, 1, tpb) + track(ev)


def smpte():
    # 25 frames a second, 40 ticks a frame: the division's top bit is set.
    ev = [(0, text(0x03, "Timecode")), (0, meta(0x54, bytes([0x21, 0, 0, 2, 0, 0]))),
          (0, bytes([0x90, 60, 90])), (1000, bytes([60, 0])), (0, bytes([0x90, 64, 90])), (1000, bytes([64, 0])), (0, EOT)]
    return header(0, 1, 0xE728) + track(ev)


def lyrics():
    tpb = 240
    words = ["Frè-", "re", "Jac-", "ques"]
    notes = [60, 62, 64, 60]
    ev = [(0, text(0x03, "Frère Jacques", "utf-8"))]
    for w, n in zip(words, notes):
        ev.append((0, text(0x05, w, "utf-8")))
        ev.append((0, bytes([0x90, n, 80])))
        ev.append((tpb, bytes([0x80, n, 64])))
    ev.append((0, EOT))
    return header(1, 1, tpb) + track(ev)


def odd():
    # A six-byte header plus two padding bytes, and every meta kind.
    ev = [
        (0, meta(0x00, b"")),
        (0, meta(0x00, bytes([0x01, 0x02]))),
        (0, meta(0x20, bytes([9]))),
        (0, meta(0x21, b"")),
        (0, meta(0x21, bytes([2]))),
        (0, meta(0x01, b"caf\xe9")),
        (0, meta(0x04, b"Organ")),
        (0, meta(0x07, b"cue 1")),
        (0, meta(0x09, b"Port A")),
        (0, meta(0x59, bytes([0xFB, 1]))),
        (0, meta(0x54, bytes([0x61, 1, 2, 3, 4, 5]))),
        (0, meta(0x7F, bytes([0x00, 0x00, 0x41, 0x10]))),
        (12, meta(0x60, bytes([1, 2, 3]))),
        (5, bytes([0xF1, 0x23])),
        (0, bytes([0xF2, 0x10, 0x02])),
        (0, bytes([0xF3, 3])),
        (0, bytes([0xF6])),
        (0, bytes([0xF8])),
        (7, bytes([0xA0, 60, 30])),
        (0, bytes([0xD0, 40])),
        (0, bytes([0xE0, 0x00, 0x00])),
        (0, bytes([0x7F, 0x7F])),
        (0, EOT),
    ]
    return header(1, 1, 120, extra=b"\x00\x00") + track(ev)


def broken():
    files = {}
    files["not_midi.mid"] = b"RIFF\x24\x00\x00\x00RMIDdata"
    files["short_header.mid"] = b"MThd\x00\x00\x00\x06\x00\x01"
    files["no_track.mid"] = header(1, 2, 96) + track([(0, EOT)])
    files["wrong_chunk.mid"] = header(1, 1, 96) + chunk(b"XFIH", b"\x00\x01") + track([(0, EOT)])
    files["truncated.mid"] = (header(0, 1, 96) + b"MTrk\x00\x00\x00\x20" + vlq(0) + bytes([0x90, 60, 80]) + vlq(96))
    # The second event runs past the chunk's end, into the next track.
    files["overrun.mid"] = (header(1, 2, 96)
                            + chunk(b"MTrk", vlq(0) + bytes([0x90, 60, 80]) + vlq(10) + bytes([0x80, 60]))
                            + track([(0, bytes([0xC0, 5])), (0, EOT)]))
    files["running_first.mid"] = header(0, 1, 96) + track([(0, bytes([60, 80])), (0, EOT)])
    files["undefined_status.mid"] = header(0, 1, 96) + track([(0, bytes([0x90, 60, 80])), (0, bytes([0xF4])), (0, EOT)])
    files["hot_velocity.mid"] = header(0, 1, 96) + track([(0, bytes([0x90, 60, 200])), (96, bytes([0x80, 60, 0])), (0, EOT)])
    files["hot_sysex.mid"] = header(0, 1, 96) + track([(0, bytes([0xF0, 4, 0x43, 0x90, 0x01, 0xF7])), (0, EOT)])
    files["bad_key.mid"] = header(0, 1, 96) + track([(0, meta(0x59, bytes([1, 2]))), (0, EOT)])
    files["bad_key_sharps.mid"] = header(0, 1, 96) + track([(0, meta(0x59, bytes([9, 0]))), (0, EOT)])
    files["bad_frame_rate.mid"] = header(0, 1, 96) + track([(0, meta(0x54, bytes([0x80, 0, 0, 0, 0]))), (0, EOT)])
    files["short_seq.mid"] = header(0, 1, 96) + track([(0, meta(0x00, bytes([7]))), (0, EOT)])
    files["huge_sysex.mid"] = header(0, 1, 96) + track([(0, bytes([0xF0]) + vlq(2000000))])
    files["async.mid"] = (header(2, 2, 96) + track([(0, bytes([0x90, 60, 80])), (96, bytes([60, 0])), (0, EOT)])
                          + track([(0, bytes([0x91, 67, 80])), (48, bytes([67, 0])), (0, EOT)]))
    files["format_three.mid"] = header(3, 1, 96) + track([(0, EOT)])
    files["tiny.mid"] = header(0, 1, 96) + track([(0, bytes([0x90, 60, 80])), (96, bytes([60, 0])), (0, EOT)])
    return files


# ------------------------------------------------------------- SysEx

def roland(addr, data, model=0x6A, device=0x10, fix=0):
    s = sum(addr) + sum(data)
    cs = (128 - s % 128) % 128
    return bytes([0xF0, 0x41, device, model, 0x12] + addr + data + [(cs + fix) % 128, 0xF7])


def patches():
    files = {}
    msgs = [
        roland([0x00, 0x00, 0x00, 0x00], [0x7F]),
        roland([0x03, 0x00, 0x00, 0x00], list(b"Warm Pad    ")),
        roland([0x03, 0x00, 0x00, 0x0C], [0x01, 0x02, 0x40]),
        roland([0x03, 0x00, 0x10, 0x00], [0x05], fix=3),
        bytes([0xF0, 0x43, 0x10, 0x4C, 0x00, 0x00, 0x7E, 0x00, 0xF7]),
        bytes([0xF0, 0x7E, 0x7F, 0x09, 0x01, 0xF7]),
        bytes([0xF0, 0x7F, 0x7F, 0x04, 0x01, 0x00, 0x60, 0xF7]),
    ]
    blob = msgs[0] + msgs[1] + bytes([0x90, 60, 100]) + msgs[2] + bytes([0xF8]) + msgs[3] + msgs[4] + msgs[5] + msgs[6]
    files["jv1080.syx"] = blob
    lines = []
    for m in [msgs[1], msgs[4], msgs[5]]:
        lines.append(" ".join(f"{b:02X}" for b in m))
    files["bank.txt.syx"] = ("\n".join(lines) + "\n").encode()
    files["tabs.syx"] = b"f0 7e 7f\t09 01\r\nf7\n"
    files["empty.syx"] = b""
    files["garbled.syx"] = b"F0 41 10 ZZ F7\n"
    files["odd_digit.syx"] = b"F0 41 1 F7\n"
    files["note.syx"] = bytes([0x90, 60, 100])
    files["unended.syx"] = bytes([0xF0, 0x41, 0x10]) + msgs[5]
    return files


# ------------------------------------------------------------- events

RIFF = """\
# a riff for the compose program: one message a line, as str(msg)
# writes it; time is the gap in seconds since the line before.
program_change channel=0 program=24 time=0
control_change channel=0 control=7 value=100 time=0
note_on channel=0 note=64 velocity=90 time=0
note_off channel=0 note=64 velocity=64 time=0.3
note_on channel=0 note=67 velocity=90 time=0
note_off channel=0 note=67 velocity=64 time=0.3   # a held note
note_on channel=0 note=69 velocity=95 time=0
note_on channel=16 note=60 velocity=90 time=0
note_off channel=0 note=69 velocity=64 time=0.6
pitchwheel channel=0 pitch=9000 time=0
pitchwheel channel=0 pitch=-2048 time=0.05
pitchwheel channel=0 pitch=0 time=0.05
note_on channel=0 note=6O velocity=90 time=0
sysex data=(65,16,66,18) time=0.1
sysex data=1,2,3 time=0
note_on channel=0 note time=0

note_on channel=0 note=72 velocity=100 time=1_0e-1
note_off channel=0 note=72 velocity=64 time=0.45
control_change channel=0 control=64 value=127 time=0
control_change channel=0 control=64 value=0 time=1
"""

CHORDS = """\
note_on channel=1 note=48 velocity=70 time=0
note_on channel=1 note=55 velocity=70 time=0
note_on channel=1 note=64 velocity=70 time=0
note_off channel=1 note=48 time=1.2
note_off channel=1 note=55 time=0
note_off channel=1 note=64 time=0
note_on channel=1 note=50 velocity=70 time=0
note_off channel=1 note=50 time=+1
aftertouch channel=1 value=40 time=0.25
"""

BROKEN_STREAM = """\
note_on channel=0 note=60 velocity=90 time=0
note_off channel=0 note=60 time=0.5
noteon channel=0 note=62 time=0
note_on channel=0 note=64 time=0
"""


# ------------------------------------------------------------- jobs

def msg(var, kind, **kw):
    return ("msg", var, kind, kw)


def show(var, *what):
    return ("show", var) + what


ALL = ("repr", "str", "bytes", "hex", "len", "dict")

# --- building messages

job("note_on with defaults", msg("m", "note_on"), show("m", *ALL, "is_meta", "is_realtime", "is_cc"))
job("note_on with values", msg("m", "note_on", channel=9, note=36, velocity=100, time=12),
    show("m", *ALL, "a:note", "a:channel"))
job("note_off", msg("m", "note_off", note=60), show("m", "repr", "hex", "dict"))
job("every channel message",
    msg("a", "polytouch", channel=2, note=61, value=30), show("a", "repr", "hex", "len"),
    msg("b", "control_change", channel=3, control=7, value=90), show("b", "repr", "hex", "is_cc", "is_cc=7", "is_cc=10"),
    msg("c", "program_change", channel=4, program=19), show("c", "repr", "hex", "len"),
    msg("d", "aftertouch", channel=5, value=64), show("d", "repr", "hex", "len"),
    msg("e", "pitchwheel", channel=6, pitch=-8192), show("e", "repr", "hex", "len"),
    msg("f", "pitchwheel", pitch=8191), show("f", "hex"),
    msg("g", "pitchwheel", pitch=0), show("g", "hex"))
job("system common messages",
    msg("a", "sysex", data=[1, 2, 3]), show("a", *ALL),
    msg("b", "quarter_frame", frame_type=3, frame_value=9), show("b", "repr", "hex", "len"),
    msg("c", "songpos", pos=16383), show("c", "repr", "hex", "len"),
    msg("d", "song_select", song=5), show("d", "repr", "hex"),
    msg("e", "tune_request"), show("e", "repr", "hex", "is_realtime"))
job("realtime messages",
    msg("a", "clock"), show("a", "repr", "hex", "is_realtime"),
    msg("b", "start"), show("b", "hex", "is_realtime"),
    msg("c", "continue"), show("c", "hex", "is_realtime"),
    msg("d", "stop"), show("d", "hex", "is_realtime"),
    msg("e", "active_sensing"), show("e", "hex", "is_realtime"),
    msg("f", "reset"), show("f", "hex", "is_realtime", "len"))
job("sysex data forms",
    msg("a", "sysex"), show("a", "repr", "str", "len", "hex"),
    msg("b", "sysex", data=[0x7D]), show("b", "repr", "str", "dict"),
    msg("c", "sysex", data=T(65, 16, 66)), show("c", "repr", "str", "bin"),
    msg("d", "sysex", data="AB"),
    msg("e", "sysex", data=5),
    msg("f", "sysex", data=[1, 200]),
    msg("g", "sysex", data=[True, False]), show("g", "repr", "hex", "bytes"))
job("hex with a separator", msg("m", "note_on", channel=1, note=0x3C, velocity=0x7F),
    show("m", "hex", "hex/:", "hex/", "hex/ - "))
job("bin keeps the bytes", msg("m", "note_on", note=60, velocity=64), show("m", "bin"),
    msg("q", "sysex", data=[9, 10, 13, 39, 92, 34]), show("q", "bin"),
    msg("r", "sysex", data=[39]), show("r", "bin"),
    msg("s", "sysex", data=[39, 34]), show("s", "bin"))
job("unknown type", msg("m", "note_up"), msg("n", "Note_on"))
job("checks on values",
    msg("a", "note_on", channel=16), msg("b", "note_on", channel=-1), msg("c", "note_on", channel=1.0),
    msg("d", "note_on", note=128), msg("e", "note_on", velocity="loud"), msg("f", "note_on", note=None),
    msg("g", "pitchwheel", pitch=8192), msg("h", "pitchwheel", pitch=1.5),
    msg("i", "songpos", pos=16384), msg("j", "songpos", pos="1"),
    msg("k", "quarter_frame", frame_type=8), msg("l", "quarter_frame", frame_value=16),
    msg("m", "quarter_frame", frame_type="x"), msg("n", "program_change", program=-3))
job("bools pass as ints",
    msg("a", "note_on", channel=True, note=False, velocity=True), show("a", "repr", "str", "hex", "dict"),
    msg("b", "pitchwheel", pitch=True), show("b", "repr", "hex"))
job("time checks",
    msg("a", "clock", time=0.25), show("a", "repr", "str"),
    msg("b", "clock", time=-3), show("b", "repr"),
    msg("c", "clock", time=True), show("c", "repr"),
    msg("d", "clock", time="now"), msg("e", "clock", time=None),
    msg("f", "clock", time=1e-05), show("f", "repr", "str"),
    msg("g", "clock", time=123456789.5), show("g", "repr"),
    msg("h", "clock", time=1e16), show("h", "repr"))
job("unknown attribute", msg("a", "note_on", pitch=3), msg("b", "clock", channel=0),
    msg("c", "note_on", channel=99, pitch=3), msg("d", "note_on", pitch=3, channel=99),
    msg("e", "note_on", time="x", pitch=3))
job("skip_checks lets anything in",
    msg("a", "note_on", channel=99, note=-5, skip_checks=True), show("a", "repr", "str", "dict"),
    msg("b", "note_on", pitch=3, skip_checks=True), show("b", "repr", "dict"),
    msg("c", "note_on", channel=20, note=1, velocity=2, skip_checks=True), show("c", "hex"))

# --- setting and copying

job("set attributes",
    msg("m", "note_on"),
    ("set", "m", "note", 72), ("set", "m", "velocity", 0), ("set", "m", "channel", 15), ("set", "m", "time", 0.5),
    show("m", "repr", "str"),
    ("set", "m", "type", "note_off"), ("set", "m", "pitch", 3), ("set", "m", "note", 300),
    ("set", "m", "channel", "1"), ("set", "m", "time", "late"),
    show("m", "repr"))
job("set sysex data",
    msg("m", "sysex", data=[1]),
    ("set", "m", "data", [4, 5, 6]), show("m", "repr", "len"),
    ("set", "m", "data", "xy"), ("set", "m", "data", 3), ("set", "m", "data", [300]),
    ("set", "m", "data", T()), show("m", "repr", "hex"))
job("copy",
    msg("m", "note_on", channel=2, note=60, velocity=90, time=5),
    ("copy", "m", "a", {}), show("a", "repr", "dict"),
    ("copy", "m", "b", {"note": 64, "time": 0}), show("b", "repr", "dict"),
    ("copy", "m", "c", {"type": "note_on", "velocity": 1}), show("c", "repr"),
    ("copy", "m", "d", {"type": "note_off"}),
    ("copy", "m", "e", {"note": 200}),
    ("copy", "m", "f", {"note": 200, "skip_checks": True}), show("f", "repr"),
    ("copy", "m", "g", {"pitch": 1}),
    ("copy", "m", "h", {"data": [1, 2]}),
    ("eq", "m", "a"), ("eq", "m", "b"))
job("copy order follows the type",
    ("from_bytes", "m", [0x92, 60, 90], 0), show("m", "dict"),
    ("copy", "m", "a", {}), show("a", "dict"),
    ("copy", "m", "b", {"time": 3}), show("b", "dict"))
job("copy sysex data",
    msg("s", "sysex", data=[1, 2]),
    ("copy", "s", "a", {"data": [3, 4, 5]}), show("a", "repr", "dict"),
    ("copy", "s", "b", {"data": 3}), show("b", "repr"),
    ("copy", "s", "c", {"data": "ab"}),
    ("copy", "s", "d", {"data": [256]}),
    ("copy", "s", "e", {"data": [1.0]}),
    ("copy", "s", "f", {"data": -1}),
    ("copy", "s", "g", {"data": [200]}),
    ("copy", "s", "h", {"data": [True]}), show("h", "repr"))
job("equality",
    msg("a", "note_on", note=60), msg("b", "note_on", note=60), msg("c", "note_on", note=60, time=1),
    msg("d", "note_on", note=60, time=0.0), msg("e", "note_on", note=60, velocity=True),
    msg("f", "note_off", note=60),
    ("eq", "a", "b"), ("eq", "a", "c"), ("eq", "a", "d"), ("eq", "a", "e"), ("eq", "a", "f"),
    ("eq_val", "a", 60), ("eq_val", "a", "note_on"))
job("equality of data",
    msg("a", "sysex", data=[1, 2]), msg("b", "sysex", data=T(1, 2)), ("from_bytes", "c", [0xF0, 1, 2, 0xF7], 0),
    ("eq", "a", "b"), ("eq", "a", "c"),
    ("meta", "x", "sequencer_specific", {"data": [1, 2]}), ("meta_bytes", "y", [0xFF, 0x7F, 2, 1, 2]),
    show("x", "repr"), show("y", "repr"), ("eq", "x", "y"))

# --- decoding

job("from_bytes",
    ("from_bytes", "a", [0x90, 60, 64], 0), show("a", "repr", "dict"),
    ("from_bytes", "b", [0x8F, 1, 2], 7), show("b", "repr", "dict"),
    ("from_bytes", "c", [0xE3, 0x00, 0x40], 0), show("c", "repr", "dict"),
    ("from_bytes", "d", [0xE3, 0x7F, 0x7F], 0), show("d", "repr"),
    ("from_bytes", "e", [0xE3, 0x01, 0x00], 0), show("e", "repr"),
    ("from_bytes", "f", [0xF1, 0x5A], 0), show("f", "repr", "dict"),
    ("from_bytes", "g", [0xF2, 0x7F, 0x01], 0), show("g", "repr"),
    ("from_bytes", "h", [0xF0, 0xF7], 0), show("h", "repr", "len"),
    ("from_bytes", "i", [0xF0, 1, 2, 3, 0xF7], 0.5), show("i", "repr", "dict"),
    ("from_bytes", "j", [0xC5, 3], 0), show("j", "repr", "dict"),
    ("from_bytes", "k", [0xFF], 0), show("k", "repr", "dict"))
job("from_bytes errors",
    ("from_bytes", "a", [], 0), ("from_bytes", "b", [0x90, 60], 0), ("from_bytes", "c", [0x90, 60, 64, 1], 0),
    ("from_bytes", "d", [0xF4], 0), ("from_bytes", "e", [0x60, 1, 2], 0), ("from_bytes", "f", [0x90, 128, 1], 0),
    ("from_bytes", "g", [0xF0], 0), ("from_bytes", "h", [0xF0, 1, 2], 0), ("from_bytes", "i", [0xF0, 200, 0xF7], 0),
    ("from_bytes", "j", [0xF6, 1], 0), ("from_bytes", "k", [0xF9], 0))
job("from_hex",
    ("from_hex", "a", "90 3C 40", None), show("a", "repr"),
    ("from_hex", "b", "903c40", None), show("b", "repr"),
    ("from_hex", "c", "90\t3c\n40", None), show("c", "repr"),
    ("from_hex", "d", "90:3C:40", ":"), show("d", "repr"),
    ("from_hex", "e", "F0-01-02-F7", "-"), show("e", "repr"),
    ("from_hex", "f", "90 3C", None), ("from_hex", "g", "9", None), ("from_hex", "h", "90 3G 40", None),
    ("from_hex", "i", "  ", None), ("from_hex", "j", "9 03C", None), ("from_hex", "k", "90, 3C, 40", ", "),
    ("from_hex", "l", "90::3C::40", ":"), ("from_hex", "m", "F8", None), show("m", "repr"))
job("from_str",
    ("from_str", "a", "note_on channel=1 note=60 velocity=64 time=0"), show("a", "repr"),
    ("from_str", "b", "note_on"), show("b", "repr"),
    ("from_str", "c", "  control_change   control=7 value=100\n time=0.5 "), show("c", "repr", "dict"),
    ("from_str", "d", "sysex data=(1,2,3) time=0"), show("d", "repr"),
    ("from_str", "e", "sysex data=() time=0"),
    ("from_str", "f", "sysex data=1,2,3"), ("from_str", "g", "sysex data=(1,2,3"),
    ("from_str", "h", "sysex data=x1,2y"), show("h", "repr"),
    ("from_str", "i", "note_on note=+5 velocity=1_0 time=-2"), show("i", "repr"),
    ("from_str", "j", "note_on note=0x10"), ("from_str", "k", "note_on note"), ("from_str", "l", "note_on note=1=2"),
    ("from_str", "m", "clock time=1e3"), show("m", "repr"),
    ("from_str", "n", "clock time=inf"), show("n", "repr", "str"),
    ("from_str", "o", "clock time=.5"), show("o", "repr"),
    ("from_str", "p", "clock time=soon"), ("from_str", "q", "clocks"), ("from_str", "r", "note_on channel=17"),
    ("from_str", "s", "pitchwheel pitch=-8192"), show("s", "repr", "hex"),
    ("from_str", "t", ""), ("from_str", "u", "note_on time=1 time=2"), show("u", "repr"))
job("str round trip",
    msg("a", "sysex", data=[1, 2]), show("a", "str"),
    ("from_str", "b", "sysex data=(1,2) time=0"), ("eq", "a", "b"),
    msg("c", "sysex"), show("c", "str"),
    ("from_str", "d", "sysex data=() time=0"),
    ("format", "a", True), ("format", "a", False))

# --- meta messages

def meta_job(name, kind, kw, *more):
    return job(name, ("meta", "m", kind, kw), show("m", "repr", "str", "bytes", "hex", "dict", "is_meta", "is_realtime"), *more)


meta_job("meta sequence_number", "sequence_number", {"number": 513})
meta_job("meta text", "text", {"text": "hello"})
meta_job("meta copyright default", "copyright", {})
meta_job("meta track_name", "track_name", {"name": "Lead"})
meta_job("meta instrument_name", "instrument_name", {"name": "Fretless Bass"})
meta_job("meta lyrics latin1", "lyrics", {"text": "café"})
meta_job("meta marker", "marker", {"text": "chorus", "time": 960})
meta_job("meta cue_marker", "cue_marker", {"text": "fade"})
meta_job("meta device_name", "device_name", {"name": "Synth 1"})
meta_job("meta channel_prefix", "channel_prefix", {"channel": 9})
meta_job("meta midi_port", "midi_port", {"port": 3})
meta_job("meta end_of_track", "end_of_track", {})
meta_job("meta set_tempo", "set_tempo", {"tempo": 461538})
meta_job("meta smpte_offset", "smpte_offset", {"frame_rate": 29.97, "hours": 1, "minutes": 2, "seconds": 3, "frames": 4, "sub_frames": 5})
meta_job("meta time_signature", "time_signature", {"numerator": 6, "denominator": 8})
meta_job("meta key_signature", "key_signature", {"key": "F#m"})
meta_job("meta sequencer_specific", "sequencer_specific", {"data": [0, 0, 0x41]})
meta_job("meta sequencer_specific tuple", "sequencer_specific", {"data": T(1, 2)})
meta_job("meta long text", "text", {"text": "x" * 130})
job("meta errors",
    ("meta", "a", "tempo", {}), ("meta", "b", "set_tempo", {"bpm": 120}), ("meta", "c", "set_tempo", {"tempo": 0x1000000}),
    ("meta", "d", "set_tempo", {"tempo": 1.5}), ("meta", "e", "text", {"text": 5}),
    ("meta", "f", "key_signature", {"key": "H"}), ("meta", "g", "key_signature", {"key": ["C"]}),
    ("meta", "h", "smpte_offset", {"frame_rate": 23}), ("meta", "i", "smpte_offset", {"minutes": 60}),
    ("meta", "j", "smpte_offset", {"sub_frames": 100}), ("meta", "k", "time_signature", {"denominator": 6}),
    ("meta", "l", "time_signature", {"denominator": 0}), ("meta", "m", "time_signature", {"denominator": 536870912}),
    ("meta", "n", "time_signature", {"numerator": 256}), ("meta", "o", "channel_prefix", {"channel": 256}),
    ("meta", "p", "sequence_number", {"number": 65536}), ("meta", "q", "marker", {"time": "x"}),
    ("meta", "r", "midi_port", {"port": -1}), ("meta", "s", "end_of_track", {"text": "x"}))
job("meta odd but allowed",
    ("meta", "a", "time_signature", {"denominator": 1024}), show("a", "repr", "hex"),
    ("meta", "b", "time_signature", {"denominator": True}), show("b", "repr", "hex"),
    ("meta", "c", "smpte_offset", {"frame_rate": 24.0}), show("c", "repr", "hex"),
    ("meta", "d", "smpte_offset", {"frame_rate": True}),
    ("meta", "e", "set_tempo", {"tempo": True}), show("e", "repr", "hex"),
    ("meta", "f", "sequencer_specific", {"data": "ab"}), show("f", "repr"),
    ("meta", "g", "text", {"text": "€"}), show("g", "repr"), show("g", "hex"),
    ("meta", "h", "key_signature", {"key": "Cb", "skip_checks": True, "tempo": 3}), show("h", "repr"))
job("meta set and copy",
    ("meta", "m", "set_tempo", {"tempo": 500000}),
    ("set", "m", "tempo", 400000), ("set", "m", "time", 10), show("m", "repr"),
    ("set", "m", "tempo", -1), ("set", "m", "type", "text"), ("set", "m", "text", "x"), ("set", "m", "time", None),
    ("copy", "m", "a", {}), show("a", "repr"),
    ("copy", "m", "b", {"tempo": 300000}), show("b", "repr", "dict"),
    ("copy", "m", "c", {"type": "text"}), ("copy", "m", "d", {"type": "set_tempo", "time": 2}), show("d", "repr"),
    ("copy", "m", "e", {"text": "x"}),
    ("eq", "m", "a"), ("eq", "m", "b"))
job("meta from_bytes",
    ("meta_bytes", "a", [0xFF, 0x51, 3, 0x07, 0xA1, 0x20]), show("a", "repr"),
    ("meta_bytes", "b", [0xFF, 0x03, 4, 0x4C, 0x65, 0x61, 0x64]), show("b", "repr"),
    ("meta_bytes", "c", [0xFF, 0x2F, 0]), show("c", "repr"),
    ("meta_bytes", "d", [0xFF, 0x59, 2, 0xFE, 0x01]), show("d", "repr"),
    ("meta_bytes", "e", [0xFF, 0x60, 2, 9, 9]), show("e", "repr", "hex", "dict"),
    ("meta_bytes", "f", [0xFF, 0x58, 4, 4, 3, 24, 8]), show("f", "repr"),
    ("meta_bytes", "g", [0x90, 0x51, 3, 1, 2, 3]), ("meta_bytes", "h", [0xFF, 0x51, 3, 1, 2]),
    ("meta_bytes", "i", [0xFF, 0x51, 5, 1, 2, 3]), ("meta_bytes", "j", [0xFF, 0x01, 0x81, 0x00] + [65] * 128), show("j", "len_text"),
    ("meta_bytes", "k", [0xFF, 0x54, 5, 0x60, 0, 0, 0, 0]), show("k", "repr"),
    ("meta_bytes", "l", [0xFF, 0x54, 5, 0x80, 0, 0, 0, 0]),
    ("meta_bytes", "m", [0xFF, 0x59, 2, 1, 5]), ("meta_bytes", "n", [0xFF, 0x59, 2, 0xF7, 0]),
    ("meta_bytes", "o", [0xFF, 0x59, 2, 0x08, 0]),
    ("meta_bytes", "p", [0xFF, 0x00, 0]), show("p", "repr"),
    ("meta_bytes", "q", [0xFF, 0x00, 1, 5]))
job("unknown meta",
    ("unknown", "u", 0x60, [1, 2, 3], 5), show("u", "repr", "str", "hex", "bytes", "dict", "is_meta"),
    ("unknown", "v", 0x0A, None, 0), show("v", "repr", "hex"),
    ("set", "u", "anything", 7), show("u", "repr", "dict"),
    ("copy", "u", "w", {"time": 9}), show("w", "repr"),
    ("unknown", "x", 0x60, [1, 2, 3], 5), ("eq", "w", "x"), ("eq", "u", "x"))

# --- frozen messages

job("freeze and thaw",
    msg("m", "note_on", note=60),
    ("freeze", "m", "f"), show("f", "repr", "str", "frozen", "hex", "dict"),
    ("set", "f", "note", 61), ("eq", "m", "f"),
    ("freeze", "f", "g"), show("g", "repr"),
    ("thaw", "f", "t"), show("t", "repr", "frozen"), ("set", "t", "note", 62), show("t", "repr"),
    ("thaw", "m", "u"), show("u", "repr", "frozen"),
    ("copy", "f", "c", {}), show("c", "repr", "frozen"),
    ("copy", "f", "d", {"note": 70}), show("d", "repr", "frozen"))
job("freeze meta and unknown",
    ("meta", "m", "key_signature", {"key": "D"}), ("freeze", "m", "f"), show("f", "repr", "frozen"),
    ("set", "f", "key", "A"), ("thaw", "f", "t"), ("set", "t", "key", "A"), show("t", "repr"),
    ("unknown", "u", 0x60, [1], 0), ("freeze", "u", "g"), show("g", "repr", "frozen"),
    ("set", "g", "data", [2]), ("thaw", "g", "h"), show("h", "repr", "frozen"))

# --- byte streams

job("parse",
    ("parse", [0x90, 60, 64]), ("parse", [0x90, 60]), ("parse", []),
    ("parse", [0x80, 1, 2, 0x90, 3, 4]), ("parse", [0x30, 0x90, 1, 2]),
    ("parse_all", [0x90, 60, 64, 0x80, 60, 0, 0xF8, 0xC1, 5]),
    ("parse_all", [0x90, 60, 0xF8, 64]),
    ("parse_all", [0xF0, 1, 2, 0xF8, 3, 0xF7]),
    ("parse_all", [0xF0, 1, 2, 0x90, 60, 64, 0xF7]),
    ("parse_all", [0xF7, 0xF4, 1, 2, 0xF9, 0xFD, 0xFE]),
    ("parse_all", [0x90, 60, 0x91, 61, 62]),
    ("parse_all", [0xF6, 0xF1, 9, 0xF2, 1, 2, 0xF3, 4]),
    ("parse_all", [0x90, 60, 64, 61, 64]),
    ("parse_all", [256]), ("parse_all", [-1]), ("parse_all", [1.5]))
job("parser fed a little at a time",
    ("parser", "p"),
    ("feed", "p", [0x90]), ("pending", "p"), ("feed", "p", [60]), ("pending", "p"),
    ("feed", "p", [100, 0x80, 60]), ("pending", "p"), ("feed_byte", "p", 0), ("pending", "p"),
    ("get", "p"), ("get", "p"), ("get", "p"),
    ("feed", "p", [0xF8, 0xFA]), ("drain", "p"), ("pending", "p"),
    ("feed_byte", "p", 300), ("feed_byte", "p", "x"))
job("tokenizer", ("tokenize", [0x90, 60, 64, 0xF0, 1, 2, 0xF7, 0xFE, 0xF4, 5, 0xC0, 1]),
    ("tokenize", [0xF0, 1, 0xFF, 2, 0xF7]), ("tokenize", [0x7F, 0xF7]))
job("string streams",
    ("stream", ["note_on channel=0 note=60 velocity=64 time=0", "", "  # just a comment",
                "note_off note=60 # trailing comment", "note_on channel=20", "pitchwheel pitch=x",
                "sysex data=(1,2)", "control_change control=7 value=128"]),
    ("stream", ["clock", "fish x=1", "start"]))

# --- units and variable ints

job("tick2second and second2tick",
    ("t2s", 480, 480, 500000), ("t2s", 1, 480, 500000), ("t2s", 0, 96, 500000), ("t2s", 1000, 96, 461538),
    ("t2s", 960, 480, 600000), ("t2s", 100, -6360, 500000),
    ("s2t", 1.0, 480, 500000), ("s2t", 0.5, 480, 500000), ("s2t", 0.0010417, 480, 500000),
    ("s2t", 0.003125, 96, 500000), ("s2t", 0.009375, 96, 500000), ("s2t", 2.5, 1, 1000000), ("s2t", 3.5, 1, 1000000),
    ("s2t", 1, 0, 500000))
job("bpm2tempo and tempo2bpm",
    ("bpm2tempo", 120, None), ("bpm2tempo", 130, None), ("bpm2tempo", 140.5, None), ("bpm2tempo", 60, [6, 8]),
    ("bpm2tempo", 90, [3, 2]), ("bpm2tempo", 0, None),
    ("tempo2bpm", 500000, None), ("tempo2bpm", 461538, None), ("tempo2bpm", 600000, [6, 8]), ("tempo2bpm", 333333, None),
    ("tempo2bpm", 1, None), ("tempo2bpm", 0, None))
job("variable length ints",
    ("varint", 0), ("varint", 127), ("varint", 128), ("varint", 8192), ("varint", 16383), ("varint", 16384),
    ("varint", 0x0FFFFFFF), ("varint", 2000000), ("varint", -1), ("varint", 1.0), ("varint", True),
    ("devarint", [0x00]), ("devarint", [0x81, 0x00]), ("devarint", [0xFF, 0x7F]), ("devarint", [0x81, 0x80, 0x00]),
    ("devarint", [0x7F, 0x7F]), ("devarint", []))
job("signed and unsigned",
    ("signed", "byte", 0xFB), ("signed", "byte", 5), ("unsigned", "byte", -5), ("signed", "short", 0x8000),
    ("unsigned", "short", -1), ("signed", "long", 0xFFFFFFFF), ("signed", "byte", 256), ("unsigned", "byte", 200),
    ("signed", "nibble", 3))

# --- tracks

job("tracks",
    msg("a", "note_on", note=60), msg("b", "note_off", note=60, time=96),
    ("meta", "n", "track_name", {"name": "Piano"}),
    ("track", "e", []), ("tshow", "e", "repr", "len", "name"),
    ("track", "one", ["a"]), ("tshow", "one", "repr"),
    ("track", "onemeta", ["n"]), ("tshow", "onemeta", "repr"),
    ("track", "t", ["n", "a", "b"]), ("tshow", "t", "repr", "len", "name"))
job("track names",
    msg("a", "note_on", note=60),
    ("track", "t", ["a"]), ("tname", "t", "Strings"), ("tshow", "t", "repr", "name"),
    ("tname", "t", "Violins"), ("tshow", "t", "repr", "name"),
    ("tname", "t", 5),
    ("meta", "x", "track_name", {"name": "first"}), ("meta", "y", "track_name", {"name": "second"}),
    ("track", "u", ["a", "x", "y"]), ("tshow", "u", "name"), ("tname", "u", "renamed"), ("tshow", "u", "repr"))
job("track slices and sums",
    msg("a", "note_on", note=60), msg("b", "note_off", note=60, time=10), msg("c", "clock"),
    ("track", "t", ["a", "b", "c"]),
    ("tslice", "t", "s", 1, 3), ("tshow", "s", "repr"),
    ("tslice", "t", "s2", 5, 9), ("tshow", "s2", "repr"),
    ("tindex", "t", 0, "m"), show("m", "repr"),
    ("tindex", "t", -1, "m2"), show("m2", "repr"),
    ("tindex", "t", 3, "m3"),
    ("tadd", "t", "s", "u"), ("tshow", "u", "repr", "len"),
    ("tmul", "s", 2, "w"), ("tshow", "w", "repr"), ("tmul", "s", 0, "z"), ("tshow", "z", "repr"),
    ("tappend", "z", "c"), ("tshow", "z", "repr"))
job("fix_end_of_track",
    msg("a", "note_on", note=60), ("meta", "e1", "end_of_track", {"time": 5}), msg("b", "note_off", note=60, time=10),
    ("meta", "e2", "end_of_track", {"time": 7}),
    ("track", "t", ["a", "e1", "b", "e2"]), ("fix_eot", "t", "f"), ("tshow", "f", "repr"),
    ("track", "e", []), ("fix_eot", "e", "g"), ("tshow", "g", "repr"),
    ("track", "only", ["e1", "e2"]), ("fix_eot", "only", "h"), ("tshow", "h", "repr"))
job("merge_tracks",
    msg("a1", "note_on", note=60), msg("a2", "note_off", note=60, time=96), ("meta", "ae", "end_of_track", {"time": 0}),
    msg("b1", "note_on", channel=1, note=67, time=48), msg("b2", "note_off", channel=1, note=67, time=96),
    ("meta", "be", "end_of_track", {"time": 20}),
    msg("c1", "program_change", channel=2, program=5, time=96),
    ("track", "ta", ["a1", "a2", "ae"]), ("track", "tb", ["b1", "b2", "be"]), ("track", "tc", ["c1"]),
    ("merge", "m", ["ta", "tb", "tc"], False), ("tshow", "m", "repr", "len"),
    ("merge", "n", [], False), ("tshow", "n", "repr"),
    msg("bad", "note_on", channel=99, skip_checks=True), ("track", "tbad", ["bad"]),
    ("merge", "o", ["tbad"], False), ("merge", "p", ["tbad"], True), ("tshow", "p", "repr"))
job("merge keeps floats",
    msg("a", "note_on", time=0.5), msg("b", "note_off", time=0.25), msg("c", "note_on", note=1, time=0.6),
    ("track", "x", ["a", "b"]), ("track", "y", ["c"]),
    ("merge", "m", ["x", "y"], False), ("tshow", "m", "repr"))

# --- MIDI files in memory

job("new file",
    ("file", "f", {}, []), ("fshow", "f", "repr", "type", "tpb", "length"),
    ("add_track", "f", None), ("add_track", "f", "Bass"), ("fshow", "f", "repr"),
    ("save", "f", "out/new.mid"), ("fshow", "f", "repr"))
job("file errors",
    ("file", "a", {"type": 3}, []), ("file", "b", {"type": -1}, []),
    ("file", "c", {"type": 0}, []), ("save", "c", "out/type0.mid"),
    ("file", "d", {"ticks_per_beat": 40000}, []), ("save", "d", "out/tpb.mid"),
    ("file", "e", {"type": 2}, []), ("fshow", "e", "length", "merged", "play_list"))
job("save and load a small song",
    msg("p", "program_change", program=12), msg("a", "note_on", note=60, velocity=90),
    msg("b", "note_on", note=64, velocity=90), msg("c", "note_off", note=60, velocity=0, time=480),
    msg("d", "note_off", note=64, velocity=0), msg("e", "note_on", note=67, velocity=90, time=0),
    msg("g", "note_off", note=67, time=240),
    ("meta", "n", "track_name", {"name": "Vibes"}), ("meta", "s", "set_tempo", {"tempo": 400000, "time": 0}),
    ("meta", "k", "key_signature", {"key": "Eb"}), ("meta", "ts", "time_signature", {"numerator": 2, "denominator": 4}),
    ("track", "t0", ["n", "s", "k", "ts"]), ("track", "t1", ["p", "a", "b", "c", "d", "e", "g"]),
    ("file", "f", {"ticks_per_beat": 240}, ["t0", "t1"]),
    ("save", "f", "out/vibes.mid"), ("load", "g", "out/vibes.mid", {}),
    ("fshow", "g", "repr", "length", "play_list"),
    ("save", "g", "out/vibes2.mid"), ("same_file", "out/vibes.mid", "out/vibes2.mid"))
job("running status on save",
    msg("a", "note_on", note=60), msg("b", "note_on", note=60, velocity=0, time=10),
    msg("c", "note_on", channel=1, note=62, time=0), msg("d", "note_on", channel=1, note=62, velocity=0, time=10),
    msg("e", "song_select", song=2), msg("f", "song_select", song=3),
    msg("s", "sysex", data=[1]), msg("h", "note_on", channel=1, note=64),
    ("meta", "m", "marker", {"text": "x"}), msg("i", "note_on", channel=1, note=65),
    ("track", "t", ["a", "b", "c", "d", "e", "f", "s", "h", "m", "i"]),
    ("file", "f", {"type": 0}, ["t"]), ("save", "f", "out/running.mid"), ("load", "g", "out/running.mid", {}),
    ("fshow", "g", "print_tracks"))
job("save refuses",
    msg("a", "clock"), ("track", "t", ["a"]), ("file", "f", {}, ["t"]), ("save", "f", "out/clock.mid"),
    msg("b", "note_on", time=0.5), ("track", "u", ["b"]), ("file", "g", {}, ["u"]), ("save", "g", "out/float.mid"),
    msg("c", "note_on", time=-1), ("track", "v", ["c"]), ("file", "h", {}, ["v"]), ("save", "h", "out/neg.mid"),
    msg("d", "note_on", time=True), ("track", "w", ["d"]), ("file", "i", {}, ["w"]), ("save", "i", "out/bool.mid"),
    ("meta", "e", "text", {"text": "€"}), ("track", "x", ["e"]), ("file", "j", {}, ["x"]), ("save", "j", "out/euro.mid"),
    ("file", "k", {"charset": "utf-8"}, ["x"]), ("save", "k", "out/euro8.mid"), ("load", "l", "out/euro8.mid", {}),
    ("fshow", "l", "print_tracks"), ("load", "m", "out/euro8.mid", {"charset": "utf-8"}), ("fshow", "m", "print_tracks"))

# --- MIDI files on disk

job("load the minuet", ("load", "f", "songs/minuet.mid", {}), ("fshow", "f", "type", "tpb", "length", "print_meta"))
job("minuet track by track", ("load", "f", "songs/minuet.mid", {}), ("fshow", "f", "print_tracks"))
job("minuet played", ("load", "f", "songs/minuet.mid", {}), ("fshow", "f", "play_list"))
job("drums", ("load", "f", "songs/drums.mid", {}), ("fshow", "f", "repr", "length"))
job("smpte division", ("load", "f", "songs/smpte.mid", {}), ("fshow", "f", "repr", "tpb", "length", "play_list"),
    ("save", "f", "out/smpte.mid"), ("same_file", "songs/smpte.mid", "out/smpte.mid"))
job("lyrics in utf-8",
    ("load", "a", "songs/lyrics.mid", {}), ("fshow", "a", "print_meta"),
    ("load", "b", "songs/lyrics.mid", {"charset": "utf-8"}), ("fshow", "b", "print_meta"),
    ("load", "c", "songs/odd.mid", {"charset": "utf-8"}),
    ("load", "d", "songs/lyrics.mid", {"charset": "ascii"}))
job("every meta kind", ("load", "f", "songs/odd.mid", {}), ("fshow", "f", "repr", "length"),
    ("save", "f", "out/odd.mid"), ("load", "g", "out/odd.mid", {}), ("fshow", "g", "print_tracks"))
job("debug load", ("load", "f", "songs/tiny.mid", {"debug": True}))
job("broken files",
    *[("load", n.split(".")[0], "songs/" + n, {}) for n in
      ["not_midi.mid", "short_header.mid", "no_track.mid", "wrong_chunk.mid", "truncated.mid", "overrun.mid",
       "running_first.mid", "undefined_status.mid", "hot_velocity.mid", "hot_sysex.mid", "bad_key.mid",
       "bad_key_sharps.mid", "bad_frame_rate.mid", "short_seq.mid", "huge_sysex.mid", "missing.mid"]])
job("clip", ("load", "a", "songs/hot_velocity.mid", {"clip": True}), ("fshow", "a", "print_tracks"),
    ("load", "b", "songs/hot_sysex.mid", {"clip": True}), ("fshow", "b", "print_tracks"))
job("async and format three",
    ("load", "a", "songs/async.mid", {}), ("fshow", "a", "repr", "length", "play_list"),
    ("load", "b", "songs/format_three.mid", {}), ("fshow", "b", "repr", "type"),
    ("save", "b", "out/three.mid"), ("same_file", "songs/format_three.mid", "out/three.mid"))

# --- SysEx files

job("read syx files",
    *[("read_syx", "patches/" + n) for n in
      ["jv1080.syx", "bank.txt.syx", "tabs.syx", "empty.syx", "garbled.syx", "odd_digit.syx", "note.syx",
       "unended.syx", "missing.syx"]])
job("write syx files",
    msg("a", "sysex", data=[0x7E, 0x7F, 9, 1]), msg("b", "note_on"), msg("c", "sysex", data=[0x43, 0x10]),
    ("write_syx", "out/two.syx", ["a", "b", "c"], False), ("read_syx", "out/two.syx"), ("dump", "out/two.syx"),
    ("write_syx", "out/two.txt.syx", ["a", "b", "c"], True), ("read_syx", "out/two.txt.syx"), ("dump", "out/two.txt.syx"),
    ("write_syx", "out/none.syx", ["b"], True), ("read_syx", "out/none.syx"))

# --- ports

job("echo port",
    ("port", "p", "loop", False), ("prepr", "p"),
    msg("a", "note_on", note=60), msg("b", "note_off", note=60, time=3),
    ("send", "p", "a"), ("send", "p", "b"), ("set", "a", "note", 61),
    ("poll", "p"), ("receive", "p"), ("poll", "p"),
    ("meta", "m", "marker", {"text": "x"}), ("send", "p", "m"),
    ("freeze", "a", "f"), ("send", "p", "f"), ("poll", "p"),
    ("close", "p"), ("prepr", "p"), ("send", "p", "a"), ("poll", "p"), ("receive", "p"), ("close", "p"))
job("reset and panic",
    ("port", "p", "synth", False), ("reset", "p"), ("panic", "p"), ("iter", "p"), ("poll", "p"),
    ("port", "q", "", True), ("prepr", "q"), ("send_new", "q", "note_on", {"note": 64}), ("close", "q"), ("count", "q"),
    ("reset", "q"))

# ------------------------------------------------------------ write data/

if os.path.isdir("data"):
    shutil.rmtree("data")
os.makedirs("data/songs")
os.makedirs("data/patches")
os.makedirs("data/events")


def put(p, b):
    with open(os.path.join("data", p), "wb") as f:
        f.write(b)


put("songs/minuet.mid", minuet())
put("songs/drums.mid", drums())
put("songs/smpte.mid", smpte())
put("songs/lyrics.mid", lyrics())
put("songs/odd.mid", odd())
for n, b in broken().items():
    put("songs/" + n, b)
for n, b in patches().items():
    put("patches/" + n, b)
put("events/riff.txt", RIFF.encode())
put("events/chords.txt", CHORDS.encode())
put("events/broken.txt", BROKEN_STREAM.encode())

with open("data/jobs.jsonl", "w", encoding="utf-8") as f:
    for j in JOBS:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
print(len(JOBS), "jobs")
