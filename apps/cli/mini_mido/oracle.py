# Runs data/jobs.jsonl and the five programs through mido 1.3.3 itself
# (the copy in mido/, unchanged) and prints what mini_mido.kara must
# print.
import glob
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(write_through=True)
os.chdir(HERE)

import mido  # noqa: E402
from mido.frozen import freeze_message, is_frozen, thaw_message  # noqa: E402
from mido.midifiles.meta import (  # noqa: E402
    decode_variable_int, encode_variable_int, signed, unsigned)
from mido.midifiles.tracks import fix_end_of_track  # noqa: E402
from mido.ports import EchoPort  # noqa: E402
from mido.tokenizer import Tokenizer  # noqa: E402

assert mido.__file__.startswith(HERE), mido.__file__


def err(e):
    return f"{type(e).__name__}: {e}"


def val(x):
    """A job value: JSON, with {"tuple": [...]} for a tuple."""
    if isinstance(x, dict):
        return tuple(val(y) for y in x["tuple"])
    if isinstance(x, list):
        return [val(y) for y in x]
    return x


def kwargs(kw):
    return {k: val(v) for k, v in kw.items()}


def data_path(p):
    return os.path.join("data", p)


def hexdump(b, indent="    "):
    for i in range(0, len(b), 16):
        print(f"{indent}{i:04x}: {b[i:i + 16].hex(' ')}")


def show_value(what, m):
    if what == "repr":
        return repr(m)
    if what == "str":
        return str(m)
    if what == "bytes":
        return repr(m.bytes())
    if what == "hex":
        return repr(m.hex())
    if what.startswith("hex/"):
        return repr(m.hex(what[4:]))
    if what == "bin":
        return repr(m.bin())
    if what == "len":
        return repr(len(m))
    if what == "len_text":
        return repr(len(m.text))
    if what == "dict":
        return repr(m.dict())
    if what == "is_cc":
        return repr(m.is_cc())
    if what.startswith("is_cc="):
        return repr(m.is_cc(int(what[6:])))
    if what == "is_meta":
        return repr(m.is_meta)
    if what == "is_realtime":
        return repr(m.is_realtime)
    if what == "frozen":
        return repr(is_frozen(m))
    if what.startswith("a:"):
        return repr(getattr(m, what[2:]))
    raise AssertionError(what)


def show_file(what, f):
    if what == "repr":
        print("  repr:")
        for line in repr(f).split("\n"):
            print("    " + line)
    elif what == "type":
        print(f"  type: {f.type!r}")
    elif what == "tpb":
        print(f"  ticks_per_beat: {f.ticks_per_beat!r}")
    elif what == "length":
        try:
            print(f"  length: {f.length!r}")
        except Exception as e:
            print(f"  length: {err(e)}")
    elif what in ("print_tracks", "print_meta"):
        print(f"  {what}:")
        f.print_tracks(meta_only=what == "print_meta")
    elif what == "play_list":
        print("  play:")
        try:
            for m in f:
                print(f"    {m!r}")
        except Exception as e:
            print(f"    {err(e)}")
    elif what == "merged":
        try:
            print(f"  merged: {f.merged_track!r}")
        except Exception as e:
            print(f"  merged: {err(e)}")
    else:
        raise AssertionError(what)


