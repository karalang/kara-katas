#!/usr/bin/env python3
"""Writes data/jobs.tsv: synthetic photo files for mini_exifread, one job a
line. Each file is built byte by byte here (TIFF IFDs, JPEG segments, PNG
chunks, WebP RIFF chunks, HEIC and JPEG XL boxes) the way a camera, a phone
or an editor would write it, including the broken files real photo
libraries meet. Fields: kind, flags, file name, file bytes as hex.

  cli    the exifread command line on one file (flags: q quick, s strict,
         b builtin types, t=<Tag> stop tag; "-" for none)
  gps    process_file, then utils.get_gps_coords on the tags
  thumb  process_file, then the thumbnail it extracted

Run: python3 -s -P -B mk.py"""
import os
import struct
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
TL = {0: 0, 1: 1, 2: 1, 3: 2, 4: 4, 5: 8, 6: 1, 7: 1, 8: 2, 9: 4, 10: 8, 11: 4, 12: 8, 13: 4}
FMT = {1: "B", 2: "B", 7: "B", 3: "H", 4: "I", 6: "b", 8: "h", 9: "i", 11: "f", 12: "d", 13: "I"}


class Ptr:
    """The offset of a labelled IFD or blob, as a one-value LONG."""

    def __init__(self, label):
        self.label = label


class Raw:
    """An explicit count and the bytes to store for it."""

    def __init__(self, count, data):
        self.count = count
        self.data = data


class At:
    """An explicit count and a raw value/offset field."""

    def __init__(self, count, off):
        self.count = count
        self.off = off


class Fn:
    """n bytes produced by f(position) once the position is known."""

    def __init__(self, n, f):
        self.n = n
        self.f = f


def pack_vals(e, typ, vals):
    out = b""
    for v in vals:
        if typ in (5, 10):
            out += struct.pack(e + ("II" if typ == 5 else "ii"), v[0], v[1])
        else:
            out += struct.pack(e + FMT[typ], v)
    return out


def entry_data(e, typ, val):
    """(count, data or None, field or None) for one entry."""
    if isinstance(val, Ptr):
        return 1, None, ("ptr", val.label)
    if isinstance(val, Raw):
        return val.count, val.data, None
    if isinstance(val, At):
        return val.count, None, ("int", val.off)
    if isinstance(val, Fn):
        return val.n // max(TL.get(typ, 1), 1), val, None
    if isinstance(val, str):
        b = val.encode("utf-8") + b"\x00"
        return len(b), b, None
    if isinstance(val, bytes):
        return len(val) // max(TL.get(typ, 1), 1), val, None
    return len(val), pack_vals(e, typ, val), None


def data_len(d):
    return d.n if isinstance(d, Fn) else len(d)


def out_of_line(typ, count, d):
    tl = TL.get(typ)
    if tl is None or tl == 0:
        return False
    return count * tl > 4


def block_size(e, entries):
    size = 2 + 12 * len(entries) + 4
    for tag, typ, val in entries:
        count, d, field = entry_data(e, typ, val)
        if d is not None and out_of_line(typ, count, d):
            n = data_len(d)
            size += n + (n & 1)
    return size


def block(e, entries, pos, origin, nxt, resolve):
    """An IFD at absolute position pos, its data area after it; offsets
    are written relative to origin."""
    head = struct.pack(e + "H", len(entries))
    body = b""
    cur = pos + 2 + 12 * len(entries) + 4
    for tag, typ, val in entries:
        count, d, field = entry_data(e, typ, val)
        if field is not None:
            if field[0] == "ptr":
                fv = struct.pack(e + "I", resolve(field[1]) - origin)
            else:
                fv = struct.pack(e + "I", field[1] & 0xFFFFFFFF)
        elif out_of_line(typ, count, d):
            raw = d.f(cur) if isinstance(d, Fn) else d
            assert len(raw) == data_len(d), (tag, len(raw), data_len(d))
            fv = struct.pack(e + "I", cur - origin)
            body += raw + (b"\x00" if len(raw) & 1 else b"")
            cur += len(raw) + (len(raw) & 1)
        else:
            raw = d.f(cur) if isinstance(d, Fn) else d
            fv = (raw + b"\x00\x00\x00\x00")[:4]
        head += struct.pack(e + "HHI", tag, typ, count & 0xFFFFFFFF) + fv
    head += struct.pack(e + "I", nxt & 0xFFFFFFFF)
    return head + body


def tiff(order, ifds, blobs=(), first=None, magic=42):
    """ifds: [(label, entries, next)], next a label, an int or None."""
    e = "<" if order == "II" else ">"
    pos = {}
    p = 8
    for label, entries, _ in ifds:
        pos[label] = p
        p += block_size(e, entries)
    for label, data in blobs:
        pos[label] = p
        p += len(data) + (len(data) & 1)
    out = order.encode() + struct.pack(e + "H", magic)
    out += struct.pack(e + "I", pos[ifds[0][0]] if first is None else first)
    for label, entries, nxt in ifds:
        if nxt is None:
            nv = 0
        elif isinstance(nxt, str):
            nv = pos[nxt]
        else:
            nv = nxt
        assert len(out) == pos[label]
        out += block(e, entries, pos[label], 0, nv, pos.__getitem__)
    for label, data in blobs:
        out += data + (b"\x00" if len(data) & 1 else b"")
    return out


# ---- maker notes, built at the position they land on

def mn_plain(order_e, entries, prefix=b"", ifd_at=0, origin_at=None, inner=b""):
    """prefix + inner header, then an IFD at note+ifd_at whose offsets are
    relative to note+origin_at (absolute when origin_at is None)."""
    n = len(prefix) + len(inner) + block_size(order_e, entries)

    def f(pos):
        origin = 0 if origin_at is None else pos + origin_at
        return prefix + inner + block(order_e, entries, pos + ifd_at, origin, 0, None)

    return Fn(n, f)


def nikon1(e, entries):
    return mn_plain(e, entries, b"Nikon\x00\x01\x00", 8)


def nikon2(e, entries, inner_order=b"MM"):
    ie = ">" if inner_order == b"MM" else "<"
    inner = inner_order + struct.pack(ie + "HI", 42, 8)
    return mn_plain(e, entries, b"Nikon\x00\x02\x10\x00\x00", 18, 10, inner)


def olympus(e, entries):
    return mn_plain(e, entries, b"OLYMP\x00\x01\x00", 8)


