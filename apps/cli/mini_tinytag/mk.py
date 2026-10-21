"""Writes data/: a small music library in every format tinytag reads (MP3
with ID3v2.2, 2.3 and 2.4 and ID3v1, raw MPEG, FLAC, Ogg Vorbis, Opus,
Ogg FLAC, Speex, WAV, MP4/M4A with AAC and ALAC, WMA and AIFF), some
broken and mislabelled files, and the job list. The files are built
byte by byte here from the format specifications; the audio itself is
silence, since tinytag reads only headers."""
import base64
import os
import shutil
import struct
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def png(w, h, rgb):
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    raw = b"".join(b"\x00" + bytes(rgb) * w for _ in range(h))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


COVER = png(4, 4, (200, 40, 40))
BACK = png(2, 2, (20, 20, 160))
JPEG = (b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
        + bytes(range(64)) + b"\xff\xd9")


# ---- ID3v2

def synchsafe(n):
    return bytes([(n >> 21) & 0x7f, (n >> 14) & 0x7f, (n >> 7) & 0x7f, n & 0x7f])


def frame(fid, body, version=3):
    if version == 2:
        return fid + struct.pack(">I", len(body))[1:] + body
    size = synchsafe(len(body)) if version == 4 else struct.pack(">I", len(body))
    return fid + size + b"\x00\x00" + body


def text(enc, s):
    if enc == 0:
        return b"\x00" + s.encode("latin-1")
    if enc == 1:
        return b"\x01" + b"\xff\xfe" + s.encode("utf-16-le")
    if enc == 2:
        return b"\x02" + s.encode("utf-16-be")
    return b"\x03" + s.encode("utf-8")


def id3v2(frames, version=3, padding=0, extended=False):
    body = b"".join(frames) + b"\x00" * padding
    flags = 0
    if extended:
        ext = synchsafe(6) + b"\x01\x00"
        body = ext + body
        flags |= 0x40
    return b"ID3" + bytes([version, 0, flags]) + synchsafe(len(body)) + body


def id3v1(title, artist, album, year, comment, track, genre):
    def pad(s, n):
        return s.encode("latin-1")[:n].ljust(n, b"\x00")
    if track is not None:
        com = pad(comment, 28) + b"\x00" + bytes([track])
    else:
        com = pad(comment, 30)
    return b"TAG" + pad(title, 30) + pad(artist, 30) + pad(album, 30) + pad(year, 4) + com + bytes([genre])


# ---- MPEG audio frames

def mpeg_header(version, layer, br_id, sr_id, padding, mode):
    # version: 3 = MPEG1, 2 = MPEG2, 0 = MPEG2.5; layer: 3 = I, 2 = II, 1 = III
    b1 = 0xE0 | (version << 3) | (layer << 1) | 1
    b2 = (br_id << 4) | (sr_id << 2) | (padding << 1)
    b3 = mode << 6
    return bytes([0xFF, b1, b2, b3])


BITRATES = {
    (3, 1): (0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320),
    (3, 2): (0, 32, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 384),
    (3, 3): (0, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448),
    (2, 1): (0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160),
    (0, 1): (0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160),
}
RATES = {3: (44100, 48000, 32000), 2: (22050, 24000, 16000), 0: (11025, 12000, 8000)}


