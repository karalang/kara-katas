# Runs data/jobs.txt through the copy of python-hl7 0.4.5 in hl7/ and
# prints what it does; expected.out is this program's output.
#
# create_ack and generate_message_control_id read the clock and the
# random module, so the oracle gives hl7 a clock that starts at
# 2026-10-21 08:00:00 UTC and ticks one second per reading, and a
# `sample` that picks by a counter; mini_hl7.kara has the same two.
import asyncio
import datetime as real_datetime
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import hl7  # noqa: E402
import hl7.client  # noqa: E402
import hl7.containers  # noqa: E402
import hl7.util  # noqa: E402
from hl7.mllp import HL7StreamReader  # noqa: E402


class _Clock:
    ticks = 0

    @classmethod
    def utcnow(cls):
        t = real_datetime.datetime(2026, 10, 21, 8, 0, 0) + real_datetime.timedelta(seconds=cls.ticks)
        cls.ticks += 1
        return t


class _DatetimeModule:
    datetime = _Clock


class _Random:
    calls = 0

    @classmethod
    def sample(cls, population, k):
        n = len(population)
        out = [population[(cls.calls * 5 + i * 11) % n] for i in range(k)]
        cls.calls += 1
        return out


hl7.containers.datetime = _DatetimeModule
hl7.util.datetime = _DatetimeModule
hl7.util.random = _Random


def read(name):
    with open(os.path.join("data", name), newline="") as f:
        return f.read()


def read_bytes(name):
    with open(os.path.join("data", name), "rb") as f:
        return f.read()


def err(e):
    return "! %s: %r" % (type(e).__name__, str(e))


def decode_line(v):
    return v.replace("<CR>", "\r").replace("<LF>", "\n").replace("<TAB>", "\t")


def app_map(text):
    if text == "-":
        return None
    out = {}
    for part in text.split(","):
        k, v = part.split("=", 1)
        out[decode_line(k)] = v
    return out


def none_arg(v):
    return None if v == "-" else v


def int_arg(v):
    return None if v == "-" else int(v)


# ------------------------------------------------------------ structure


def show(obj, ind):
    print("%s%s len=%d" % (ind, type(obj).__name__, len(obj)))
    if isinstance(obj, (hl7.Batch, hl7.File)):
        print("%s header %r" % (ind, obj.header))
        print("%s trailer %r" % (ind, obj.trailer))
        for child in obj:
            show(child, ind + "  ")
    else:
        print("%s %r" % (ind, obj))


def show_str(obj):
    try:
        print("str %r" % str(obj))
    except Exception as e:
        print("str " + err(e))


def job_tree(name):
    text = read(name)
    for label, fn in (("parse_hl7", hl7.parse_hl7), ("parse", hl7.parse)):
        try:
            obj = fn(text)
        except Exception as e:
            print("%s %s" % (label, err(e)))
            continue
        print(label)
        show(obj, "  ")
        show_str(obj)
        try:
            print("same %r" % (str(obj) == text))
        except Exception as e:
            print("same " + err(e))


def job_batchof(name):
    h = hl7.parse(read(name))
    b = h.create_batch([h, h])
    print("batch len=%d" % len(b))
    show_str(b)
    b.header = b.create_header()
    print("header %r" % b.header)
    show_str(b)
    b.trailer = b.create_trailer()
    b.trailer.assign_field("2", 1)
    show_str(b)
    for label, seg in (("header", h.segment("PID")), ("trailer", h.segment("MSH"))):
        try:
            setattr(b, label, seg)
            print("set %s ok" % label)
        except Exception as e:
            print("set %s %s" % (label, err(e)))
    b.header = None
    show_str(b)
    b.trailer = None
    show_str(b)


def job_fileof(name):
    b = hl7.parse_batch(read(name))
    f = b.create_file([b])
    show(f, "")
    show_str(f)
    f.header = f.create_header()
    show_str(f)
    f.trailer = f.create_trailer()
    show_str(f)
    try:
        f.trailer = b[0].segment("PID")
    except Exception as e:
        print("set trailer " + err(e))
    m = b[0]
    print("message create_file %r" % m.create_file([]))
    print("message create_message %r" % str(m.create_message([m.segment("PID")])))


# ------------------------------------------------------------ access


def job_get(name, keys):
    h = hl7.parse(read(name))
    for k in keys:
        try:
            print("%s = %r" % (k, h[k]))
        except Exception as e:
            print("%s %s" % (k, err(e)))


def job_accessor(keys):
    for k in keys:
        try:
            a = hl7.Accessor.parse_key(k)
            print("%s -> %r key=%r str=%s" % (k, a, a.key, a))
        except Exception as e:
            print("%s %s" % (k, err(e)))