def fujifilm(entries):
    return mn_plain("<", entries, b"FUJIFILM" + struct.pack("<I", 12), 12, 0)


def apple(e, entries):
    return mn_plain(e, entries, b"Apple iOS\x00\x00\x01MM", 14, 14)


def dji(entries):
    return mn_plain("<", entries, b"", 0, 0)


# ---- containers

def seg(marker, payload):
    return bytes([0xFF, marker]) + struct.pack(">H", len(payload) + 2) + payload


JFIF = seg(0xE0, b"JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00")
JFXX = seg(0xE0, b"JFXX\x00\x10" + bytes(4))
ICC = seg(0xE2, b"ICC_PROFILE\x00\x01\x01" + bytes(24))
DQT = seg(0xDB, b"\x00" + bytes(range(1, 65)))
SCAN = seg(0xDA, b"\x01\x01\x00\x00\x3f\x00") + b"\x12\x34\x56\x78" + b"\xff\xd9"


def jpeg(t, pre=(), app1=True):
    out = b"\xff\xd8"
    for s in pre:
        out += s
    if app1:
        out += seg(0xE1, b"Exif\x00\x00" + t)
    return out + DQT + SCAN


def chunk(kind, data):
    c = kind + data
    return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)


IHDR = chunk(b"IHDR", struct.pack(">IIBBBBB", 4, 3, 8, 2, 0, 0, 0))


def png(t, before=(), after=()):
    out = b"\x89PNG\r\n\x1a\n" + IHDR
    for c in before:
        out += c
    if t is not None:
        out += chunk(b"eXIf", t)
    for c in after:
        out += c
    return out + chunk(b"IDAT", zlib.compress(bytes(36))) + chunk(b"IEND", b"")


def riff(kind, data, pad=True):
    out = kind + struct.pack("<I", len(data)) + data
    if pad and len(data) & 1:
        out += b"\x00"
    return out


def webp(chunks, flags=0x08):
    vp8x = riff(b"VP8X", bytes([flags, 0, 0, 0]) + bytes([3, 0, 0, 2, 0, 0]))
    body = b"WEBP" + vp8x + b"".join(chunks)
    return b"RIFF" + struct.pack("<I", len(body)) + body


VP8 = riff(b"VP8 ", b"\x30\x01\x00\x9d\x01\x2a\x04\x00\x03\x00" + bytes(8))


def box(kind, data):
    return struct.pack(">I", len(data) + 8) + kind + data


def fullbox(kind, version, flags, data):
    return box(kind, struct.pack(">I", (version << 24) | flags) + data)


def ftyp(brand, minor=0, compat=(b"mif1", b"heic")):
    return box(b"ftyp", brand + struct.pack(">I", minor) + b"".join(compat))


def infe(item_id, kind, name=b"", version=2):
    if version == 2:
        data = struct.pack(">HH", item_id, 0) + kind + name + b"\x00"
    elif version == 3:
        data = struct.pack(">IH", item_id, 0) + kind + name + b"\x00"
    else:
        data = struct.pack(">HH", item_id, 0) + name + b"\x00"
    return fullbox(b"infe", version, 0, data)


def iloc(version, items, sizes=(4, 4, 0, 0)):
    """items: [(item_id, [(offset, length)])]."""
    osz, lsz, bsz, isz = sizes
    data = bytes([(osz << 4) | lsz, (bsz << 4) | isz])
    data += struct.pack(">H" if version < 2 else ">I", len(items))
    szf = {0: "", 2: "H", 4: "I", 8: "Q"}
    for item_id, extents in items:
        data += struct.pack(">H" if version < 2 else ">I", item_id)
        if version in (1, 2):
            data += struct.pack(">H", 0)
        data += struct.pack(">H", 0)
        if bsz:
            data += struct.pack(">" + szf[bsz], 0)
        data += struct.pack(">H", len(extents))
        for off, length in extents:
            if version in (1, 2) and isz:
                data += struct.pack(">" + szf[isz], 1)
            if osz:
                data += struct.pack(">" + szf.get(osz, "I"), off)
            if lsz:
                data += struct.pack(">" + szf.get(lsz, "I"), length)
    return fullbox(b"iloc", version, 0, data)


HDLR = fullbox(b"hdlr", 0, 0, bytes(4) + b"pict" + bytes(12) + b"\x00")
PITM = fullbox(b"pitm", 0, 0, struct.pack(">H", 1))


def heic(payload, brand=b"heic", minor=0, iloc_version=0, sizes=(4, 4, 0, 0),
         exif_id=2, infe_version=2, loc_id=None, extents=None, iinf=True,
         with_iloc=True, extra_meta=(), meta_version=0):
    """ftyp, meta (hdlr, pitm, iinf, iloc), then mdat with the payload."""
    head = ftyp(brand, minor)

    def meta_for(mdat_pos):
        subs = HDLR + PITM
        if iinf:
            items = infe(1, b"hvc1", b"image", infe_version) + infe(exif_id, b"Exif", b"", infe_version)
            subs += fullbox(b"iinf", 0, 0, struct.pack(">H", 2) + items)
        for b in extra_meta:
            subs += b
        if with_iloc:
            ex = extents if extents is not None else [(mdat_pos + 8, len(payload))]
            ex = [(mdat_pos + 8 + o if isinstance(o, str) is False and o < 0 else o, n) for o, n in ex]
            subs += iloc(iloc_version, [(1, [(mdat_pos + 8 + len(payload), 4)]),
                                        (exif_id if loc_id is None else loc_id, ex)], sizes)
        return fullbox(b"meta", meta_version, 0, subs)

    m = meta_for(0)
    m = meta_for(len(head) + len(m))
    return head + m + box(b"mdat", payload + b"\x00\x00\x00\x00")


def jxl(t, brand=b"jxl ", exif=True):
    out = b"\x00\x00\x00\x0cJXL \r\n\x87\n" + box(b"ftyp", brand + struct.pack(">I", 0) + brand)
    out += box(b"jxll", b"\x05")
    if exif:
        out += box(b"Exif", b"\x00\x00\x00\x00" + t)
    return out + box(b"jxlc", b"\xff\x0a\x00")


# ---- a camera's IFDs