def frame_len(version, layer, br_id, sr_id, padding):
    br = BITRATES[(version, layer)][br_id] * 1000
    sr = RATES[version][sr_id]
    if layer == 3:
        return (12 * br // sr + padding) * 4
    spf = 1152 if (layer == 2 or version == 3) else 576
    return spf // 8 * br // sr + padding


def mpeg_frame(version, layer, br_id, sr_id, padding, mode, body=b""):
    n = frame_len(version, layer, br_id, sr_id, padding)
    head = mpeg_header(version, layer, br_id, sr_id, padding, mode)
    return (head + body + b"\x00" * n)[:n]


# ---- Ogg

def ogg_crc(data):
    crc = 0
    for b in data:
        crc ^= b << 24
        for _ in range(8):
            crc = ((crc << 1) ^ 0x04C11DB7) if crc & 0x80000000 else (crc << 1)
            crc &= 0xffffffff
    return crc


class OggWriter:
    def __init__(self, serial):
        self.serial = serial
        self.seq = 0
        self.out = b""

    def page(self, segments_data, granule, header_type=0, lacing=None):
        if lacing is None:
            lacing = []
            for packet in segments_data:
                n = len(packet)
                while n >= 255:
                    lacing.append(255)
                    n -= 255
                lacing.append(n)
        body = b"".join(segments_data)
        head = (b"OggS" + bytes([0, header_type]) + struct.pack("<qII", granule, self.serial, self.seq)
                + b"\x00\x00\x00\x00" + bytes([len(lacing)]) + bytes(lacing))
        crc = ogg_crc(head + body)
        head = head[:22] + struct.pack("<I", crc) + head[26:]
        self.seq += 1
        self.out += head + body


def vorbis_comment(vendor, comments, framing=False):
    out = struct.pack("<I", len(vendor)) + vendor.encode()
    out += struct.pack("<I", len(comments))
    for c in comments:
        b = c.encode("utf-8") if isinstance(c, str) else c
        out += struct.pack("<I", len(b)) + b
    if framing:
        out += b"\x01"
    return out


def flac_picture(pic_type, mime, desc, data, w=4, h=4):
    return (struct.pack(">II", pic_type, len(mime)) + mime.encode() + struct.pack(">I", len(desc.encode()))
            + desc.encode() + struct.pack(">IIII", w, h, 24, 0) + struct.pack(">I", len(data)) + data)


def streaminfo(rate, channels, bits, total):
    info = (rate << 44) | ((channels - 1) << 41) | ((bits - 1) << 36) | total
    return struct.pack(">HH", 4096, 4096) + b"\x00\x00\x10\x00\x30\x00" + struct.pack(">Q", info) + bytes(range(16))


def flac_block(btype, data, last=False):
    return bytes([btype | (0x80 if last else 0)]) + struct.pack(">I", len(data))[1:] + data


# ---- the library

def song_mp3():
    frames = [
        frame(b"TIT2", text(0, "Night Train")),
        frame(b"TPE1", text(1, "Ana Lúcia")),
        frame(b"TALB", text(0, "Platform 9")),
        frame(b"TPE2", text(0, "Various Artists")),
        frame(b"TRCK", text(0, "3/12")),
        frame(b"TPOS", text(0, "1/2")),
        frame(b"TCON", text(0, "(17)")),
        frame(b"TYER", text(0, "2019")),
        frame(b"TCOM", text(1, "Jörg Weiss")),
        frame(b"COMM", b"\x00eng" + b"\x00" + "recorded live at the depot".encode("latin-1")),
        frame(b"COMM", b"\x00eng" + b"iTunNORM\x00" + b" 000003E8 00000412 00002A1B"),
        frame(b"TXXX", text(0, "CATALOGNUMBER") + b"\x00" + b"PLAT-009"),
        frame(b"TXXX", text(0, "ARTISTS") + b"\x00" + b"Bo Chen"),
        frame(b"TXXX", text(0, "Mood") + b"\x00" + b"wistful"),
        frame(b"TIT1", text(0, "Commute")),
        frame(b"GRP1", text(0, "Evening")),
        frame(b"USLT", b"\x00eng" + b"\x00" + b"la la la\nthe last train"),
        frame(b"SYLT", b"\x00eng\x02\x01" + b"\x00" + b"\nHere it comes\x00" + struct.pack(">I", 1500)
              + b"\nthrough the dark\x00" + struct.pack(">I", 63250)),
        frame(b"WOAR", b"https://example.com/ana"),
        frame(b"TBPM", text(0, "120")),
        frame(b"POPM", b"listener@example.com\x00\xc4\x00\x00\x00\x07"),
        frame(b"PRIV", b"XMP\x00<x:xmpmeta xmlns:x='adobe:ns:meta/'/>\x00"),
        frame(b"APIC", b"\x00image/png\x00\x03cover\x00" + COVER),
        frame(b"APIC", b"\x00image/jpeg\x00\x04\x00" + JPEG),
        frame(b"TXYZ", text(0, "a frame nobody knows")),
        frame(b"TLEN", text(0, "4000")),
    ]
    tag = id3v2(frames, 3, padding=64)
    audio = b"".join(mpeg_frame(3, 1, 9, 0, i % 3 == 0 and 1 or 0, 1) for i in range(12))
    return tag + audio + id3v1("Night Train", "Ana Lucia", "", "2019", "from v1", 4, 17)


def vbr_mp3():
    frames = [
        frame(b"TIT2", text(3, "Séance"), 4),
        frame(b"TPE1", text(3, "Kim\x00Lee"), 4),
        frame(b"TDRC", text(3, "2021-05-01"), 4),
        frame(b"TRCK", text(3, "7"), 4),
        frame(b"TCON", text(3, "Ambient\x0013"), 4),
        frame(b"TPOS", text(3, "x/2"), 4),
        frame(b"MVIN", text(3, "2/4"), 4),
        frame(b"MVNM", text(3, "Andante"), 4),
        frame(b"TKEY", text(2, "Am"), 4),
        frame(b"TXXX", text(3, "FILENAME") + b"\x00" + "séance-final.wav".encode(), 4),
        frame(b"TIT1", text(3, "Old Grouping"), 4),
        frame(b"TPUB", b"\x03Caf\xe9 Records \xf0\x9f\x8e", 4),
        frame(b"XSOP", b"\x07bell\tring", 4),
    ]
    tag = id3v2(frames, 4, padding=10, extended=True)
    first = mpeg_header(3, 1, 9, 0, 0, 1) + b"\x00" * 32 + b"Xing" + struct.pack(">ii", 3, 1000) + struct.pack(">i", 400000)
    first = (first + b"\x00" * 417)[:417]
    audio = first + b"".join(mpeg_frame(3, 1, br, 0, 0, 1) for br in (9, 10, 11, 9, 7, 13))
    return tag + audio


def vbri_mp3():
    first = mpeg_header(2, 1, 8, 0, 0, 3) + b"\x00" * 32 + b"VBRI" + struct.pack(">HHH", 1, 1234, 75) \
        + struct.pack(">II", 98765, 777)
    n = frame_len(2, 1, 8, 0, 0)
    first = (first + b"\x00" * n)[:n]
    return first + b"".join(mpeg_frame(2, 1, 8, 0, 0, 3) for _ in range(4))


def old_mp3():
    frames = [
        frame(b"TT2", text(0, "Blue in Green"), 2),
        frame(b"TP1", text(1, "The Quartet"), 2),
        frame(b"TAL", text(0, "Late Set"), 2),
        frame(b"TRK", text(0, "05"), 2),
        frame(b"TCO", text(0, "Jazz"), 2),
        frame(b"TYE", text(0, "1959"), 2),
        frame(b"COM", b"\x01eng" + b"\xff\xfe" + "note".encode("utf-16-le") + b"\x00\x00"
              + b"\xff\xfe" + "mono transfer".encode("utf-16-le"), 2),
        frame(b"ULT", b"\x00eng\x00(instrumental)", 2),
        frame(b"PIC", b"\x00PNG\x03front\x00" + COVER, 2),
        frame(b"TXX", text(0, "Barcode") + b"\x00" + b"0123456789012", 2),
        frame(b"TT1", text(0, "Side B"), 2),
        frame(b"TP2", b"\x01\xff\xfe" + "Ab".encode("utf-16-le") + b"\x00\xd8" + "c".encode("utf-16-le"), 2),
        frame(b"SLT", b"\x00eng\x01\x01\x00" + b"one\x00" + struct.pack(">I", 10) + b"two\x00"
              + struct.pack(">I", 20), 2),
    ]
    tag = id3v2(frames, 2)
    audio = b""
    brs = [10, 10, 9, 12, 10, 8, 11, 10, 10, 9]
    for i, br in enumerate(brs):
        audio += mpeg_frame(3, 2, br, 1, i % 2, 0)
        if i == 4:
            audio += b"\x13\x37\xff\x00garbage"
    return tag + audio


def v1only_mp3():
    audio = b"".join(mpeg_frame(0, 1, 6, 2, 0, 3) for _ in range(12))
    return audio + id3v1("Field Recording", "Unknown", "Tapes", "1987",
                         "thirty characters of comment!!", None, 12)


def stream_dat():
    return b"".join(mpeg_frame(3, 3, 4, 2, 0, 3) for _ in range(9))


def album_flac():
    comments = [
        "TITLE=Harbour Lights", "ARTIST=Mira Sol", "ALBUMARTIST=Mira Sol", "ALBUM=Coastline",
        "TRACKNUMBER=2/9", "DISCNUMBER=1", "DISCTOTAL=1", "DATE=2023", "GENRE=Folk",
        "COMMENT=mastered for vinyl", "ISRC=GBXYZ2300042", "MOOD=calm", "artist=Mira Sol",
        "Artist=Guest Choir", "OTHER=collides with other", "TRACKTOTAL=x",
        "LYRICS=first line\nsecond line", "no equals sign here",
        "METADATA_BLOCK_PICTURE=" + base64.b64encode(flac_picture(3, "image/png", "ignored", COVER)).decode(),
    ]
    blocks = (flac_block(0, streaminfo(44100, 2, 16, 441000))
              + flac_block(4, vorbis_comment("reference libFLAC 1.4.3 20230623", comments))
              + flac_block(6, flac_picture(3, "image/png", "Front", COVER))
              + flac_block(6, flac_picture(8, "image/jpeg", "Mira on stage", JPEG))
              + flac_block(1, b"\x00" * 100, last=True))
    return b"fLaC" + blocks + b"\xff\xf8" + b"\x00" * 1000


def tagged_flac():
    tag = id3v2([frame(b"TIT2", text(0, "From ID3")), frame(b"TPE1", text(0, "Mira Sol"))], 3)
    comments = ["TITLE=From Vorbis", "ARTIST=Mira Sol", "TRACKNUMBER=3"]
    blocks = (flac_block(0, streaminfo(96000, 2, 24, 4800000))
              + flac_block(4, vorbis_comment("ffmpeg", comments), last=True))
    return tag + b"fLaC" + blocks + b"\x00" * 1500


def vorbis_ogg():
    w = OggWriter(0x1234)
    ident = (b"\x01vorbis" + struct.pack("<IBIiii", 0, 2, 44100, 0, 160000, 0) + b"\xb8\x01")
    w.page([ident], 0, 0x02)
    comments = [
        "TITLE=Long Way Round", "ARTIST=Dune Ensemble", "ALBUM=Sand", "TRACKNUMBER=4",
        "TRACKTOTAL=10", "DISCNUMBER=1/1", "DATE=2020", "GENRE=Ambient", "DESCRIPTION=" + "a" * 300,
        "ENCODER=Lavc60.31.102 libvorbis", "COMMENT=", "TOTALDISCS=1",
        "METADATA_BLOCK_PICTURE=" + base64.b64encode(flac_picture(3, "image/png", "dune", COVER)).decode(),
    ]
    comment = b"\x03vorbis" + vorbis_comment("Xiph.Org libVorbis I 20200704 (Reducing Environment)", comments,
                                              framing=True)
    setup = b"\x05vorbis" + b"\x00" * 40
    # the comment packet starts on one page and ends on the next
    cut = 2 * 255
    w.page([comment[:cut]], 0, 0, lacing=[255, 255])
    rest = comment[cut:]
    lacing = [255] * (len(rest) // 255) + [len(rest) % 255, len(setup)]
    w.page([rest, setup], 0, 0x01, lacing=lacing)
    for i, g in enumerate((44100, 88200, 132300, 150000)):
        w.page([b"\x00" * 120, b"\x00" * 80], g, 0x04 if i == 3 else 0)
    return w.out


def voice_opus():
    w = OggWriter(0x51)
    w.page([b"OpusHead" + struct.pack("<BBHIhB", 1, 2, 312, 48000, 0, 0)], 0, 0x02)
    tags = b"OpusTags" + vorbis_comment("libopus 1.4", ["TITLE=Morning Call", "ARTIST=Tom", "artist=tom",
                                                         "TRACKNUMBER=1", "LANGUAGE=en", "BPM=90"])
    w.page([tags], 0)
    grans = (48312, 96312, 144312, 192312, 240312)
    for i, g in enumerate(grans):
        w.page([b"\x00" * (60 + 10 * i)] * 3, g, 0x04 if i == len(grans) - 1 else 0)
    return w.out


def flac_oga():
    w = OggWriter(0xF1AC)
    head = b"\x7fFLAC\x01\x00\x00\x01" + b"fLaC" + flac_block(0, streaminfo(48000, 1, 16, 96000))
    w.page([head], 0, 0x02)
    vc = flac_block(4, vorbis_comment("reference libFLAC 1.4.3", ["TITLE=Bell", "ARTIST=Chapel",
                                                                  "DISCNUMBER=2/3"]), last=True)
    w.page([vc], 0)
    w.page([b"\xff\xf8" + b"\x00" * 200], 48000)
    w.page([b"\xff\xf8" + b"\x00" * 200], 96000, 0x04)
    return w.out


def talk_spx():
    w = OggWriter(7)
    header = (b"Speex   " + b"1.2.1".ljust(20, b"\x00") + struct.pack("<iiiiiiiiiiii", 1, 80, 16000, 1, 4, 1,
                                                                        -1, 320, 0, 0, 0, 0))
    w.page([header], 0, 0x02)
    w.page([vorbis_comment("Encoded with Speex 1.2.1", ["TITLE=Minutes", "AUTHOR=Board", "DATE=2024"])], 0)
    w.page([b"\x00" * 38] * 5, 16000)
    w.page([b"\x00" * 38] * 5, 40000, 0x04)
    return w.out


def riff_chunk(cid, data):
    out = cid + struct.pack("<I", len(data)) + data
    if len(data) % 2:
        out += b"\x00"
    return out


def info_list(items):
    body = b"INFO"
    for cid, s in items:
        b = s.encode("utf-8") + b"\x00"
        body += riff_chunk(cid, b)
    return riff_chunk(b"LIST", body)


def field_wav():
    fmt = struct.pack("<HHIIHH", 1, 2, 44100, 44100 * 4, 4, 16)
    info = info_list([(b"INAM", "Rain on Tin"), (b"IART", "Field Kit"), (b"IPRD", "Weather"),
                      (b"ICRD", "2018"), (b"IGNR", "Field recording"), (b"ICMT", "close mic"),
                      (b"ITRK", "5"), (b"IPRT", "five"), (b"ISFT", "Lavf60.16.100")])
    id3 = id3v2([frame(b"TPE1", text(0, "Field Kit Duo")), frame(b"TBPM", text(0, "60")),
                 frame(b"TIT2", text(0, "Rain on Tin"))], 3)
    pmx = b"<x:xmpmeta xmlns:x='adobe:ns:meta/'><wav/></x:xmpmeta>\x00\x00"
    data = b"\x00" * (44100 * 4 // 100 + 1)
    body = (b"WAVE" + riff_chunk(b"fmt ", fmt) + info + riff_chunk(b"id3 ", id3) + riff_chunk(b"_PMX", pmx)
            + riff_chunk(b"data", data) + riff_chunk(b"junk", b"\x00" * 7))
    return b"RIFF" + struct.pack("<I", len(body)) + body


def ext_wav():
    fmt = (struct.pack("<HHIIHH", 0xFFFE, 6, 48000, 48000 * 18, 18, 24) + struct.pack("<HHI", 22, 24, 0x3F)
           + struct.pack("<H", 1) + b"\x00\x00\x00\x00\x10\x00\x80\x00\x00\xaa\x00\x38\x9b\x71")
    data = b"\x00" * (18 * 100)
    body = b"WAVE" + riff_chunk(b"fmt ", fmt) + riff_chunk(b"data", data)
    return b"RIFF" + struct.pack("<I", len(body)) + body


def adpcm_wav():
    fmt = struct.pack("<HHIIHHHH", 0x11, 1, 22050, 11100, 512, 4, 2, 1017)
    fact = struct.pack("<I", 22050 * 3)
    data = b"\x00" * (512 * 4)
    body = (b"WAVE" + riff_chunk(b"fmt ", fmt) + riff_chunk(b"fact", fact)
            + info_list([(b"INAM", "Voicemail"), (b"TRCK", "x")]) + riff_chunk(b"data", data))
    return b"RIFF" + struct.pack("<I", len(body)) + body


def atom(name, data):
    return struct.pack(">I", len(data) + 8) + name + data


def data_atom(dtype, payload):
    return atom(b"data", struct.pack(">II", dtype, 0) + payload)


def mp4_ilst(items):
    return atom(b"ilst", b"".join(items))


def meta(ilst):
    hdlr = atom(b"hdlr", b"\x00" * 8 + b"mdirappl" + b"\x00" * 9)
    return atom(b"meta", b"\x00\x00\x00\x00" + hdlr + ilst)


def esds(avg):
    dsi = b"\x05\x80\x80\x80\x02\x12\x10"
    dcd = (b"\x04\x80\x80\x80\x14" + b"\x40\x15" + b"\x00\x18\x00" + struct.pack(">II", 160000, avg) + dsi)
    es = b"\x03\x80\x80\x80\x22" + b"\x00\x01\x00" + dcd + b"\x06\x80\x80\x80\x01\x02"
    return atom(b"esds", b"\x00\x00\x00\x00" + es)


def sample_entry(name, channels, rate, extra):
    body = (b"\x00" * 6 + struct.pack(">H", 1) + b"\x00" * 8 + struct.pack(">HHHH", channels, 16, 0, 0)
            + struct.pack(">I", (rate & 0xffff) << 16) + extra)
    return atom(name, body)


def trak(entry):
    stsd = atom(b"stsd", b"\x00\x00\x00\x00" + struct.pack(">I", 1) + entry)
    stbl = atom(b"stbl", stsd + atom(b"stts", b"\x00" * 16))
    minf = atom(b"minf", atom(b"smhd", b"\x00" * 8) + stbl)
    mdia = atom(b"mdia", atom(b"mdhd", b"\x00" * 24) + minf)
    return atom(b"trak", atom(b"tkhd", b"\x00" * 84) + mdia)


def tune_m4a():
    mvhd = atom(b"mvhd", b"\x00" + b"\x00" * 3 + struct.pack(">IIII", 0, 0, 44100, 44100 * 187 + 22050)
                + b"\x00" * 80)
    entry = sample_entry(b"mp4a", 2, 44100, esds(128000))
    ilst = mp4_ilst([
        atom(b"\xa9nam", data_atom(1, "Glass Hours".encode())),
        atom(b"\xa9ART", data_atom(1, "Noor & The Lanterns".encode())),
        atom(b"\xa9alb", data_atom(1, "Glass Hours".encode())),
        atom(b"aART", data_atom(1, "Noor".encode())),
        atom(b"trkn", data_atom(0, struct.pack(">HHHH", 0, 6, 11, 0))),
        atom(b"disk", data_atom(0, struct.pack(">HHH", 0, 1, 0))),
        atom(b"\xa9day", data_atom(1, b"2022-03-04T08:00:00Z")),
        atom(b"\xa9gen", data_atom(1, b"Indie")),
        atom(b"gnre", data_atom(0, struct.pack(">H", 18))),
        atom(b"tmpo", data_atom(21, struct.pack(">h", 96))),
        atom(b"cprt", data_atom(1, "℗ 2022 Lantern Records".encode())),
        atom(b"\xa9wrt", data_atom(1, b"N. Haddad")),
        atom(b"\xa9lyr", data_atom(1, b"hours of glass\rand light")),
        atom(b"\xa9too", data_atom(1, b"iTunes 12.12")),
        atom(b"covr", data_atom(14, COVER)),
        atom(b"----", atom(b"mean", b"\x00\x00\x00\x00com.apple.iTunes") + atom(b"name", b"\x00\x00\x00\x00ISRC")
             + data_atom(1, b"USABC2200011")),
        atom(b"----", atom(b"mean", b"\x00\x00\x00\x00com.apple.iTunes") + atom(b"name", b"\x00\x00\x00\x00MOOD")
             + data_atom(1, b"bright") + data_atom(1, b"ignored second value")),
        atom(b"xid ", data_atom(1, b"Lantern:isrc:USABC2200011")),
        atom(b"rate", data_atom(21, struct.pack(">i", 80))),
        atom(b"pgap", data_atom(21, b"\x01")),
        atom(b"stik", data_atom(21, b"\x00\x01\x02")),
    ])
    moov = atom(b"moov", mvhd + trak(entry) + atom(b"udta", meta(ilst)))
    uuid = atom(b"uuid", b"\xBE\x7A\xCF\xCB\x97\xA9\x42\xE8\x9C\x71\x99\x94\x91\xE3\xAF\xAC"
                + b"<x:xmpmeta xmlns:x='adobe:ns:meta/'/>")
    ftyp = atom(b"ftyp", b"M4A \x00\x00\x02\x00M4A mp42isom")
    return ftyp + atom(b"free", b"\x00" * 16) + moov + uuid + atom(b"mdat", b"\x00" * 2000)


def lossless_m4a():
    mvhd = atom(b"mvhd", b"\x01" + b"\x00" * 3 + struct.pack(">QQIQ", 0, 0, 96000, 96000 * 42) + b"\x00" * 80)
    cookie = atom(b"alac", b"\x00\x00\x00\x00" + struct.pack(">IBBBBBBHIII", 4096, 0, 24, 40, 10, 14, 2, 255,
                                                             0, 2304000, 96000))
    entry = sample_entry(b"alac", 2, 96000, cookie)
    ilst = mp4_ilst([atom(b"\xa9nam", data_atom(1, b"Room Tone")),
                     atom(b"----", atom(b"mean", b"\x00\x00\x00\x00com.apple.iTunes")
                          + atom(b"name", b"\x00\x00\x00\x00CONDUCTOR") + data_atom(1, b"Ida Berg"))])
    moov = atom(b"moov", mvhd + trak(entry) + atom(b"udta", meta(ilst)))
    return atom(b"ftyp", b"M4A \x00\x00\x00\x00M4A ") + moov + atom(b"mdat", b"\x00" * 500)


def guid(s):
    return bytes.fromhex(s)


ASF_HEADER = guid("3026B2758E66CF11A6D900AA0062CE6C")


def asf_obj(g, data):
    return g + struct.pack("<Q", len(data) + 24) + data


def utf16z(s):
    return s.encode("utf-16-le") + b"\x00\x00"


def show_wma():
    fileprop = (b"\x11" * 16 + struct.pack("<QQQQQQIIII", 9000, 0, 12, 1824 * 10000000 // 10 + 31000000, 0, 3100,
                                           2, 3200, 3200, 64000))
    fmt = struct.pack("<HHIIHHH", 0x161, 2, 44100, 16000, 2973, 16, 10) + b"\x00" * 10
    streamprop = (guid("409E69F84D5BCF11A8FD00805F5C442B") + b"\x00" * 16 + struct.pack("<QIIHI", 0, len(fmt), 0, 1, 0)
                  + fmt)
    title, author, cprt, desc, rating = (utf16z("Weekly Roundup"), utf16z("Station 9"), utf16z("(c) Station 9"),
                                         utf16z(""), utf16z("PG"))
    content = struct.pack("<5H", len(title), len(author), len(cprt), len(desc), len(rating)) + title + author \
        + cprt + desc + rating

    def ext_desc(name, vtype, value):
        n = utf16z(name)
        return struct.pack("<H", len(n)) + n + struct.pack("<HH", vtype, len(value)) + value
    descs = [
        ext_desc("WM/AlbumTitle", 0, utf16z("Roundups 2024")),
        ext_desc("WM/TrackNumber", 3, struct.pack("<I", 14)),
        ext_desc("WM/Year", 0, utf16z("2024")),
        ext_desc("WM/Genre", 0, utf16z("Podcast")),
        ext_desc("WM/PartOfSet", 0, utf16z("1/2")),
        ext_desc("WM/Mood", 0, utf16z("informative")),
        ext_desc("IsVBR", 2, struct.pack("<I", 1)),
        ext_desc("WM/Picture", 1, b"\x03" + b"\x00" * 9),
        ext_desc("WM/EncodingTime", 4, struct.pack("<Q", 133500000000000000)),
        ext_desc("WM/Bitrate", 5, struct.pack("<H", 128)),
    ]
    extcontent = struct.pack("<H", len(descs)) + b"".join(descs)

    def md(name, vtype, value):
        n = utf16z(name)
        return b"\x00\x00\x00\x00" + struct.pack("<HHI", len(n), vtype, len(value)) + n + value
    metadata = struct.pack("<H", 2) + md("WM/Composer", 0, utf16z("R. Ito")) + md("WM/SharedUserRating", 3,
                                                                                    struct.pack("<I", 75))
    sub = asf_obj(guid("EACBF8C5AF5B77488467AA8C44FA4CCA"), metadata) \
        + asf_obj(guid("D2D0A440E30711D297F000A0C95EA850"), b"\x00" * 6)
    hdrext = struct.pack("<16sHI", b"\x00" * 16, 6, len(sub)) + sub
    xmp = b"<x:xmpmeta xmlns:x='adobe:ns:meta/'><wma/></x:xmpmeta>"
    objects = [
        asf_obj(guid("A1DCAB8C47A9CF118EE400C00C205365"), fileprop),
        asf_obj(guid("9107DCB7B7A9CF118EE600C00C205365"), streamprop),
        asf_obj(guid("3326B2758E66CF11A6D900AA0062CE6C"), content),
        asf_obj(guid("40A4D0D207E3D21197F000A0C95EA850"), extcontent),
        asf_obj(guid("B503BF5F2EA9CF118EE300C00C205365"), hdrext),
        asf_obj(guid("CBCF7ABEA997E8429C71999491E3AFAC"), xmp),
        asf_obj(b"\xee" * 16, b"\x00" * 33),
    ]
    body = b"".join(objects)
    head = ASF_HEADER + struct.pack("<QI", 30 + len(body), len(objects)) + b"\x01\x02"
    return head + body + asf_obj(guid("3626B2758E66CF11A6D900AA0062CE6C"), b"\x00" * 50)


def ext80(rate):
    exp = 0x3FFF + 63
    m = rate
    while m < (1 << 63):
        m <<= 1
        exp -= 1
    return struct.pack(">HQ", exp, m)


def iff_chunk(cid, data):
    out = cid + struct.pack(">I", len(data)) + data
    if len(data) % 2:
        out += b"\x00"
    return out


def loop_aiff():
    comm = struct.pack(">hIh", 1, 22050 * 2, 8) + ext80(22050)
    id3 = id3v2([frame(b"TIT2", text(3, "Drum Loop 4"), 4), frame(b"TCON", text(3, "Breakbeat"), 4),
                 frame(b"TRCK", text(3, "4"), 4)], 4)
    body = (b"AIFF" + iff_chunk(b"COMM", comm) + iff_chunk(b"NAME", b"Drum Loop 4")
            + iff_chunk(b"AUTH", b"Beat Lab") + iff_chunk(b"ANNO", b"take one\x00take two\x00")
            + iff_chunk(b"(c) ", b"2016 Beat Lab")
            + iff_chunk(b"SSND", b"\x00" * 8 + b"\x00" * 1001) + iff_chunk(b"ID3 ", id3)
            + iff_chunk(b"APPL", b"XMP <x:xmpmeta xmlns:x='adobe:ns:meta/'/>\x00"))
    return b"FORM" + struct.pack(">I", len(body)) + body


def comp_aifc():
    comm = struct.pack(">hIh", 2, 48000 * 5, 16) + ext80(48000) + b"sowt" + b"\x0bnot swapped"
    body = (b"AIFC" + iff_chunk(b"FVER", struct.pack(">I", 0xA2805140)) + iff_chunk(b"COMM", comm)
            + iff_chunk(b"SSND", b"\x00" * 2000))
    return b"FORM" + struct.pack(">I", len(body)) + body


def main():
    if os.path.isdir(DATA):
        shutil.rmtree(DATA)
    os.makedirs(os.path.join(DATA, "out"))
    files = {
        "song.mp3": song_mp3(),
        "vbr.mp3": vbr_mp3(),
        "vbri.mp3": vbri_mp3(),
        "old.mp3": old_mp3(),
        "v1only.mp3": v1only_mp3(),
        "stream.dat": stream_dat(),
        "album.flac": album_flac(),
        "tagged.flac": tagged_flac(),
        "vorbis.ogg": vorbis_ogg(),
        "voice.opus": voice_opus(),
        "flac.oga": flac_oga(),
        "talk.spx": talk_spx(),
        "field.wav": field_wav(),
        "ext.wav": ext_wav(),
        "adpcm.wav": adpcm_wav(),
        "tune.m4a": tune_m4a(),
        "lossless.m4a": lossless_m4a(),
        "show.wma": show_wma(),
        "loop.aiff": loop_aiff(),
        "comp.aifc": comp_aifc(),
        # broken and mislabelled files
        "empty.mp3": b"",
        "notes.txt": b"setlist: open with track 3, close with the reprise\n",
        "bad.ogg": b"OggZ this is not an ogg stream at all",
        "bad.flac": b"fLaX" + b"\x00" * 40,
        "fake.wav": b"RIFF\x10\x00\x00\x00AVI LIST",
        "noise.m4a": b"\x00\x00\x00\x10\xff\xfe\xfd\xfc" + b"\x00" * 8,
        "short.m4a": atom(b"ftyp", b"M4A ") + atom(b"moov", atom(b"mvhd", b"\x00" * 10)),
        "cut.mp3": id3v2([frame(b"TIT2", text(0, "Cut Short"))], 3)[:-6],
        "real_flac.bin": tagged_flac()[tagged_flac().index(b"fLaC"):],
        "really_ogg.mp4": voice_opus(),
        "mystery.bin": b"\x01\x02\x03 just some bytes",
    }
    for name, body in files.items():
        with open(os.path.join(DATA, name), "wb") as f:
            f.write(body)
    with open(os.path.join(DATA, "jobs.txt"), "w") as f:
        f.write(JOBS)


JOBS = """# mini_tinytag jobs: the tinytag command line, then the Python API
tinytag data/song.mp3
tinytag --format json data/vbr.mp3 data/vbri.mp3
tinytag -f json data/old.mp3 data/v1only.mp3 data/stream.dat
tinytag -f csv data/album.flac
tinytag -f tsv data/tagged.flac data/vorbis.ogg
tinytag -f tabularcsv data/voice.opus data/flac.oga data/talk.spx
tinytag -f json data/field.wav data/ext.wav data/adpcm.wav
tinytag data/tune.m4a data/lossless.m4a
tinytag -f csv data/show.wma
tinytag -f json data/loop.aiff data/comp.aifc
tinytag -i data/out/cover.png data/song.mp3
tinytag --save-image data/out/art.jpg -f tsv data/album.flac data/tune.m4a data/vorbis.ogg data/v1only.mp3
tinytag -s data/notes.txt data/empty.mp3 data/mystery.bin data/real_flac.bin
tinytag data/notes.txt data/loop.aiff
tinytag data/empty.mp3 data/real_flac.bin data/really_ogg.mp4
tinytag data/bad.ogg
tinytag data/bad.flac
tinytag data/fake.wav
tinytag data/noise.m4a
tinytag data/short.m4a
tinytag data/cut.mp3
tinytag data/mystery.bin
tinytag data/missing.mp3
tinytag -f xml data/field.wav
tinytag -f csv
tinytag -h data/song.mp3
get data/vorbis.ogg tags=0
get data/vorbis.ogg duration=0
get data/tune.m4a duration=0 image=1
get data/tune.m4a tags=0
get data/song.mp3 tags=0
get data/song.mp3 duration=0 image=1
get data/album.flac duration=0 image=1
get data/vorbis.ogg image=1
get data/old.mp3 image=1
get data/field.wav tags=0 duration=0
get data/show.wma duration=0
get data/loop.aiff tags=0
get data/real_flac.bin magic=0
get data/song.mp3 magic=0 tags=0
images data/song.mp3
images data/album.flac
images data/old.mp3
images data/field.wav
supported song.mp3 SONG.MP3 a.m4b x.aifc clip.wmv notes.txt archive.flac.zip .ogg
files data/out
"""

if __name__ == "__main__":
    main()
