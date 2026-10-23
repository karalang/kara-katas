#!/usr/bin/env python3
"""Writes data/jobs.tsv: the caption files a streaming service's caption desk
gets from its vendors (WebVTT, SubRip and YouTube SBV, in several encodings,
some of them broken) and the jobs the desk runs on them.
Run: python3 -s -P -B mk.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
F = {}


def vtt(name, text, enc="utf-8", bom=False, crlf=False):
    if crlf:
        text = text.replace("\n", "\r\n")
    data = text.encode(enc)
    if bom:
        data = {"utf-8": b"\xef\xbb\xbf", "utf-16-le": b"\xff\xfe", "utf-16-be": b"\xfe\xff",
                "utf-32-le": b"\xff\xfe\x00\x00", "utf-32-be": b"\x00\x00\xfe\xff"}[enc] + data
    F[name] = data


def raw(name, data):
    F[name] = data


EP01 = """WEBVTT - The Lighthouse, episode 1
Kind: captions
Language: en

NOTE Translated by the Lisbon desk.
Checked against the 2024 master.

NOTE Style for the narrator

STYLE
::cue(v[voice="Narrator"]) {
  color: lightblue;
}

NOTE second style has no comment
STYLE
::cue(.yellow) { color: yellow; }

intro
00:00:01.000 --> 00:00:04.500 align:start position:10%
<v Narrator>The lighthouse had stood for two hundred years.

00:00:05.000 --> 00:00:07.250
<v.loud Keeper>Who's there?
<c.yellow>Answer me!</c>

NOTE The next cue overlaps on purpose.

storm-1
00:00:06.900 --> 00:00:10.000
<i>Thunder</i> rolls <00:00:08.000>across the bay.

00:00:12.000 --> 00:00:15.000
<v Mara Silva>I brought the oil, like you asked.
<v Keeper>You're late.

NOTE end of reel one
"""

EP02 = """WEBVTT

1
00:00:00.500 --> 00:00:02.000
Morning, harbour master.

2
00:00:02.500 --> 00:00:05.000
 Two boats out, one back.\x20

3
00:00:05.500 --> 00:00:09.999
- Where's the third?
- Still out past the reef.
"""

EP03 = """WEBVTT

NOTE Japanese and French tracks merged by vendor

00:00:01.000 --> 00:00:03.000
<v Aiko>灯台はまだ光っている。

00:00:03.500 --> 00:00:06.000
<v Élodie>Le phare brille encore… 🌊

00:01:00.000 --> 00:01:02.000
Café, s’il vous plaît.
"""

QUIRKS = """WEBVTT
X-TIMESTAMP-MAP=MPEGTS:900000,LOCAL:00:00:00.000

00:00:01.000 --> 00:00:02.000

timing only above, so that block is dropped
00:00:03.000-->00:00:04.000
no spaces around the arrow

  00:00:05.000 --> 00:00:06.000
leading spaces before the timing

00:07.000 --> 00:08.500
no hours

1:00:09.000 --> 1:00:10.000
one-digit hours

STYLE
00:00:11.000 --> 00:00:12.000
a STYLE block with a timing is a cue

NOTE

NOTEworthy: no space after NOTE

00:00:13.000 --> 00:00:14.000
a --> b in the first payload line

cue with a second timing
00:00:15.000 --> 00:00:16.000
first payload
00:00:20.000 --> 00:00:21.000
second payload

00:00:17.000 --> 00:00:18.000
tags: a < b and c > d, <b>bold</b>, <i>open
close</i>, <c.
x>

00:00:19.000 --> 00:00:19.500
<v  >two spaces then the bracket

00:00:22.000 --> 00:00:23.000
<vNoSpace>voice without a space

00:00:24.000 --> 00:00:25.000
<v.first.loud\tEsme Ng>tab before the name
<v Second>only the first line counts

\t
00:00:26.000 --> 00:00:27.000
\tindented payload\x20\x20\x20

STYLE
::cue { color: red }
--> arrow inside a style

STYLE
::cue(b) {
  font-weight: bold }
