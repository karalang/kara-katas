"""Write data/: the image files, the jobs that probe them and the inputs of
the three programs.

The images are built here byte by byte, as their formats lay them out:
real headers (PNG chunks with CRCs, JPEG markers, JP2 boxes, TIFF IFDs,
RIFF chunks) over small bodies, plus broken and truncated variants.

Run: python3 -s -P -B mk.py
"""
import os
import struct
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")
IMG = os.path.join(D, "images")
os.makedirs(IMG, exist_ok=True)

FILES = []
JOBS = []


def put(name, data):
    with open(os.path.join(IMG, name), "wb") as f:
        f.write(data)
    FILES.append(name)
    JOBS.append("images/%s" % name)


def section(title):
    JOBS.append("# " + title)


# ------------------------------------------------------------ PNG

section("PNG: the IHDR size, and the pHYs density getDPI reads")

def chunk(kind, body):
    return struct.pack(">L", len(body)) + kind + body + struct.pack(">L", zlib.crc32(kind + body))


SIG = b"\x89PNG\r\n\x1a\n"


def png(w, h, extra=(), bit_depth=8, color=2):
    raw = b""
    for _ in range(min(h, 2)):
        raw += b"\0" + b"\x80" * (min(w, 4) * 3)
    out = SIG + chunk(b"IHDR", struct.pack(">LLBBBBB", w, h, bit_depth, color, 0, 0, 0))
    for c in extra:
        out += c
    return out + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")


def phys(x, y, unit):
    return chunk(b"pHYs", struct.pack(">LLB", x, y, unit))


put("photo.png", png(1920, 1080, [chunk(b"sRGB", b"\0"), phys(2835, 2835, 1)]))
put("logo.png", png(512, 512, [chunk(b"gAMA", struct.pack(">L", 45455))], color=6))
put("scan_aspect.png", png(2480, 3508, [phys(1, 1, 0)]))
put("retina.png", png(750, 1334, [chunk(b"tEXt", b"Software\0Kara mk.py"),
                                  chunk(b"tEXt", b"Comment\0two text chunks first"),
                                  phys(5669, 5669, 1)]))
put("screen96.png", png(1366, 768, [phys(3780, 3779, 1)]))
put("print300.png", png(3300, 2550, [phys(11811, 11811, 1)]))
put("icon16.png", png(16, 16, color=3, extra=[chunk(b"PLTE", b"\0\0\0\xff\xff\xff")]))
# pHYs before IHDR: the 24 bytes getDPI reads hold only half the chunk
put("phys_first.png", SIG + phys(2835, 2835, 1) + png(10, 10)[8:])
# A chain of chunks that ends before any pHYs or IDAT
put("no_idat.png", SIG + chunk(b"IHDR", struct.pack(">LLBBBBB", 64, 48, 8, 2, 0, 0, 0)) +
    chunk(b"tEXt", b"Title\0cut short"))
put("short20.png", png(800, 600)[:20])
put("short12.png", png(800, 600)[:12])
# An IHDR chunk under another name: the older-PNG branch reads bytes 8..16
put("not_ihdr.png", SIG + chunk(b"CgBI", b"\x50\x00\x20\x02") + png(57, 57)[8:])

# ------------------------------------------------------------ GIF

section("GIF: the logical screen size")

def gif(ver, w, h):
    return ver + struct.pack("<HH", w, h) + b"\xf7\x00\x00" + b"\0" * 24 + b"\x2c" + \
        struct.pack("<HHHH", 0, 0, w, h) + b"\x00\x02\x02\x44\x01\x00\x3b"


put("anim.gif", gif(b"GIF89a", 480, 270))
put("old.gif", gif(b"GIF87a", 320, 200))
put("pixel.gif", gif(b"GIF89a", 1, 1))
put("wide.gif", gif(b"GIF89a", 40000, 300))
put("short9.gif", b"GIF89a\x10\x00\x10")

# ------------------------------------------------------------ JPEG

section("JPEG: the SOFn frame size, and the JFIF density getDPI reads")

def seg(marker, body):
    return b"\xff" + bytes([marker]) + struct.pack(">H", len(body) + 2) + body


def jfif(unit, x, y):
    return seg(0xE0, b"JFIF\0\x01\x02" + struct.pack(">BHH", unit, x, y) + b"\0\0")


