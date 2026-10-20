# Runs data/jobs.tsv through torrentool itself (vendor/torrentool,
# unchanged) and prints what each job gives; expected.out is this output.
# The `info` and `create` jobs are the bodies of torrentool's click
# commands (cli.py) with click.secho as print; `create` then sets the
# creation date to a fixed time, since create_from stamps utcnow().
import datetime
import hashlib
import os
import re
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
sys.dont_write_bytecode = True
warnings.simplefilter("ignore")
os.chdir(HERE)

from torrentool.api import Bencode, Torrent  # noqa: E402
from torrentool.utils import humanize_filesize  # noqa: E402

DATA = "data"
FIXED = datetime.datetime(2024, 10, 20, 12, 0, 0)


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
    # Every line goes out through show().
    sys.stdout.write(show(line) + "\n")


def err(e):
    # A function's repr carries its address, which changes per run.
    return "error: %s: %s" % (type(e).__name__, re.sub(" at 0x[0-9a-f]+>", " at 0x...>", str(e)))


def value(v):
    if callable(v):
        return "<open dict>" if v.__name__ == "create_dict" else "<open list>"
    if isinstance(v, bytes):
        return repr(v) if len(v) <= 32 else "<%d bytes>" % len(v)
    if isinstance(v, list):
        return "[" + ", ".join(value(x) for x in v) + "]"
    if isinstance(v, dict):
        return "{" + ", ".join("%s: %s" % (value(k), value(x)) for k, x in v.items()) + "}"
    return repr(v)


def unescape(text):
    out = bytearray()
    i = 0
    while i < len(text):
        if text.startswith("\\x", i):
            out.append(int(text[i + 2:i + 4], 16))
            i += 4
        else:
            out += text[i].encode()
            i += 1
    return bytes(out)


def escape(b):
    return "".join(chr(c) if 0x20 <= c < 0x7f and c != 0x5c else "\\x%02x" % c for c in b)


def bdecode_job(args):
    keys = None if args[0] == "-" else set(args[0].split(","))
    try:
        print(value(Bencode.decode(unescape(args[1]), byte_keys=keys)))
    except Exception as e:
        print(err(e))


def read_string_job(args):
    try:
        print(value(Bencode.read_string(args[0])))
    except Exception as e:
        print(err(e))


def humanize_job(args):
    print(humanize_filesize(int(args[0])))


def prop(label, f):
    try:
        print("  %s: %s" % (label, show(f())))
    except Exception as e:
        print("  %s: %s" % (label, err(e)))


def files_text(t):
    return "[" + ", ".join("%s (%d)" % (repr(f.name), f.length) for f in t.files) + "]"


def describe(t):
    prop("str", lambda: str(t))
    prop("name", lambda: repr(t.name))
    prop("files", lambda: files_text(t))
    prop("total_size", lambda: str(t.total_size))
    prop("info_hash", lambda: repr(t.info_hash))
    prop("announce_urls", lambda: value(t.announce_urls))
    prop("webseeds", lambda: value(t.webseeds))
    prop("httpseeds", lambda: value(t.httpseeds))
    prop("comment", lambda: value(t.comment))
    prop("source", lambda: value(t.source))
    prop("creation_date", lambda: str(t.creation_date))
    prop("created_by", lambda: value(t.created_by))
    prop("private", lambda: value(t.private))
    prop("magnet_link", lambda: t.magnet_link)
    prop("get_magnet()", lambda: t.get_magnet())
    prop("get_magnet(['ws'])", lambda: t.get_magnet(["ws"]))


def torrent_job(args):
    try:
        t = Torrent.from_file(os.path.join(DATA, args[0]))
    except Exception as e:
        print(err(e))
        return
    describe(t)


def recode_job(args):
    path = os.path.join(DATA, args[0])
    raw = open(path, "rb").read()
    try:
        t = Torrent.from_file(path)
        back = t.to_string()
    except Exception as e:
        print(err(e))
        return
    if back == raw:
        print("same %d bytes" % len(raw))
        return
    i = 0
    while i < min(len(raw), len(back)) and raw[i] == back[i]:
        i += 1
    print("differs at byte %d of %d (now %d bytes)" % (i, len(raw), len(back)))
    print("  was: " + escape(raw[max(0, i - 16):i + 24]))
    print("  now: " + escape(back[max(0, i - 16):i + 24]))
    print("  sha1 now " + hashlib.sha1(back).hexdigest())


def info_job(args):
    # cli.py `torrent info`
    try:
        my_torrent = Torrent.from_file(os.path.join(DATA, args[0]))
        size = my_torrent.total_size
        print(f'Name: {my_torrent.name}')
        print('Files:')
        for file_tuple in my_torrent.files:
            print(file_tuple.name)
        print(f'Hash: {my_torrent.info_hash}')
        print(f'Size: {humanize_filesize(size)} ({size})')
        print(f'Magnet: {my_torrent.get_magnet()}')
    except Exception as e:
        print(err(e))


def split_top(text):
    parts, depth, cur = [], 0, ""
    for c in text:
        if c == "," and depth == 0:
            parts.append(cur)
            cur = ""
            continue
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
        cur += c
    parts.append(cur)
    return parts


def spec(text):
    if text == "-":
        return None
    if text.startswith("["):
        inner = text[1:-1]
        return [] if inner == "" else [spec(p) for p in split_top(inner)]
    return text


