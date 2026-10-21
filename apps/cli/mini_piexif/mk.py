# Writes data/: the images the jobs and programs read (data/img/ for the
# jobs, data/photos/ for the programs), a GPS track (data/track.csv),
# camera clock corrections (data/clock.txt) and the jobs
# (data/jobs.jsonl).
#
# Most Exif blocks come from a small TIFF writer here rather than from
# piexif, so that they can be little-endian, carry tags piexif does not
# know, store a tag with a different type from piexif's table, or be cut
# short. A few come from piexif.dump itself.
#
# A job is a list of steps over named variables:
#   ["load", var, file]            piexif.load(filename)
#   ["loadb", var, file]           piexif.load(the file's bytes)
#   ["loadn", var, file]           piexif.load(filename, key_is_name=True)
#   ["loadx", var, {"b": text}]    piexif.load(bytes given here)
#   ["dict", var, spec]            an exif dict written out (see below)
#   ["bytes", var, spec]           bytes written out
#   ["dump", var, dict_var]        piexif.dump(...)
#   ["insert", exif_var, file, out]
#   ["remove", file, out]
#   ["transplant", src, file, out]
#   ["show", var]                  print a variable
#   ["file", path]                 print a file's bytes
#   ["set"/"del", dict_var, ifd, tag, value]
#   ["ucload", value], ["ucdump", text, encoding]
# In a spec, a text is a str, {"b": text} bytes (the text's code points,
# then {"then": t, "times": n} t repeated n times),
# a list a tuple, {"f": x} a float, {"file": path} a file's bytes and
# {"v": name} a variable. A job stops at its first error.
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import piexif  # noqa: E402

DATA = os.path.join(HERE, "data")

# --- JPEG and TIFF builders --------------------------------------------


def seg(marker, payload):
    return bytes([0xFF, marker]) + struct.pack(">H", len(payload) + 2) + payload


APP0 = seg(0xE0, b"JFIF\x00\x01\x01\x00\x00\x48\x00\x48\x00\x00")
DQT = seg(0xDB, b"\x00" + bytes(range(1, 65)))
SOF0 = seg(0xC0, b"\x08\x00\x10\x00\x10\x03\x01\x22\x00\x02\x11\x01\x03\x11\x01")
DHT = seg(0xC4, b"\x00" + b"\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00"
          + bytes(range(12)))
SCAN = b"\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00" + bytes(
    [(i * 37 + 11) % 256 for i in range(48)]).replace(b"\xff", b"\xfe") + b"\xff\xd9"


def jpeg(*segs, scan=SCAN):
    return b"\xff\xd8" + b"".join(segs) + scan


def thumb(n):
    """A small JPEG to stand in for a thumbnail, with its own APP0."""
    body = bytes([(i * n + 3) % 251 for i in range(20 + n)]).replace(b"\xff", b"\xfe")
    return jpeg(APP0, DQT, scan=b"\xff\xda\x00\x08\x01\x01\x00\x00\x3f\x00" + body + b"\xff\xd9")


TYPE_SIZE = {1: 1, 2: 1, 3: 2, 4: 4, 5: 8, 6: 1, 7: 1, 8: 2, 9: 4, 10: 8, 11: 4, 12: 8}
FMT = {1: "B", 3: "H", 4: "L", 6: "b", 8: "h", 9: "l", 11: "f", 12: "d"}


def enc(e, typ, vals):
    if typ in (2, 7, 13):
        return vals
    if typ in (5, 10):
        f = "L" if typ == 5 else "l"
        return b"".join(struct.pack(e + f + f, n, d) for n, d in vals)
    return b"".join(struct.pack(e + FMT[typ], v) for v in vals)


def count_of(typ, vals):
    if typ in (2, 7):
        return len(vals)
    return len(vals)