def job_set(name, assigns):
    h = hl7.parse(read(name))
    keys = []
    for a in assigns:
        k, v = a.split("=", 1)
        keys.append(k)
        try:
            h[k] = v
            print("set %s ok" % k)
        except Exception as e:
            print("set %s %s" % (k, err(e)))
    print("str %r" % str(h))
    for k in keys:
        try:
            print("  %s = %r" % (k, h[k]))
        except Exception as e:
            print("  %s %s" % (k, err(e)))


def job_assign(name, args):
    h = hl7.parse(read(name))
    seg, segnum = args[0], int(args[1])
    nums = [int_arg(x) for x in args[2:6]]
    value = args[6]
    try:
        h.assign_field(value, seg, segnum, *nums)
        print("assign ok")
    except Exception as e:
        print("assign " + err(e))
    try:
        print("  %r" % str(h.segments(seg)(segnum)))
    except Exception as e:
        print("  " + err(e))


def job_idx(name, args):
    h = hl7.parse(read(name))
    for a in args:
        try:
            if ":" in a:
                i, j = a.split(":")
                part = h[int(i):int(j)]
                print("%s -> %s %r" % (a, type(part).__name__, str(part)))
            else:
                print("%s -> %r" % (a, h[int(a)]))
        except Exception as e:
            print("%s %s" % (a, err(e)))


# ------------------------------------------------------------ escapes, datetimes


def escape_values():
    with open("data/escapes.txt", newline="") as f:
        return [decode_line(v) for v in f.read().split("\n")[:-1]]


def job_escape(name, mapping, out):
    h = hl7.parse(read(name))
    amap = app_map(mapping)
    for v in escape_values():
        try:
            r = h.escape(v, amap) if out else h.unescape(v, amap)
            print("%r -> %r" % (v, r))
        except Exception as e:
            print("%r %s" % (v, err(e)))


def job_dtm():
    with open("data/dtm.txt") as f:
        values = f.read().split("\n")[:-1]
    for v in values:
        try:
            dt = hl7.parse_datetime(v)
        except Exception as e:
            print("%r %s" % (v, err(e)))
            continue
        if dt is None:
            print("%r -> None" % v)
            continue
        try:
            s = str(dt)
        except Exception as e:
            s = err(e)
        tz = dt.tzname() if dt.tzinfo is not None else None
        print("%r -> %s tz=%r" % (v, s, tz))


# ------------------------------------------------------------ acks, files


def job_ack(name, args):
    h = hl7.parse(read(name))
    code, mid, app, fac = args[0], none_arg(args[1]), none_arg(args[2]), none_arg(args[3])
    try:
        ack = h.create_ack(code, mid, app, fac)
    except Exception as e:
        print("ack " + err(e))
        return
    print("ack %r" % str(ack))
    print("  %r" % ack)


def job_mcid(n):
    for _ in range(n):
        print("mcid %s" % hl7.generate_message_control_id())


def job_split(name):
    print(repr(hl7.split_file(read(name))))


def job_is(names):
    for n in names:
        t = read(n)
        print("%s ishl7=%r isbatch=%r isfile=%r" % (n, hl7.ishl7(t), hl7.isbatch(t), hl7.isfile(t)))


# ------------------------------------------------------------ MLLP


def job_stream(name, size):
    hl7.client.RECV_BUFFER = size
    try:
        for m in hl7.client.read_stream(io.BytesIO(read_bytes(name))):
            print("message %r" % m)
    except Exception as e:
        print(err(e))


def job_loose(name):
    for m in hl7.client.read_loose(io.BytesIO(read_bytes(name))):
        print("message %r" % m)


def parse_encoding(text):
    if text == "-":
        return None, None
    if "," in text:
        e, errs = text.split(",")
        return e, errs
    return text, None


async def read_blocks(data, limit, enc, errs, handle):
    reader = HL7StreamReader(limit=limit, encoding=enc, encoding_errors=errs)
    reader.feed_data(data)
    reader.feed_eof()
    while True:
        try:
            m = await reader.readmessage()
        except asyncio.IncompleteReadError as e:
            print("end " + err(e))
            return
        except Exception as e:
            print(err(e))
            continue
        handle(m)


def job_blocks(name, limit, encoding):
    enc, errs = parse_encoding(encoding)
    asyncio.run(read_blocks(read_bytes(name), limit, enc, errs, lambda m: print("message %r" % str(m))))


# ------------------------------------------------------------ the interface engine