def gps_entries(lat=(51, 30, 2652, 100), lng=(0, 7, 3972, 100), ns="N", ew="W"):
    return [
        (0x0000, 1, [2, 3, 0, 0]),
        (0x0001, 2, ns),
        (0x0002, 5, [(lat[0], 1), (lat[1], 1), (lat[2], lat[3])]),
        (0x0003, 2, ew),
        (0x0004, 5, [(lng[0], 1), (lng[1], 1), (lng[2], lng[3])]),
        (0x0005, 1, [0]),
        (0x0006, 5, [(3550, 100)]),
        (0x0007, 5, [(14, 1), (32, 1), (5, 1)]),
        (0x0012, 2, "WGS-84"),
        (0x001D, 2, "2024:05:17"),
    ]


def ifd0(make, model, extra=(), exif=True, gps=True, software="Firmware 1.02"):
    out = [
        (0x010F, 2, make),
        (0x0110, 2, model),
        (0x0112, 3, [1]),
        (0x011A, 5, [(72, 1)]),
        (0x011B, 5, [(72, 1)]),
        (0x0128, 3, [2]),
        (0x0131, 2, software),
        (0x0132, 2, "2024:05:17 14:32:05"),
        (0x0213, 3, [2]),
    ]
    out += list(extra)
    if exif:
        out.append((0x8769, 4, Ptr("exif")))
    if gps:
        out.append((0x8825, 4, Ptr("gps")))
    out.sort(key=lambda x: x[0])
    return out


def exif_ifd(makernote=None, extra=(), interop=False, comment=None):
    out = [
        (0x829A, 5, [(1, 250)]),
        (0x829D, 5, [(28, 10)]),
        (0x8822, 3, [3]),
        (0x8827, 3, [200]),
        (0x9000, 7, b"0232"),
        (0x9003, 2, "2024:05:17 14:32:05"),
        (0x9004, 2, "2024:05:17 14:32:05"),
        (0x9101, 7, bytes([1, 2, 3, 0])),
        (0x9201, 10, [(7965784, 1000000)]),
        (0x9202, 5, [(2970854, 1000000)]),
        (0x9204, 10, [(-1, 3)]),
        (0x9207, 3, [5]),
        (0x9209, 3, [16]),
        (0x920A, 5, [(50, 1)]),
        (0xA000, 7, b"0100"),
        (0xA001, 3, [1]),
        (0xA002, 4, [4000]),
        (0xA003, 4, [3000]),
        (0xA402, 3, [0]),
        (0xA403, 3, [0]),
        (0xA406, 3, [0]),
    ]
    if makernote is not None:
        out.append((0x927C, 7, makernote))
    if comment is not None:
        out.append((0x9286, 7, comment))
    if interop:
        out.append((0xA005, 4, Ptr("interop")))
    out += list(extra)
    out.sort(key=lambda x: x[0])
    return out


INTEROP = [(0x0001, 2, "R98"), (0x0002, 7, b"0100")]


def thumb_jpeg():
    return b"\xff\xd8" + seg(0xDB, bytes(5)) + b"\xff\xd9"


def camera(order, make, model, mn=None, gps=True, thumb=False, interop=False,
           comment=None, i0=(), ex=(), extra_ifds=(), software="Firmware 1.02"):
    ifds = [("ifd0", ifd0(make, model, i0, True, gps, software), "ifd1" if thumb else None)]
    blobs = []
    if thumb:
        ifds.append(("ifd1", [
            (0x0103, 3, [6]),
            (0x011A, 5, [(72, 1)]),
            (0x011B, 5, [(72, 1)]),
            (0x0128, 3, [2]),
            (0x0201, 4, Ptr("tj")),
            (0x0202, 4, [len(thumb_jpeg())]),
        ], None))
        blobs.append(("tj", thumb_jpeg()))
    ifds.append(("exif", exif_ifd(mn, ex, interop, comment), None))
    if gps:
        ifds.append(("gps", gps_entries(), None))
    if interop:
        ifds.append(("interop", INTEROP, None))
    ifds += list(extra_ifds)
    return tiff(order, ifds, blobs)


def le(order):
    return "<" if order == "II" else ">"


# ---- maker note contents

NIKON_OLD = [(0x0003, 3, [2]), (0x0004, 3, [1]), (0x0005, 3, [0]), (0x0006, 3, [9]), (0x0007, 3, [5])]


def nikon_new(ev=(bytes([252, 1, 6, 0]),)):
    out = [
        (0x0001, 7, b"0210"),
        (0x0002, 3, [0, 400]),
        (0x0003, 2, "COLOR"),
        (0x0004, 2, "FINE  "),
        (0x0005, 2, "AUTO1"),
        (0x0007, 2, "AF-S  "),
        (0x000B, 8, [0, 0]),
        (0x001E, 3, [1]),
        (0x001D, 2, "6012345"),
    ]
    tags = [0x000D, 0x000E, 0x0012, 0x0017, 0x0018]
    for t, b in zip(tags, ev):
        out.append((t, 7, b))
    out.sort(key=lambda x: x[0])
    return out


OLY = [
    (0x0200, 4, [0, 3, 1]),
    (0x0201, 3, [2]),
    (0x0202, 3, [0]),
    (0x0204, 5, [(100, 100)]),
    (0x0207, 2, "SX756"),
    (0x0209, 7, b"OLYMPUS DIGITAL CAMERA\x00\x00"),
]
CASIO = [(0x0001, 3, [1]), (0x0002, 3, [3]), (0x0003, 3, [3]), (0x0004, 3, [1]), (0x0007, 3, [1]), (0x000A, 4, [65536])]
SONY = [(0x0102, 4, [2]), (0x0104, 10, [(0, 10)]), (0x0105, 4, [0]), (0x0115, 4, [16]), (0x1000, 3, [0])]
FUJI = [(0x0000, 7, b"0130"), (0x0010, 2, "FC  X-T4 12345"), (0x1000, 2, "NORMAL "),
        (0x1001, 3, [3]), (0x1002, 3, [256]), (0x1003, 3, [0]), (0x1010, 3, [1])]
APPLE = [(0x0001, 9, [14]), (0x0004, 9, [1]), (0x0005, 9, [178]), (0x0007, 9, [1]),
         (0x000A, 9, [4]), (0x0014, 9, [10]), (0x002E, 9, [0])]
DJI = [(0x0001, 2, "DJI"), (0x0003, 11, [0.0]), (0x0004, 11, [-1.25]), (0x0006, 11, [0.1]),
       (0x0007, 11, [178.5]), (0x0009, 11, [-90.0]), (0x000B, 11, [2.5e-7])]