def tiff(e, ifd0, exif=None, gps=None, interop=None, first=None, thumbnail=None, count_fix=None):
    """A TIFF block: e is "<" or ">"; each IFD is a list of (tag, type,
    values), values being bytes for ASCII/UNDEFINED and a list
    otherwise. The pointer tags are added here. count_fix maps a tag to
    the count to write instead of the real one."""
    count_fix = count_fix or {}
    ifd0 = list(ifd0)
    exif = list(exif) if exif is not None else None
    if exif is not None:
        ifd0.append((34665, 4, [0]))
    if gps is not None:
        ifd0.append((34853, 4, [0]))
    if interop is not None:
        exif.append((40965, 4, [0]))
    first = list(first) if first is not None else None
    if first is not None and thumbnail is not None:
        first.append((513, 4, [0]))
        first.append((514, 4, [len(thumbnail)]))

    order = [("0th", ifd0)]
    if exif is not None:
        order.append(("Exif", exif))
    if gps is not None:
        order.append(("GPS", gps))
    if interop is not None:
        order.append(("Interop", interop))
    if first is not None:
        order.append(("1st", first))

    # Lay out each IFD followed by its out-of-line values.
    def size(entries, has_next):
        n = 2 + 12 * len(entries) + (4 if has_next else 0)
        for tag, typ, vals in entries:
            b = len(enc(e, typ, vals))
            if b > 4:
                n += b + (b % 2)
        return n

    pos = 8
    offsets = {}
    for name, entries in order:
        offsets[name] = pos
        pos += size(entries, name in ("0th", "1st"))
    thumb_at = pos

    def fixup(entries):
        out = []
        for tag, typ, vals in entries:
            if tag == 34665:
                vals = [offsets["Exif"]]
            elif tag == 34853:
                vals = [offsets["GPS"]]
            elif tag == 40965:
                vals = [offsets["Interop"]]
            elif tag == 513:
                vals = [thumb_at]
            out.append((tag, typ, vals))
        return sorted(out, key=lambda t: t[0])

    blob = (b"II*\x00" if e == "<" else b"MM\x00*") + struct.pack(e + "L", 8)
    for name, entries in order:
        entries = fixup(entries)
        start = offsets[name]
        has_next = name in ("0th", "1st")
        extra_at = start + 2 + 12 * len(entries) + (4 if has_next else 0)
        head = struct.pack(e + "H", len(entries))
        extra = b""
        for tag, typ, vals in entries:
            b = enc(e, typ, vals)
            cnt = count_fix.get(tag, count_of(typ, vals))
            if len(b) > 4:
                head += struct.pack(e + "HHLL", tag, typ, cnt, extra_at + len(extra))
                extra += b + b"\x00" * (len(b) % 2)
            else:
                head += struct.pack(e + "HHL", tag, typ, cnt) + b + b"\x00" * (4 - len(b))
        if has_next:
            nxt = offsets["1st"] if name == "0th" and "1st" in offsets else 0
            head += struct.pack(e + "L", nxt)
        blob += head + extra
    if thumbnail is not None:
        blob += thumbnail
    return blob


def app1(tiff_bytes):
    return seg(0xE1, b"Exif\x00\x00" + tiff_bytes)


XMP = seg(0xE1, b"http://ns.adobe.com/xap/1.0/\x00<x:xmpmeta xmlns:x=\"adobe:ns:meta/\">"
          b"<rdf:RDF/></x:xmpmeta>")


def A(s):
    return s.encode("latin-1") + b"\x00"


def R(*pairs):
    return list(pairs)


# --- the job images ----------------------------------------------------

IMG = {}

# Little-endian, every type, unknown tags, a tag piexif types otherwise.
le_ifd0 = [
    (271, 2, A("NIKON CORPORATION")), (272, 2, A("NIKON Z 6_2")), (274, 3, [6]),
    (282, 5, R((300, 1))), (283, 5, R((300, 1))), (296, 3, [2]), (305, 2, A("Ver.01.10")),
    (306, 2, A("2026:05:02 17:44:09")), (318, 5, R((313, 1000), (329, 1000))),
    (258, 3, [8, 8, 8]), (336, 1, [1, 2, 3, 4, 5, 6]), (60608, 6, [-3, 4, -128, 127, 0]),
    (60609, 8, [-2, 30000]), (60610, 12, [0.5, -2.25]), (50940, 11, [0.25]),
    (50938, 11, [1.5, 0.1, -3.0]), (50715, 10, R((-1, 3))), (50721, 10, R((7, -2), (-5, 4))),
    (40001, 3, [77]), (531, 3, [2]), (700, 1, [60, 120, 47, 62]),
    (11, 2, b"no-nul"), (269, 2, A("abc")), (315, 2, A("")),
]
le_exif = [
    (33434, 5, R((1, 200))), (33437, 5, R((28, 10))), (34855, 3, [800]),
    (36864, 7, b"0232"), (36867, 2, A("2026:05:02 17:44:09")), (36868, 2, A("2026:05:02 17:44:09")),
    (37377, 10, R((7643856, 1000000))), (37380, 10, R((-1, 3))), (37386, 5, R((50, 1))),
    (37500, 7, b"Nikon\x00\x02\x11\x00\x00MM\x00*\x00\x00\x00\x08"), (37510, 7, b"ASCII\x00\x00\x00 shot at dusk"),
    (40960, 7, b"0100"), (41986, 3, [0]), (42033, 2, A("6012345")), (42036, 2, A("NIKKOR Z 24-70mm f/4 S")),
    (59932, 7, b"\x1c\xea\x00\x00\x00\x08"),
]
le_gps = [
    (0, 1, [2, 3, 0, 0]), (1, 2, A("S")), (2, 5, R((33, 1), (51, 1), (3192, 100))), (3, 2, A("E")),
    (4, 5, R((151, 1), (12, 1), (3984, 100))), (5, 1, [0]), (6, 5, R((5800, 100),)),
    (7, 5, R((7, 1), (44, 1), (9, 1))), (29, 2, A("2026:05:02")), (27, 7, b"ASCII\x00\x00\x00GPS"),
]
le_interop = [(1, 2, A("R98")), (2, 7, b"0100")]
le_first = [(259, 3, [6]), (282, 5, R((72, 1))), (283, 5, R((72, 1))), (296, 3, [2])]
IMG["img/nikon_le.jpg"] = jpeg(app1(tiff("<", le_ifd0, le_exif, le_gps, le_interop, le_first, thumb(9))),
                               DQT, SOF0, DHT)