def run_step(env, step):
    op = step[0]
    if op in ("msg", "meta"):
        _, v, kind, kw = step
        try:
            if op == "msg":
                env[v] = mido.Message(kind, **kwargs(kw))
            else:
                env[v] = mido.MetaMessage(kind, **kwargs(kw))
            print(f"  {v} = {env[v]!r}")
        except Exception as e:
            print(f"  {v}: {err(e)}")
    elif op == "unknown":
        _, v, tb, data, time = step
        env[v] = mido.UnknownMetaMessage(tb, val(data), time)
        print(f"  {v} = {env[v]!r}")
    elif op in ("from_bytes", "from_hex", "from_str", "meta_bytes"):
        v = step[1]
        try:
            if op == "from_bytes":
                env[v] = mido.Message.from_bytes(step[2], time=step[3])
            elif op == "from_hex":
                env[v] = mido.Message.from_hex(step[2], sep=step[3])
            elif op == "from_str":
                env[v] = mido.Message.from_str(step[2])
            else:
                env[v] = mido.MetaMessage.from_bytes(step[2])
            print(f"  {v} = {env[v]!r}")
        except Exception as e:
            print(f"  {v}: {err(e)}")
    elif op == "show":
        if step[1] not in env:
            print(f"  {step[1]}: no value")
            return
        m = env[step[1]]
        for what in step[2:]:
            try:
                print(f"  {step[1]}.{what}: {show_value(what, m)}")
            except Exception as e:
                print(f"  {step[1]}.{what}: {err(e)}")
    elif op == "set":
        _, v, name, value = step
        try:
            setattr(env[v], name, val(value))
            print(f"  {v}.{name} = {val(value)!r}: ok")
        except Exception as e:
            print(f"  {v}.{name} = {val(value)!r}: {err(e)}")
    elif op == "copy":
        _, v, new, kw = step
        try:
            env[new] = env[v].copy(**kwargs(kw))
            print(f"  {new} = {env[new]!r}")
        except Exception as e:
            print(f"  {new}: {err(e)}")
    elif op == "eq":
        print(f"  {step[1]} == {step[2]}: {env[step[1]] == env[step[2]]!r}")
    elif op == "eq_val":
        try:
            print(f"  {step[1]} == {val(step[2])!r}: {env[step[1]] == val(step[2])!r}")
        except Exception as e:
            print(f"  {step[1]} == {val(step[2])!r}: {err(e)}")
    elif op == "format":
        print(f"  format_as_string({step[1]}, include_time={step[2]}): "
              f"{mido.format_as_string(env[step[1]], include_time=step[2])!r}")
    elif op == "freeze":
        env[step[2]] = freeze_message(env[step[1]])
        print(f"  {step[2]} = {env[step[2]]!r}")
    elif op == "thaw":
        env[step[2]] = thaw_message(env[step[1]])
        print(f"  {step[2]} = {env[step[2]]!r}")
    elif op in ("parse", "parse_all"):
        try:
            if op == "parse":
                print(f"  parse {step[1]}: {mido.parse(step[1])!r}")
            else:
                print(f"  parse_all {step[1]}: {mido.parse_all(step[1])!r}")
        except Exception as e:
            print(f"  {op} {step[1]}: {err(e)}")
    elif op == "parser":
        env[step[1]] = mido.Parser()
        print(f"  {step[1]} = Parser()")
    elif op in ("feed", "feed_byte"):
        try:
            getattr(env[step[1]], op)(step[2])
            print(f"  {op} {step[2]!r}: ok")
        except Exception as e:
            print(f"  {op} {step[2]!r}: {err(e)}")
    elif op == "pending":
        print(f"  pending: {env[step[1]].pending()}")
    elif op == "get":
        print(f"  get_message: {env[step[1]].get_message()!r}")
    elif op == "drain":
        print(f"  drained: {list(env[step[1]])!r}")
    elif op == "tokenize":
        print(f"  tokens of {step[1]}: {list(Tokenizer(step[1]))!r}")
    elif op == "stream":
        print("  stream:")
        try:
            for m, e in mido.parse_string_stream(step[1]):
                print(f"    {m!r}, {e!r}")
        except Exception as e:
            print(f"    {err(e)}")
    elif op == "t2s":
        print(f"  tick2second{tuple(step[1:])}: {mido.tick2second(*step[1:])!r}")
    elif op == "s2t":
        try:
            print(f"  second2tick{tuple(step[1:])}: {mido.second2tick(*step[1:])!r}")
        except Exception as e:
            print(f"  second2tick{tuple(step[1:])}: {err(e)}")
    elif op in ("bpm2tempo", "tempo2bpm"):
        fn = getattr(mido, op)
        args = (step[1],) if step[2] is None else (step[1], tuple(step[2]))
        try:
            print(f"  {op}{args!r}: {fn(*args)!r}")
        except Exception as e:
            print(f"  {op}{args!r}: {err(e)}")
    elif op == "varint":
        try:
            print(f"  encode_variable_int({step[1]!r}): {encode_variable_int(step[1])!r}")
        except Exception as e:
            print(f"  encode_variable_int({step[1]!r}): {err(e)}")
    elif op == "devarint":
        print(f"  decode_variable_int({step[1]!r}): {decode_variable_int(list(step[1]))!r}")
    elif op in ("signed", "unsigned"):
        fn = signed if op == "signed" else unsigned
        try:
            print(f"  {op}({step[1]!r}, {step[2]!r}): {fn(step[1], step[2])!r}")
        except Exception as e:
            print(f"  {op}({step[1]!r}, {step[2]!r}): {err(e)}")
    elif op == "track":
        env[step[1]] = mido.MidiTrack([env[x] for x in step[2]])
        print(f"  {step[1]} = MidiTrack of {len(step[2])}")
    elif op == "tshow":
        t = env[step[1]]
        for what in step[2:]:
            if what == "repr":
                print(f"  {step[1]}.repr:")
                for line in repr(t).split("\n"):
                    print("    " + line)
            elif what == "len":
                print(f"  {step[1]}.len: {len(t)}")
            elif what == "name":
                print(f"  {step[1]}.name: {t.name!r}")
    elif op == "tname":
        try:
            env[step[1]].name = step[2]
            print(f"  {step[1]}.name = {step[2]!r}: ok")
        except Exception as e:
            print(f"  {step[1]}.name = {step[2]!r}: {err(e)}")
    elif op == "tslice":
        env[step[2]] = env[step[1]][step[3]:step[4]]
        print(f"  {step[2]} = {step[1]}[{step[3]}:{step[4]}]")
    elif op == "tindex":
        try:
            env[step[3]] = env[step[1]][step[2]]
            print(f"  {step[3]} = {step[1]}[{step[2]}]")
        except Exception as e:
            print(f"  {step[3]}: {err(e)}")
    elif op == "tadd":
        env[step[3]] = env[step[1]] + env[step[2]]
        print(f"  {step[3]} = {step[1]} + {step[2]}")
    elif op == "tmul":
        env[step[3]] = env[step[1]] * step[2]
        print(f"  {step[3]} = {step[1]} * {step[2]}")
    elif op == "tappend":
        env[step[1]].append(env[step[2]])
        print(f"  {step[1]}.append({step[2]})")
    elif op == "fix_eot":
        env[step[2]] = mido.MidiTrack(fix_end_of_track(env[step[1]]))
        print(f"  {step[2]} = fix_end_of_track({step[1]})")
    elif op == "merge":
        try:
            env[step[1]] = mido.merge_tracks([env[x] for x in step[2]], skip_checks=step[3])
            print(f"  {step[1]} = merge_tracks({', '.join(step[2])})")
        except Exception as e:
            print(f"  {step[1]}: {err(e)}")
    elif op == "file":
        _, v, kw, tracks = step
        try:
            env[v] = mido.MidiFile(tracks=[env[x] for x in tracks] if tracks else None, **kw)
            print(f"  {v} = MidiFile with {len(env[v].tracks)} tracks")
        except Exception as e:
            print(f"  {v}: {err(e)}")
    elif op == "add_track":
        t = env[step[1]].add_track(step[2])
        print(f"  add_track({step[2]!r}): {t!r}")
    elif op == "save":
        p = data_path(step[2])
        try:
            env[step[1]].save(p)
            with open(p, "rb") as f:
                b = f.read()
            print(f"  saved {step[2]}: {len(b)} bytes")
            hexdump(b)
        except Exception as e:
            print(f"  save {step[2]}: {err(e)}")
    elif op == "load":
        _, v, p, kw = step
        try:
            env[v] = mido.MidiFile(data_path(p), **kw)
            print(f"  {v} = {p}: type {env[v].type}, {len(env[v].tracks)} tracks")
        except Exception as e:
            print(f"  {v}: {err(e)}")
    elif op == "fshow":
        if step[1] not in env:
            print(f"  {step[1]}: no value")
            return
        for what in step[2:]:
            show_file(what, env[step[1]])
    elif op == "same_file":
        a = open(data_path(step[1]), "rb").read()
        b = open(data_path(step[2]), "rb").read()
        print(f"  {step[1]} == {step[2]}: {a == b}")
    elif op == "read_syx":
        try:
            ms = mido.read_syx_file(data_path(step[1]))
            print(f"  read_syx_file {step[1]}: {len(ms)} messages")
            for m in ms:
                print(f"    {m!r}")
        except Exception as e:
            print(f"  read_syx_file {step[1]}: {err(e)}")
    elif op == "write_syx":
        _, p, vs, plain = step
        mido.write_syx_file(data_path(p), [env[x] for x in vs], plaintext=plain)
        print(f"  write_syx_file {p} plaintext={plain}")
    elif op == "dump":
        b = open(data_path(step[1]), "rb").read()
        print(f"  {step[1]}: {len(b)} bytes")
        hexdump(b)
    elif op == "port":
        env[step[1]] = EchoPort(step[2], autoreset=step[3])
        print(f"  {step[1]} = {env[step[1]]!r}")
    elif op == "prepr":
        print(f"  {step[1]}: {env[step[1]]!r}")
    elif op == "send":
        try:
            env[step[1]].send(env[step[2]])
            print(f"  send {step[2]}: ok")
        except Exception as e:
            print(f"  send {step[2]}: {err(e)}")
    elif op == "send_new":
        env[step[1]].send(mido.Message(step[2], **step[3]))
        print(f"  send {step[2]}: ok")
    elif op == "poll":
        print(f"  poll: {env[step[1]].poll()!r}")
    elif op == "receive":
        try:
            print(f"  receive: {env[step[1]].receive()!r}")
        except Exception as e:
            print(f"  receive: {err(e)}")
    elif op == "iter":
        ms = list(env[step[1]].iter_pending())
        print(f"  iter_pending: {len(ms)} messages")
        for m in ms:
            print(f"    {m}")
    elif op == "count":
        print(f"  pending on {step[1]}: {len(env[step[1]]._messages)}")
    elif op == "close":
        env[step[1]].close()
        print(f"  closed {step[1]}")
    elif op in ("reset", "panic"):
        getattr(env[step[1]], op)()
        print(f"  {op} {step[1]}")
    else:
        raise AssertionError(op)