NOTE trailing comment of the file
"""

LONG_CUES = [
    ("00:00:00.500", "00:00:03.000", "Previously on The Lighthouse."),
    ("00:00:03.500", "00:00:08.000", "<v Keeper>Keep the lamp lit."),
    ("00:00:08.500", "00:00:12.000", "It crosses the ten-second mark."),
    ("00:00:12.500", "00:00:19.900", "<i>Waves.</i>"),
    ("00:00:20.000", "00:00:21.000", "Exactly on a boundary."),
    ("00:00:25.000", "00:00:41.000", "A long shot of the sea,\nheld across two segments."),
    ("00:00:42.000", "00:00:44.000", "<v Mara Silva>Did you see that?"),
    ("00:00:50.000", "00:00:59.999", "Fifty-nine point nine nine nine."),
    ("00:01:00.000", "00:01:05.500", "The end of the cold open."),
]


def cue_text(cues, ids=False):
    out = ["WEBVTT", ""]
    for i, (s, e, t) in enumerate(cues):
        if ids:
            out.append(f"c{i + 1}")
        out.append(f"{s} --> {e}")
        out.extend(t.split("\n"))
        out.append("")
    return "\n".join(out)


SRT1 = """1
00:00:01,000 --> 00:00:03,500
<i>Previously...</i>

2
00:00:04,000 --> 00:00:06,000
The lamp went out
at <b>midnight</b>.

3
00:00:06,500 --> 00:00:08,000
Trailing spaces stay inside,\x20\x20\x20
but not at the very end.\x20\x20\x20
"""

SRT2 = """007
00:00:01,000 --> 00:00:02,000
Index with leading zeros.

A
00:00:02,000 --> 00:00:03,000
A letter index is skipped.

3
00:00:03,000 --> 00:00:04,000

4
00:00:04,000 --> 00:00:05,000

5
00:00:05.000 --> 00:00:06.000
Dots instead of commas are skipped.

6
 1:00:06,000  -->  1:00:07,250  X1:40 X2:600
Spaces and coordinates after the timing.

7
00:00:08,000 --> 00:00:09,000
Last one, no blank line after."""

SBV1 = """0:00:01.000,0:00:03.500
Welcome back to the harbour channel.

0:00:04.000,0:00:06.000
Today: knots
and splices

0:00:07.000,0:00:08.000
>> Two speakers, one block.
>> Yes.

note without a timing

