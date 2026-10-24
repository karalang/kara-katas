"""Runs data/jobs.txt on the vendored h2 4.2.0 and prints what it does.

Each job is a conversation between H2Connection objects, one command per
line (see mk.py). Bytes an endpoint sends are parsed back with hyperframe
and printed frame by frame; events are printed with their own repr, and
exceptions as `error <class>: <str>`.

Run: python3 -I -B oracle.py > expected.out"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))

from h2.config import H2Configuration  # noqa: E402
from h2.connection import H2Connection  # noqa: E402
from hpack.struct import NeverIndexedHeaderTuple  # noqa: E402
from hyperframe.frame import Frame  # noqa: E402

PREAMBLE = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"


def unesc(s):
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "~" and i + 1 < len(s):
            d = s[i + 1]
            out.append({"s": " ", "t": "\t", "n": "\n", "e": "=", "~": "~", "c": ",", "z": ""}.get(d, d))
            i += 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


def parse_header(tok):
    never = tok.startswith("!")
    raw = tok.startswith("%")
    if never or raw:
        tok = tok[1:]
    eq = tok.index("=", 1)
    name = unesc(tok[:eq])
    value = unesc(tok[eq + 1:])
    if raw:
        return (name.encode("utf-8"), value.encode("utf-8"))
    if never:
        return NeverIndexedHeaderTuple(name, value)
    return (name, value)


def payload(tok):
    if tok.startswith("len="):
        n = int(tok[4:])
        return bytes((i * 7 + 3) % 251 for i in range(n))
    if tok.startswith("hex="):
        return bytes.fromhex(tok[4:])
    return unesc(tok).encode("utf-8")


def show_frames(data):
    if data.startswith(PREAMBLE):
        print("    > preamble")
        data = data[len(PREAMBLE):]
    while len(data) >= 9:
        f, length = Frame.parse_frame_header(memoryview(data[:9]))
        if len(data) < 9 + length:
            break
        f.parse_body(memoryview(data[9:9 + length]))
        print(f"    > {f!r}")
        data = data[9 + length:]
    if data:
        print(f"    > {len(data)} trailing bytes")


def show_error(e):
    print(f"    error {type(e).__name__}: {e}")


def opts_of(words):
    out = {}
    for w in words:
        k, _, v = w.partition("=")
        out[k] = v
    return out


def make_conn(side, opts):
    kw = {"client_side": side == "client"}
    if "encoding" in opts:
        kw["header_encoding"] = opts["encoding"]
    for k in ("validate_outbound_headers", "normalize_outbound_headers", "split_outbound_cookies",
              "validate_inbound_headers", "normalize_inbound_headers"):
        if k in opts:
            kw[k] = opts[k] == "1"
    return H2Connection(config=H2Configuration(**kw))


def state_line(name, c):
    out_n = c.open_outbound_streams
    in_n = c.open_inbound_streams
    print(f"    {name}: {c.state_machine.state}, open out {out_n} in {in_n}, "
          f"window out {c.outbound_flow_control_window} in {c.inbound_flow_control_window}, "
          f"next {next_id(c)}")
    for sid in sorted(c.streams):
        s = c.streams[sid]
        print(f"      {s!r} out {s.outbound_flow_control_window} in {s.inbound_flow_control_window}"
              f" frame {s.max_outbound_frame_size}")


def next_id(c):
    try:
        return c.get_next_available_stream_id()
    except Exception as e:
        return f"error {type(e).__name__}"


def deliver(dst, data):
    try:
        events = dst.receive_data(data)
    except Exception as e:
        show_error(e)
        return
    for ev in events:
        print(f"    {ev!r}")


def run_job(lines):
    conns = {}
    for line in lines:
        w = line.split(" ")
        if len(w) > 2 and w[1] == "raw":
            print(f"  {w[0]} raw {len(w[2]) // 2} bytes")
        else:
            print(f"  {line}")
        name, verb, args = w[0], w[1], w[2:]
        if name == "pipe":
            src, dst = conns[verb], conns[args[0]]
            if len(args) > 1:
                data = src.data_to_send(int(args[1]))
                print(f"    > {len(data)} bytes")
            else:
                data = src.data_to_send()
                show_frames(data)
            deliver(dst, data)
            continue
        if verb == "new":
            conns[name] = make_conn(args[0], opts_of(args[1:]))
            continue
        c = conns[name]
        try:
            if verb == "initiate":
                c.initiate_connection()
            elif verb == "upgrade":
                hdr = args[0].encode("ascii") if args else None
                r = c.initiate_upgrade_connection(hdr)
                print(f"    -> {r!r}")
            elif verb == "headers":
                sid = int(args[0])
                kw = {}
                hs = []
                for a in args[1:]:
                    if a == "end":
                        kw["end_stream"] = True
                    elif a.startswith("w=") or a.startswith("d=") or a.startswith("x="):
                        key = {"w": "priority_weight", "d": "priority_depends_on", "x": "priority_exclusive"}[a[0]]
                        kw[key] = (a[2:] == "1") if a[0] == "x" else int(a[2:])
                    else:
                        hs.append(parse_header(a))
                c.send_headers(sid, hs, **kw)
            elif verb == "data":
                sid = int(args[0])
                kw = {}
                for a in args[2:]:
                    if a == "end":
                        kw["end_stream"] = True
                    elif a.startswith("pad="):
                        kw["pad_length"] = int(a[4:])
                c.send_data(sid, payload(args[1]), **kw)
            elif verb == "end":
                c.end_stream(int(args[0]))
            elif verb == "window":
                if len(args) > 1:
                    c.increment_flow_control_window(int(args[0]), stream_id=int(args[1]))
                else:
                    c.increment_flow_control_window(int(args[0]))
            elif verb == "push":
                c.push_stream(int(args[0]), int(args[1]), [parse_header(a) for a in args[2:]])
            elif verb == "ping":
                c.ping(payload(args[0]))
            elif verb == "reset":
                if len(args) > 1:
                    c.reset_stream(int(args[0]), int(args[1]))
                else:
                    c.reset_stream(int(args[0]))
            elif verb == "goaway":
                kw = opts_of(args)
                c.close_connection(error_code=int(kw.get("code", "0")),
                                   additional_data=payload(kw["data"]) if "data" in kw else None,
                                   last_stream_id=int(kw["last"]) if "last" in kw else None)
            elif verb == "settings":
                c.update_settings({int(k): int(v) for k, v in opts_of(args).items()})
            elif verb == "altsvc":
                kw = opts_of(args[1:])
                c.advertise_alternative_service(payload(args[0]),
                                                origin=payload(kw["origin"]) if "origin" in kw else None,
                                                stream_id=int(kw["sid"]) if "sid" in kw else None)
            elif verb == "prio":
                kw = opts_of(args[1:])
                c.prioritize(int(args[0]), weight=int(kw["w"]) if "w" in kw else None,
                             depends_on=int(kw["d"]) if "d" in kw else None,
                             exclusive=(kw["x"] == "1") if "x" in kw else None)
            elif verb == "ack":
                c.acknowledge_received_data(int(args[0]), int(args[1]))
            elif verb == "raw":
                deliver(c, bytes.fromhex(args[0]))
            elif verb == "drop":
                print(f"    dropped {len(c.data_to_send())} bytes")
            elif verb == "show":
                show_frames(c.data_to_send())
            elif verb == "state":
                state_line(name, c)
            elif verb == "windows":
                sid = int(args[0])
                print(f"    local {c.local_flow_control_window(sid)} remote {c.remote_flow_control_window(sid)}")
            else:
                raise SystemExit(f"unknown verb {verb}")
        except Exception as e:
            show_error(e)


def main():
    with open(os.path.join(HERE, "data", "jobs.txt"), encoding="utf-8") as fh:
        text = fh.read()
    jobs = []
    for line in text.split("\n"):
        if line.startswith("job "):
            jobs.append((line[4:], []))
        elif line:
            jobs[-1][1].append(line)
    for title, lines in jobs:
        print(f"> {title}")
        run_job(lines)


main()