def patient_name(m):
    fam, given, middle, prefix = (m["PID.5.1.%d" % i] for i in (1, 2, 3, 5))
    name = "%s, %s" % (fam, given)
    if middle:
        name += " " + middle
    if prefix:
        name += " (%s)" % prefix
    return name


def when(v):
    dt = hl7.parse_datetime(v)
    return "-" if dt is None else str(dt)


def leaves(c):
    if isinstance(c, str):
        return [c]
    out = []
    for x in c:
        out.extend(leaves(x))
    return out


def job_route(name):
    census = {}
    results = []
    acks = []
    count = [0]

    def handle(m):
        count[0] += 1
        ctrl = m["MSH.10"]
        mtype = m["MSH.9.1.1"]
        try:
            event = m["MSH.9.1.2"]
        except IndexError:
            # MSH.9 with no components ("QRY"): the event is missing
            event = ""
        print("in %d %s %s^%s from %s" % (count[0], ctrl, mtype, event, m["MSH.3"]))
        code, text = "AA", ""
        try:
            m.segment("PID")
            has_pid = True
        except KeyError:
            has_pid = False
        if mtype == "ADT" and event in ("A01", "A03", "A08"):
            if not has_pid:
                code, text = "AE", "PID segment missing"
            else:
                mrn = m["PID.3.1.1"]
                rec = census.get(mrn, {"status": "-", "admitted": "-", "discharged": "-"})
                rec["name"] = patient_name(m)
                try:
                    pv1 = m.segment("PV1")
                    rec["bed"] = "%s/%s" % (m["PV1.3.1.1"], m["PV1.3.1.2"])
                    if len(pv1) > 7:
                        rec["doctor"] = "%s %s %s" % (m["PV1.7.1.6"], m["PV1.7.1.3"], m["PV1.7.1.2"])
                    if event == "A01":
                        rec["status"] = "admitted"
                        rec["admitted"] = when(m["PV1.44"])
                    elif event == "A03":
                        rec["status"] = "discharged"
                        rec["admitted"] = when(m["PV1.44"])
                        rec["discharged"] = when(m["PV1.45"])
                except KeyError:
                    pass
                census[mrn] = rec
                print("  census %s %s %s" % (mrn, rec["status"], rec.get("bed", "-")))
        elif mtype == "ORU" and event == "R01":
            mrn = m["PID.3.1.1"]
            current = None
            for seg in m:
                sid = seg[0][0]
                if sid == "OBR":
                    current = {"test": m.unescape(str(seg(4)(1)(2))), "rows": [], "notes": []}
                    results.append((mrn, current))
                elif sid == "OBX" and current is not None:
                    values = [m.unescape(str(r)) for r in seg(5)]
                    flag = str(seg(8)) if len(seg) > 8 else ""
                    current["rows"].append(
                        (str(seg(3)(1)(2)), " / ".join(values), str(seg(6)), str(seg(7)), flag)
                    )
                elif sid == "NTE" and current is not None:
                    current["notes"].append(m.unescape(str(seg(3)), {"H": "*", "N": "*"}))
            print("  results %s %d groups" % (mrn, sum(1 for r in results if r[0] == mrn)))
        else:
            code, text = "AR", "unsupported message type %s^%s" % (mtype, event)
        try:
            ack = m.create_ack(code, "ACK" + ctrl, "RIVERSIDE-IE", "RIVERSIDE")
        except Exception as e:
            print("  no ack " + err(e))
            return
        if text:
            ack["MSA.3"] = text
        acks.append(str(ack))
        print("  ack %r" % str(ack))

    asyncio.run(read_blocks(read_bytes(name), 65536, "utf-8", None, handle))
    with open("data/out/acks.mllp", "wb") as f:
        for a in acks:
            f.write(b"\x0b" + a.encode("utf-8") + b"\x1c\r")
    print("acks written %d" % len(acks))
    print("census")
    for mrn in sorted(census):
        r = census[mrn]
        print("  %s %-28s %-10s %-9s %s admitted %s discharged %s" % (
            mrn, r["name"], r["status"], r.get("bed", "-"), r.get("doctor", "-"), r["admitted"], r["discharged"]))
    lines = []
    for mrn, g in results:
        lines.append("%s %s" % (mrn, g["test"]))
        for test, value, units, ref, flag in g["rows"]:
            mark = {"H": "high", "L": "low", "HH": "CRITICAL", "LL": "CRITICAL"}.get(flag, "")
            lines.append("  %-12s %-40s %-8s %-10s %s" % (test, value, units, ref, mark))
        for n in g["notes"]:
            lines.append("  note %r" % n)
    with open("data/out/results.txt", "w") as f:
        f.write("".join(x + "\n" for x in lines))
    print("results")
    for x in lines:
        print(x)
    critical = sum(1 for _, g in results for row in g["rows"] if row[4] in ("HH", "LL"))
    print("critical %d" % critical)


