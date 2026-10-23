#!/usr/bin/env python3
"""Writes the firmware images into data/files/ and the job list into
data/jobs.tsv: one job per line, tab-separated, the first field naming the
kind. A "file" job carries one image's bytes as hex, so the Kara port can
build the same files in memory; the rest name images by file name.

  load <f>                      IntelHex(f): length, bounds, start address,
                                segments (or the reader's exception)
  todict <f>                    todict(), in the dict's insertion order
  dump <f> <width> <pad> <start> <end>
                                hex2dump: an optional ih[start:end] slice,
                                then dump(width, withpadding)
  hex <f> <byte_count> <start_rec> <eolstyle>
                                write_hex_file
  bin <f> <start> <end> <size> <pad>
                                tobinstr after setting .padding
  get <f> <addrs>               ih[addr] for each address
  gets <f> <addr> <n> | getsz <f> <addr> | find <f> <sub> <start> <end>
  seg <f> <min_gap>             segments(min_gap)
  edit <f|-> <ops>              a sequence of edits on a copy (or an empty
                                object), then its summary and its hex
  merge <a> <b> <overlap>       a.merge(b, overlap)
  h16 <f> <start> <end> <size> <addrs>
                                IntelHex16bit: bounds, words, ih[addr]
  record <kind> <args>          the Record builders
  info <files>                  hexinfo's summarize_yaml
  diff <a> <b>                  hexdiff (diff_dumps)
  hex2bin <f> <start> <end> <size> <pad> | bin2hex <f> <offset>
  hexmerge <args>               hexmerge.py's main(), arguments split on \\x1f
"-" means "not given".
Run: python3 -I -B mk.py"""
import os
import random
import sys

sys.path.insert(0, "vendor")
from intelhex import Record  # noqa: E402

R = random.Random(310)
files = {}
jobs = []


def add(*f):
    jobs.append("\t".join(str(x) for x in f))


def records(data, start, per_line=16):
    """Data records for a run of bytes at a 16-bit offset."""
    out = []
    for i in range(0, len(data), per_line):
        out.append(Record.data(start + i, data[i:i + per_line]))
    return out


def text(lines, eol="\n"):
    return (eol.join(lines) + eol).encode("ascii")


def rbytes(n):
    return [R.randrange(256) for _ in range(n)]


# A small AVR program at 0x0000, 16 bytes a line
blinky = rbytes(600)
files["blinky.hex"] = text(records(blinky, 0) + [Record.eof()])

# The same program with three bytes patched, for hexdiff and merge
patched = list(blinky)
patched[0x40] = 0x00
patched[0x41] = 0x00
patched[0x150] ^= 0xFF
files["blinky_v2.hex"] = text(records(patched, 0) + [Record.eof()])

# ARM firmware at 0x08000000 with a vector table, a gap and a config page,
# 32 bytes a line, and a start linear address
arm = [Record.extended_linear_address(0x0800)]
arm += records(rbytes(400), 0x0000, 32)
arm += records(rbytes(100), 0x1000, 32)
arm += [Record.extended_linear_address(0x0801)]
arm += records([0x55, 0xAA] * 16, 0xF800, 32)
arm += [Record.start_linear_address(0x080001C1), Record.eof()]
files["stm32.hex"] = text(arm)

# An 8086 image: extended segment addresses and a CS:IP start record
dos = [Record.extended_segment_address(0x1000)]
dos += records(rbytes(64), 0x0000)
dos += [Record.extended_segment_address(0xF000)]
dos += records(rbytes(16), 0xFFF0)
dos += [Record.start_segment_address(0x1000, 0x0100), Record.eof()]
files["dos.hex"] = text(dos)

# CRLF line ends, lower-case digits, blank lines, and data after the EOF
# record, which the reader never sees
crlf = [r.lower() for r in records(rbytes(40), 0x0100)]
crlf.insert(1, "")
crlf += [Record.eof(), Record.data(0x0200, [1, 2, 3])]
files["crlf.hex"] = text(crlf, "\r\n")

