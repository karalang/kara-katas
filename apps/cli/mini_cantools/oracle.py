"""Oracle for mini_cantools: the same program as mini_cantools.kara, written
against cantools 39.4.5 itself.

    CANTOOLS_PATH=<cantools src>:<textparser>:<bitstruct src> python3 -I -B oracle.py > expected.out

python-can and diskcache are only imported by parts of cantools this
program does not use; empty stand-ins take their place in sys.modules.
"""

import os
import re
import sys
import types

for p in reversed(os.environ["CANTOOLS_PATH"].split(":")):
    sys.path.insert(0, p)

can_stub = types.ModuleType("can")
for cls in ("Listener", "Message", "Notifier", "BusABC"):
    setattr(can_stub, cls, type(cls, (), {}))
can_stub.rc = {}
sys.modules["can"] = can_stub
sys.modules["diskcache"] = types.ModuleType("diskcache")

import cantools  # noqa: E402
from cantools.database.namedsignalvalue import NamedSignalValue  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def read(name):
    with open(os.path.join(DATA, name)) as f:
        return f.read()


def err(e):
    return f"{type(e).__name__}: {e}"


def hexid(m):
    return f"0x{m.frame_id:x}"


def summary(db):
    print(f"version {db.version!r}")
    for bus in db.buses:
        print(f"bus {bus.name!r}: {bus.comment!r}")
    for node in db.nodes:
        attrs = node.dbc.attributes if node.dbc is not None else {}
        addr = attrs["ECUAddress"].value if "ECUAddress" in attrs else None
        print(f"node {node.name}: comment {node.comment!r}, address {addr!r}")
    for name, table in db.dbc.value_tables.items():
        items = ", ".join(f"{k}={v}" for k, v in table.items())
        print(f"value table {name}: {items}")
    for m in db.messages:
        kind = "extended" if m.is_extended_frame else "standard"
        print(f"message {m.name} {hexid(m)} {kind}, {m.length} bytes, "
              f"senders {m.senders}, cycle {m.cycle_time}, send type {m.send_type!r}")
        if m.comment is not None:
            print(f"  comment {m.comment!r}")
        print(f"  receivers {sorted(m.receivers)}, multiplexed {m.is_multiplexed()}")
        print(f"  tree {m.signal_tree}")
        for s in m.signals:
            order = "little" if s.byte_order == "little_endian" else "big"
            sign = "signed" if s.is_signed else "unsigned"
            print(f"  {s.name}: {s.start}|{s.length} {order} {sign}, "
                  f"range [{s.minimum}, {s.maximum}], unit {s.unit!r}, "
                  f"receivers {s.receivers}, initial {s.raw_initial}")
            print(f"    {s.conversion!r}, scale {s.scale}, offset {s.offset}")
            if s.is_multiplexer:
                print("    multiplexer")
            if s.multiplexer_signal is not None:
                print(f"    under {s.multiplexer_signal} for {s.multiplexer_ids}")
            if s.comment is not None:
                print(f"    comment {s.comment!r}")


def parse_value(text):
    if text.startswith("'"):
        return text[1:-1]
    if any(c in text for c in ".eE"):
        return float(text)
    return int(text)


def run_job(db, line):
    words = line.split()
    if words[0] == "encode":
        opts = [w for w in words[2:] if w.startswith("-")]
        values = {}
        for w in words[2:]:
            if not w.startswith("-"):
                k, v = w.split("=", 1)
                values[k] = parse_value(v)
        try:
            m = db.get_message_by_name(words[1])
            data = m.encode(values,
                            scaling="-noscale" not in opts,
                            padding="-pad" in opts,
                            strict="-loose" not in opts)
            return data.hex()
        except Exception as e:  # noqa: BLE001
            return err(e)
    key = int(words[1], 16) if words[1].startswith("0x") else words[1]
    opts = words[3:]
    try:
        decoded = db.decode_message(key, bytes.fromhex(words[2]),
                                    decode_choices="-nochoices" not in opts,
                                    scaling="-noscale" not in opts,
                                    allow_truncated="-trunc" in opts)
        return repr(decoded)
    except Exception as e:  # noqa: BLE001
        return err(e)


def secs(us):
    return f"{us // 1000000}.{us % 1000000:06d}"


