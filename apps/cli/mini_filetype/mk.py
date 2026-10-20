# Writes data/: the first bytes of files of each kind filetype knows (as
# the tools that make them write them: PNG and APNG chunks, a JFIF JPEG,
# ISO-BMFF boxes for MP4, HEIC and AVIF, ZIP entries as Word, Excel,
# PowerPoint and LibreOffice lay them out, OLE headers, tar, ELF, zstd
# frames ...), files that sit on the edge of a matcher, and jobs.tsv, the
# jobs oracle.py and mini_filetype.kara run.
import os
import shutil
import struct
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def put(rel, data):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def chunk(kind, body):
    return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))


PNG_SIG = b"\x89PNG\r\n\x1a\n"
IHDR = chunk(b"IHDR", struct.pack(">IIBBBBB", 4, 4, 8, 6, 0, 0, 0))
IDAT = chunk(b"IDAT", zlib.compress(b"\x00" * 68))
IEND = chunk(b"IEND", b"")


def box(kind, body):
    return struct.pack(">I", 8 + len(body)) + kind + body


def ftyp(major, minor, brands):
    return box(b"ftyp", major + struct.pack(">I", minor) + b"".join(brands))


def zip_entry(name, data):
    # a stored ZIP local file header, then the data
    crc = zlib.crc32(data)
    return (b"PK\x03\x04" + struct.pack("<HHHHHIIIHH", 20, 0, 0, 0, 0, crc, len(data), len(data), len(name), 0)
            + name + data)


def zip_of(entries):
    return b"".join(zip_entry(n, d) for n, d in entries) + b"PK\x05\x06" + b"\x00" * 18


CT = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types/>'
RELS = b'<?xml version="1.0"?><Relationships/>'
OLE = b"\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1"


def ole(at512, size=1024, extra=None):
    b = bytearray(OLE + b"\x00" * (size - 8))
    b[512:512 + len(at512)] = at512
    if extra:
        off, data = extra
        b[off:off + len(data)] = data
    return bytes(b)


def tar_of(name, data):
    h = bytearray(512)
    h[0:len(name)] = name
    h[100:108] = b"0000644\x00"
    h[108:116] = b"0001750\x00"
    h[116:124] = b"0001750\x00"
    h[124:136] = b"%011o\x00" % len(data)
    h[136:148] = b"14572545623\x00"
    h[148:156] = b" " * 8
    h[156] = ord("0")
    h[257:263] = b"ustar\x00"
    h[263:265] = b"00"
    h[148:156] = b"%06o\x00 " % sum(h)
    return bytes(h) + data + b"\x00" * (512 - len(data) % 512)


def elf64():
    ident = b"\x7fELF\x02\x01\x01" + b"\x00" * 9
    return ident + struct.pack("<HHIQQQIHHHHHH", 2, 0x3E, 1, 0x401000, 64, 0, 0, 64, 56, 1, 64, 0, 0)


def ebml(doctype):
    dt = bytes([0x42, 0x82, 0x80 | len(doctype)]) + doctype
    body = b"\x42\x86\x81\x01\x42\xF7\x81\x01\x42\xF2\x81\x04\x42\xF3\x81\x08" + dt + b"\x42\x87\x81\x04\x42\x85\x81\x02"
    return b"\x1A\x45\xDF\xA3" + bytes([0x80 | len(body)]) + body + b"\x18\x53\x80\x67\x01\x00\x00\x00\x00\x00\x10\x00"


def riff(form, body):
    return b"RIFF" + struct.pack("<I", 4 + len(body)) + form + body