# Old Mac line ends: universal newlines split on a bare CR
files["mac.hex"] = text(records(rbytes(24), 0x0040) + [Record.eof()], "\r")

# No EOF record, no final newline
files["noeof.hex"] = ("\n".join(records(rbytes(20), 0x0000))).encode("ascii")

files["empty.hex"] = b""
files["eofonly.hex"] = text([Record.eof()])

# Sparse EEPROM contents with one- and two-byte holes, and a record that
# runs across the 64K boundary (the reader does not wrap it)
ee = []
for base in range(0x0000, 0x0100, 0x10):
    data = rbytes(R.randint(3, 16))
    ee += records(data, base + R.randint(0, 16 - len(data)))
ee += records(rbytes(16), 0xFFF8)
ee += [Record.extended_linear_address(0x0002)]
ee += records([0x11, 0x22, 0x33], 0x0010)
ee += [Record.eof()]
files["eeprom.hex"] = text(ee)

# A Microchip PIC image of 16-bit words, with one odd byte left alone
pic = records(rbytes(32), 0x0000) + records([0x34], 0x0041) + [Record.eof()]
files["pic16.hex"] = text(pic)

# Two images that overlap at 0x0010..0x001F, and one with its own start address
files["part_a.hex"] = text(records(rbytes(32), 0x0000) +
                           [Record.start_linear_address(0x100), Record.eof()])
files["part_b.hex"] = text(records(rbytes(32), 0x0010) +
                           [Record.start_linear_address(0x200), Record.eof()])
files["part_c.hex"] = text(records(rbytes(16), 0x0100) + [Record.eof()])

# Text in flash, for gets / getsz / find
msg = list(b"Hello, firmware!\x00v2.3.0\x00") + list(b"OK")
files["strings.hex"] = text(records(msg, 0x0200) + [Record.eof()])


def rec(*b):
    s = (-sum(b)) & 0xFF
    return ":" + bytes(list(b) + [s]).hex().upper()


good = Record.data(0x0000, [1, 2, 3, 4])
BAD = {
    "bad_colon.hex": ["0400000001020304F2"],
    "bad_odd.hex": [good + "0"],
    "bad_nonhex.hex": [good[:5] + "GG" + good[7:]],
    "bad_short.hex": [":00000001"],
    "bad_len.hex": [rec(5, 0, 0, 0, 1, 2, 3, 4)],
    "bad_type.hex": [rec(0, 0, 0, 6)],
    "bad_sum.hex": [good[:-2] + "00"],
    "bad_overlap.hex": [good, Record.data(0x0002, [9, 9])],
    "bad_eof.hex": [rec(1, 0, 0, 1, 0)],
    "bad_ext_seg.hex": [rec(2, 0, 4, 2, 0x10, 0)],
    "bad_ext_lin.hex": [rec(3, 0, 0, 4, 0, 1, 2)],
    "bad_start_seg.hex": [rec(2, 0, 0, 3, 1, 2)],
    "bad_start_lin.hex": [rec(4, 0, 1, 5, 0, 0, 1, 0)],
    "bad_dup_start.hex": [Record.start_linear_address(1), Record.start_segment_address(1, 2)],
    "bad_space.hex": [" " + good],
    "bad_trailing.hex": [good + " "],
    "bad_line7.hex": records(rbytes(80), 0) + ["", ":0"],
}
for name, lines in BAD.items():
    files[name] = text(lines + [Record.eof()])

# Binary images for bin2hex / loadbin
files["app.bin"] = bytes(rbytes(300))
files["small.bin"] = bytes([0x00, 0x01, 0xFF, 0x7F, 0x20, 0x41])

for name in sorted(files):
    add("file", name, files[name].hex())