def sof(marker, w, h):
    return seg(marker, struct.pack(">BHHB", 8, h, w, 3) + b"\x01\x22\x00\x02\x11\x01\x03\x11\x01")


DQT = seg(0xDB, b"\x00" + bytes(range(1, 65)))
DHT = seg(0xC4, b"\x00" + b"\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00" + bytes(range(12)))
SOS = seg(0xDA, b"\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00") + b"\x12\x34\x56\x78\x9a" + b"\xff\xd9"
EXIF = seg(0xE1, b"Exif\0\0MM\0\x2a\0\0\0\x08\0\x01\x01\x12\0\x03\0\0\0\x01\0\x01\0\0" + b"\0" * 40)

put("jfif72.jpg", b"\xff\xd8" + jfif(1, 72, 72) + DQT + sof(0xC0, 640, 480) + DHT + SOS)
put("jfif_cm.jpg", b"\xff\xd8" + jfif(2, 118, 118) + DQT + sof(0xC0, 2480, 3508) + DHT + SOS)
put("jfif_aspect.jpg", b"\xff\xd8" + jfif(0, 1, 1) + DQT + sof(0xC0, 800, 600) + DHT + SOS)
put("jfif_unit3.jpg", b"\xff\xd8" + jfif(3, 300, 300) + DQT + sof(0xC0, 100, 100) + DHT + SOS)
put("camera.jpg", b"\xff\xd8" + EXIF + DQT + sof(0xC0, 4032, 3024) + DHT + SOS)
put("progressive.jpg", b"\xff\xd8" + jfif(1, 96, 96) + DQT + DHT + sof(0xC2, 1024, 768) + SOS)
put("dht_first.jpg", b"\xff\xd8" + DQT + DHT + sof(0xC0, 1200, 800) + SOS)
put("fill_bytes.jpg", b"\xff\xd8" + jfif(1, 300, 300) + b"\xff\xff\xff" + DQT + b"\xff\xff" +
    sof(0xC1, 2000, 1500) + SOS)
put("lossless.jpg", b"\xff\xd8" + DQT + seg(0xC8, b"JPG ext") + sof(0xC3, 512, 512) + SOS)
put("arith.jpg", b"\xff\xd8" + DQT + seg(0xCC, b"\x00\x11") + sof(0xC9, 333, 222) + SOS)
put("cut_after_app0.jpg", b"\xff\xd8" + jfif(1, 72, 72))
put("cut_in_sof.jpg", b"\xff\xd8" + jfif(1, 72, 72) + DQT + sof(0xC0, 640, 480)[:7])
put("cut_in_app0.jpg", b"\xff\xd8" + jfif(1, 72, 72)[:9])
put("cut_in_exif.jpg", b"\xff\xd8" + EXIF[:30])
put("soi_only.jpg", b"\xff\xd8")

# ------------------------------------------------------------ JPEG 2000

section("JPEG 2000: the ihdr box, and the resd box getDPI reads")

def box(kind, body):
    return struct.pack(">L", len(body) + 8) + kind + body


JP2_SIG = b"\x00\x00\x00\x0cjP  \r\n\x87\n"
FTYP = box(b"ftyp", b"jp2 \0\0\0\0jp2 ")


def ihdr(w, h):
    return box(b"ihdr", struct.pack(">LLHBBBB", h, w, 3, 7, 7, 0, 0))


COLR = box(b"colr", b"\x01\x00\x00\x00\x00\x00\x10")


def jp2(w, h, extra=b"", tail=b""):
    header = ihdr(w, h) + COLR + extra
    return JP2_SIG + FTYP + box(b"jp2h", header) + tail + box(b"jp2c", b"\xff\x4f\xff\x51" + b"\0" * 20)


def resd(vn, hn, vu, hu):
    return box(b"resd", struct.pack(">HHHHbb", vn, 1, hn, 1, vu, hu))