def run_jobs():
    with open("data/jobs.jsonl", encoding="utf-8") as f:
        jobs = [json.loads(line) for line in f]
    for j in jobs:
        print(f"== {j['name']}")
        env = {}
        for step in j["steps"]:
            run_step(env, step)


# ------------------------------------------------------------ programs

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def note_name(n):
    return f"{NOTE_NAMES[n % 12]}{n // 12 - 1}"


def song_files():
    return sorted(glob.glob(data_path("songs/*.mid")))


def report():
    """A report on every song: its tracks, notes, tempo map and length."""
    print("== program: report")
    for p in song_files():
        name = os.path.basename(p)
        try:
            f = mido.MidiFile(p)
        except Exception as e:
            print(f"{name}: cannot read: {err(e)}")
            continue
        print(f"{name}: format {f.type}, {len(f.tracks)} tracks, {f.ticks_per_beat} ticks per beat")
        for i, t in enumerate(f.tracks):
            counts = {}
            for m in t:
                counts[m.type] = counts.get(m.type, 0) + 1
            kinds = ", ".join(f"{k} {counts[k]}" for k in sorted(counts))
            label = t.name or "(no name)"
            print(f"  track {i} {label!r}: {len(t)} messages: {kinds}")
            notes = [m.note for m in t if m.type == "note_on" and m.velocity > 0]
            if notes:
                chans = sorted({m.channel for m in t if m.type == "note_on"})
                print(f"    {len(notes)} notes on channel {', '.join(str(c) for c in chans)}, "
                      f"{note_name(min(notes))} to {note_name(max(notes))}")
        if f.type == 2:
            print("  tracks play on their own; no tempo map or length")
            continue
        now = 0
        sounding = set()
        for m in f.merged_track:
            now += m.time
            if m.type == "set_tempo":
                print(f"  tick {now}: {mido.tempo2bpm(m.tempo):.2f} bpm")
            elif m.type == "time_signature":
                print(f"  tick {now}: {m.numerator}/{m.denominator} time")
            elif m.type == "key_signature":
                print(f"  tick {now}: key of {m.key}")
            elif m.type == "note_on" and m.velocity > 0:
                sounding.add((m.channel, m.note))
            elif m.type in ("note_on", "note_off"):
                sounding.discard((m.channel, m.note))
        print(f"  ends at tick {now}, {f.length:.3f} seconds")
        if sounding:
            held = ", ".join(f"{note_name(n)} on {c}" for c, n in sorted(sounding))
            print(f"  still sounding at the end: {held}")