HEXES = ["blinky.hex", "stm32.hex", "dos.hex", "crlf.hex", "mac.hex", "noeof.hex", "empty.hex",
         "eofonly.hex", "eeprom.hex", "pic16.hex", "part_a.hex", "part_b.hex", "part_c.hex",
         "strings.hex"] + sorted(BAD)
for f in HEXES:
    add("load", f)

for f in ["dos.hex", "crlf.hex", "mac.hex", "eofonly.hex", "part_c.hex", "strings.hex"]:
    add("todict", f)

for f, w, p, s, e in [("blinky.hex", 16, 0, "-", "-"), ("blinky.hex", 8, 0, "0x20", "0x60"),
                      ("stm32.hex", 32, 0, "0x08000180", "0x08001010"), ("dos.hex", 16, 1, "0x10030", "0x10050"),
                      ("eeprom.hex", 16, 0, "-", "0x100"), ("eeprom.hex", 16, 1, "0x0", "0x40"),
                      ("eeprom.hex", 7, 0, "0xFFF0", "0x10010"), ("strings.hex", 16, 0, "-", "-"),
                      ("strings.hex", 5, 1, "-", "0x210"), ("crlf.hex", 3, 0, "-", "-"),
                      ("empty.hex", 16, 0, "-", "-"), ("pic16.hex", 1, 0, "0x3C", "-"),
                      ("blinky.hex", 0, 0, "-", "-")]:
    add("dump", f, w, p, s, e)

for f, bc, sa, eol in [("blinky.hex", 16, 1, "native"), ("blinky.hex", 32, 1, "native"),
                       ("blinky.hex", 255, 1, "native"), ("stm32.hex", 16, 1, "native"),
                       ("stm32.hex", 16, 0, "CRLF"), ("dos.hex", 16, 1, "CRLF"),
                       ("dos.hex", 7, 1, "native"), ("eeprom.hex", 16, 1, "native"),
                       ("eeprom.hex", 1, 1, "native"), ("crlf.hex", 16, 1, "native"),
                       ("empty.hex", 16, 1, "native"), ("mac.hex", 0, 1, "native"),
                       ("mac.hex", 256, 1, "native"), ("mac.hex", 16, 1, "LF"),
                       ("part_a.hex", 64, 1, "native")]:
    add("hex", f, bc, sa, eol)

for f, s, e, n, p in [("blinky.hex", "-", "-", "-", "-"), ("blinky.hex", "0x10", "0x1F", "-", "-"),
                      ("blinky.hex", "0x250", "0x260", "-", "0"), ("eeprom.hex", "0", "0x3F", "-", "0"),
                      ("eeprom.hex", "-", "0x20", "-", "-"), ("eeprom.hex", "0x30", "-", "0x10", "-"),
                      ("eeprom.hex", "-", "0x20", "0x10", "0xAA"), ("eeprom.hex", "-", "0x8", "0x10", "-"),
                      ("eeprom.hex", "0x10", "0x20", "0x10", "-"), ("blinky.hex", "-", "-", "0", "-"),
                      ("empty.hex", "-", "-", "-", "-"), ("empty.hex", "0", "7", "-", "-"),
                      ("empty.hex", "-", "-", "4", "-"), ("dos.hex", "0x100F0", "0x10010", "-", "-"),
                      ("strings.hex", "0x230", "0x200", "-", "-"), ("blinky.hex", "-", "-", "8", "-")]:
    add("bin", f, s, e, n, p)

add("get", "blinky.hex", "0,1,2,0x100,0x257,0x258,1000")
add("get", "eeprom.hex", "0x0,0xF,0x10007,0x10008,0x20010,-1")
add("get", "stm32.hex", "0x08000000,0x080001C1,0x0800F800")

for f, a, n in [("strings.hex", "0x200", "5"), ("strings.hex", "0x207", "8"),
                ("strings.hex", "0x200", "0"), ("strings.hex", "0x210", "40"),
                ("blinky.hex", "0", "16"), ("eeprom.hex", "0", "64")]:
    add("gets", f, a, n)