def rel(us, t0):
    d = us - t0
    return f"{d // 1000000}.{d % 1000000 // 1000:03d}"


LINE = re.compile(r"\(([0-9]+)\.([0-9]{6})\) ([a-z0-9]+) ([0-9A-F]{3}|[0-9A-F]{8})#((?:[0-9A-F]{2}){0,8})")


WATCHED = ("Gear", "PackState", "FaultCode", "ChargeState")


class Stat:
    def __init__(self):
        self.count = 0
        self.lo = None
        self.hi = None
        self.last = None
        self.names = {}

    def add(self, v):
        self.last = v
        if isinstance(v, NamedSignalValue):
            self.names[v.name] = self.names.get(v.name, 0) + 1
            return
        self.count += 1
        if self.lo is None or v < self.lo:
            self.lo = v
        if self.hi is None or v > self.hi:
            self.hi = v


def analyse(db, text):
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    bad_lines = []
    unknown = {}
    frames = {}  # name -> [count, first, last, max gap, gap at]
    stats = {}  # name -> {signal: Stat}
    decode_errors = []
    checksum_bad = []
    counter_gaps = []
    encode_errors = {}  # text -> [count, first time]
    mismatches = []
    transitions = []
    prev_named = {}
    t0 = None
    dist_km = 0.0
    prev_speed = None
    energy_wh = 0.0
    prev_pack = None
    peak_kw = 0.0
    regen_kw = 0.0
    cell_lo = None
    cell_hi = None
    prev_counter = None
    derate_frames = 0
    total = 0
    for lineno, line in enumerate(lines, 1):
        mo = LINE.fullmatch(line)
        if mo is None:
            bad_lines.append(lineno)
            continue
        total += 1
        ts = int(mo.group(1)) * 1000000 + int(mo.group(2))
        if t0 is None:
            t0 = ts
        ident = mo.group(4)
        data = bytes.fromhex(mo.group(5))
        try:
            m = db.get_message_by_frame_id(int(ident, 16))
        except KeyError:
            unknown[ident] = unknown.get(ident, 0) + 1
            continue
        fr = frames.setdefault(m.name, [0, ts, ts, 0, ts])
        if fr[0] > 0 and ts - fr[2] > fr[3]:
            fr[3] = ts - fr[2]
            fr[4] = ts
        fr[0] += 1
        fr[2] = ts
        try:
            decoded = m.decode(data)
        except Exception as e:  # noqa: BLE001
            decode_errors.append(f"{rel(ts, t0)} {m.name} [{data.hex()}]: {err(e)}")
            continue
        sigs = stats.setdefault(m.name, {})
        for name, v in decoded.items():
            sigs.setdefault(name, Stat()).add(v)
            if name in WATCHED:
                text_v = str(v)
                old = prev_named.get(name)
                if old is not None and old != text_v:
                    transitions.append(f"{rel(ts, t0)} {name} {old} -> {text_v}")
                prev_named[name] = text_v
        try:
            again = m.encode(decoded)
            if again != data:
                mismatches.append(f"{rel(ts, t0)} {m.name} [{data.hex()}] re-encodes as [{again.hex()}]")
        except Exception as e:  # noqa: BLE001
            key = f"{m.name}: {err(e)}"
            if key in encode_errors:
                encode_errors[key][0] += 1
            else:
                encode_errors[key] = [1, rel(ts, t0)]
        if m.name == "VCU_Status":
            want = (~sum(data[0:7])) & 0xFF
            if decoded["Checksum"] != want:
                checksum_bad.append(f"{rel(ts, t0)} checksum {decoded['Checksum']:#04x}, bytes say {want:#04x}")
            c = decoded["Counter"]
            if prev_counter is not None and c != (prev_counter + 1) % 16:
                counter_gaps.append(f"{rel(ts, t0)} counter {prev_counter} -> {c}")
            prev_counter = c
            sp = decoded["VehicleSpeed"]
            if prev_speed is not None:
                dist_km += prev_speed[1] * ((ts - prev_speed[0]) / 3600000000)
            prev_speed = (ts, sp)
        elif m.name == "BMS_Pack":
            p = decoded["PackVoltage"] * decoded["PackCurrent"]
            if prev_pack is not None:
                energy_wh += prev_pack[1] * ((ts - prev_pack[0]) / 3600000000)
            prev_pack = (ts, p)
            if p / 1000 > peak_kw:
                peak_kw = p / 1000
            if p / 1000 < regen_kw:
                regen_kw = p / 1000
        elif m.name == "BMS_Cells":
            for name, v in decoded.items():
                if name.startswith("CellVolt"):
                    cell = name[8:]
                    if cell_lo is None or v < cell_lo[0]:
                        cell_lo = (v, cell, rel(ts, t0))
                    if cell_hi is None or v > cell_hi[0]:
                        cell_hi = (v, cell, rel(ts, t0))
        elif m.name == "MCU_Motor":
            if decoded["DeratePct"] > 0:
                derate_frames += 1

    print(f"{len(lines)} lines, {total} frames from {secs(t0)}, {len(bad_lines)} unreadable lines: {bad_lines}")
    for ident in sorted(unknown):
        print(f"unknown id {ident}: {unknown[ident]} frames")
    for m in db.messages:
        if m.name not in frames:
            print(f"{m.name}: no frames")
            continue
        n, first, last, gap, gap_at = frames[m.name]
        period = (last - first) // (n - 1) if n > 1 else 0
        print(f"{m.name}: {n} frames, mean period {period // 1000}.{period % 1000:03d} ms "
              f"(cycle {m.cycle_time}), longest gap {gap // 1000}.{gap % 1000:03d} ms before {rel(gap_at, t0)}")
        for name, st in stats.get(m.name, {}).items():
            parts = []
            if st.count:
                parts.append(f"{st.count} values in [{st.lo}, {st.hi}]")
            if st.names:
                parts.append(", ".join(f"{k} x{v}" for k, v in st.names.items()))
            print(f"  {name}: {'; '.join(parts)}; last {st.last!r}")
    print(f"decode errors: {len(decode_errors)}")
    for e in decode_errors:
        print(f"  {e}")
    print(f"re-encode errors: {sum(v[0] for v in encode_errors.values())}")
    for e, (n, first) in encode_errors.items():
        print(f"  x{n} from {first} {e}")
    print(f"re-encode mismatches: {len(mismatches)}")
    for e in mismatches:
        print(f"  {e}")
    print(f"checksum failures: {len(checksum_bad)}")
    for e in checksum_bad:
        print(f"  {e}")
    print(f"counter gaps: {len(counter_gaps)}")
    for e in counter_gaps:
        print(f"  {e}")
    print(f"state changes: {len(transitions)}")
    for e in transitions:
        print(f"  {e}")
    print(f"distance {dist_km:.4f} km, pack energy {energy_wh:.3f} Wh, "
          f"peak {peak_kw:.2f} kW, regen {regen_kw:.2f} kW, derated in {derate_frames} motor frames")
    print(f"lowest cell {cell_lo[1]} {cell_lo[0]} mV at {cell_lo[2]}, "
          f"highest cell {cell_hi[1]} {cell_hi[0]} mV at {cell_hi[2]}, spread {cell_hi[0] - cell_lo[0]} mV")
    odo = stats["DASH_Odometer"]["Odometer"]
    print(f"odometer {odo.lo} -> {odo.hi} km, {odo.hi - odo.lo:.1f} km on the dash")


def main():
    print("== vehicle.dbc")
    db = cantools.database.load_string(read("vehicle.dbc"), database_format="dbc")
    summary(db)

    print("== broken files")
    for name in sorted(n for n in os.listdir(DATA) if n.startswith("bad_")):
        text = read(name)
        try:
            bad = cantools.database.load_string(text, database_format="dbc")
            print(f"{name}: {len(bad.messages)} messages")
        except Exception as e:  # noqa: BLE001
            print(f"{name}: {err(e)}")
            try:
                loose = cantools.database.load_string(text, database_format="dbc", strict=False)
                m = loose.messages[0]
                print(f"  not strict: {m.name} {m.signal_tree}")
            except Exception as e2:  # noqa: BLE001
                print(f"  not strict: {err(e2)}")

    print("== jobs")
    for line in read("jobs.txt").split("\n"):
        if line:
            print(f"> {line}")
            print(f"  {run_job(db, line)}")

    print("== drive.log")
    analyse(db, read("drive.log"))


main()