# The same tags big-endian, written by piexif.dump.
be_dict = {
    "0th": {271: b"Canon", 272: b"Canon EOS R6", 274: 1, 282: (72, 1), 283: (72, 1), 296: 2,
            305: b"Firmware Version 1.8.1", 306: b"2026:07:14 09:12:30", 315: b"Ana Ruiz"},
    "Exif": {33434: (1, 250), 33437: (40, 10), 34855: 200, 36864: b"0231", 36867: b"2026:07:14 09:12:30",
             36868: b"2026:07:14 09:12:30", 37386: (85, 1), 41987: 0, 42035: b"Canon",
             42036: b"RF85mm F2 MACRO IS STM", 42033: b"083021000123"},
    "GPS": {0: (2, 2, 0, 0), 1: b"N", 2: ((40, 1), (26, 1), (4659, 100)), 3: b"W", 4: ((79, 1), (58, 1), (5640, 100)),
            5: 0, 6: (2310, 10)},
    "Interop": {1: b"R98"},
    "1st": {259: 6, 282: (72, 1), 283: (72, 1), 296: 2},
    "thumbnail": thumb(5),
}
be_exif = piexif.dump(be_dict)
IMG["img/canon_be.jpg"] = jpeg(APP0, b"\xff\xe1" + struct.pack(">H", len(be_exif) + 2) + be_exif, DQT, SOF0)

IMG["img/plain.jpg"] = jpeg(APP0, DQT, SOF0, DHT)
IMG["img/no_app0.jpg"] = jpeg(DQT, SOF0)
IMG["img/xmp_first.jpg"] = jpeg(XMP, app1(tiff(">", [(305, 2, A("GIMP 2.10.38"))], [(36867, 2, A("2025:12:31 23:59:59"))])),
                                DQT, SOF0)
IMG["img/exif_only_0th.jpg"] = jpeg(APP0, app1(tiff(">", [(271, 2, A("Apple")), (272, 2, A("iPhone 15 Pro"))])), DQT)
IMG["img/two_exif.jpg"] = jpeg(APP0, app1(tiff(">", [(271, 2, A("First"))])),
                               app1(tiff(">", [(271, 2, A("Second"))])), DQT)
IMG["img/app1_not_exif.jpg"] = jpeg(APP0, seg(0xE1, b"Exiv\x00\x00MM\x00*"), DQT)
IMG["img/app2_icc.jpg"] = jpeg(APP0, seg(0xE2, b"ICC_PROFILE\x00\x01\x01" + bytes(20)),
                               app1(tiff("<", [(274, 3, [3])])), DQT)
# Counts that point past the data, or a type piexif does not know.
IMG["img/short_rational.jpg"] = jpeg(app1(tiff(">", [(282, 5, R((72, 1)))], count_fix={282: 3})), DQT)
IMG["img/bad_type.jpg"] = jpeg(app1(tiff("<", [(271, 13, b"zzzz")])), DQT)
IMG["img/zero_count.jpg"] = jpeg(app1(tiff("<", [(271, 2, b""), (258, 3, [])])), DQT)
IMG["img/ascii_count_1.jpg"] = jpeg(app1(tiff(">", [(271, 2, b"\x00")])), DQT)
# Cut short inside the Exif block, and segments that run off the end.
full = app1(tiff(">", [(271, 2, A("Truncated Co")), (272, 2, A("T-1000"))], [(36867, 2, A("2026:01:01 00:00:00"))]))
IMG["img/cut_exif.jpg"] = jpeg(full[:40])
IMG["img/cut_ifd.jpg"] = b"\xff\xd8" + full[:30]
IMG["img/no_sos.jpg"] = b"\xff\xd8" + APP0 + DQT
IMG["img/not_jpeg.jpg"] = b"GIF89a\x01\x00\x01\x00\x00\x00\x00;"
IMG["img/tiff_le.tif"] = tiff("<", [(256, 4, [16]), (257, 4, [16]), (271, 2, A("Scanner Inc")),
                                    (259, 3, [1])], [(41728, 7, b"\x03")]) + bytes(16)