def transpose():
    """The minuet in C: melody up a fourth, bass down an octave, faster."""
    print("== program: transpose")
    f = mido.MidiFile(data_path("songs/minuet.mid"))
    shift = {0: 5, 1: -12}
    changed = 0
    for t in f.tracks:
        for i, m in enumerate(t):
            if m.type in ("note_on", "note_off"):
                n = m.note + shift.get(m.channel, 0)
                if 0 <= n <= 127:
                    t[i] = m.copy(note=n)
                    changed += 1
            elif m.type == "set_tempo":
                bpm = mido.tempo2bpm(m.tempo) * 1.25
                t[i] = m.copy(tempo=mido.bpm2tempo(bpm))
                print(f"  tempo {m.tempo} -> {t[i].tempo} ({bpm:.2f} bpm)")
            elif m.type == "key_signature":
                t[i] = m.copy(key="C")
        if t.name:
            t.name = t.name + " (in C)"
    print(f"  {changed} note messages moved")
    out = data_path("out/minuet_in_c.mid")
    f.save(out)
    b = open(out, "rb").read()
    print(f"  saved out/minuet_in_c.mid: {len(b)} bytes, length {f.length:.3f} seconds")
    hexdump(b[:48])
    g = mido.MidiFile(out)
    same = all(a == c for ta, tc in zip(f.tracks, g.tracks) for a, c in zip(ta, tc))
    print(f"  reloaded: {len(g.tracks)} tracks, same messages: {same}")
    orig = mido.MidiFile(data_path("songs/minuet.mid"))
    for i, (ta, tb) in enumerate(zip(orig.tracks, g.tracks)):
        diffs = sum(1 for a, c in zip(ta, tb) if a != c)
        print(f"  track {i} {tb.name!r}: {diffs} of {len(tb)} messages differ from the original")
    print("  first notes:")
    for m in [m for m in g.tracks[1] if m.type == "note_on"][:6]:
        print(f"    {m} ({note_name(m.note)})")