def convert(node, old, new, level):
    if isinstance(node, str):
        return new.escape(old.unescape(node))
    makers = {1: new.create_segment, 2: new.create_field, 3: new.create_repetition, 4: new.create_component}
    return makers[level]([convert(x, old, new, level + 1) for x in node])


def job_reencode(name, seps):
    h = hl7.parse(read(name))
    fsep, comp, rep, esc, sub = seps
    new = hl7.Message(separators="\r" + fsep + rep + comp + sub, esc=esc)
    for seg in h:
        if seg[0][0] == "MSH":
            nseg = new.create_segment(
                [new.create_field(["MSH"]), new.create_field([fsep]), new.create_field([comp + rep + esc + sub])]
            )
            for field in seg[3:]:
                nseg.append(convert(field, h, new, 2))
        else:
            nseg = convert(seg, h, new, 1)
        new.append(nseg)
    text = str(new)
    print("out %r" % text)
    back = hl7.parse(text)
    print("roundtrip %r" % (str(back) == text))
    a = [h.unescape(x) for s in h for x in leaves(s[3:] if s[0][0] == "MSH" else s)]
    b = [back.unescape(x) for s in back for x in leaves(s[3:] if s[0][0] == "MSH" else s)]
    print("leaves %d same %r" % (len(a), a == b))
    for x, y in zip(a, b):
        if x != y:
            print("  %r != %r" % (x, y))


def job_audit(name):
    f = hl7.parse_hl7(read(name))
    print("file %s batches=%d declared=%s" % (str(f.header(11)), len(f), str(f.trailer(1))))
    seen = {}
    for b in f:
        label = str(b.header(11)) if b.header else "(default)"
        declared = str(b.trailer(1)) if b.trailer else "-"
        ok = "ok" if declared in ("-", str(len(b))) else "MISMATCH"
        print("  batch %s messages=%d declared=%s %s" % (label, len(b), declared, ok))
        for m in b:
            ctrl = m["MSH.10"]
            counts = {}
            for seg in m:
                counts[seg[0][0]] = counts.get(seg[0][0], 0) + 1
            shape = " ".join("%s:%d" % (k, counts[k]) for k in sorted(counts))
            dup = " DUPLICATE of %s" % seen[ctrl] if ctrl in seen else ""
            seen.setdefault(ctrl, label)
            print("    %s %s^%s %s%s" % (ctrl, m["MSH.9.1.1"], m["MSH.9.1.2"], shape, dup))
    total = sum(len(b) for b in f)
    print("  total messages %d ok=%r" % (total, str(len(f)) == str(f.trailer(1))))


def main():
    with open("data/jobs.txt") as f:
        jobs = f.read().split("\n")[:-1]
    for line in jobs:
        print("== " + line)
        try:
            run_job(line.split(" "))
        except Exception as e:
            print(err(e))


def run_job(w):
    if True:
        k = w[0]
        if k == "tree":
            job_tree(w[1])
        elif k == "batchof":
            job_batchof(w[1])
        elif k == "fileof":
            job_fileof(w[1])
        elif k == "get":
            job_get(w[1], w[2:])
        elif k == "accessor":
            job_accessor(w[1:])
        elif k == "set":
            job_set(w[1], split_assigns(w[2:]))
        elif k == "assign":
            job_assign(w[1], w[2:])
        elif k == "idx":
            job_idx(w[1], w[2:])
        elif k == "escape":
            job_escape(w[1], w[2], False)
        elif k == "escapeout":
            job_escape(w[1], w[2], True)
        elif k == "dtm":
            job_dtm()
        elif k == "ack":
            job_ack(w[1], w[2:])
        elif k == "mcid":
            job_mcid(int(w[1]))
        elif k == "split":
            job_split(w[1])
        elif k == "is":
            job_is(w[1:])
        elif k == "stream":
            job_stream(w[1], int(w[2]))
        elif k == "loose":
            job_loose(w[1])
        elif k == "blocks":
            job_blocks(w[1], int(w[2]), w[3])
        elif k == "route":
            job_route(w[1])
        elif k == "reencode":
            job_reencode(w[1], w[2])
        elif k == "audit":
            job_audit(w[1])


def split_assigns(words):
    # "PID.F13.R3=01632 960199" holds a space: a word with no '=' joins
    # the assignment before it.
    out = []
    for word in words:
        if "=" in word or not out:
            out.append(word)
        else:
            out[-1] += " " + word
    return out


main()