IMG["img/tiff_be.tif"] = tiff(">", [(256, 3, [8]), (271, 2, A("Big Scan"))])
IMG["img/raw_exif.bin"] = b"Exif\x00\x00" + tiff(">", [(271, 2, A("RawExif"))])
IMG["img/first_no_thumb.jpg"] = jpeg(app1(tiff(">", [(271, 2, A("X"))], first=[(259, 3, [6])])), DQT)
IMG["img/thumb_only.jpg"] = jpeg(app1(tiff("<", [], first=[(259, 3, [6])], thumbnail=thumb(2))), DQT)


def riff(chunks):
    body = b"WEBP"
    for fourcc, data in chunks:
        body += fourcc + struct.pack("<L", len(data)) + data + b"\x00" * (len(data) % 2)
    return b"RIFF" + struct.pack("<L", len(body)) + body


VP8 = b"\x30\x01\x00\x9d\x01\x2a\x40\x00\x30\x00" + bytes(15)  # 64x48
VP8L = b"\x2f\x3f\xc0\x0b\x10" + bytes(10)                       # 64x48, alpha flag
vp8x = lambda flags, w, h: bytes([flags]) + b"\x00\x00\x00" + struct.pack("<L", w - 1)[:3] + struct.pack("<L", h - 1)[:3]  # noqa: E731
webp_exif = tiff(">", [(271, 2, A("Google")), (272, 2, A("Pixel 8"))], [(36867, 2, A("2026:08:01 18:30:05"))])
IMG["img/lossy.webp"] = riff([(b"VP8 ", VP8)])
IMG["img/lossless.webp"] = riff([(b"VP8L", VP8L)])
IMG["img/extended.webp"] = riff([(b"VP8X", vp8x(0x08, 64, 48)), (b"VP8 ", VP8), (b"EXIF", webp_exif)])
IMG["img/xmp.webp"] = riff([(b"VP8X", vp8x(0x04, 64, 48)), (b"VP8 ", VP8), (b"XMP ", b"<x:xmpmeta/>")])
IMG["img/anim.webp"] = riff([(b"VP8X", vp8x(0x02, 32, 20)), (b"ANIM", bytes(6)),
                             (b"ANMF", bytes(6) + b"\x1f\x00\x00\x13\x00\x00" + bytes(4) + b"VP8 " + bytes(4))])

# --- the program photos ------------------------------------------------

PHOTOS = {}


def canon(dt, model="Canon EOS R6", gps=None, serial="083021000123", n=1):
    d = {
        "0th": {271: b"Canon", 272: model.encode(), 274: 1, 282: (72, 1), 283: (72, 1), 296: 2,
                306: dt.encode(), 315: b"Ana Ruiz"},
        "Exif": {33434: (1, 250 * n), 33437: (28 + 4 * n, 10), 34855: 100 * 2 ** n, 36867: dt.encode(),
                 36868: dt.encode(), 37386: (24 * n, 1), 42033: serial.encode(),
                 42036: b"RF24-105mm F4 L IS USM", 37510: b"ASCII\x00\x00\x00Holiday " + str(n).encode()},
        "GPS": gps or {},
        "1st": {259: 6, 282: (72, 1), 283: (72, 1), 296: 2},
        "thumbnail": thumb(n + 3),
    }
    e = piexif.dump(d)
    return jpeg(APP0, b"\xff\xe1" + struct.pack(">H", len(e) + 2) + e, DQT, SOF0, DHT)


GPS_LISBON = {0: (2, 3, 0, 0), 1: b"N", 2: ((38, 1), (42, 1), (3120, 100)), 3: b"W",
              4: ((9, 1), (8, 1), (2280, 100)), 5: 0, 6: (510, 10)}
