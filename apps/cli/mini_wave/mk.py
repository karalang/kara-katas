# Writes data/: a podcast's upload folder (WAV files as recorders, phones,
# editors and broken uploads produce them, and files that only claim to
# be WAV), a playlist, and jobs.tsv, the jobs oracle.py and mini_wave.kara
# run. The files are built byte by byte here, so the malformed ones are
# exactly what they say; the tones are computed once and stored.
import math
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

PCM_GUID = b"\x01\x00\x00\x00\x00\x00\x10\x00\x80\x00\x00\xaa\x00\x38\x9b\x71"
FLOAT_GUID = b"\x03" + PCM_GUID[1:]


def chunk(name, body, size=None):
    n = len(body) if size is None else size
    pad = b"\x00" if len(body) & 1 else b""
    return name + struct.pack("<L", n) + body + pad


def riff(chunks, size=None, form=b"WAVE", tag=b"RIFF"):
    body = form + b"".join(chunks)
    return tag + struct.pack("<L", len(body) if size is None else size) + body


def fmt(nch, rate, bits, tag=1):
    width = (bits + 7) // 8
    return struct.pack("<HHLLHH", tag, nch, rate, rate * nch * width, nch * width, bits)


def fmt_ext(nch, rate, bits, guid, mask=4):
    return fmt(nch, rate, bits, 0xFFFE) + struct.pack("<HHL", 22, bits, mask) + guid


def tone(rate, ms, parts):
    # parts: (lead ms, tail ms, freq, amplitude) per channel; a little
    # noise in the quiet parts, as a real recording has.
    n = rate * ms // 1000
    frames = []
    for i in range(n):
        frame = []
        for c, (lead, tail, freq, amp) in enumerate(parts):
            a, b = rate * lead // 1000, n - rate * tail // 1000
            if a <= i < b:
                frame.append(int(round(amp * math.sin(2 * math.pi * freq * (i - a) / rate))))
            else:
                frame.append((i * 7 + c * 3) % 5 - 2)
        frames.append(frame)
    return frames


def pack(frames, width):
    out = bytearray()
    for frame in frames:
        for s in frame:
            if width == 1:
                out.append(s + 128)
            else:
                out += s.to_bytes(width, "little", signed=True)
    return bytes(out)