def edit_job(args):
    path = os.path.join(DATA, args[0])
    try:
        t = Torrent.from_file(path)
    except Exception as e:
        print(err(e))
        return
    for op in args[1:]:
        k, v = op.split("=", 1)
        try:
            if k == "announce":
                t.announce_urls = spec(v)
            elif k == "webseeds":
                t.webseeds = spec(v)
            elif k == "httpseeds":
                t.httpseeds = spec(v)
            elif k == "comment":
                t.comment = v
            elif k == "source":
                t.source = v
            elif k == "private":
                t.private = v == "1"
            elif k == "name":
                t.name = v
            elif k == "date":
                t.creation_date = datetime.datetime.fromisoformat(v)
            print("  set %s" % op)
        except Exception as e:
            print("  set %s: %s" % (op, err(e)))
    prop("announce_urls", lambda: value(t.announce_urls))
    prop("webseeds", lambda: value(t.webseeds))
    prop("httpseeds", lambda: value(t.httpseeds))
    prop("private", lambda: value(t.private))
    prop("str", lambda: str(t))
    prop("creation_date", lambda: str(t.creation_date))
    prop("get_magnet()", lambda: t.get_magnet())
    try:
        b = t.to_string()
        print("  to_string: %d bytes, sha1 %s" % (len(b), hashlib.sha1(b).hexdigest()))
        print("  decoded: " + value(Bencode.decode(b)))
    except Exception as e:
        print("  to_string: " + err(e))


def create_job(args):
    # cli.py `torrent create`, with --dest data/out
    source = args[0]
    opts = dict(a.split("=", 1) for a in args[1:])
    tracker = opts.get("tracker")
    comment = opts.get("comment")
    source_title = os.path.basename(source).replace('.', '_').replace(' ', '_')
    dest = f'{os.path.join("data/out", source_title)}.torrent'
    print(f'Creating torrent from {source} ...')
    try:
        my_torrent = Torrent.create_from(source)
    except Exception as e:
        print(err(e))
        return
    my_torrent.creation_date = FIXED
    if comment:
        my_torrent.comment = comment
    urls = []
    if tracker:
        urls = tracker.split(',')
    if urls:
        my_torrent.announce_urls = urls
    os.makedirs("data/out", exist_ok=True)
    my_torrent.to_file(dest)
    print(f'Torrent file created: {dest}')
    print(f'Torrent info hash: {my_torrent.info_hash}')
    raw = open(dest, "rb").read()
    print("  %d bytes, sha1 %s" % (len(raw), hashlib.sha1(raw).hexdigest()))
    print("  " + value(Bencode.decode(raw)))


# --- programs

def library_job(args):
    folder = os.path.join(DATA, args[0])
    seen = {}
    total = 0
    count = 0
    for fname in sorted(os.listdir(folder)):
        try:
            t = Torrent.from_file(os.path.join(folder, fname))
            name = t.name
            if name is None:
                print("%s: no name, skipped" % fname)
                continue
            size = t.total_size
            h = t.info_hash
            urls = t.announce_urls
            tracker = urls[0][0].split("/")[2] if urls else "no tracker"
            flags = ("private " if t.private else "") + ("webseed " if t.webseeds else "")
            print("%s" % show(name))
            print("  %s in %d file%s, %s, %s%s" % (humanize_filesize(size), len(t.files), "" if len(t.files) == 1 else "s",
                                                   tracker, flags, h[:12]))
        except Exception as e:
            print("%s: %s" % (fname, err(e)))
            continue
        count += 1
        total += size
        if h in seen:
            print("  same content as %s" % seen[h])
        else:
            seen[h] = fname
    print("%d torrents, %s (%d bytes) in all, %d distinct" % (count, humanize_filesize(total), total, len(seen)))


def verify_job(args):
    try:
        t = Torrent.from_file(os.path.join(DATA, args[0]))
        info = t._struct["info"]
        plen = info["piece length"]
        pieces = info["pieces"]
        files = t.files
    except Exception as e:
        print(err(e))
        return
    base = os.path.join(DATA, args[1])
    blob = bytearray()
    have = []  # per byte range: (start, end, present)
    for f in files:
        p = os.path.join(base, f.name)
        start = len(blob)
        if os.path.isfile(p):
            body = open(p, "rb").read()
            status = "ok" if len(body) == f.length else "%d of %d bytes" % (len(body), f.length)
            body = body[:f.length]
            blob += body
            have.append((start, start + len(body)))
            blob += b"\0" * (f.length - len(body))
        else:
            status = "missing"
            blob += b"\0" * f.length
        print("  %s: %s" % (show(f.name), status))
    count = len(pieces) // 20
    good = 0
    good_bytes = 0
    marks = []
    for i in range(count):
        a, b = i * plen, min((i + 1) * plen, len(blob))
        covered = sum(max(0, min(b, e) - max(a, s)) for s, e in have)
        if covered < b - a:
            marks.append("-")
        elif hashlib.sha1(bytes(blob[a:b])).digest() == pieces[i * 20:i * 20 + 20]:
            marks.append("#")
            good += 1
            good_bytes += b - a
        else:
            marks.append("x")
    for i in range(0, len(marks), 64):
        print("  [%s]" % "".join(marks[i:i + 64]))
    left = t.total_size - good_bytes
    print("  %d of %d pieces ok, %s left" % (good, count, humanize_filesize(left)))
    if good == count:
        print("  complete: " + t.magnet_link)


JOBS = {
    "bdecode": bdecode_job, "read_string": read_string_job, "humanize": humanize_job, "torrent": torrent_job,
    "recode": recode_job, "info": info_job, "edit": edit_job, "create": create_job, "library": library_job,
    "verify": verify_job,
}


def main():
    with open(os.path.join(DATA, "jobs.tsv"), encoding="utf-8") as f:
        for line in f.read().split("\n")[:-1]:
            job = line.split("\t")
            print("== " + show(" ".join(job)))
            JOBS[job[0]](job[1:])


main()