PHOTOS["photos/IMG_0001.JPG"] = canon("2026:07:14 09:12:30", gps=GPS_LISBON, n=1)
PHOTOS["photos/IMG_0002.JPG"] = canon("2026:07:14 13:40:02", n=2)
PHOTOS["photos/IMG_0003.JPG"] = canon("2026:07:14 09:12:30", n=3)
PHOTOS["photos/IMG_0107.JPG"] = canon("2026:07:15 23:20:45", model="Canon EOS R6 Mark II",
                                      serial="102044001877", n=4)
PHOTOS["photos/DSC00417.JPG"] = jpeg(APP0, app1(tiff(
    "<",
    [(271, 2, A("SONY")), (272, 2, A("ILCE-7M4")), (274, 3, [8]), (306, 2, A("2026:07:15 06:05:10"))],
    [(33434, 5, R((1, 60))), (33437, 5, R((56, 10))), (34855, 3, [1600]), (36867, 2, A("2026:07:15 06:05:10")),
     (37386, 5, R((35, 1))), (37500, 7, b"SONY DSC \x00\x00\x00" + bytes(range(16))),
     (42032, 2, A("Ana Ruiz")), (42033, 2, A("4872211")), (42036, 2, A("FE 35mm F1.8"))],
    [(0, 1, [2, 2, 0, 0]), (1, 2, A("N")), (2, 5, R((38, 1), (41, 1), (5310, 100))), (3, 2, A("W")),
     (4, 5, R((9, 1), (25, 1), (2010, 100))), (5, 1, [0]), (6, 5, R((1200, 10),))],
    None, [(259, 3, [6])], thumb(7))), DQT, SOF0)
PHOTOS["photos/PXL_20260801_183005123.jpg"] = jpeg(app1(tiff(
    "<",
    [(271, 2, A("Google")), (272, 2, A("Pixel 8")), (274, 3, [1]), (306, 2, A("2026:08:01 18:30:05"))],
    [(33434, 5, R((1, 1000))), (33437, 5, R((168, 100))), (34855, 3, [45]), (36867, 2, A("2026:08:01 18:30:05")),
     (36881, 2, A("+02:00")), (37386, 5, R((6810, 1000)))],
    [(1, 2, A("S")), (2, 5, R((22, 1), (57, 1), (1320, 100))), (3, 2, A("W")), (4, 5, R((43, 1), (12, 1), (3150, 100))),
     (5, 1, [1]), (6, 5, R((35, 10),))])), DQT, SOF0)
PHOTOS["photos/scan_0042.jpg"] = jpeg(APP0, DQT, SOF0)
PHOTOS["photos/edited.jpg"] = jpeg(XMP, app1(tiff(">", [(305, 2, A("GIMP 2.10.38")), (271, 2, A("Canon")),
                                                       (272, 2, A("Canon EOS R6"))],
                                                  [(36867, 2, A("2026:07:14 13:40:02"))])), DQT, SOF0)
PHOTOS["photos/broken.jpg"] = jpeg(full[:44])
PHOTOS["photos/notes.txt.jpg"] = b"shopping: milk, eggs\n"
PHOTOS["photos/vacation.webp"] = riff([(b"VP8X", vp8x(0x08, 64, 48)), (b"VP8 ", VP8), (b"EXIF", tiff(
    ">", [(271, 2, A("Google")), (272, 2, A("Pixel 8"))],
    [(36867, 2, A("2026:08:02 10:01:00"))],
    [(1, 2, A("N")), (2, 5, R((38, 1), (43, 1), (120, 100))), (3, 2, A("W")), (4, 5, R((9, 1), (9, 1), (3300, 100)))]))])
PHOTOS["photos/screenshot.webp"] = riff([(b"VP8L", VP8L)])

TRACK = """time,lat,lon,ele
2026-07-14T06:50:00Z,38.700100,-9.170200,12.0
2026-07-14T07:05:00Z,38.705400,-9.141900,48.5
2026-07-14T07:20:00Z,38.713200,-9.133600,90.0
2026-07-14T11:30:00Z,38.691500,-9.215800,4.2
2026-07-14T12:45:00Z,38.676300,-9.326900,-2.0
2026-07-15T05:00:00Z,38.697700,-9.420600,30.0
2026-07-15T05:10:00Z,38.700100,-9.424300,35.5
2026-07-15T22:00:00Z,38.721300,-9.139500,77.0
"""

CLOCK = """# camera model, seconds to add to its clock, and the offset it was in
Canon EOS R6 -3600 +01:00
SONY ILCE-7M4 +125 +01:00
Canon EOS R6 Mark II 0 +01:00
"""

# --- jobs --------------------------------------------------------------

jobs = []


def job(name, *steps):
    jobs.append({"name": name, "steps": [list(s) for s in steps]})