for f, a in [("strings.hex", "0x200"), ("strings.hex", "0x211"), ("strings.hex", "0x218"),
             ("strings.hex", "0x210"), ("blinky.hex", "0")]:
    add("getsz", f, a)
for f, sub, s, e in [("strings.hex", b"firm".hex(), "-", "-"), ("strings.hex", b"v2".hex(), "-", "-"),
                     ("strings.hex", b"OK".hex(), "0x200", "0x21A"),
                     ("strings.hex", b"OK".hex(), "0x200", "-"),
                     ("strings.hex", b"zz".hex(), "-", "-"), ("strings.hex", "", "-", "-"),
                     ("strings.hex", b"!\x00v".hex(), "0x20F", "-"),
                     ("eeprom.hex", "1122", "-", "-"), ("empty.hex", "00", "-", "-")]:
    add("find", f, sub or "-", s, e)

for f, g in [("eeprom.hex", 1), ("eeprom.hex", 2), ("eeprom.hex", 3), ("eeprom.hex", 100),
             ("stm32.hex", 1), ("stm32.hex", 0x10000), ("dos.hex", 1), ("empty.hex", 1),
             ("pic16.hex", 1)]:
    add("seg", f, g)

EDITS = [
    ("-", "set:0:1;set:1:2;set:5:0xFF;set:3:4"),
    ("-", "set:-1:5"),
    ("-", "setsl:0x10:0x14:-:1,2,3,4;setsl:-:0x30:-:9,8;setsl:0x40:-:2:7,7,7"),
    ("-", "setsl:0:4:-:1,2"),
    ("-", "setsl:-:-:-:1"),
    ("-", "setsl:-:2:-:1,2,3"),
    ("blinky.hex", "delsl:0x10:0x20:-;del:0x100;delsl:-:4:-;delsl:0x200:-:2"),
    ("blinky.hex", "del:0x1000"),
    ("blinky.hex", "del:-5"),
    ("-", "puts:0x100:" + b"boot".hex() + ";putsz:0x110:" + b"name".hex() + ";pad:0"),
    ("-", "dict:0=1,1=2,7=0x80;start:EIP=0x1234"),
    ("-", "dict:0=1,-1=2"),
    ("-", "dict:16=1;start:CS=0x10,IP=0x20"),
    ("-", "dict:16=1;start:CS=0x10"),
    ("-", "dict:16=1;start:CS=1,IP=2,EIP=3"),
    ("-", "set:0:300"),
    ("-", "set:0x100000000:1"),
    ("-", "set:0x1000000:1;set:0x1000001:2"),
    ("stm32.hex", "pad:0x1234;bin:0x08000180:0x08000200"),
    ("strings.hex", "set:0x205:0x0A;set:0x206:0x7F;pad:0x2E;dumppad"),
    ("-", "frombin:small.bin:0x10"),
    ("dos.hex", "copy"),
]
for f, ops in EDITS:
    add("edit", f, ops)

for a, b, ov in [("part_a.hex", "part_b.hex", "error"), ("part_a.hex", "part_b.hex", "ignore"),
                 ("part_a.hex", "part_b.hex", "replace"), ("part_a.hex", "part_c.hex", "error"),
                 ("part_c.hex", "part_a.hex", "error"), ("part_b.hex", "part_a.hex", "replace"),
                 ("blinky.hex", "blinky_v2.hex", "error"), ("part_a.hex", "part_a.hex", "keep"),
                 ("part_a.hex", "self", "error"), ("dos.hex", "stm32.hex", "error"),
                 ("dos.hex", "stm32.hex", "replace")]:
    add("merge", a, b, ov)

for f, s, e, n, addrs in [("pic16.hex", "-", "-", "-", "0,1,15,16,0x20,0x21"),
                          ("pic16.hex", "0", "7", "-", "-"), ("pic16.hex", "-", "-", "4", "-"),
                          ("pic16.hex", "0x1E", "0x22", "-", "-"), ("empty.hex", "-", "-", "-", "0"),
                          ("blinky.hex", "0x10", "-", "8", "0x12C,0x12B")]:
    add("h16", f, s, e, n, addrs)