def pcm(nch, rate, bits, frames, extra=()):
    return riff([chunk(b"fmt ", fmt(nch, rate, bits))] + list(extra)
                + [chunk(b"data", pack(frames, (bits + 7) // 8))])


def files():
    f = {}
    intro = tone(8000, 300, [(50, 50, 440, 12000)])
    f["uploads/01-intro.wav"] = pcm(1, 8000, 16, intro)
    f["uploads/02-interview.wav"] = pcm(2, 11025, 16, tone(11025, 100, [(10, 0, 300, 8000), (0, 20, 500, 20000)]))
    f["uploads/03-phone.wav"] = pcm(1, 8000, 8, tone(8000, 150, [(20, 20, 350, 100)]))
    info = chunk(b"LIST", b"INFO" + chunk(b"INAM", b"Theme\x00") + chunk(b"IART", b"The Band\x00"))
    f["uploads/04-music.wav"] = pcm(2, 8000, 24, tone(8000, 50, [(0, 0, 220, 4000000), (0, 0, 330, 6500000)]),
                                    [info])
    ext = tone(8000, 50, [(5, 5, 1000, 30000)])
    f["uploads/05-extensible.wav"] = riff([chunk(b"fmt ", fmt_ext(1, 8000, 16, PCM_GUID)),
                                           chunk(b"fact", struct.pack("<L", len(ext))),
                                           chunk(b"data", pack(ext, 2))])
    f["uploads/06-float.wav"] = riff([chunk(b"fmt ", fmt(1, 8000, 32, 3)), chunk(b"data", bytes(40))])
    f["uploads/07-ext-float.wav"] = riff([chunk(b"fmt ", fmt_ext(2, 48000, 32, FLOAT_GUID, 3)),
                                          chunk(b"data", bytes(64))])
    f["uploads/08-episode.mp3.wav"] = b"ID3\x04\x00\x00\x00\x00\x00\x00" + bytes(30)
    f["uploads/09-clip.avi.wav"] = riff([chunk(b"avih", bytes(56))], form=b"AVI ")
    whole = pcm(1, 8000, 16, intro)
    f["uploads/10-cut-off.wav"] = whole[:1044]
    f["uploads/11-no-data.wav"] = riff([chunk(b"fmt ", fmt(1, 8000, 16))])
    f["uploads/12-data-first.wav"] = riff([chunk(b"data", bytes(8)), chunk(b"fmt ", fmt(1, 8000, 16))])
    f["uploads/13-short-fmt.wav"] = riff([chunk(b"fmt ", fmt(1, 8000, 16)[:12]), chunk(b"data", bytes(8))])
    f["uploads/14-12bit.wav"] = pcm(1, 8000, 12, tone(8000, 20, [(0, 0, 500, 1500)]))
    f["uploads/15-no-channels.wav"] = riff([chunk(b"fmt ", fmt(0, 8000, 16)), chunk(b"data", bytes(8))])
    f["uploads/16-big-list.wav"] = riff([chunk(b"fmt ", fmt(1, 8000, 16)),
                                         chunk(b"LIST", b"INFO" + bytes(20), 1000000),
                                         chunk(b"data", bytes(8))])
    f["uploads/17-short-riff.wav"] = riff([chunk(b"fmt ", fmt(1, 8000, 16)), chunk(b"data", pack(intro[:20], 2))],
                                          size=28)
    f["uploads/18-empty.wav"] = b""
    f["uploads/19-zero-bits.wav"] = riff([chunk(b"fmt ", fmt(1, 8000, 0)), chunk(b"data", bytes(8))])
    f["uploads/20-silence.wav"] = pcm(1, 8000, 16, [[0]] * 800)
    odd = pack(tone(8000, 40, [(5, 0, 600, 90)])[:301], 1)
    f["uploads/21-odd.wav"] = riff([chunk(b"fmt ", fmt(1, 8000, 8)), chunk(b"data", odd),
                                    chunk(b"junk", b"trailing junk")])
    f["uploads/22-long-riff.wav"] = riff([chunk(b"fmt ", fmt(1, 8000, 16)), chunk(b"data", pack(intro[:30], 2))],
                                         size=4000)
    f["uploads/23-fmt-only-14.wav"] = riff([chunk(b"fmt ", fmt(1, 8000, 16)[:14]), chunk(b"data", bytes(8))])
    f["uploads/24-quiet.wav"] = pcm(2, 8000, 16, tone(8000, 40, [(0, 0, 200, 60), (0, 0, 250, 40)]))
    f["uploads/notes.txt"] = b"episode 12: intro, interview, theme. phone call at 14:05.\n"
    f["playlist.txt"] = (b"# episode 12, in order\nuploads/01-intro.wav\nuploads/20-silence.wav\n"
                         b"uploads/02-interview.wav\nuploads/05-extensible.wav\nuploads/missing.wav\n"
                         b"uploads/10-cut-off.wav\nuploads/06-float.wav\nuploads/01-intro.wav\n")
    f["phone-playlist.txt"] = b"uploads/03-phone.wav\nuploads/21-odd.wav\nuploads/03-phone.wav\n"
    return f


JOBS = [
    # Reading, op by op.
    "reader\tuploads/01-intro.wav\tparams\tnframes\tread:4\ttell\tread:2\tsetpos:2398\tread:10\ttell\trewind\tread:1",
    "reader\tuploads/02-interview.wav\tparams\tread:3\tsetpos:1102\tread:5\tsetpos:1103\tsetpos:-1\ttell",
    "reader\tuploads/03-phone.wav\tparams\tread:6\tread:0\ttell",
    "reader\tuploads/04-music.wav\tparams\tread:2",
    "reader\tuploads/05-extensible.wav\tparams\tread:2",
    "reader\tuploads/10-cut-off.wav\tparams\tread:3000\ttell\tsetpos:1000\tread:4\ttell",
    "reader\tuploads/14-12bit.wav\tparams\tread:3",
    "reader\tuploads/21-odd.wav\tparams\tsetpos:299\tread:5\ttell",
    "reader\tuploads/22-long-riff.wav\tparams\tread:40\ttell",
    "reader\tuploads/24-quiet.wav\tmarkers",
] + ["reader\tuploads/%s\tparams" % n for n in [
    "06-float.wav", "07-ext-float.wav", "08-episode.mp3.wav", "09-clip.avi.wav", "11-no-data.wav",
    "12-data-first.wav", "13-short-fmt.wav", "15-no-channels.wav", "16-big-list.wav", "17-short-riff.wav",
    "18-empty.wav", "19-zero-bits.wav", "23-fmt-only-14.wav", "notes.txt", "nothing-here.wav"]] + [
    # Writing, op by op; the file is read back after the writer closes.
    "writer\tw1.wav\tnch:1\tsw:2\trate:8000\twrite:0100ff7f0080",
    "writer\tw2.wav\tnch:2\tsw:1\trate:22050.5\twrite:8080\tgetnframes\twrite:7f817e82\ttell\tgetparams",
    "writer\tw3.wav\tparams:1,2,8000,4,NONE,not compressed\traw:01000200\ttell",
    "writer\tw4.wav\tnch:1\tsw:2\trate:8000\tnframes:10\twrite:0100020003",
    "writer\tw5.wav\twrite:0000",
    "writer\tw6.wav\tnch:1\tsw:2\twrite:0000",
    "writer\tw7.wav\tnch:1\tsw:5\tsw:0\tnch:0\trate:0\trate:-5\tcomp:ULAW:u-law\tgetparams\tsw:3\trate:8000.5",
    "writer\tw8.wav\tnch:1\tsw:2\trate:8000\twrite:\tnch:2\twrite:01020304\tnch:1\tgetnframes",
    "writer\tw9.wav\tnch:1\tsw:1\trate:8000\twrite:808182\tclose\twrite:83",
    "writer\tw10.wav\tparams:2,3,44100,0,NONE,pcm\twrite:000000010000ffffff000080\tgetparams",
    "writer\tw11.wav\tnch:1\tsw:4\trate:96000\tgetnframes\tgetparams\tmarkers",
    "writer\tw12.wav\tnch:1\tsw:2\trate:7999.5\twrite:01",
    # The programs.
    "inspect\tuploads",
    "mixdown\tuploads/02-interview.wav\tout/interview-mono.wav",
    "mixdown\tuploads/04-music.wav\tout/music-mono.wav",
    "mixdown\tuploads/01-intro.wav\tout/intro-mono.wav",
    "mixdown\tuploads/06-float.wav\tout/float-mono.wav",
    "normalize\tuploads/01-intro.wav\tout/intro-loud.wav\t90",
    "normalize\tuploads/03-phone.wav\tout/phone-loud.wav\t100",
    "normalize\tuploads/24-quiet.wav\tout/quiet-loud.wav\t50",
    "normalize\tuploads/20-silence.wav\tout/silence-loud.wav\t90",
    "trim\tuploads/01-intro.wav\tout/intro-trim.wav\t1",
    "trim\tuploads/02-interview.wav\tout/interview-trim.wav\t5",
    "trim\tuploads/20-silence.wav\tout/silence-trim.wav\t1",
    "trim\tuploads/21-odd.wav\tout/odd-trim.wav\t10",
    "convert\tuploads/03-phone.wav\tout/phone-16.wav\t16",
    "convert\tuploads/04-music.wav\tout/music-16.wav\t16",
    "convert\tuploads/01-intro.wav\tout/intro-8.wav\t8",
    "convert\tuploads/14-12bit.wav\tout/12bit-32.wav\t32",
    "concat\tplaylist.txt\tout/episode.wav",
    "concat\tphone-playlist.txt\tout/phone-call.wav",
    "inspect\tout",
]


def main():
    if os.path.isdir(DATA):
        shutil.rmtree(DATA)
    for name, body in files().items():
        path = os.path.join(DATA, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(body)
    with open(os.path.join(DATA, "jobs.tsv"), "w") as fh:
        fh.write("".join(j + "\n" for j in JOBS))


main()