def B(s):
    return {"b": s}


def F(x):
    return {"f": x}


def V(n):
    return {"v": n}


for path in sorted(IMG):
    if path.endswith((".jpg", ".tif", ".webp", ".bin")):
        job(f"load {path}", ("load", "d", path), ("show", "d"))

job("load by name", ("loadn", "d", "img/nikon_le.jpg"), ("show", "d"))
job("load by name, big-endian", ("loadn", "d", "img/canon_be.jpg"), ("show", "d"))
job("load bytes", ("loadb", "d", "img/xmp_first.jpg"), ("show", "d"), ("loadb", "e", "img/tiff_be.tif"),
    ("show", "e"), ("loadb", "w", "img/extended.webp"), ("show", "w"))
job("load bytes of an XMP-first file finds the Exif segment",
    ("loadb", "d", "img/two_exif.jpg"), ("show", "d"), ("load", "e", "img/two_exif.jpg"), ("show", "e"))
job("load raw Exif bytes", ("loadx", "d", B("Exif\x00\x00MM\x00*\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00")),
    ("show", "d"))
job("load a webp without VP8X", ("load", "d", "img/lossy.webp"))
job("load short TIFF", ("loadx", "d", B("II*\x00\x08\x00")))
job("load TIFF with a bad pointer", ("loadx", "d", B("MM\x00*\x00\x00\x00\x40\x00\x01")))
job("load a JPEG whose segment walk runs off", ("loadx", "d", B("\xff\xd8\xff\xe0\x00\x02")))
job("load a JPEG with only SOI", ("loadx", "d", B("\xff\xd8")))

d0 = {"0th": {"271": "Kaabe", "272": "K-1", "282": [72, 1], "283": [72, 1], "296": 2,
              "274": 1, "258": [8, 8, 8], "306": "2026:10:21 12:00:00"},
      "Exif": {"36867": "2026:10:21 12:00:00", "33434": [1, 125], "37510": B("ASCII\x00\x00\x00hi"),
               "37380": [-2, 3], "34855": 400},
      "GPS": {"0": [2, 3, 0, 0], "1": "N", "2": [[1, 1], [2, 1], [3, 1]]},
      "Interop": {"1": "R98"},
      "1st": {"259": 6},
      "thumbnail": {"file": "img/plain.jpg"}}
job("dump and load back", ("dict", "x", d0), ("dump", "b", "x"), ("show", "b"), ("loadx", "d", V("b")),
    ("show", "d"))
job("dump empty", ("dict", "x", {}), ("dump", "b", "x"), ("show", "b"),
    ("dict", "y", {"0th": {}, "Exif": {}, "GPS": {}, "Interop": {}, "1st": {}, "thumbnail": None}),
    ("dump", "c", "y"), ("show", "c"))
job("dump drops stale pointer tags",
    ("dict", "x", {"0th": {"34665": 999, "34853": 5, "271": "A"}, "Exif": {"40965": 1}}),
    ("dump", "b", "x"), ("show", "b"), ("loadx", "d", V("b")), ("show", "d"))
job("dump Interop without Exif",
    ("dict", "x", {"0th": {}, "Interop": {"1": "R03"}}), ("dump", "b", "x"), ("loadx", "d", V("b")),
    ("show", "d"))
job("dump 1st without a thumbnail", ("dict", "x", {"0th": {"271": "A"}, "1st": {"259": 6}}),
    ("dump", "b", "x"), ("show", "b"))
job("dump thumbnail without 1st", ("dict", "x", {"0th": {"271": "A"}, "thumbnail": {"file": "img/plain.jpg"}}),
    ("dump", "b", "x"), ("show", "b"))
job("dump a thumbnail's APP segments are dropped",
    ("dict", "x", {"1st": {"259": 6}, "thumbnail": {"file": "img/app2_icc.jpg"}}), ("dump", "b", "x"),
    ("loadx", "d", V("b")), ("show", "d"))
job("dump every type",
    ("dict", "x", {"0th": {
        "336": [1, 2, 3, 4, 5], "11": "", "269": "abc", "270": "four", "271": B("raw\xe9"), "305": "caf\xe9",
        "274": [3], "258": [1, 2], "301": [1, 2, 3], "254": 0, "273": [1, 2], "282": [[1, 2]],
        "318": [[1, 2], [3, 4]], "60608": [-1, 2], "60609": [-300], "60610": [0.5, -1.5], "50940": [0.1],
        "50938": 2.5, "50715": [-1, 2], "50721": [[1, -2], [-3, 4]], "37398": [1, 0, 0, 0],
        "700": B("<x/>"), "530": [2, 2]}}),
    ("dump", "b", "x"), ("show", "b"), ("loadx", "d", V("b")), ("show", "d"))