MAKERS = {0x41: "Roland", 0x43: "Yamaha", 0x7E: "universal non-realtime", 0x7F: "universal realtime"}


def describe(m):
    d = m.data
    if not d:
        return "empty"
    who = MAKERS.get(d[0], f"maker 0x{d[0]:02x}")
    if d[0] == 0x41 and len(d) >= 5 and d[3] == 0x12:
        addr = d[4:8]
        body = d[8:-1]
        cs = d[-1]
        want = (128 - (sum(addr) + sum(body)) % 128) % 128
        ok = "ok" if cs == want else f"bad, want {want:02X}"
        text = "".join(chr(b) if 32 <= b < 127 else "." for b in body)
        return (f"{who} DT1 model 0x{d[2]:02x} device 0x{d[1]:02x} address {bytes(addr).hex()} "
                f"{len(body)} bytes {text!r} checksum {cs:02X} {ok}")
    if d[0] == 0x7E and d[2:4] == (0x09, 0x01):
        return f"{who}: General MIDI on"
    if d[0] == 0x7F and d[2:4] == (0x04, 0x01) and len(d) >= 6:
        return f"{who}: master volume {d[4] | d[5] << 7}"
    if d[0] == 0x43 and d[2:] == (0x4C, 0x00, 0x00, 0x7E, 0x00):
        return f"{who}: XG system on"
    return f"{who}: {len(d)} bytes"


