"""The oracle for mini_polib: runs data/jobs.txt against polib itself and
prints what the port must print. It wrote expected.out.

Run from this directory, after mk.py:
    python3 -I -B oracle.py > expected.out
It imports the vendored vendor/polib.py, or polib from POLIB_PATH."""
import os
import sys

sys.path.insert(
    0,
    os.environ.get(
        "POLIB_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor")
    ),
)
import polib  # noqa: E402

MASK32 = 4294967295


def fnv(b):
    h = 2166136261
    for x in b:
        h = ((h ^ x) * 16777619) & MASK32
    return h


def markers(s):
    return s.replace("⏎", "\n").replace("⇥", "\t")


def entry_line(e):
    parts = []
    if e.msgctxt is not None:
        parts.append(f"ctx={e.msgctxt!r}")
    parts.append(f"id={e.msgid!r}")
    if e.msgid_plural:
        parts.append(f"plural={e.msgid_plural!r}")
    if e.msgstr_plural:
        for k in sorted(e.msgstr_plural):
            parts.append(f"[{k}]={e.msgstr_plural[k]!r}")
    else:
        parts.append(f"str={e.msgstr!r}")
    if e.flags:
        parts.append(f"flags={e.flags!r}")
    if e.occurrences:
        parts.append(f"occ={len(e.occurrences)} first={e.occurrences[0]!r}")
    if e.tcomment:
        parts.append(f"tc={e.tcomment!r}")
    if e.comment:
        parts.append(f"gc={e.comment!r}")
    if e.previous_msgctxt is not None:
        parts.append(f"prev_ctx={e.previous_msgctxt!r}")
    if e.previous_msgid is not None:
        parts.append(f"prev_id={e.previous_msgid!r}")
    if e.previous_msgid_plural is not None:
        parts.append(f"prev_plural={e.previous_msgid_plural!r}")
    if e.obsolete:
        parts.append("obsolete")
    if getattr(e, "linenum", None) is not None:
        parts.append(f"line {e.linenum}")
    return " ".join(parts)


def stats(po):
    return (f"{po.percent_translated()}% translated; translated {len(po.translated_entries())}, "
            f"untranslated {len(po.untranslated_entries())}, fuzzy {len(po.fuzzy_entries())}, "
            f"obsolete {len(po.obsolete_entries())}; {len(po)} entries; header flags {po.metadata_is_fuzzy!r}, "
            f"encoding {po.encoding}")


def show_text(text):
    for line in text.split("\n"):
        print(f"  |{line}")


def read_bytes(path):
    with open(path, "rb") as f:
        return f.read()


def mo_header(b):
    import struct
    if len(b) < 28:
        return "short"
    vals = struct.unpack("<7I", b[:28])
    return " ".join(str(v) for v in vals)


def job(f):
    cmd = f[0]
    if cmd == "detect":
        print(polib.detect_encoding(f[1], f[1].endswith(".mo")))
    elif cmd == "stats":
        print(stats(polib.pofile(f[1])))
    elif cmd == "metadata":
        po = polib.pofile(f[1])
        for k, v in po.ordered_metadata():
            print(f"  {k}: {v!r}")
    elif cmd == "entries":
        po = polib.pofile(f[1])
        for e in po:
            print("  " + entry_line(e))
    elif cmd in ("find", "find-all"):
        po = polib.pofile(f[1])
        ctx = f[4] if len(f) > 4 else False
        e = po.find(f[3], by=f[2], include_obsolete_entries=cmd == "find-all", msgctxt=ctx)
        print(entry_line(e) if e is not None else "None")
    elif cmd == "contains":
        po = polib.pofile(f[1])
        e = polib.POEntry(msgid=f[2], msgctxt=f[3] if len(f) > 3 else None)
        print(e in po)
    elif cmd == "roundtrip":
        po = polib.pofile(f[1])
        text = read_bytes(f[1]).decode(po.encoding)
        if text.startswith("﻿"):
            text = text[1:]
        out = str(po)
        if out == text:
            print("same")
        else:
            a = out.split("\n")
            b = text.split("\n")
            k = 0
            while k < len(a) and k < len(b) and a[k] == b[k]:
                k += 1
            na = a[k] if k < len(a) else None
            nb = b[k] if k < len(b) else None
            print(f"differs: {len(a)} lines written, {len(b)} read; first at line {k + 1}: {na!r} for {nb!r}")
    elif cmd == "print":
        po = polib.pofile(f[1], wrapwidth=int(f[2]))
        show_text(str(po))
    elif cmd == "fuzzy":
        po = polib.pofile(f[1])
        e = po.find(f[2])
        e.fuzzy = f[3] == "on"
        print(f"flags {e.flags!r}; translated {e.translated()}; {po.percent_translated()}% translated")
        show_text(str(e))
    elif cmd == "merge":
        po = polib.pofile(f[1])
        pot = polib.pofile(f[2])
        po.merge(pot)
        po.save(f[3])
        print(stats(po))
        b = read_bytes(f[3])
        print(f"wrote {f[3]}: {len(b)} bytes, fnv {fnv(b):08x}")
        if f[1].endswith("pt_BR.po"):
            show_text(b.decode("utf-8"))
        for e in po:
            if e.obsolete:
                print("  obsolete " + entry_line(e))
    elif cmd == "sort":
        po = polib.pofile(f[1])
        for e in sorted(po):
            ctx = f"{e.msgctxt}|" if e.msgctxt else ""
            print(f"  {'~' if e.obsolete else ' '} {ctx}{e.msgid!r} {[o[0] + ':' + o[1] for o in sorted(e.occurrences)][:2]!r}")
    elif cmd == "compile":
        po = polib.pofile(f[1])
        po.save_as_mofile(f[2])
        b = read_bytes(f[2])
        print(f"wrote {f[2]}: {len(b)} bytes, fnv {fnv(b):08x}, header {mo_header(b)}")
        mo = polib.mofile(f[2])
        print(f"  read back: {len(mo)} entries, {len(mo.metadata)} metadata fields, encoding {mo.encoding}")
    elif cmd == "mo":
        mo = polib.mofile(f[1])
        print(f"magic {mo.magic_number:08x}, version {mo.version}, {len(mo)} entries, encoding {mo.encoding}")
        for k, v in mo.ordered_metadata():
            print(f"  {k}: {v!r}")
        for e in mo:
            print("  " + entry_line(e))
    elif cmd == "mo-to-po":
        mo = polib.mofile(f[1])
        mo.save_as_pofile(f[2])
        show_text(read_bytes(f[2]).decode("utf-8"))
    elif cmd == "mo-save":
        mo = polib.mofile(f[1])
        mo.save(f[2])
        b = read_bytes(f[2])
        print(f"wrote {f[2]}: {len(b)} bytes, fnv {fnv(b):08x}, header {mo_header(b)}")
        for e in polib.mofile(f[2]):
            print("  " + entry_line(e))
    elif cmd == "po":
        po = polib.pofile(f[1])
        print(f"{len(po)} entries; " + stats(po))
    elif cmd == "escape":
        print(repr(polib.escape(markers(f[1]))))
    elif cmd == "unescape":
        print(repr(polib.unescape(markers(f[1]))))
    elif cmd == "natural-sort":
        print(polib.natural_sort(f[1].split(" ")))


def main():
    with open("data/jobs.txt", encoding="utf-8") as fh:
        jobs = [ln for ln in fh.read().split("\n") if ln]
    for ln in jobs:
        f = ln.split("\t")
        print("== " + " | ".join(f))
        try:
            job(f)
        except Exception as e:  # noqa: BLE001
            print(f"{type(e).__name__}: {e}")


main()