job("dump short undefined", ("dict", "x", {"Exif": {"36864": B("02"), "37500": B("")}}), ("dump", "b", "x"),
    ("show", "b"), ("loadx", "d", V("b")), ("show", "d"))
job("dump an unknown tag", ("dict", "x", {"0th": {"9999": 1}}), ("dump", "b", "x"))
job("dump a str where bytes belong", ("dict", "x", {"Exif": {"37500": "text"}}), ("dump", "b", "x"))
job("dump bytes where a short belongs", ("dict", "x", {"0th": {"274": B("ab")}}), ("dump", "b", "x"))
job("dump a non-latin-1 string", ("dict", "x", {"0th": {"271": "☃"}}), ("dump", "b", "x"))
job("dump an int where ASCII belongs", ("dict", "x", {"0th": {"271": 5}}), ("dump", "b", "x"))
for tag, v in (("274", 70000), ("254", -1), ("336", [256]), ("60608", [200]), ("282", [-1, 2]),
               ("60609", [40000]), ("50715", [3000000000, 1]), ("301", [1, -1, 2]), ("273", [5, 4294967296])):
    job(f"dump out of range: {tag} {v}", ("dict", "x", {"0th": {tag: v}}), ("dump", "b", "x"))
for ifd, tag, v in (("0th", "282", [1, 2, 3]), ("0th", "282", 72), ("0th", "318", [[1, 2], [3, 4, 5]]),
                    ("0th", "274", "x"), ("0th", "254", 1.5), ("Exif", "36864", [1, 2]), ("0th", "271", [1, 2]),
                    ("0th", "50715", [0.5, 2]), ("0th", "50940", 5), ("0th", "60610", [1, 2]),
                    ("0th", "336", B("\x01\x02\x03\x04\x05\x06")), ("GPS", "2", [[1, 1], [2, 1]])):
    label = "bytes" if isinstance(v, dict) else json.dumps(v)
    job(f"dump {ifd} {tag} as {label}", ("dict", "x", {ifd: {tag: v}}), ("dump", "b", "x"),
        ("loadx", "d", V("b")), ("show", "d"))
job("dump a rational given as floats", ("dict", "x", {"0th": {"282": [0.5, 1]}}), ("dump", "b", "x"))
job("dump a too-large thumbnail",
    ("dict", "x", {"1st": {"259": 6}, "thumbnail": {"b": "\xff\xd8\xff\xda", "then": "x", "times": 64001}}), ("dump", "b", "x"))
job("dump a thumbnail that is not a JPEG",
    ("dict", "x", {"1st": {"259": 6}, "thumbnail": {"b": "PNG"}}), ("dump", "b", "x"))
job("insert into a file with APP0",
    ("dict", "x", {"0th": {"271": "Kaabe"}}), ("dump", "b", "x"),
    ("insert", "b", "img/plain.jpg", "out/plain_exif.jpg"), ("file", "out/plain_exif.jpg"),
    ("load", "d", "out/plain_exif.jpg"), ("show", "d"))
job("insert replaces an existing Exif",
    ("dict", "x", {"0th": {"271": "Replaced"}}), ("dump", "b", "x"),
    ("insert", "b", "img/exif_only_0th.jpg", "out/replaced.jpg"), ("file", "out/replaced.jpg"),
    ("load", "d", "out/replaced.jpg"), ("show", "d"))
job("insert without APP0",
    ("dict", "x", {"0th": {"271": "NoApp0"}}), ("dump", "b", "x"),
    ("insert", "b", "img/no_app0.jpg", "out/no_app0.jpg"), ("file", "out/no_app0.jpg"),
    ("insert", "b", "img/thumb_only.jpg", "out/thumb_only.jpg"), ("file", "out/thumb_only.jpg"),
    ("insert", "b", "img/xmp_first.jpg", "out/xmp_first.jpg"), ("file", "out/xmp_first.jpg"))
job("insert into webp",
    ("dict", "x", {"0th": {"271": "Kaabe", "272": "Web"}}), ("dump", "b", "x"),
    ("insert", "b", "img/lossy.webp", "out/lossy.webp"), ("file", "out/lossy.webp"),
    ("load", "d", "out/lossy.webp"), ("show", "d"),
    ("insert", "b", "img/lossless.webp", "out/lossless.webp"), ("file", "out/lossless.webp"),
    ("insert", "b", "img/xmp.webp", "out/xmp.webp"), ("file", "out/xmp.webp"),
    ("insert", "b", "img/anim.webp", "out/anim.webp"), ("file", "out/anim.webp"),
    ("insert", "b", "img/extended.webp", "out/extended.webp"), ("file", "out/extended.webp"),
    ("load", "e", "out/extended.webp"), ("show", "e"))