0:00:09.000,0:00:10.500
Last one.
"""


def build():
    vtt("ep01.vtt", EP01)
    vtt("ep02.vtt", EP02, bom=True, crlf=True)
    vtt("ep03_le.vtt", EP03, enc="utf-16-le", bom=True)
    vtt("ep03_be.vtt", EP03, enc="utf-16-be", bom=True)
    vtt("ep03_32.vtt", EP03, enc="utf-32-le", bom=True)
    vtt("ep03_32be.vtt", EP03, enc="utf-32-be", bom=True)
    vtt("ep03_nobom.vtt", EP03, enc="utf-16-le")
    vtt("quirks.vtt", QUIRKS)
    vtt("long.vtt", cue_text(LONG_CUES, ids=True))
    vtt("edge.vtt", cue_text([("00:00:01.000", "00:00:09.000", "first"),
                              ("00:00:11.000", "00:00:20.250", "ends at 20.25 s")]))
    vtt("order.vtt", cue_text([("00:00:30.000", "00:00:32.000", "out of order"),
                               ("00:00:01.000", "00:00:05.000", "this one is last")]))
    vtt("zero.vtt", cue_text([("00:00:00.000", "00:00:00.900", "under a second")]))
    vtt("bad_hours.vtt", cue_text([("123:00:00.000", "123:00:01.000", "three-digit hours")]))
    vtt("bad_comma.vtt", cue_text([("00:00:01,000", "00:00:02,000", "commas from an SRT")]))
    vtt("bad_seconds.vtt", cue_text([("00:00:75.000", "00:00:76.000", "seventy-five seconds")]))
    vtt("bad_colon.vtt", cue_text([("00:00:00:500", "00:00:01:000", "a colon before the ms")]))
    vtt("noheader.vtt", "00:00:01.000 --> 00:00:02.000\nno WEBVTT line\n")
    vtt("lower.vtt", "webvtt\n\n00:00:01.000 --> 00:00:02.000\nlowercase header\n")
    vtt("header_only.vtt", "WEBVTT\n")
    raw("empty.vtt", b"")
    vtt("cr.vtt", "WEBVTT\r\r00:00:01.000 --> 00:00:02.000\rold Mac line ends\r"
                  "\n00:00:03.000 --> 00:00:04.000\nmixed\rend\n")
    vtt("seps.vtt", "WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nline\x0bsplit\x1cby splitlines"
                    "\x85too\n\n00:00:03.000 --> 00:00:04.000\nform\x0cfeed\n")
    raw("latin1.vtt", "WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nUn café, garçon.\n".encode("latin-1"))
    raw("badbyte.vtt", b"WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nok\n\n00:00:03.000 --> 00:00:04.000\nbad \xff byte\n")
    raw("badcont.vtt", b"WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nbad \xc3( continuation\n")
    raw("lonecont.vtt", b"\xef\xbb\xbfWEBVTT\n\n00:00:01.000 --> 00:00:02.000\n\x80 lone continuation\n")
    vtt("ep07.srt", SRT1, crlf=True)
    vtt("ep08.srt", SRT2, bom=True)
    vtt("bad_hours.srt", "1\n100:00:00,000 --> 100:00:01,000\nhundred hours\n")
    vtt("blank_start.srt", "\n1\n00:00:01,000 --> 00:00:02,000\nblank line first\n")
    vtt("no_text.srt", "1\n00:00:01,000 --> 00:00:02,000\n   \n")
    vtt("short.srt", "1\n00:00:01,000 --> 00:00:02,000\n")
    vtt("ep09.sbv", SBV1)
    vtt("ep09_bom.sbv", SBV1, bom=True, crlf=True)
    vtt("bad.sbv", "0:00:01.000,0:00:75.000\nseventy-five\n")
    vtt("comma.sbv", "0:00:01,000,0:00:02,000\ncommas everywhere\n")
    vtt("blank.sbv", "\n  \n")
    vtt("one_line.sbv", "0:00:01.000,0:00:02.000\n")
    vtt("title.sbv", "Harbour channel\n0:00:01.000,0:00:02.000\ntitle first\n")
    vtt("not_vtt.vtt", "<html><body>404 Not Found</body></html>\n")


def h(s):
    return "h:" + s.encode("utf-8").hex()


JOBS = []


def job(name, files, ops, dirs=()):
    fs = ",".join(f"{f}={F[f].hex()}" for f in files) or "-"
    JOBS.append("\t".join([name, fs, ",".join(dirs) or "-"] + ops))


def jobs():
    # Reading every container.
    job("ep01 clean", ["ep01.vtt"], ["read ep01.vtt", "show", "content", "write srt", "slice 00:00:05.000 00:00:12.000",
                                    "slice - 00:00:10.000", "slice 00:00:06.000 -", "slice - -"])
    job("ep02 utf-8 BOM and CRLF", ["ep02.vtt"], ["read ep02.vtt", "show", "content", "write srt"])
    for f in ("ep03_le.vtt", "ep03_be.vtt", "ep03_32.vtt", "ep03_32be.vtt"):
        job(f + " BOM", [f], [f"read {f}", "show", "content"])
    job("ep03 utf-16 without BOM", ["ep03_nobom.vtt"], ["read ep03_nobom.vtt", "read ep03_nobom.vtt utf-16-le", "show"])
    job("quirks", ["quirks.vtt"], ["read quirks.vtt", "show", "content", "write srt", "write sbv"])
    job("long", ["long.vtt"], ["read long.vtt", "show", "slice 00:00:20.000 00:00:45.000", "slice h: h:", "content"])
    for f in ("bad_hours.vtt", "bad_comma.vtt", "bad_seconds.vtt", "bad_colon.vtt", "noheader.vtt",
              "lower.vtt", "empty.vtt", "not_vtt.vtt"):
        job("broken " + f, [f], [f"read {f}", f"buffer {f} vtt", f"string {f}"])
    job("header only", ["header_only.vtt"], ["read header_only.vtt", "show", "content", "write srt"])
    job("missing file", [], ["read gone.vtt", "srt gone.srt", "sbv gone.sbv"])
    job("directory", ["ep01.vtt"], ["read out", "segment out out 10 0"], dirs=["out"])
    job("old Mac line ends", ["cr.vtt"], ["read cr.vtt", "show", "buffer cr.vtt vtt", "show", "string cr.vtt", "show"])
    job("other line separators", ["seps.vtt"], ["read seps.vtt", "show", "string seps.vtt", "show", "write srt"])
    job("latin-1", ["latin1.vtt"], ["read latin1.vtt", "read latin1.vtt latin-1", "show", "save -",
                                    "save - latin-1", "string latin1.vtt"])
    job("bad bytes", ["badbyte.vtt", "badcont.vtt", "lonecont.vtt"],
        ["read badbyte.vtt", "buffer badbyte.vtt vtt", "string badbyte.vtt", "read badcont.vtt",
         "buffer badcont.vtt vtt", "read lonecont.vtt", "buffer lonecont.vtt vtt", "read lonecont.vtt latin-1"])
    # Buffers.
    job("buffers", ["ep01.vtt", "ep02.vtt", "ep07.srt", "ep09.sbv"],
        ["buffer ep01.vtt vtt", "show", "buffer ep02.vtt vtt", "buffer ep07.srt srt", "show",
         "buffer ep09.sbv sbv", "show", "buffer ep01.vtt ass", "buffer ep01.vtt srt", "show",
         "buffer ep07.srt vtt", "string ep01.vtt", "show"])
    # SubRip.
    job("srt ep07", ["ep07.srt"], ["srt ep07.srt", "show", "content", "write srt", "savesrt -", "savesrt round.srt",
                                   "srt round.srt", "show"])
    job("srt ep08", ["ep08.srt"], ["srt ep08.srt", "show", "content", "write srt", "save ep08-converted"])
    for f in ("bad_hours.srt", "blank_start.srt", "no_text.srt", "short.srt", "ep01.vtt"):
        job("srt broken " + f, [f], [f"srt {f}", f"buffer {f} srt"])
    # SBV.
    job("sbv ep09", ["ep09.sbv", "ep09_bom.sbv"], ["sbv ep09.sbv", "show", "content", "write srt",
                                                  "sbv ep09_bom.sbv", "show", "buffer ep09_bom.sbv sbv"])
    for f in ("bad.sbv", "comma.sbv", "blank.sbv", "one_line.sbv", "title.sbv", "ep01.vtt", "empty.vtt"):
        job("sbv broken " + f, [f], [f"sbv {f}", f"buffer {f} sbv"])
    # Saving.
    job("save utf-16", ["ep03_le.vtt"], ["read ep03_le.vtt", "save -", "save out", "save out/", "save copy.txt",
                                         "save CAPS.VTT", "save out/sub/x.vtt", "save a utf-8", "save b UTF-8 1",
                                         "save c utf-8 0", "save d utf-16-be", "save e latin-1", "save f klingon",
                                         "save /work/out/abs", "show", "savesrt -", "savesrt out", "show"],
        dirs=["out"])
    job("save new", [], ["new", "save -", "save out", "savesrt -", "save made", "show", "content"], dirs=["out"])
    job("save names", ["ep02.vtt"], ["read ep02.vtt", "save x.y.z", "save .hidden", "save out/..", "save trailing.",
                                     "save ./dot", "show"], dirs=["out"])
    # Building captions by hand.
    job("build", [], [
        "new", f"hdr {h('Generated by the caption desk')}", f"hdr {h('two lines' + chr(10) + 'of header')}",
        f"style {h('::cue { color: lime }')}", f"stylecomment 0 {h('lime for the pilot')}",
        f"cap 00:00:01.000 00:00:02.500 {h('Hello' + chr(10) + 'there')} intro",
        f"cap - - {h('zero')} -",
        f"cap 00:01.000 1:00:02.000 {h('<v Ana>short forms')} -",
        f"cap 00:00:03.000 00:00:04.000 - {h('')}",
        f"cap bad 00:00:04.000 {h('never added')} -",
        f"capcomment 1 {h('a note about zero')}", f"capcomment 1 {h('and' + chr(10) + 'another')}",
        f"ftr {h('the end')}", "show", "content", "write srt",
        f"settext 0 {h('Replaced' + chr(13) + chr(10) + 'text' + chr(0x2028) + 'here')}",
        "setstart 1 00:00:00.250", "setend 1 99:59:59.999", "setstart 2 00:60:00.000", "setend 2 1:2:3",
        "get 0", "get -1", "get 9", "eq 0 0", "eq 0 1", "del 3", "del 7", "show", "content",
        "savesrt pilot", "srt pilot.srt", "show", "segment pilot.srt seg 10 0", "save pilot", "segment pilot.vtt seg 3600 1",
    ])
    job("timestamps", [], [
        "ts 00:00:00.000", "ts 1:2:3.456", "ts 01:02.345", "ts 99:59:59.999", "ts 00:60:00.000",
        "ts 1:02:03.4567", f"ts {h('abc')}", f"ts {h(' 00:00:01.000')}", "ts 100:00:00.000", "ts 0:0.000",
        "ts 7.000", f"ts {h('')}",
        "cmp 00:00:01.000 00:00:01.000", "cmp 00:00:01.000 00:00:02.000", "cmp 1:00:00.000 59:59.999",
        "cmp 00:00:10.000 00:00:09.999",
    ])
    # Segmenting for HLS.
    job("segment long", ["long.vtt"], ["segment long.vtt hls 10 900000"])
    job("segment long 7s", ["long.vtt"], ["segment long.vtt hls/a/b 7 0"])
    job("segment boundaries", ["edge.vtt", "order.vtt", "zero.vtt", "ep01.vtt", "header_only.vtt"],
        ["segment edge.vtt e 10 0", "segment order.vtt o 10 0", "segment zero.vtt z 10 0",
         "segment ep01.vtt ep 0 0", "segment ep01.vtt ep -5 0", "segment ep01.vtt ep 1 0",
         "segment header_only.vtt h 10 0", "segment ep01.vtt ep01.vtt 10 0"])
    # The command line.
    cli_jobs = [
        ["segment", "long.vtt", "-o", "out"],
        ["segment", "long.vtt", "--output", "out2", "--target-duration", "30", "--mpegts", "0"],
        ["segment", "long.vtt", "-oout3", "-d20", "-m=180000"],
        ["-d", "40", "segment", "long.vtt", "-o", "out4"],
        ["segment", "-o", "out5", "long.vtt", "-d", "60"],
        ["segment", "long.vtt", "--out", "out6", "--target", "45", "--mp", "7"],
        ["segment", "long.vtt", "--output=out7", "--target-duration=50"],
        ["segment", "-o", "out8", "-d", "35", "--", "long.vtt"],
        ["segment", "long.vtt", "-o", "x", "-o", "out9", "-d", " 25 "],
        ["segment", "long.vtt", "-o", "out10", "-d", "+1_5"],
        ["segment", "long.vtt"],
        ["split", "long.vtt", "-o", "out"],
        ["segment"],
        [],
        ["segment", "long.vtt", "-o", "out", "-d", "ten"],
        ["segment", "long.vtt", "-o", "out", "-d", "1e3"],
        ["segment", "long.vtt", "-o", "out", "-d"],
        ["segment", "long.vtt", "-o", "-x"],
        ["segment", "long.vtt", "-o", "out", "extra"],
        ["segment", "long.vtt", "-o", "out", "--bogus", "more"],
        ["segment", "long.vtt", "-o", "out", "-d", "-5"],
        ["segment", "long.vtt", "-o", "out", "-d", "0"],
        ["segment", "gone.vtt", "-o", "out"],
        ["segment", "gone.vtt"],
        ["-h"],
        ["segment", "long.vtt", "--help", "-d", "ten"],
        ["segment", "long.vtt", "-d", "ten", "--help"],
        ["split", "long.vtt", "-d", "ten"],
        ["segment", "long.vtt", "-o", "out", "-m", "-1", "-d", "70"],
    ]
    for i, argv in enumerate(cli_jobs):
        job(f"cli {i + 1}", ["long.vtt"], ["cli" + "".join(" " + h(x) for x in argv)])


def main():
    build()
    jobs()
    os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
    with open(os.path.join(HERE, "data", "jobs.tsv"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(JOBS) + "\n")
    print(len(JOBS), "jobs")


main()