put("plain.jp2", jp2(1024, 768))
put("resd.jp2", jp2(800, 600, box(b"res ", resd(300, 300, 0, 0))))
put("resc_only.jp2", jp2(800, 600, box(b"res ", box(b"resc", struct.pack(">HHHHbb", 72, 1, 72, 1, 0, 0)))))
# A resd box cut after six bytes, so read(10) gets exactly the six
# that ">HHBB" unpacks: the vertical numerator, the vertical denominator
# read as the horizontal density, then the two bytes of the horizontal
# numerator read as the units
cut = JP2_SIG + FTYP + box(b"jp2h", ihdr(640, 480) + COLR + box(b"res ", resd(118, 2 << 8 | 3, 0, 0)))
put("resd_cut.jp2", cut[:-4])
cut2 = JP2_SIG + FTYP + box(b"jp2h", ihdr(640, 480) + COLR + box(b"res ", resd(11811, 4 << 8 | 1, 2, 4)))
put("resd_cut_units.jp2", cut2[:-4])
put("short.jp2", (JP2_SIG + FTYP + box(b"jp2h", ihdr(10, 10)))[:52])

# ------------------------------------------------------------ TIFF

section("TIFF: the first IFD's ImageWidth and ImageLength")

def ifd(order, entries, nxt=0):
    out = struct.pack(order + "H", len(entries))
    for tag, typ, count, value in entries:
        out += struct.pack(order + "HHL", tag, typ, count) + value
    return out + struct.pack(order + "L", nxt)


def short_be(v):
    return struct.pack(">HH", v, 0)


def long_be(v):
    return struct.pack(">L", v)


put("big_endian.tif", b"MM\0\x2a" + struct.pack(">L", 8) + ifd(">", [
    (254, 4, 1, long_be(0)), (256, 3, 1, short_be(1600)), (257, 3, 1, short_be(1200)),
    (258, 3, 1, short_be(8)), (259, 3, 1, short_be(1))]))
put("big_endian_long.tif", b"MM\0\x2a" + struct.pack(">L", 8) + ifd(">", [
    (256, 4, 1, long_be(70000)), (257, 4, 1, long_be(50000))]))
put("big_endian_rational.tif", b"MM\0\x2a" + struct.pack(">L", 8) + ifd(">", [
    (256, 5, 1, long_be(26)), (257, 4, 1, long_be(10))]))
put("big_endian_bad_height.tif", b"MM\0\x2a" + struct.pack(">L", 8) + ifd(">", [
    (256, 4, 1, long_be(10)), (257, 1, 1, b"\x0a\0\0\0")]))
put("big_endian_no_height.tif", b"MM\0\x2a" + struct.pack(">L", 8) + ifd(">", [
    (256, 3, 1, short_be(640)), (262, 3, 1, short_be(2))]))
put("big_endian_cut.tif", (b"MM\0\x2a" + struct.pack(">L", 8) + ifd(">", [
    (254, 4, 1, long_be(0)), (256, 3, 1, short_be(64)), (257, 3, 1, short_be(64))]))[:30])
put("big_endian_far_ifd.tif", b"MM\0\x2a" + struct.pack(">L", 4000) + b"\0" * 16)
put("little_endian.tif", b"II\x2a\0" + struct.pack("<L", 8) + ifd("<", [
    (256, 3, 1, struct.pack("<HH", 3000, 0)), (257, 3, 1, struct.pack("<HH", 2000, 0)),
    (277, 3, 1, struct.pack("<HH", 3, 0))]))
# A SHORT value with junk in the unused half: the LE reader takes all four bytes
put("little_endian_junk.tif", b"II\x2a\0" + struct.pack("<L", 8) + ifd("<", [
    (256, 3, 1, struct.pack("<HH", 300, 1)), (257, 4, 1, struct.pack("<L", 200))]))
put("camera_raw.dng", b"II\x2a\0" + struct.pack("<L", 16) + b"\0" * 8 + ifd("<", [
    (254, 4, 1, struct.pack("<L", 1)), (256, 4, 1, struct.pack("<L", 256)),
    (257, 4, 1, struct.pack("<L", 171)), (271, 2, 6, struct.pack("<L", 200))]))
put("little_endian_empty.tif", b"II\x2a\0" + struct.pack("<L", 8) + ifd("<", []))


def bigtiff(entries, bytesize=8):
    out = b"II\x2b\0" + struct.pack("<HHQ", bytesize, 0, 16)
    out += struct.pack("<Q", len(entries))
    for tag, typ, count, value in entries:
        out += struct.pack("<HHQQ", tag, typ, count, value)
    return out + struct.pack("<Q", 0)


put("big.tif", bigtiff([(256, 16, 1, 100000), (257, 16, 1, 80000)]))
put("big_no_width.tif", bigtiff([(257, 4, 1, 80)]))
put("big_bad_bytesize.tif", bigtiff([(256, 4, 1, 10), (257, 4, 1, 10)], bytesize=4))
put("big_short.tif", b"II\x2b\0\x08\0\0\0\x10\0")

