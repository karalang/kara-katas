# Runs data/jobs.tsv through Python's own wave module (3.13) and prints
# what each job gives; expected.out is this output.
import os
import sys
import warnings
import wave
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
os.chdir(os.path.join(HERE, "data"))
# getmarkers() warns that it goes away in 3.15; the jobs still call it.
warnings.simplefilter("ignore", DeprecationWarning)


def show(text):
    out = []
    for c in text:
        if c == "\r":
            out.append("<CR>")
        elif (c < " " and c not in "\t\n") or "\x7f" <= c <= "\x9f":
            out.append("<x%02x>" % ord(c))
        else:
            out.append(c)
    return "".join(out)


def print(line):
    sys.stdout.write(show(line) + "\n")


def err(e):
    return "error: %s: %s" % (type(e).__name__, e)


def short(data):
    return "%d bytes %s%s" % (len(data), data[:16].hex(), "..." if len(data) > 16 else "")


# --- the module, op by op

def reader_op(w, op):
    name, _, arg = op.partition(":")
    if name == "params":
        return repr(w.getparams())
    if name == "nframes":
        return str(w.getnframes())
    if name == "read":
        return short(w.readframes(int(arg)))
    if name == "tell":
        return str(w.tell())
    if name == "setpos":
        w.setpos(int(arg))
        return "ok"
    if name == "rewind":
        w.rewind()
        return "ok"
    return repr(w.getmarkers())


def reader_job(path, ops):
    try:
        w = wave.open(path)
    except Exception as e:
        print("  open: " + err(e))
        return
    for op in ops:
        try:
            print("  %s: %s" % (op, reader_op(w, op)))
        except Exception as e:
            print("  %s: %s" % (op, err(e)))
    w.close()


def writer_op(w, op):
    name, _, arg = op.partition(":")
    if name == "nch":
        w.setnchannels(int(arg))
    elif name == "sw":
        w.setsampwidth(int(arg))
    elif name == "rate":
        w.setframerate(float(arg))
    elif name == "nframes":
        w.setnframes(int(arg))
    elif name == "comp":
        kind, _, label = arg.partition(":")
        w.setcomptype(kind, label)
    elif name == "params":
        p = arg.split(",")
        w.setparams((int(p[0]), int(p[1]), int(p[2]), int(p[3]), p[4], p[5]))
    elif name == "write":
        w.writeframes(bytes.fromhex(arg))
    elif name == "raw":
        w.writeframesraw(bytes.fromhex(arg))
    elif name == "getnframes":
        return str(w.getnframes())
    elif name == "tell":
        return str(w.tell())
    elif name == "getparams":
        return repr(w.getparams())
    elif name == "markers":
        return repr(w.getmarkers())
    else:
        w.close()
    return "ok"


def writer_job(path, ops):
    w = wave.open(path, "wb")
    for op in ops + ["end"]:
        try:
            print("  %s: %s" % (op, writer_op(w, op)))
        except Exception as e:
            print("  %s: %s" % (op, err(e)))
    with open(path, "rb") as f:
        data = f.read()
    print("  file %d bytes: %s" % (len(data), data.hex()))


# --- programs

def full(sw):
    return 1 << (8 * sw - 1)


def load(path):
    with wave.open(path) as w:
        return w.getparams(), w.readframes(w.getnframes())


