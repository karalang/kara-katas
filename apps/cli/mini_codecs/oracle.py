# Runs data/ through Python 3.13's own codecs and prints what
# expected.out holds. Run it from the app directory, after mk.py.
import ast
import codecs
import os
import shutil


def read_lines(path):
    with open(path, encoding="utf-8", newline="") as f:
        return [line[:-1] if line.endswith("\n") else line for line in f]


def fail(e):
    return "! %s: %s" % (type(e).__name__, e)


# ------------------------------------------------------------ jobs

def run_jobs():
    for line in read_lines("data/jobs.tsv"):
        f = line.split("\t")
        op = f[0]
        if op == "job":
            print("== " + f[1])
        elif op == "lookup":
            try:
                out = repr(codecs.lookup(f[1]).name)
            except Exception as e:
                out = fail(e)
            print("lookup %r -> %s" % (f[1], out))
        elif op == "decode":
            data = ast.literal_eval(f[3])
            try:
                out = repr(data.decode(f[1], f[2]))
            except Exception as e:
                out = fail(e)
            print("decode %s %s %s -> %s" % (f[1], f[2], f[3], out))
        elif op == "encode":
            text = ast.literal_eval(f[3])
            try:
                out = repr(text.encode(f[1], f[2]))
            except Exception as e:
                out = fail(e)
            print("encode %s %s %s -> %s" % (f[1], f[2], f[3], out))
        elif op == "feed":
            print("feed %s %s" % (f[1], f[2]))
            dec = codecs.getincrementaldecoder(f[1])(f[2])
            pieces = f[3:]
            for i, p in enumerate(pieces):
                final = i == len(pieces) - 1
                try:
                    out = repr(dec.decode(ast.literal_eval(p), final))
                except Exception as e:
                    print("  %s -> %s" % (p, fail(e)))
                    break
                print("  %s%s -> %s" % (p, " final" if final else "", out))


# ------------------------------------------------------------ programs

def endings(b):
    crlf = b.count(b"\r\n")
    cr = b.count(b"\r") - crlf
    lf = b.count(b"\n") - crlf
    return "crlf=%d cr=%d lf=%d" % (crlf, cr, lf)


# Converts each file the manifest lists to UTF-8 with \n line endings,
# and flags text that looks like the wrong codec was named.
def convert_legacy():
    print("== convert legacy files to utf-8")
    for line in read_lines("data/legacy/manifest.tsv"):
        name, enc = line.split("\t")
        print("%s (%s)" % (name, enc))
        try:
            info = codecs.lookup(enc)
        except LookupError as e:
            print("  " + fail(e))
            continue
        path = "data/legacy/" + name
        try:
            with open(path, "rb") as f:
                raw = f.read()
        except OSError as e:
            print("  " + fail(e))
            continue
        try:
            text = raw.decode(info.name)
        except UnicodeDecodeError as e:
            print("  " + fail(e))
            continue
        print("  codec %s, %d bytes, %s" % (info.name, len(raw), endings(raw)))
        # C1 controls, or three or more characters in a row from
        # U+00C0..U+00FF, usually mean the file is in another codec
        c1 = sum(1 for c in text if 0x80 <= ord(c) < 0xA0)
        best, run, start, at = 0, 0, 0, 0
        for i, c in enumerate(text):
            if 0xC0 <= ord(c) <= 0xFF:
                if run == 0:
                    start = i
                run += 1
                if run > best:
                    best, at = run, start
            else:
                run = 0
        if c1 or best >= 3:
            print("  suspicious: %d C1 controls, longest run %r" % (c1, text[at:at + best]))
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        out = text.encode("utf-8")
        dest = "work/" + name
        with open(dest, "wb") as f:
            f.write(out)
        with open(dest, "rb") as f:
            back = f.read().decode("utf-8")
        print("  wrote %s: %d bytes, %d lines, same=%s"
              % (dest, len(out), text.count("\n"), back == text))
        for t in text.split("\n"):
            if t:
                print("  | " + repr(t))
        again = text.encode(info.name, "replace")
        print("  back to %s: %d bytes" % (info.name, len(again)))


BOMS = [
    (codecs.BOM_UTF32_LE, "utf-32"),
    (codecs.BOM_UTF32_BE, "utf-32"),
    (codecs.BOM_UTF8, "utf-8-sig"),
    (codecs.BOM_UTF16_LE, "utf-16"),
    (codecs.BOM_UTF16_BE, "utf-16"),
]


# Reads CSV uploads of unknown encoding: a BOM names the codec, then
# UTF-8 is tried, then cp1252, then UTF-8 with replacement characters.
def read_uploads():
    print("== read csv uploads")
    for name in sorted(os.listdir("data/uploads")):
        with open("data/uploads/" + name, "rb") as f:
            raw = f.read()
        enc = None
        for bom, codec in BOMS:
            if raw.startswith(bom):
                enc = codec
                print("%s: %d bytes, BOM %s -> %s" % (name, len(raw), bom.hex(), codec))
                break
        if enc is not None:
            text = raw.decode(enc)
        else:
            try:
                text = raw.decode("utf-8")
                print("%s: %d bytes, utf-8" % (name, len(raw)))
            except UnicodeDecodeError as e:
                print("%s: %d bytes, not utf-8 (%s)" % (name, len(raw), e))
                try:
                    text = raw.decode("cp1252")
                    print("  fallback cp1252")
                except UnicodeDecodeError as e2:
                    print("  not cp1252 (%s)" % e2)
                    text = raw.decode("utf-8", "replace")
                    print("  fallback utf-8 with replacement")
        rows = [r.split(",") for r in text.split("\n") if r]
        for r in rows:
            print("  " + " | ".join(repr(c) for c in r))


# Keeps undecodable bytes in a log through surrogateescape, so that
# the line can be written back unchanged, and shows a safe view.
def sanitise_log():
    print("== sanitise server.log")
    with open("data/server.log", "rb") as f:
        raw = f.read()
    for n, line in enumerate(raw.split(b"\n")):
        if not line:
            continue
        text = line.decode("utf-8", "surrogateescape")
        bad = [c for c in text if 0xDC80 <= ord(c) <= 0xDCFF]
        print("line %d: %d bytes, %d chars, %d undecodable" % (n + 1, len(line), len(text), len(bad)))
        print("  escaped  " + repr(text))
        print("  shown    " + line.decode("utf-8", "backslashreplace"))
        print("  ascii    " + text.encode("ascii", "backslashreplace").decode("ascii"))
        try:
            text.encode("utf-8")
            print("  strict encode ok")
        except UnicodeEncodeError as e:
            print("  strict encode " + fail(e))
        print("  round trip " + str(text.encode("utf-8", "surrogateescape") == line))
        fields = dict(kv.split("=", 1) for kv in text.split(" ")[2:])
        print("  user=%r path=%r" % (fields["user"], fields["path"]))


# Undoes UTF-8 that was read as cp1252.
def fix_mojibake():
    print("== fix mojibake")
    for line in read_lines("data/mojibake.txt"):
        if not line:
            continue
        print(repr(line))
        try:
            fixed = line.encode("cp1252").decode("utf-8")
        except UnicodeError as e:
            print("  cannot fix: " + fail(e))
            continue
        if fixed == line:
            print("  unchanged")
        else:
            print("  fixed " + repr(fixed))


run_jobs()
if os.path.exists("work"):
    shutil.rmtree("work")
os.makedirs("work")
convert_legacy()
read_uploads()
sanitise_log()
fix_mojibake()