# ------------------------------------------------------------ SVG

section("SVG: the width and height attributes in the first 1024 bytes")

def svg(attrs, pre=b"", body=b'<rect width="10" height="10"/>'):
    return pre + b"<svg xmlns=\"http://www.w3.org/2000/svg\" " + attrs + b">" + body + b"</svg>\n"


put("icon.svg", svg(b'width="24" height="24" viewBox="0 0 24 24"'))
put("a4.svg", svg(b'width="210mm" height="297mm"', pre=b'<?xml version="1.0" encoding="UTF-8"?>\n'))
put("letter.svg", svg(b'width="8.5in" height="11in"'))
put("card.svg", svg(b'width="10cm" height="6.5cm"'))
put("type.svg", svg(b'width="72pt" height="36pc"'))
put("pixels.svg", svg(b'width="300px" height="150.75px"'))
put("stroke_first.svg", svg(b'stroke-width="2" data-height="1" width="48" height="32"'))
put("percent.svg", svg(b'width="100%" height="100%"'))
put("em.svg", svg(b'width="10em" height="5em"'))
put("empty_width.svg", svg(b'width="" height="10"'))
put("unit_only.svg", svg(b'width="px" height="10"'))
put("viewbox_only.svg", svg(b'viewBox="0 0 100 50"'))
put("single_quotes.svg", svg(b"width='24' height='24'"))
put("exponent.svg", svg(b'width="1e3" height="5"'))
put("trailing_dot.svg", svg(b'width="12." height="5"'))
put("upper_unit.svg", svg(b'width="10PX" height="5"'))
put("late_width.svg", svg(b'width="40" height="30"', pre=b"<?xml version=\"1.0\"?>\n<!-- " + b"x" * 1100 + b" -->\n"))
# 1024 bytes end inside a three-byte character, so the decode fails
head = b'<svg xmlns="http://www.w3.org/2000/svg" width="40" height="30"><!-- '
put("split_utf8.svg", head + b"y" * (1022 - len(head)) + " — ".encode()[1:] + b"-->" + b"</svg>\n")
put("nl_in_value.svg", svg(b'width="4\n0" height="30" width="12"'))
put("leading_space.svg", b"  " + svg(b'width="40" height="30"'))
put("utf8_title.svg", svg(b'width="64" height="64"', body="<title>Café — logo</title>".encode()))

# ------------------------------------------------------------ Netpbm

section("Netpbm: the first two numbers of the header")

put("ascii.pbm", b"P1\n# CREATOR: GIMP PNM Filter\n8 4\n" + b"0 1 0 1 0 1 0 1\n" * 4)
put("binary.pbm", b"P4\n16 2\n" + b"\xaa\x55" * 2)
put("gray.pgm", b"P5 640 480 255\n" + b"\x80" * 32)
put("ascii.pgm", b"P2\n\t3\t2\n15\n0 7 15\n15 7 0\n")
put("color.ppm", b"P6\n# made by mk.py\n# second comment\n1280\n# between\n720\n255\n" + b"\0" * 12)
put("ascii.ppm", b"P3\r\n2 1\r\n255\r\n255 0 0  0 255 0\r\n")
put("comment_after.pgm", b"P2 640# width\n480 255\n")
put("eof_after_width.ppm", b"P6\n640")
put("letters.ppm", b"P6 abc 12\n")
put("only_p.pnm", b"P")
put("pam.pam", b"P7\nWIDTH 4\nHEIGHT 2\nDEPTH 3\nMAXVAL 255\nTUPLTYPE RGB\nENDHDR\n")

# ------------------------------------------------------------ WebP

section("WebP: the VP8, VP8L and VP8X headers")

def riff(chunks):
    return b"RIFF" + struct.pack("<L", 4 + len(chunks)) + b"WEBP" + chunks


def vp8(w, h, sw=0, sh=0):
    frame = b"\x9d\x01\x2a" + struct.pack("<HH", w | (sw << 14), h | (sh << 14))
    body = b"\x50\x02\x00" + frame + b"\0" * 10
    return riff(b"VP8 " + struct.pack("<L", len(body)) + body)