def canon_mn(info=None, extra=()):
    settings = [0, 2, 0, 3, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0,
                1, 0, 105, 24, 1, 0, 0, 0, 0, 0, 0, 0]
    out = [
        (0x0001, 3, settings),
        (0x0002, 3, [2, 50, 36, 24]),
        (0x0004, 3, [68, 0, 160, 284, 128, 144, 0, 0, 0, 0, 0, 0, 152, 0, 0, 0, 0, 2]),
        (0x0006, 2, "Canon EOS 5D Mark III"),
        (0x0007, 2, "Firmware Version 1.3.6"),
        (0x0009, 2, "Ada Lovelace"),
        (0x0010, 4, [2147484293]),
        (0x0012, 3, [9, 9, 5760, 3840, 5760, 3840, 99, 99]),
        (0x0093, 3, [30, 0, 104, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
        (0x00B4, 3, [1]),
    ]
    if info is not None:
        out.append((0x000D, 7, info))
    out += list(extra)
    out.sort(key=lambda x: x[0])
    return out


def camera_info(n, fields):
    b = bytearray(n)
    for off, fmt, v in fields:
        b[off:off + struct.calcsize(fmt)] = struct.pack(fmt, v)
    return bytes(b)


INFO_5D = camera_info(224, [(23, "<B", 153), (204, "<L", 101), (208, "<H", 1247)])
INFO_5D3 = camera_info(700, [(27, "<B", 160), (652, "<L", 3401), (656, "<L", 3402),
                             (664, "<L", 101), (668, "<L", 102)])
INFO_600D = camera_info(500, [(25, "<B", 150), (475, "<L", 6603), (487, "<L", 100)])
INFO_BIG = camera_info(1100, [(27, "<B", 160), (652, "<L", 3401)])


# ---- the jobs

JOBS = []


def job(kind, flags, name, data):
    JOBS.append((kind, flags, name, data.hex()))


def cli(name, data, flags="-"):
    job("cli", flags, name, data)


def broken_tiff(order, entries, extra_ifds=(), blobs=(), first=None, nxt=None, magic=42):
    return tiff(order, [("ifd0", entries, nxt)] + list(extra_ifds), blobs, first, magic)


def main():
    # -- whole cameras, raw TIFF, both byte orders
    d70 = camera("II", "NIKON CORPORATION", "NIKON D70", nikon2("<", nikon_new()), thumb=True, interop=True)
    cli("nikon_d70.nef", d70)
    cli("nikon_d70.nef", d70, "q")
    cli("nikon_d70.nef", d70, "b")
    cli("nikon_d70.nef", d70, "t=Model")
    cli("nikon_d70.nef", d70, "t=FNumber")
    cli("nikon_d70.nef", d70, "q,b")
    job("gps", "-", "nikon_d70.nef", d70)
    job("gps", "b", "nikon_d70.nef", d70)
    job("thumb", "-", "nikon_d70.nef", d70)
    mm = camera("MM", "NIKON CORPORATION", "NIKON D3", nikon2(">", nikon_new(), b"MM"))
    cli("nikon_d3.nef", mm)
    cli("nikon_d3.nef", mm, "s")
    # Nikon flavours
    evs = [bytes(x) for x in ([252, 1, 6, 0], [253, 1, 6, 0], [254, 1, 6, 0], [0, 1, 6, 0], [2, 1, 6, 0])]
    cli("nikon_ev_a.jpg", jpeg(camera("II", "NIKON", "E995", nikon2("<", nikon_new(evs)), gps=False)))
    evs = [bytes(x) for x in ([3, 1, 6, 0], [4, 1, 6, 0], [12, 1, 6, 0], [9, 1, 6, 0], [244, 1, 6, 0])]
    cli("nikon_ev_b.jpg", jpeg(camera("II", "NIKON", "E995", nikon2("<", nikon_new(evs)), gps=False)))
    evs = [bytes(x) for x in ([1, 1, 12, 0], [250, 1, 12, 0], [7, 1, 2, 0], [6, 0, 6], [0, 0, 0, 0])]
    cli("nikon_ev_c.jpg", jpeg(camera("II", "NIKON", "E995", nikon2("<", nikon_new(evs)), gps=False)))
    evs = [bytes(x) for x in ([5, 1, 0, 0],)]
    cli("nikon_ev_zero.jpg", jpeg(camera("II", "NIKON", "E995", nikon2("<", nikon_new(evs)), gps=False)))
    cli("nikon_e950.jpg", jpeg(camera("MM", "NIKON", "E950", nikon1(">", NIKON_OLD), gps=False)))
    cli("nikon_d1.jpg", jpeg(camera("MM", "NIKON", "D1", mn_plain(">", nikon_new()), gps=False)))
    nomark = Fn(30, lambda pos: b"Nikon\x00\x02\x10\x00\x00MM\x00\x00" + bytes(16))
    cli("nikon_nomark.jpg", jpeg(camera("II", "NIKON", "D200", nomark, gps=False)))
    cli("nikon_nomark.jpg", jpeg(camera("II", "NIKON", "D200", nomark, gps=False)), "s")
    cli("nikon_jfif.jpg", jpeg(camera("II", "NIKON", "D200", nikon2("<", nikon_new()), gps=False), [JFIF]))
    # other makers
    oly = camera("II", "OLYMPUS IMAGING CORP.  ", "E-M1",
                 olympus("<", OLY + [(0x0100, 7, thumb_jpeg())]), gps=False)
    cli("olympus_em1.orf", oly)
    job("thumb", "-", "olympus_em1.orf", oly)
    olyt = tiff("II", [("ifd0", ifd0("OLYMPUS IMAGING CORP.", "E-M5", (), True, False), "ifd1"),
                       ("ifd1", [(0x0103, 3, [6]), (0x0128, 3, [2])], None),
                       ("exif", exif_ifd(olympus("<", OLY + [(0x0100, 7, thumb_jpeg())])), None)])
    cli("olympus_em5.orf", olyt)
    job("thumb", "-", "olympus_em5.orf", olyt)
    cli("olympus_short.orf", camera("II", "OLYMPUS", "C5050Z", olympus("<", [(0x0200, 4, [1, 2])]), gps=False))
    cli("casio_qv.jpg", jpeg(camera("MM", "CASIO COMPUTER CO.,LTD.", "QV-R62", mn_plain(">", CASIO), gps=False)))
    cli("casio_ex.jpg", jpeg(camera("MM", "Casio", "EX-Z750", mn_plain(">", CASIO[:3]), gps=False)))
    cli("sony_a7.arw", camera("II", "SONY", "ILCE-7M3", mn_plain("<", SONY)))
    cli("fuji_xt4.raf", jpeg(camera("MM", "FUJIFILM", "X-T4", fujifilm(FUJI))))
    cli("fuji_xt4.raf", jpeg(camera("MM", "FUJIFILM", "X-T4", fujifilm(FUJI))), "b")
    iphone = camera("MM", "Apple", "iPhone 15 Pro", apple(">", APPLE), software="17.4.1")
    cli("iphone.jpg", jpeg(iphone))
    cli("iphone.jpg", jpeg(iphone), "b")
    cli("apple_nohdr.jpg", jpeg(camera("MM", "Apple", "iPhone 6", mn_plain(">", APPLE), gps=False)))
    cli("dji_mavic.jpg", jpeg(camera("II", "DJI", "FC3170", dji(DJI))))
    cli("dji_mavic.jpg", jpeg(camera("II", "DJI", "FC3170", dji(DJI))), "b")
    cli("unknown_maker.jpg", jpeg(camera("II", "Hasselblad", "X2D", mn_plain("<", CASIO), gps=False)))
    # Canon, with the CameraInfo blocks
    c5d3 = camera("II", "Canon", "Canon EOS 5D Mark III", mn_plain("<", canon_mn(INFO_5D3)), thumb=True)
    cli("canon_5d3.cr2", c5d3)
    cli("canon_5d3.cr2", c5d3, "b")
    cli("canon_5d3.cr2", c5d3, "q")
    cli("canon_5d.jpg", jpeg(camera("II", "Canon", "Canon EOS 5D", mn_plain("<", canon_mn(INFO_5D)), gps=False)))
    cli("canon_5d2.jpg", jpeg(camera("II", "Canon", "Canon EOS 5D Mark II", mn_plain("<", canon_mn(INFO_5D3)), gps=False)))
    cli("canon_t3i.jpg", jpeg(camera("II", "Canon", "Canon EOS REBEL T3i", mn_plain("<", canon_mn(INFO_600D)), gps=False)))
    cli("canon_kiss.jpg", jpeg(camera("II", "Canon", "Canon EOS Kiss X5", mn_plain("<", canon_mn(INFO_600D)), gps=False)))
    cli("canon_600dx.jpg", jpeg(camera("II", "Canon", "Canon EOS 600DX", mn_plain("<", canon_mn(INFO_600D)), gps=False)))
    cli("canon_r5.jpg", jpeg(camera("II", "Canon", "Canon EOS R5", mn_plain("<", canon_mn(INFO_5D3)), gps=False)))
    cli("canon_big.jpg", jpeg(camera("II", "Canon", "Canon EOS 5D Mark III", mn_plain("<", canon_mn(INFO_BIG)), gps=False)))
    cli("canon_short.jpg", jpeg(camera("II", "Canon", "Canon EOS 5D", mn_plain("<", canon_mn(INFO_5D[:150])), gps=False)))
    cli("canon_shortinfo.jpg", jpeg(camera("II", "Canon", "Canon EOS 5D", mn_plain("<", canon_mn(None, [(0x000D, 3, [1, 2, 3])])),
                                           gps=False)))
    cli("canon_nomodel.jpg", jpeg(tiff("II", [("ifd0", [(0x010F, 2, "Canon"), (0x8769, 4, Ptr("exif"))], None),
                                              ("exif", [(0x927C, 7, mn_plain("<", canon_mn(INFO_5D)))], None)])))
    # -- JPEG segment layouts
    plain = camera("MM", "Panasonic", "DMC-GH5", None, comment=b"ASCII\x00\x00\x00Lake Bled at dawn   ")
    cli("gh5.jpg", jpeg(plain))
    cli("gh5_jfif.jpg", jpeg(plain, [JFIF]))
    cli("gh5_jfif_jfxx.jpg", jpeg(plain, [JFIF, JFXX]))
    cli("gh5_icc.jpg", jpeg(plain, [ICC]))
    cli("gh5_jfif_icc.jpg", jpeg(plain, [JFIF, ICC]))
    cli("gh5_adobe.jpg", jpeg(plain, [seg(0xEE, b"Adobe\x00\x64\x00\x00\x00\x00\x01"), seg(0xEC, b"Ducky\x00\x01")]))
    cli("gh5_xmp_first.jpg", jpeg(plain, [seg(0xE1, b"http://ns.adobe.com/xap/1.0/\x00<x/>")]))
    cli("gh5_com.jpg", jpeg(plain, [seg(0xFE, b"Edited with GIMP")]))
    cli("gh5_double_soi.jpg", jpeg(plain, [b"\xff\xd8\x00\x02"]))
    cli("noexif.jpg", jpeg(b"", [JFIF], app1=False))
    cli("noexif_raw.jpg", b"\xff\xd8" + DQT + SCAN)
    cli("trunc_app0.jpg", b"\xff\xd8\xff\xe0")
    cli("trunc_soi.jpg", b"\xff\xd8")
    cli("trunc_app1.jpg", jpeg(plain)[:40])
    cli("garbage_after_soi.jpg", b"\xff\xd8\x12\x34\x56")
    cli("jfif_short.jpg", b"\xff\xd8\xff\xe0\x00\x04JF")
    # -- PNG, WebP, HEIC, JPEG XL
    cli("screenshot.png", png(plain))
    cli("screenshot_text.png", png(plain, [chunk(b"tEXt", b"Software\x00GIMP")]))
    cli("noexif.png", png(None))
    cli("trunc.png", png(plain)[:30])
    cli("odd_chunk.png", png(plain, [b"\x00\x00\x00\x02\xc3\xa9\x41\x41" + b"zz" + bytes(4)]))
    cli("photo.webp", webp([VP8, riff(b"EXIF", b"Exif\x00\x00" + plain)]))
    cli("photo_iccp.webp", webp([riff(b"ICCP", bytes(5)), VP8, riff(b"EXIF", b"Exif\x00\x00" + plain)]))
    cli("photo_odd_unpadded.webp", webp([riff(b"ICCP", bytes(5), pad=False), VP8,
                                          riff(b"EXIF", b"Exif\x00\x00" + plain)]))
    cli("photo_noprefix.webp", webp([VP8, riff(b"EXIF", plain)]))
    cli("noexif_flag.webp", webp([VP8, riff(b"EXIF", b"Exif\x00\x00" + plain)], flags=0x10))
    cli("simple.webp", b"RIFF" + struct.pack("<I", 4 + len(VP8)) + b"WEBP" + VP8)
    cli("trunc.webp", webp([VP8]))
    pix = camera("MM", "Google", "Pixel 8", None)
    cli("pixel.heic", heic(struct.pack(">I", 6) + b"Exif\x00\x00" + pix))
    cli("pixel.heic", heic(struct.pack(">I", 6) + b"Exif\x00\x00" + pix), "b")
    job("gps", "-", "pixel.heic", heic(struct.pack(">I", 6) + b"Exif\x00\x00" + pix))
    app1 = struct.pack(">I", 10) + b"\xff\xe1\x12\x34Exif\x00\x00" + pix
    cli("android_q.heic", heic(app1, iloc_version=1, sizes=(4, 4, 4, 0)))
    cli("iloc_v2.heic", heic(struct.pack(">I", 6) + b"Exif\x00\x00" + pix, iloc_version=2, sizes=(8, 8, 0, 4),
                             infe_version=3, exif_id=70000))
    cli("photo.avif", heic(struct.pack(">I", 6) + b"Exif\x00\x00" + pix, brand=b"avif"))
    cli("photo.mif1", heic(struct.pack(">I", 6) + b"Exif\x00\x00" + pix, brand=b"mif1"))
    cli("nokia.heif", heic(struct.pack(">I", 0) + pix))
    pix_ii = camera("II", "HMD Global", "Nokia 8.3 5G", None)
    cli("nokia_ii.heif", heic(struct.pack(">I", 0) + pix_ii))
    cli("nokia_short.heif", ftyp(b"heic") + box(b"meta", bytes(4)) + b"II")
    cli("minor1.heic", heic(struct.pack(">I", 6) + b"Exif\x00\x00" + pix, minor=1))
    cli("noexif_item.heic", heic(struct.pack(">I", 6) + b"Exif\x00\x00" + pix, exif_id=2, loc_id=2,
                                 infe_version=1))
    cli("lost_item.heic", heic(struct.pack(">I", 6) + b"Exif\x00\x00" + pix, loc_id=9))
    cli("two_extents.heic", heic(struct.pack(">I", 6) + b"Exif\x00\x00" + pix, extents=[(0, 4), (4, 4)]))
    cli("iloc_v3.heic", heic(struct.pack(">I", 6) + b"Exif\x00\x00" + pix, iloc_version=3))
    cli("bad_size.heic", heic(struct.pack(">I", 6) + b"Exif\x00\x00" + pix, sizes=(3, 4, 0, 0)))
    cli("short_hdr.heic", heic(struct.pack(">I", 2) + b"Exif\x00\x00" + pix))
    cli("wrong_hdr.heic", heic(struct.pack(">I", 6) + b"Exof\x00\x00" + pix))
    cli("trunc.heic", heic(struct.pack(">I", 6) + b"Exif\x00\x00" + pix)[:300])
    cli("no_meta.heic", ftyp(b"heic") + box(b"free", bytes(8)))
    # meta without iinf/iloc: exifread keeps the last file's boxes (Box.subs is a class attribute)
    cli("stale_boxes.heic", heic(struct.pack(">I", 6) + b"Exif\x00\x00" + pix, iinf=False, with_iloc=False))
    cli("photo.jxl", jxl(pix))
    cli("photo.jxl", jxl(pix), "q")
    cli("bad_brand.jxl", jxl(pix, b"jxlx"))
    cli("noexif.jxl", jxl(pix, exif=False))
    cli("notes.txt", b"These are not the photos you are looking for.\n")
    cli("empty.bin", b"")
    cli("gif89a.gif", b"GIF89a\x01\x00\x01\x00\x00\x00\x00;")
    # -- TIFF structure and broken files
    e = [(0x010F, 2, "Leica Camera AG"), (0x0110, 2, "LEICA Q2")]
    cli("loop.tif", broken_tiff("II", e, [("ifd1", [(0x0100, 3, [640])], "ifd0")], nxt="ifd1"))
    cli("self_next.tif", broken_tiff("II", e, nxt=8))
    cli("three_ifds.tif", tiff("MM", [("ifd0", e, "ifd1"), ("ifd1", [(0x0100, 4, [160]), (0x0101, 4, [120])], "ifd2"),
                                      ("ifd2", [(0x0100, 4, [32]), (0x0101, 4, [24])], None)]))
    cli("bad_type.tif", broken_tiff("II", e + [(0x0131, 17, b"abcd"), (0x0132, 0, b"\x00\x00\x00\x00")]))
    cli("bad_type.tif", broken_tiff("II", e + [(0x0131, 17, b"abcd"), (0x0132, 0, b"\x00\x00\x00\x00")]), "s")
    cli("bad_type0.tif", broken_tiff("II", e + [(0x0132, 0, b"\x00\x00\x00\x00")]), "s")
    cli("past_eof.tif", broken_tiff("II", e + [(0x0131, 2, At(20, 5000)), (0x0132, 4, At(3, 5000)),
                                               (0x013B, 3, At(3, 0x6A))]))
    cli("bad_utf8.tif", broken_tiff("II", e + [(0x013B, 2, b"Bj\xf6rk Gu\xf0mundsd\xf3ttir\x00")]))
    cli("bad_utf8.tif", broken_tiff("II", e + [(0x013B, 2, b"Bj\xf6rk Gu\xf0mundsd\xf3ttir\x00")]), "b")
    cli("utf8.tif", broken_tiff("II", e + [(0x013B, 2, "Ana María Muñoz"), (0x8298, 2, "© 2024")]))
    cli("utf8.tif", broken_tiff("II", e + [(0x013B, 2, "Ana María Muñoz"), (0x8298, 2, "© 2024")]),
        "b")
    cli("after_nul.tif", broken_tiff("II", e + [(0x0131, 2, b"GIMP 2.10\x00\xff\xfejunk\x00")]))
    cli("empty_ascii.tif", broken_tiff("II", e + [(0x0131, 2, Raw(0, b"")), (0x013B, 2, b"\x00\x00\x00\x00\x00"),
                                                  (0x8298, 2, b"   \x00")]))
    cli("empty_ascii.tif", broken_tiff("II", e + [(0x0131, 2, Raw(0, b"")), (0x013B, 2, b"\x00\x00\x00\x00\x00"),
                                                  (0x8298, 2, b"   \x00")]), "b")
    ratios = [(0x011A, 5, [(0, 0)]), (0x011B, 5, [(300, 0)]), (0x9204, 10, [(-2, 6)]), (0x9201, 10, [(5, -10)]),
              (0x829A, 5, [(10, 4000)]), (0x829D, 5, [(56, 10)]), (0x920A, 5, [(9, 2)])]
    rt = broken_tiff("MM", e + ratios)
    cli("ratios.tif", rt)
    cli("ratios.tif", rt, "b")
    nums = [(0x0100, 3, [65535]), (0x0101, 8, [-32768]), (0x0102, 3, [8, 8, 8]), (0x0115, 6, [-5]),
            (0x013E, 9, [-1, 2147483647, -2147483648]), (0x0140, 3, list(range(60))),
            (0xC612, 1, list(range(1, 61))), (0xA20E, 11, [0.1, -2.5, 3.0e38]), (0xA20F, 12, [1e-300, 2.0 / 3]),
            (0x0153, 11, [float("inf")]), (0x0154, 12, [float("nan")]), (0xC4A5, 7, b"PrintIM\x000300"),
            (0x9C9B, 1, "Title".encode("utf-16-le") + b"\x00\x00"), (0x9C9D, 1, "Ana".encode("utf-16-le") + b"\x00\x00")]
    nt = broken_tiff("II", e + nums)
    cli("numbers.tif", nt)
    cli("numbers.tif", nt, "b")
    cli("ifd_type.tif", broken_tiff("II", e + [(0xC7A1, 13, [300, 400]), (0xC7A2, 13, [7])]))
    cli("ifd_type.tif", broken_tiff("II", e + [(0xC7A1, 13, [300, 400]), (0xC7A2, 13, [7])]), "b")
    cli("bad_date.tif", broken_tiff("II", e + [(0x0132, 2, b"2024:05:17 14:32:\xff\xfe\x00")]))
    cli("bad_date.tif", broken_tiff("II", e + [(0x0132, 2, b"2024:05:17 14:32:\xff\xfe\x00")]), "b")
    big = [(0xC4A5, 7, bytes(1200)), (0x0140, 3, list(range(1000))), (0x9286, 7, Raw(1500, bytes(8)))]
    cli("big_counts.tif", broken_tiff("II", e + big))
    cli("big_counts.tif", broken_tiff("II", e + big), "b")
    cli("double_eof.tif", broken_tiff("II", e + [(0xA20F, 12, At(1, 9000))]))
    cli("float_eof.tif", broken_tiff("II", e + [(0xA20E, 11, At(2, 9000)), (0xA20F, 12, At(2, 9000))]))
    cli("float_eof.tif", broken_tiff("II", e + [(0xA20E, 11, At(2, 9000)), (0xA20F, 12, At(2, 9000))]), "b")
    cli("ascii_bytes_long.tif", broken_tiff("II", e + [(0x0131, 2, bytes(range(128, 200)) + b"\x00")]))
    # dictionary lookups fed odd values
    look = [(0x0112, 5, [(6, 1)]), (0x0128, 3, [2, 3, 9]), (0x8822, 2, "AB"), (0x9207, 3, [255]),
            (0x9209, 10, [(1, 2)]), (0xA401, 7, bytes([1, 0])), (0xA406, 11, [1.0]), (0x0103, 3, [])]
    lt = broken_tiff("II", e + look)
    cli("lookups.tif", lt)
    cli("lookups.tif", lt, "b")
    # UserComment and make_string
    for i, uc in enumerate([b"ASCII\x00\x00\x00Kayaking the fjord", b"UNICODE\x00" + "Fjord".encode("utf-16-le"),
                            bytes(8) + b"After the rain", b"JIS\x00\x00\x00\x00\x00\x1b$B", b"SJIS\x00\x00\x00\x00hello",
                            bytes(24), b"ascii\x00\x00\x00  spaced  ", b"\x01\x02\x03\x04\x05\x06\x07\x08\x09"]):
        cli("comment%d.jpg" % i, jpeg(camera("II", "Panasonic", "DC-S5", None, gps=False, comment=uc)))
    cli("comment_b.jpg", jpeg(camera("II", "Panasonic", "DC-S5", None, gps=False, comment=bytes(24))), "b")
    strs = [(0x9000, 3, [48, 50, 51, 50]), (0xA000, 2, "  0100\x00"), (0x9C9D, 7, bytes([1, 2, 3])),
            (0x011D, 5, [(65, 1), (66, 1)]), (0x9C9F, 1, b"\xe9t\xe9")]
    cli("make_string.tif", broken_tiff("II", e + strs))
    cli("make_string.tif", broken_tiff("II", e + strs), "b")
    cli("make_string_u.tif", broken_tiff("II", e + [(0x9286, 2, "ASCII   hello")]))
    cli("make_string_f.tif", broken_tiff("II", e + [(0x9000, 11, [1.5, 2.0])]))
    # pointers that are not offsets
    cli("gps_ratio.tif", broken_tiff("II", e + [(0x8825, 5, [(8, 1)])]))
    cli("gps_ascii.tif", broken_tiff("II", e + [(0x8825, 2, "ab")]))
    cli("gps_empty.tif", broken_tiff("II", e + [(0x8825, 4, Raw(0, b""))]))
    cli("gps_float.tif", broken_tiff("II", e + [(0x8825, 11, [8.0])]))
    cli("exif_ascii.tif", broken_tiff("II", e + [(0x8769, 2, "ab")]))
    cli("exif_empty.tif", broken_tiff("II", e + [(0x8769, 4, Raw(0, b""))]))
    cli("exif_eof.tif", broken_tiff("II", e + [(0x8769, 4, [7000])]))
    cli("exif_short.tif", broken_tiff("II", e + [(0x8769, 3, [8])]))
    cli("subifds.dng", subifd_tiff())
    cli("subifds.dng", subifd_tiff(), "q")
    cli("subifds.dng", subifd_tiff(), "b")
    cli("subifd_ascii.dng", broken_tiff("II", e + [(0x014A, 2, "xy")]))
    # stop tags
    cli("nikon_d70.nef", d70, "t=Make")
    cli("nikon_d70.nef", d70, "t=GPSLatitude")
    cli("nikon_d70.nef", d70, "t=MakerNote")
    cli("nikon_d70.nef", d70, "t=ExifOffset")
    cli("nikon_d70.nef", d70, "t=Tag 0x0213")
    cli("nikon_d70.nef", d70, "t=YCbCrPositioning")
    # quick mode skips XMP, MakerNote and UserComment
    xq = camera("II", "SONY", "ILCE-1", mn_plain("<", SONY), comment=b"ASCII\x00\x00\x00hi",
                i0=[(0x02BC, 1, b"<x:xmpmeta/>")])
    cli("sony_xmp.arw", xq)
    cli("sony_xmp.arw", xq, "q")
    cli("sony_xmp.arw", xq, "t=MakerNote,q")
    # GPS
    job("gps", "-", "south_east.jpg", jpeg(tiff("II", [("ifd0", [(0x8825, 4, Ptr("gps"))], None),
                                                         ("gps", gps_entries((33, 51, 3540, 100), (151, 12, 2040, 100),
                                                                             "S", "E"), None)])))
    job("gps", "b", "south_east.jpg", jpeg(tiff("II", [("ifd0", [(0x8825, 4, Ptr("gps"))], None),
                                                         ("gps", gps_entries((33, 51, 3540, 100), (151, 12, 2040, 100),
                                                                             "S", "E"), None)])))
    job("gps", "-", "equator.jpg", jpeg(tiff("MM", [("ifd0", [(0x8825, 4, Ptr("gps"))], None),
                                                      ("gps", gps_entries((0, 0, 0, 1), (0, 0, 0, 1), "S", "W"),
                                                       None)])))
    job("gps", "-", "nogps.jpg", jpeg(plain))
    g2 = [(0x0001, 2, "N"), (0x0002, 5, [(51, 1), (30, 1)]), (0x0003, 2, "W"), (0x0004, 5, [(0, 1), (7, 1)])]
    job("gps", "-", "gps_two.jpg", jpeg(tiff("II", [("ifd0", [(0x8825, 4, Ptr("gps"))], None), ("gps", g2, None)])))
    g4 = [(0x0001, 2, "N"), (0x0002, 5, [(51, 1), (30, 1), (1, 1), (2, 1)]), (0x0003, 2, "W"),
          (0x0004, 5, [(0, 1), (7, 1), (3, 1)])]
    job("gps", "-", "gps_four.jpg", jpeg(tiff("II", [("ifd0", [(0x8825, 4, Ptr("gps"))], None), ("gps", g4, None)])))
    g0 = [(0x0001, 2, "N"), (0x0002, 5, Raw(0, b"")), (0x0003, 2, "W"), (0x0004, 5, Raw(0, b""))]
    job("gps", "-", "gps_none.jpg", jpeg(tiff("II", [("ifd0", [(0x8825, 4, Ptr("gps"))], None), ("gps", g0, None)])))
    gz = [(0x0001, 2, "N"), (0x0002, 5, [(51, 1), (30, 1), (0, 0)]), (0x0003, 2, "W"),
          (0x0004, 5, [(0, 1), (7, 1), (3, 1)])]
    job("gps", "-", "gps_zero.jpg", jpeg(tiff("II", [("ifd0", [(0x8825, 4, Ptr("gps"))], None), ("gps", gz, None)])))
    job("gps", "b", "gps_zero.jpg", jpeg(tiff("II", [("ifd0", [(0x8825, 4, Ptr("gps"))], None), ("gps", gz, None)])))
    gs = [(0x0001, 2, "N"), (0x0002, 3, [51, 30, 26]), (0x0003, 2, "W"), (0x0004, 3, [0, 7, 39])]
    job("gps", "-", "gps_short.jpg", jpeg(tiff("II", [("ifd0", [(0x8825, 4, Ptr("gps"))], None), ("gps", gs, None)])))
    job("gps", "b", "gps_short.jpg", jpeg(tiff("II", [("ifd0", [(0x8825, 4, Ptr("gps"))], None), ("gps", gs, None)])))
    gr = [(0x0001, 1, [78]), (0x0002, 10, [(-51, 1), (30, 1), (2652, 100)]), (0x0003, 2, "W"),
          (0x0004, 5, [(0, 1), (7, 1), (3972, 100)])]
    job("gps", "-", "gps_signed.jpg", jpeg(tiff("II", [("ifd0", [(0x8825, 4, Ptr("gps"))], None), ("gps", gr, None)])))
    job("gps", "b", "gps_signed.jpg", jpeg(tiff("II", [("ifd0", [(0x8825, 4, Ptr("gps"))], None), ("gps", gr, None)])))
    job("gps", "-", "pixel.webp", webp([VP8, riff(b"EXIF", b"Exif\x00\x00" + pix)]))
    # thumbnails
    job("thumb", "-", "canon_5d3.cr2", c5d3)
    job("thumb", "-", "gh5.jpg", jpeg(plain))
    tl = tiff("II", [("ifd0", e, "ifd1"), ("ifd1", [(0x0103, 3, [6]), (0x0201, 4, [8]), (0x0202, 4, [4000])], None)])
    job("thumb", "-", "thumb_long.tif", tl)
    tu = tiff("II", [("ifd0", e, "ifd1"), ("ifd1", [(0x0103, 3, [1]), (0x0111, 4, [8]), (0x0117, 4, [16])], None)])
    job("thumb", "-", "thumb_uncompressed.tif", tu)
    cli("thumb_uncompressed.tif", tu)

    os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
    with open(os.path.join(HERE, "data", "jobs.tsv"), "w", encoding="utf-8") as fh:
        for j in JOBS:
            fh.write("\t".join(j) + "\n")


def subifd_tiff():
    e = [(0x010F, 2, "Leica Camera AG"), (0x0110, 2, "LEICA M11")]
    sub = [("sub0", [(0x00FE, 4, [1]), (0x0100, 4, [512]), (0x0101, 4, [384])], None),
           ("sub1", [(0x00FE, 4, [0]), (0x0100, 4, [6000]), (0x0103, 3, [7])], None)]
    # the SubIFDs pointer list is written once the sub IFDs have positions
    probe = tiff("II", [("ifd0", e + [(0x014A, 4, [0, 0])], None)] + sub)
    p0 = 8 + block_size("<", e + [(0x014A, 4, [0, 0])])
    p1 = p0 + block_size("<", sub[0][1])
    out = tiff("II", [("ifd0", e + [(0x014A, 4, [p0, p1])], None)] + sub)
    assert len(out) == len(probe)
    return out


main()