for args in [("data", "0", "1,2,3"), ("data", "0xFFFF", "0"), ("data", "0x1234", ",".join(["255"] * 16)),
             ("data", "65536", "1"), ("data", "0", ""), ("eof",), ("esa", "0x1234"),
             ("ssa", "0x1234", "0x5678"), ("ela", "0xFFFF"), ("sla", "0x12345678"),
             ("sla", "0xFFFFFFFF")]:
    add("record", *args)

add("info", "blinky.hex,stm32.hex,dos.hex,eeprom.hex,empty.hex")
add("info", "part_a.hex,bad_sum.hex")
add("info", "noeof.hex")

for a, b in [("blinky.hex", "blinky_v2.hex"), ("blinky.hex", "blinky.hex"), ("part_a.hex", "part_b.hex"),
             ("empty.hex", "part_c.hex"), ("part_a.hex", "part_c.hex")]:
    add("diff", a, b)

for f, s, e, n, p in [("blinky.hex", "-", "-", "-", "-"), ("eeprom.hex", "-", "0x3F", "-", "0"),
                      ("eeprom.hex", "-", "0x20", "0x40", "-"), ("eeprom.hex", "-", "0x40", "0x10", "-"),
                      ("eeprom.hex", "0x10", "-", "0x10", "0x5A"), ("bad_sum.hex", "-", "-", "-", "-"),
                      ("bad_overlap.hex", "-", "-", "-", "-"), ("empty.hex", "-", "-", "-", "-"),
                      ("strings.hex", "-", "-", "0", "-")]:
    add("hex2bin", f, s, e, n, p)
for f, off in [("app.bin", 0), ("small.bin", 0x8000), ("small.bin", 0xFFFE), ("empty.hex", 0)]:
    add("bin2hex", f, off)

HM = [
    ["part_a.hex", "part_c.hex"],
    ["part_a.hex", "part_b.hex"],
    ["--overlap=ignore", "part_a.hex", "part_b.hex"],
    ["part_a.hex", "--overlap=replace", "part_b.hex"],
    ["--overlap", "replace", "part_b.hex", "part_a.hex", "part_c.hex"],
    ["--no-start-addr", "part_a.hex", "part_c.hex"],
    ["-r", "8:1F", "part_a.hex", "part_c.hex"],
    ["--range=100:", "part_a.hex", "part_c.hex"],
    ["--ra=:7", "part_a.hex"],
    ["part_a.hex:10:1F", "part_c.hex::103"],
    ["part_a.hex:0:7", "part_b.hex:18:"],
    ["part_a.hex:0x0:0x0f", "part_c.hex: 100 :"],
    ["part_a.hex:1", "part_c.hex"],
    ["part_a.hex:xx:", "part_c.hex"],
    ["-r", "zz", "part_a.hex"],
    ["-r", "10", "part_a.hex"],
    ["--overlap=merge", "part_a.hex"],
    ["--o=ignore", "part_a.hex", "part_b.hex"],
    ["--no", "part_a.hex"],
    ["--no-start-addr=1", "part_a.hex"],
    ["--overlap"],
    ["-x", "part_a.hex"],
    ["-r"],
    [],
    ["-v"],
    ["--version", "nope.hex"],
    ["--", "-r", "part_a.hex"],
    ["stm32.hex", "dos.hex"],
    ["-r801F808:801F81F", "stm32.hex"],
    ["blinky.hex:250:"],
]
for args in HM:
    add("hexmerge", "\x1f".join(args) if args else "-")

os.makedirs("data/files", exist_ok=True)
for name, content in files.items():
    with open(os.path.join("data/files", name), "wb") as fh:
        fh.write(content)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    fh.write("\n".join(jobs) + "\n")
print(len(jobs), "jobs,", len(files), "files")