def decode(data, nch, sw):
    frames = []
    size = nch * sw
    for i in range(len(data) // size):
        frame = []
        for c in range(nch):
            b = data[i * size + c * sw:i * size + (c + 1) * sw]
            frame.append(b[0] - 128 if sw == 1 else int.from_bytes(b, "little", signed=True))
        frames.append(frame)
    return frames


def encode(frames, sw):
    out = bytearray()
    for frame in frames:
        for s in frame:
            if sw == 1:
                out.append(s + 128)
            else:
                out += s.to_bytes(sw, "little", signed=True)
    return bytes(out)


def describe(p):
    return "%d ch, %d-bit, %d Hz" % (p[0], p[1] * 8, p[2])


def loud_frames(frames, threshold):
    return [i for i, f in enumerate(frames) if any(abs(s) > threshold for s in f)]


def inspect(folder):
    ok = bad = total = 0
    for name in sorted(os.listdir(folder)):
        try:
            p, data = load(folder + "/" + name)
        except Exception as e:
            print("%s: %s" % (name, err(e)))
            bad += 1
            continue
        frames = decode(data, p.nchannels, p.sampwidth)
        print("%s: %s, %d frames, %d ms" % (name, describe(p), p.nframes, p.nframes * 1000 // p.framerate))
        if len(frames) != p.nframes:
            print("  header says %d frames, the file holds %d" % (p.nframes, len(frames)))
        top = full(p.sampwidth)
        peaks = [max([abs(f[c]) for f in frames], default=0) for c in range(p.nchannels)]
        print("  peak " + " ".join("%d (%d%%)" % (pk, pk * 100 // top) for pk in peaks))
        loud = loud_frames(frames, top // 100)
        if not loud:
            print("  silent")
        else:
            print("  quiet %d ms in, %d ms out" % (loud[0] * 1000 // p.framerate,
                                                  (len(frames) - 1 - loud[-1]) * 1000 // p.framerate))
        ok += 1
        total += len(frames) * 1000 // p.framerate
    print("%d files read, %d refused, %d ms of audio" % (ok, bad, total))


def report(path):
    with open(path, "rb") as f:
        raw = f.read()
    p, data = load(path)
    print("  wrote %s: %s, %d frames, %d bytes, crc32 %08x" % (path, describe(p), p.nframes, len(raw),
                                                             zlib.crc32(raw)))


def opened(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return wave.open(path, "wb")


def source(src):
    try:
        p, data = load(src)
    except Exception as e:
        print("%s: %s" % (src, err(e)))
        return None, None
    return p, decode(data, p.nchannels, p.sampwidth)


def mixdown(src, dst):
    p, frames = source(src)
    if p is None:
        return
    if p.nchannels == 1:
        print("%s is already mono" % src)
        return
    mono = [[sum(f) // p.nchannels] for f in frames]
    print("mixdown %s: %d frames" % (src, len(mono)))
    with opened(dst) as w:
        w.setnchannels(1)
        w.setsampwidth(p.sampwidth)
        w.setframerate(p.framerate)
        for i in range(0, len(mono), 256):
            w.writeframes(encode(mono[i:i + 256], p.sampwidth))
    report(dst)


def normalize(src, dst, pct):
    p, frames = source(src)
    if p is None:
        return
    peak = max([abs(s) for f in frames for s in f], default=0)
    if peak == 0:
        print("%s is silent, nothing to normalize" % src)
        return
    top = full(p.sampwidth)
    target = top * pct // 100
    out = [[max(-top, min(top - 1, s * target // peak)) for s in f] for f in frames]
    print("normalize %s: peak %d -> %d" % (src, peak, max(abs(s) for f in out for s in f)))
    with opened(dst) as w:
        w.setparams((p.nchannels, p.sampwidth, p.framerate, len(out), "NONE", "not compressed"))
        w.writeframes(encode(out, p.sampwidth))
    report(dst)


def trim(src, dst, pct):
    p, frames = source(src)
    if p is None:
        return
    loud = loud_frames(frames, full(p.sampwidth) * pct // 100)
    if not loud:
        print("%s: nothing left after trimming" % src)
        return
    keep = frames[loud[0]:loud[-1] + 1]
    print("trim %s: %d frames from the start, %d from the end" % (src, loud[0], len(frames) - 1 - loud[-1]))
    w = opened(dst)
    w.setnchannels(p.nchannels)
    w.setsampwidth(p.sampwidth)
    w.setframerate(p.framerate)
    for i in range(0, len(keep), 100):
        w.writeframesraw(encode(keep[i:i + 100], p.sampwidth))
    w.close()
    report(dst)


def convert(src, dst, bits):
    p, frames = source(src)
    if p is None:
        return
    sw = bits // 8
    d = 8 * (sw - p.sampwidth)
    out = [[s << d if d >= 0 else s >> -d for s in f] for f in frames]
    print("convert %s: %d-bit to %d-bit" % (src, p.sampwidth * 8, bits))
    with opened(dst) as w:
        w.setnchannels(p.nchannels)
        w.setsampwidth(sw)
        w.setframerate(p.framerate)
        w.writeframes(encode(out, sw))
    report(dst)


def concat(playlist, dst):
    with open(playlist, encoding="utf-8") as f:
        names = [line for line in f.read().split("\n") if line and not line.startswith("#")]
    want = None
    clips = []
    for name in names:
        try:
            p, data = load(name)
        except Exception as e:
            print("  skipping %s: %s" % (name, err(e)))
            continue
        if want is None:
            want = p
        elif p[:3] != want[:3]:
            print("  skipping %s: %s, want %s" % (name, describe(p), describe(want)))
            continue
        frames = decode(data, p.nchannels, p.sampwidth)
        print("  %s: %d frames" % (name, len(frames)))
        clips.append(encode(frames, p.sampwidth))
    if not clips:
        print("concat %s: nothing to write" % playlist)
        return
    with opened(dst) as w:
        w.setnchannels(want.nchannels)
        w.setsampwidth(want.sampwidth)
        w.setframerate(want.framerate)
        for clip in clips:
            w.writeframes(clip)
    print("concat %s: %d clips, %d frames" % (playlist, len(clips), sum(len(c) for c in clips) // (
        want.nchannels * want.sampwidth)))
    report(dst)


def main():
    with open("jobs.tsv", encoding="utf-8") as f:
        jobs = f.read().split("\n")[:-1]
    for line in jobs:
        job = line.split("\t")
        print("== " + " ".join(job))
        kind, a = job[0], job[1:]
        if kind == "reader":
            reader_job(a[0], a[1:])
        elif kind == "writer":
            writer_job(a[0], a[1:])
        elif kind == "inspect":
            inspect(a[0])
        elif kind == "mixdown":
            mixdown(a[0], a[1])
        elif kind == "normalize":
            normalize(a[0], a[1], int(a[2]))
        elif kind == "trim":
            trim(a[0], a[1], int(a[2]))
        elif kind == "convert":
            convert(a[0], a[1], int(a[2]))
        elif kind == "concat":
            concat(a[0], a[1])


main()