job("insert data that is not Exif", ("bytes", "junk", B("Exif\x00MM")),
    ("insert", "junk", "img/plain.jpg", "out/x.jpg"))
job("insert into a file that is not an image",
    ("dict", "x", {}), ("dump", "b", "x"), ("insert", "b", "img/not_jpeg.jpg", "out/x.jpg"))
job("remove",
    ("remove", "img/canon_be.jpg", "out/canon_clean.jpg"), ("file", "out/canon_clean.jpg"),
    ("load", "d", "out/canon_clean.jpg"), ("show", "d"),
    ("remove", "img/plain.jpg", "out/plain_clean.jpg"), ("file", "out/plain_clean.jpg"),
    ("remove", "img/two_exif.jpg", "out/two_clean.jpg"), ("file", "out/two_clean.jpg"),
    ("remove", "img/extended.webp", "out/extended_clean.webp"), ("file", "out/extended_clean.webp"),
    ("remove", "img/lossy.webp", "out/lossy_clean.webp"), ("file", "out/lossy_clean.webp"),
    ("remove", "img/xmp.webp", "out/xmp_clean.webp"), ("file", "out/xmp_clean.webp"))
job("transplant",
    ("transplant", "img/canon_be.jpg", "img/plain.jpg", "out/t1.jpg"), ("load", "d", "out/t1.jpg"), ("show", "d"),
    ("transplant", "img/nikon_le.jpg", "img/exif_only_0th.jpg", "out/t2.jpg"), ("file", "out/t2.jpg"),
    ("transplant", "img/xmp_first.jpg", "img/no_app0.jpg", "out/t3.jpg"), ("file", "out/t3.jpg"),
    ("transplant", "img/plain.jpg", "img/canon_be.jpg", "out/t4.jpg"))
job("edit and write back",
    ("load", "d", "img/canon_be.jpg"), ("set", "d", "0th", 315, "Ana Ruiz-Ortega"),
    ("set", "d", "Exif", 36867, B("2026:07:14 10:12:30")), ("del", "d", "GPS", 2), ("del", "d", "GPS", 4),
    ("set", "d", "0th", 274, 6), ("set", "d", "thumbnail", 0, None),
    ("dump", "b", "d"), ("insert", "b", "img/canon_be.jpg", "out/edited.jpg"),
    ("load", "e", "out/edited.jpg"), ("show", "e"))
job("round trip of a little-endian file",
    ("load", "d", "img/nikon_le.jpg"), ("dump", "b", "d"), ("insert", "b", "img/plain.jpg", "out/nikon_be.jpg"),
    ("load", "e", "out/nikon_be.jpg"), ("show", "e"))
for s in (B("ASCII\x00\x00\x00hello"), B("UNICODE\x00\x00h\x00i\xd8\x3d\xde\x00"),
          B("UNICODE\x00\x00a\xd8\x00\x00b\x00"), B("UNICODE\x00\x00a\x00b"), B("UNICODE\x00\xdc\x00\x00z"),
          B("JIS\x00\x00\x00\x00\x00plain text"), B("ASCII\x00\x00\x00caf\xe9"),
          B("\x00\x00\x00\x00\x00\x00\x00\x00blank"), B("ASCII"), B("EBCDIC\x00\x00x"), B("ASCII\x00\x00\x00")):
    job("UserComment.load", ("ucload", s))
for text, encoding in (("hello", "ascii"), ("caf\xe9 \u2603", "ascii"), ("h\xe9 \U0001f600", "unicode"),
                       ("plain", "jis"), ("x", "latin-1"), ("", "unicode"), ("a\x00b", "ascii")):
    job("UserComment.dump", ("ucdump", text, encoding))


def main():
    os.makedirs(DATA, exist_ok=True)
    for name, b in list(IMG.items()) + list(PHOTOS.items()):
        p = os.path.join(DATA, name)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(b)
    with open(os.path.join(DATA, "track.csv"), "w") as f:
        f.write(TRACK)
    with open(os.path.join(DATA, "clock.txt"), "w") as f:
        f.write(CLOCK)
    with open(os.path.join(DATA, "jobs.jsonl"), "w") as f:
        for j in jobs:
            f.write(json.dumps(j, ensure_ascii=True) + "\n")


main()