def main():
    shutil.rmtree(DATA, ignore_errors=True)
    files = {}

    # images
    files["image/photo.png"] = PNG_SIG + IHDR + IDAT + IEND
    files["image/spinner.apng"] = PNG_SIG + IHDR + chunk(b"acTL", struct.pack(">II", 8, 0)) + IDAT + IEND
    files["image/late-actl.png"] = PNG_SIG + IHDR + IDAT + chunk(b"acTL", struct.pack(">II", 8, 0)) + IEND
    files["image/text-chunk.apng"] = (PNG_SIG + IHDR + chunk(b"tEXt", b"Software\x00GIMP") + chunk(b"\xe9cTL", b"")
                                      + chunk(b"acTL", struct.pack(">II", 2, 0)) + IDAT + IEND)
    files["image/camera.jpg"] = b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x00\x00\x48\x00\x48\x00\x00\xFF\xDB\x00\x43\x00" + bytes(range(64))
    files["image/logo.gif"] = b"GIF89a\x10\x00\x10\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x10\x00\x10\x00\x00\x02\x02D\x01\x00;"
    files["image/banner.webp"] = riff(b"WEBP", b"VP8L" + struct.pack("<I", 10) + b"\x2f" + b"\x00" * 9)
    files["image/scan.tif"] = b"II*\x00\x08\x00\x00\x00\x00\x00" + b"\x00" * 20
    files["image/scan-be.tif"] = b"MM\x00*\x00\x00\x00\x08\x00\x00" + b"\x00" * 20
    files["image/IMG_0001.CR2"] = b"II*\x00\x10\x00\x00\x00CR\x02\x00\x00\x00\x00\x00" + b"\x00" * 16
    files["image/icon.bmp"] = b"BM" + struct.pack("<IHHI", 70, 0, 0, 54) + struct.pack("<IiiHHIIiiII", 40, 1, 1, 1, 24, 0, 16, 2835, 2835, 0, 0) + b"\x00" * 16
    files["image/photo.jxr"] = b"II\xBC\x01\x08\x00\x00\x00" + b"\x00" * 24
    files["image/layers.psd"] = b"8BPS\x00\x01" + b"\x00" * 6 + b"\x00\x03\x00\x00\x00\x10\x00\x00\x00\x10\x00\x08\x00\x03"
    files["image/favicon.ico"] = b"\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x20\x00\x68\x04\x00\x00\x16\x00\x00\x00"
    files["image/IMG_2042.HEIC"] = ftyp(b"heic", 0, [b"mif1", b"heic"]) + box(b"meta", b"\x00" * 16)
    files["image/burst.heif"] = ftyp(b"mif1", 0, [b"mif1", b"heic"]) + box(b"meta", b"\x00" * 16)
    files["image/still.heif"] = ftyp(b"mif1", 0, [b"mif1", b"miaf"]) + box(b"meta", b"\x00" * 16)
    files["image/hero.avif"] = ftyp(b"avif", 0, [b"avif", b"mif1", b"miaf"]) + box(b"meta", b"\x00" * 16)
    files["image/seq.avif"] = ftyp(b"msf1", 0, [b"msf1", b"avis", b"avif"]) + box(b"meta", b"\x00" * 16)
    files["image/scan.dcm"] = b"\x00" * 128 + b"DICM" + b"\x02\x00\x00\x00UL\x04\x00\xc4\x00\x00\x00"
    files["image/floor.dwg"] = b"AC1032\x00\x00\x00\x00\x00\x06\x00" + b"\x00" * 20
    files["image/drawing.xcf"] = b"gimp xcf v011\x00" + b"\x00\x00\x00\x10" * 6
    files["image/map.jp2"] = (b"\x00\x00\x00\x0CjP  \r\n\x87\n" + box(b"ftyp", b"jp2 \x00\x00\x00\x00jp2 ")
                              + box(b"jp2h", b"\x00" * 30))

    # audio
    files["audio/stream.aac"] = b"\xFF\xF1\x50\x80\x02\x1F\xFC" + b"\x00" * 16
    files["audio/song.mid"] = b"MThd\x00\x00\x00\x06\x00\x01\x00\x02\x01\xe0MTrk\x00\x00\x00\x04\x00\xff\x2f\x00"
    files["audio/podcast.mp3"] = b"ID3\x04\x00\x00\x00\x00\x00\x23TIT2\x00\x00\x00\x07\x00\x00\x03Pilot\x00" + b"\xFF\xFB\x90\x44" + b"\x00" * 16
    files["audio/frame.mp3"] = b"\xFF\xFB\x90\x44" + b"\x00" * 30
    files["audio/voice.m4a"] = ftyp(b"M4A ", 0, [b"M4A ", b"mp42", b"isom"]) + box(b"free", b"")
    files["audio/legacy.m4a"] = b"M4A \x00\x00\x00\x00" + b"\x00" * 16
    files["audio/track.ogg"] = b"OggS\x00\x02" + b"\x00" * 8 + b"\x01\x02\x03\x04\x00\x00\x00\x00" + b"\x00" * 6 + b"\x01\x1e\x01vorbis"
    files["audio/master.flac"] = b"fLaC\x00\x00\x00\x22" + b"\x10\x00" * 17
    files["audio/beep.wav"] = riff(b"WAVE", b"fmt " + struct.pack("<IHHIIHH", 16, 1, 1, 8000, 16000, 2, 16) + b"data\x00\x00\x00\x00")
    files["audio/note.amr"] = b"#!AMR\n\x3c\x48\xf5\x1f\x96\x66\x79\xe1"
    files["audio/loop.aiff"] = b"FORM\x00\x00\x00\x2eAIFFCOMM\x00\x00\x00\x12" + b"\x00" * 18

    # video
    files["video/clip.mp4"] = ftyp(b"isom", 512, [b"isom", b"iso2", b"avc1", b"mp41"]) + box(b"free", b"")
    files["video/screen.mp4"] = ftyp(b"mp42", 0, [b"mp42", b"mp41"]) + box(b"free", b"")
    files["video/dash.mp4"] = ftyp(b"dash", 0, [b"iso6", b"mp41"]) + box(b"free", b"")
    files["video/phone.3gp"] = ftyp(b"3gp4", 512, [b"isom", b"3gp4"]) + box(b"free", b"")
    files["video/old.3gp"] = ftyp(b"3gp5", 0, [b"3gp5", b"3gp4"]) + box(b"free", b"")
    files["video/trailer.m4v"] = b"\x00\x00\x00\x1CftypM4V \x00\x00\x00\x01M4V M4A mp42isom" + b"\x00" * 8
    files["video/movie.mkv"] = ebml(b"matroska")
    files["video/talk.webm"] = ebml(b"webm")
    files["video/home.mov"] = ftyp(b"qt  ", 0x20050300, [b"qt  "]) + box(b"wide", b"")
    files["video/cam.avi"] = riff(b"AVI ", b"LIST\x00\x00\x00\x04hdrl")
    files["video/meeting.wmv"] = b"\x30\x26\xB2\x75\x8E\x66\xCF\x11\xA6\xD9\x00\xAA\x00\x62\xCE\x6C" + b"\x00" * 16
    files["video/dvd.mpg"] = b"\x00\x00\x01\xBA\x44\x00\x04\x00\x04\x01\x01\x89\xC3\xF8" + b"\x00" * 16
    files["video/stream.flv"] = b"FLV\x01\x05\x00\x00\x00\x09\x00\x00\x00\x00"

    # fonts
    files["font/body.woff"] = b"wOFF\x00\x01\x00\x00" + b"\x00" * 36
    files["font/body.woff2"] = b"wOF2\x00\x01\x00\x00" + b"\x00" * 40
    files["font/mono.ttf"] = b"\x00\x01\x00\x00\x00\x0F\x00\x80\x00\x03\x00\x70" + b"\x00" * 16
    files["font/display.otf"] = b"OTTO\x00\x0B\x00\x80\x00\x03\x00\x30" + b"\x00" * 16
    files["font/legacy.eot"] = (struct.pack("<IIIII", 900, 800, 0x00020001, 0, 0) + b"\x00" * 14 + b"LP" + b"\x00" * 30)

    # documents
    files["doc/report.docx"] = zip_of([(b"[Content_Types].xml", CT), (b"_rels/.rels", RELS), (b"word/document.xml", b"<w:document/>")])
    files["doc/budget.xlsx"] = zip_of([(b"[Content_Types].xml", CT), (b"_rels/.rels", RELS), (b"xl/workbook.xml", b"<workbook/>")])
    files["doc/deck.pptx"] = zip_of([(b"[Content_Types].xml", CT), (b"_rels/.rels", RELS), (b"ppt/presentation.xml", b"<p/>")])
    files["doc/libre.docx"] = zip_of([(b"_rels/.rels", RELS), (b"docProps/core.xml", b"<cp/>"), (b"docProps/app.xml", b"<a/>"),
                                      (b"[Content_Types].xml", CT), (b"word/document.xml", b"<w:document/>")])
    files["doc/deep.docx"] = zip_of([(b"[Content_Types].xml", CT), (b"_rels/.rels", RELS), (b"docProps/core.xml", b"<cp/>"),
                                     (b"docProps/app.xml", b"<a/>"), (b"customXml/item1.xml", b"<i/>"), (b"word/document.xml", b"<w/>")])
    files["doc/word-first.docx"] = zip_of([(b"word/document.xml", b"<w:document/>"), (b"[Content_Types].xml", CT)])
    files["doc/notes.odt"] = zip_of([(b"mimetype", b"application/vnd.oasis.opendocument.text"), (b"content.xml", b"<office/>")])
    files["doc/sheet.ods"] = zip_of([(b"mimetype", b"application/vnd.oasis.opendocument.spreadsheet"), (b"content.xml", b"<office/>")])
    files["doc/slides.odp"] = zip_of([(b"mimetype", b"application/vnd.oasis.opendocument.presentation"), (b"content.xml", b"<office/>")])
    files["doc/drawing.odg"] = zip_of([(b"mimetype", b"application/vnd.oasis.opendocument.graphics"), (b"content.xml", b"<office/>")])
    files["doc/letter.doc"] = ole(b"\xEC\xA5\xC1\x00")
    files["doc/legacy.doc"] = ole(b"\x00\x00\x00\x00", 2200, (2080, b"\x00\x0A\x00\x00\x00MSWordDoc\x00\x10\x00\x00\x00Word.Document.8\x00\xF49\xB2q"))
    files["doc/ledger.xls"] = ole(b"\xFD\xFF\xFF\xFF\x00\x00\x00", 1024)
    files["doc/biff.xls"] = ole(b"\x09\x08\x10\x00\x00\x06\x05\x00", 1024)
    files["doc/calc.xls"] = ole(b"\x00\x00\x00\x00", 2200, (1600, b"\xE2\x00\x00\x00\x5C\x00\x70\x00\x04\x00\x00Calc"))
    files["doc/talk.ppt"] = ole(b"\xA0\x46\x1D\xF0", 1024)
    files["doc/pp97.ppt"] = ole(b"\x00\x00\x00\x00", 2200, (2072, b"\x00\xB9\x29\xE8\x11\x00\x00\x00MS PowerPoint 97"))
    files["doc/storage.msi"] = ole(b"\xFD\xFF\xFF\xFF\x00\x00\x05", 1024)
    files["doc/short.doc"] = OLE + b"\x00" * 100

    # archives and the rest
    files["archive/site.zip"] = zip_of([(b"index.html", b"<html></html>"), (b"style.css", b"body{}")])
    files["archive/empty.zip"] = b"PK\x05\x06" + b"\x00" * 18
    files["archive/spanned.zip"] = b"PK\x07\x08" + b"\x00" * 26
    files["archive/book.epub"] = zip_of([(b"mimetype", b"application/epub+zip"), (b"META-INF/container.xml", b"<container/>")])
    files["archive/app.jar"] = zip_of([(b"META-INF/MANIFEST.MF", b"Manifest-Version: 1.0\r\n")])
    files["archive/backup.tar"] = tar_of(b"notes.txt", b"remember the milk\n")
    files["archive/old.rar"] = b"Rar!\x1A\x07\x00\xCF\x90\x73\x00\x00\x0D\x00"
    files["archive/new.rar"] = b"Rar!\x1A\x07\x01\x00\x33\x92\xB5\xE5\x0A\x01\x05\x06"
    files["archive/logs.gz"] = b"\x1F\x8B\x08\x00\x00\x00\x00\x00\x00\x03" + b"\x4b\x4c\x4a\x06\x00\xc2\x41\x24\x35\x03\x00\x00\x00"
    files["archive/dump.bz2"] = b"BZh91AY&SY" + b"\x00" * 20
    files["archive/photos.7z"] = b"7z\xBC\xAF\x27\x1C\x00\x04" + b"\x00" * 24
    files["archive/manual.pdf"] = b"%PDF-1.7\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<< /Type /Catalog >>\nendobj\n"
    files["archive/bom.pdf"] = b"\xEF\xBB\xBF%PDF-1.4\n"
    files["archive/setup.exe"] = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xFF\xFF\x00\x00" + b"\x00" * 48
    files["archive/game.swf"] = b"FWS\x0A\x30\x00\x00\x00" + b"\x00" * 8
    files["archive/zgame.swf"] = b"CWS\x0A\x30\x00\x00\x00" + b"\x00" * 8
    files["archive/memo.rtf"] = b"{\\rtf1\\ansi\\deff0 {\\fonttbl {\\f0 Times;}}\\f0 Hello}\n"
    files["archive/game.nes"] = b"NES\x1A\x02\x01\x01\x00" + b"\x00" * 8
    files["archive/ext.crx"] = b"Cr24\x03\x00\x00\x00" + b"\x00" * 8
    files["archive/drivers.cab"] = b"MSCF\x00\x00\x00\x00" + b"\x00" * 24
    files["archive/setup.cab"] = b"ISc(\x00\x00\x00\x00" + b"\x00" * 24
    files["archive/print.ps"] = b"%!PS-Adobe-3.0\n%%Title: report\n"
    files["archive/data.xz"] = b"\xFD7zXZ\x00\x00\x04\xE6\xD6\xB4\x46"
    files["archive/app.sqlite"] = b"SQLite format 3\x00\x10\x00\x01\x01\x00\x40\x20\x20" + b"\x00" * 76
    files["archive/tool.deb"] = b"!<arch>\ndebian-binary   1700000000  0     0     100644  4         `\n2.0\n"
    files["archive/libm.a"] = b"!<arch>\n/               0           0     0     0       4         `\n\x00\x00\x00\x00"
    files["archive/old.Z"] = b"\x1F\x9D\x90" + b"abc"
    files["archive/old-lzh.Z"] = b"\x1F\xA0" + b"\x00" * 4
    files["archive/fast.lzo"] = b"\x89LZO\x00\r\n\x1a\n\x10\x40\x20\xa0"
    files["archive/data.lz"] = b"LZIP\x01\x0C" + b"\x00" * 10
    files["archive/server"] = elf64()
    files["archive/tiny-elf"] = b"\x7fELF\x01\x01\x01" + b"\x00" * 9
    files["archive/frames.lz4"] = b"\x04\x22\x4D\x18\x64\x40\xA7" + b"\x00" * 8
    files["archive/data.zst"] = b"\x28\xB5\x2F\xFD\x24\x05\x29\x00\x00hello"
    files["archive/skip.zst"] = struct.pack("<II", 0x184D2A53, 4) + b"meta" + b"\x28\xB5\x2F\xFD\x24\x05\x29\x00\x00hello"
    files["archive/skip-only.zst"] = struct.pack("<II", 0x184D2A50, 4) + b"meta"
    files["archive/skip-long.zst"] = struct.pack("<II", 0x184D2A5F, 100) + b"meta"
    files["archive/module.wasm"] = b"\x00asm\x01\x00\x00\x00\x01\x07\x01\x60\x02\x7f\x7f\x01\x7f"
    files["archive/pkg.rpm"] = b"\xED\xAB\xEE\xDB\x03\x00\x00\x00\x00\x01" + b"\x00" * 20
    files["archive/data.br"] = b"\xCE\xB2\xCF\x81\x00" + b"\x00" * 4

    # files that sit on the edge of a matcher
    files["edge/empty"] = b""
    files["edge/one-byte"] = b"\x89"
    files["edge/notes.txt"] = b"Meeting notes, 2024-03-09\n- ship the release\n"
    files["edge/bmw.txt"] = b"BMW service report: brakes replaced\n"
    files["edge/gifts.txt"] = b"GIFT list for the team\n"
    files["edge/script.sh"] = b"#!/bin/sh\necho hello\n"
    files["edge/postscript-ish.txt"] = b"%!important: read me first\n"
    files["edge/csv.csv"] = b"id,name\n1,PK\n"
    files["edge/late-matroska.mkv"] = b"\x1A\x45\xDF\xA3" + b"\xec" * 8200 + b"\x42\x82\x88matroska"
    files["edge/near-matroska.mkv"] = b"\x1A\x45\xDF\xA3" + b"\xec" * 8150 + b"\x42\x82\x88matroska"
    files["edge/short-box.mp4"] = struct.pack(">I", 64) + b"ftypisom\x00\x00\x02\x00isomiso2"
    files["edge/odd-box.mp4"] = struct.pack(">I", 22) + b"ftypmp42\x00\x00\x00\x00mp41\xc3\xa9" + b"\x00" * 8
    files["edge/utf8-brand.heic"] = ftyp(b"mif1", 0, [b"\xc3\xa9he", b"heic"]) + box(b"meta", b"\x00" * 8)
    files["edge/bad-brand.avif"] = ftyp(b"\xffavif"[:4], 0, [b"mif1"]) + box(b"meta", b"\x00" * 8)
    files["edge/ignored-brand.avif"] = ftyp(b"av\xffif"[:4], 0, [b"m\x80if1"[:4], b"avif"]) + box(b"meta", b"\x00" * 8)
    files["edge/zip-late.docx"] = b"junk" + zip_of([(b"[Content_Types].xml", CT), (b"word/document.xml", b"<w/>")])
    files["edge/tar-short.tar"] = b"\x00" * 257 + b"ustar"
    files["edge/dicom-short.dcm"] = b"\x00" * 128 + b"DICM"
    files["edge/riff-other.ani"] = riff(b"ACON", b"anih\x24\x00\x00\x00")
    files["edge/mpeg-video.m2v"] = b"\x00\x00\x01\xB3\x16\x00\xF0\x15\xFF\xFF\xE0\x18"
    files["edge/mpeg-ts.ts"] = b"\x47\x40\x00\x10\x00\x00\xB0\x0D"
    files["edge/eot-like.bin"] = b"\x00" * 8 + b"\x02\x00\x02" + b"\x00" * 23 + b"LP" + b"\x00" * 4
    files["edge/ttf-empty.ttf"] = b"\x00\x01\x00\x00"

    for name, data in files.items():
        put(name, data)

    jobs = []
    for name in sorted(files):
        jobs.append(["guess", name])
    jobs += [
        ["head", "image/photo.png", "4"],
        ["head", "image/photo.png", "3"],
        ["head", "image/spinner.apng", "40"],
        ["head", "image/spinner.apng", "45"],
        ["head", "video/clip.mp4", "31"],
        ["head", "video/clip.mp4", "32"],
        ["head", "doc/report.docx", "120"],
        ["head", "archive/server", "53"],
        ["head", "archive/server", "52"],
        ["head", "archive/skip.zst", "12"],
        ["head", "archive/skip.zst", "16"],
    ]
    jobs += [
        ["get_type", "mime=image/png"],
        ["get_type", "ext=mkv"],
        ["get_type", "ext=woff2"],
        ["get_type", "mime=application/font-woff"],
        ["get_type", "mime=application/font-sfnt"],
        ["get_type", "mime=application/dicom"],
        ["get_type", "ext=dcm"],
        ["get_type", "mime=image/png", "ext=zip"],
        ["get_type", "ext=jpeg"],
        ["get_type", "ext=Z"],
        ["get_type", "ext=z"],
        ["get_type"],
        ["supported", "ext", "png"],
        ["supported", "ext", "PNG"],
        ["supported", "ext", "jpeg"],
        ["supported", "ext", "elf"],
        ["supported", "mime", "image/jpeg"],
        ["supported", "mime", "image/svg+xml"],
        ["supported", "mime", "application/octet-stream"],
        ["types"],
        ["cli", "-f", "image/photo.png", "doc/report.docx", "edge/notes.txt", "edge/empty"],
        ["cli", "--file", "audio/podcast.mp3"],
        ["cli", "--file=video/movie.mkv"],
        ["cli", "-farchive/logs.gz"],
        ["cli", "--fi", "font/body.woff2", "font/mono.ttf"],
        ["cli", "-f", "image/logo.gif", "-f", "image/banner.webp"],
        ["cli", "-f", "image/logo.gif", "-v"],
        ["cli", "-v"],
        ["cli", "--version"],
        ["cli", "--vers"],
        ["cli", "-h"],
        ["cli", "--help"],
        ["cli"],
        ["cli", "-f"],
        ["cli", "-f", "-v"],
        ["cli", "image/photo.png"],
        ["cli", "-f", "image/photo.png", "-x"],
        ["cli", "-f", "image/photo.png", "extra", "--nope"],
        ["custom", "edge/csv.csv"],
        ["custom", "edge/notes.txt"],
        ["custom-bad"],
        ["guess", "edge/csv.csv"],
        ["guess", "image/photo.png"],
    ]
    with open(os.path.join(DATA, "jobs.tsv"), "w", encoding="utf-8") as f:
        for j in jobs:
            f.write("\t".join(j) + "\n")


main()