def librarian():
    """Sort every patch file's SysEx messages, check Roland checksums and
    write the good ones to one bank, in both formats."""
    print("== program: librarian")
    keep = []
    for p in sorted(glob.glob(data_path("patches/*.syx"))):
        name = os.path.basename(p)
        try:
            ms = mido.read_syx_file(p)
        except Exception as e:
            print(f"{name}: {err(e)}")
            continue
        print(f"{name}: {len(ms)} messages")
        for m in ms:
            line = describe(m)
            print(f"  {line}")
            if "bad" not in line and m not in keep:
                keep.append(m)
    print(f"keeping {len(keep)} messages")
    mido.write_syx_file(data_path("out/library.syx"), keep)
    mido.write_syx_file(data_path("out/library.txt.syx"), keep, plaintext=True)
    for p in ["out/library.syx", "out/library.txt.syx"]:
        b = open(data_path(p), "rb").read()
        back = mido.read_syx_file(data_path(p))
        print(f"{p}: {len(b)} bytes, reads back {len(back)} messages, same: {back == keep}")
    print(open(data_path("out/library.txt.syx")).read(), end="")


def compose():
    """Turn the text event logs into MIDI files at 100 bpm."""
    print("== program: compose")
    tempo = mido.bpm2tempo(100)
    tpb = 480
    for p in sorted(glob.glob(data_path("events/*.txt"))):
        stem = os.path.basename(p)[:-4]
        print(f"{stem}.txt:")
        msgs = []
        with open(p, encoding="utf-8") as f:
            lines = f.read().splitlines()
        try:
            for m, e in mido.parse_string_stream(lines):
                if e is not None:
                    print(f"  skipped: {e}")
                else:
                    msgs.append(m)
        except Exception as e:
            print(f"  stopped: {err(e)}")
            continue
        seconds = 0.0
        last = 0
        t = mido.MidiTrack()
        t.name = stem
        t.append(mido.MetaMessage("set_tempo", tempo=tempo))
        for m in msgs:
            seconds += m.time
            tick = mido.second2tick(seconds, tpb, tempo)
            t.append(m.copy(time=tick - last))
            last = tick
        f = mido.MidiFile(ticks_per_beat=tpb)
        f.tracks.append(t)
        out = f"out/{stem}.mid"
        f.save(data_path(out))
        g = mido.MidiFile(data_path(out))
        size = os.path.getsize(data_path(out))
        print(f"  {len(msgs)} messages, {seconds!r} seconds; saved {out}: {size} bytes, length {g.length:.3f}")
        g.print_tracks()


def thru():
    """Play the minuet into an echo port through a filter, as a MIDI thru
    box would, and close the port with autoreset on."""
    print("== program: thru")
    port = EchoPort("thru", autoreset=True)
    print(f"  {port!r}")
    f = mido.MidiFile(data_path("songs/minuet.mid"))
    sent = 0
    dropped = 0
    clock = 0.0
    for m in f:
        clock += m.time
        if m.is_meta:
            continue
        if m.type == "program_change" and m.channel == 1:
            dropped += 1
            continue
        if m.type == "note_on" and m.velocity > 0 and m.channel == 0:
            m = m.copy(velocity=int(m.velocity * 0.8))
        port.send(m)
        sent += 1
    print(f"  sent {sent}, dropped {dropped}, played {clock!r} seconds")
    kinds = {}
    first = []
    for m in port.iter_pending():
        kinds[m.type] = kinds.get(m.type, 0) + 1
        if len(first) < 5:
            first.append(m)
    for k in sorted(kinds):
        print(f"  received {kinds[k]} {k}")
    for m in first:
        print(f"    {m}")
    port.close()
    print(f"  {port!r}")
    after = list(port.iter_pending())
    print(f"  after close: {len(after)} pending, first {after[0]}, last {after[-1]}")
    try:
        port.receive()
    except Exception as e:
        print(f"  receive: {err(e)}")


def main():
    if os.path.isdir(data_path("out")):
        shutil.rmtree(data_path("out"))
    os.makedirs(data_path("out"))
    run_jobs()
    report()
    transpose()
    librarian()
    compose()
    thru()


main()