def vp8l(w, h):
    bits = (w - 1) | ((h - 1) << 14) | (1 << 28)
    body = b"\x2f" + struct.pack("<L", bits) + b"\0" * 6
    return riff(b"VP8L" + struct.pack("<L", len(body)) + body)


def vp8x(w, h):
    body = b"\x10\0\0\0" + struct.pack("<L", w - 1)[:3] + struct.pack("<L", h - 1)[:3]
    return riff(b"VP8X" + struct.pack("<L", len(body)) + body + b"ALPH" + struct.pack("<L", 2) + b"\0\0")


put("lossy.webp", vp8(1024, 683))
put("lossy_scaled.webp", vp8(300, 200, 1, 2))
put("lossless.webp", vp8l(400, 301))
put("lossless_big.webp", vp8l(16384, 9))
put("extended.webp", vp8x(1920, 1080))
put("anim.webp", riff(b"ANIM" + struct.pack("<L", 6) + b"\0" * 6))
put("short_vp8l.webp", vp8l(10, 10)[:23])
put("short_vp8.webp", vp8(10, 10)[:27])
put("short_vp8x.webp", vp8x(10, 10)[:25])

# ------------------------------------------------------------ the rest

section("formats imagesize does not know")

put("image.bmp", b"BM" + struct.pack("<LHHL", 70, 0, 0, 54) + struct.pack("<LllHH", 40, 2, 2, 1, 24) + b"\0" * 32)
put("favicon.ico", b"\0\0\1\0\1\0\x10\x10\0\0\1\0\x20\0" + b"\0" * 20)
put("empty.png", b"")
put("readme.txt", b"Not an image at all.\n")

with open(os.path.join(D, "jobs.txt"), "w") as f:
    for job in JOBS:
        f.write(job + "\n")
    f.write("# a file that is not there\n")
    f.write("images/missing.png\n")
    f.write("!gallery gallery.tsv\n")
    f.write("!thumbs thumbs.txt\n")
    f.write("!audit page.html\n")

GALLERY = """photo.png\t50\tSunset over the bay
logo.png\t25\tCompany logo
retina.png\t50\tApp screenshot (2x)
camera.jpg\t10\tStreet market
progressive.jpg\t100\tProduct shot
a4.svg\t100\tFloor plan
icon.svg\t200\tMenu icon
card.svg\t33\tBusiness card
lossless.webp\t75\tChart
extended.webp\t50\tHero banner
big_endian.tif\t20\tArchive scan
color.ppm\t100\tRaw frame
percent.svg\t100\tResponsive art
readme.txt\t100\tNotes
"""

THUMBS = """photo.png
logo.png
scan_aspect.png
retina.png
print300.png
jfif72.jpg
jfif_cm.jpg
camera.jpg
fill_bytes.jpg
plain.jp2
resd_cut.jp2
big_endian_long.tif
little_endian.tif
big.tif
lossy.webp
lossless_big.webp
anim.gif
wide.gif
pixel.gif
letter.svg
pixels.svg
binary.pbm
eof_after_width.ppm
favicon.ico
"""

PAGE = """<!doctype html>
<html><head><title>Spring catalogue</title></head>
<body>
<h1>Spring catalogue</h1>
<img src="images/photo.png" width="1920" height="1080" alt="Sunset">
<p>Our new range, photographed on location.</p>
<img src="images/camera.jpg" alt="Market">
<img src="images/progressive.jpg" width="1024" height="700" alt="Product">
<img alt="Logo" src="images/logo.png" height="512" width="512">
<img src="images/lossless.webp" width="400">
<img src="images/a4.svg" width="794" height="1123" alt="Plan">
<img src="images/icon.svg" width="24" height="24">
<img src="images/missing.png" width="10" height="10">
<img src="images/cut_in_sof.jpg" width="640" height="480">
<img src="images/readme.txt" width="1" height="1">
<img src='images/old.gif' width='320' height='200'>
</body></html>
"""

for name, text in [("gallery.tsv", GALLERY), ("thumbs.txt", THUMBS), ("page.html", PAGE)]:
    with open(os.path.join(D, name), "w", encoding="utf-8") as f:
        f.write(text)

with open(os.path.join(D, "files.txt"), "w") as f:
    for name in FILES:
        f.write("images/%s\n" % name)
    f.write("gallery.tsv\nthumbs.txt\npage.html\n")
print(len(FILES), "images")
