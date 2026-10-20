# Runs data/jobs.tsv through Python 3.13's own mimetypes module and
# prints what expected.out holds. Run it from the app directory, after
# mk.py.
import contextlib
import io
import os
import sys
import urllib.parse
import posixpath

import mimetypes
from mimetypes import MimeTypes

KNOWN = ["data/system/mime.types", "data/apache/mime.types", "data/missing/mime.types"]
mimetypes.knownfiles = list(KNOWN)


def reset_module():
    mimetypes._db = None
    mimetypes.inited = False


reset_module()
mimetypes.init()


def unesc(s):
    out = []
    i = 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            if s[i + 1] == "\\":
                out.append("\\")
                i += 2
                continue
            if s[i + 1] == "x":
                out.append(chr(int(s[i + 2:i + 4], 16)))
                i += 4
                continue
        out.append(s[i])
        i += 1
    return "".join(out)


def err(e):
    return f"{type(e).__name__}: {e}"


def strict_arg(flag):
    return "" if flag == "1" else ", strict=False"


def show(head, f):
    try:
        print(f"{head} = {f()!r}")
    except Exception as e:
        print(f"{head} -> {err(e)}")


def from_file(db, defaults):
    # the entries of a types map that the defaults do not have
    return {k: v for k, v in db.items() if defaults.get(k) != v}


DEFAULTS = MimeTypes().types_map[True]


def run_job(name, lines):
    print(f"== {name}")
    db = MimeTypes()
    for line in lines:
        f = [unesc(x) for x in line.split("\t")]
        op = f[0]
        if op in ("type", "ftype", "ext", "exts", "gtype", "gext"):
            s = f[1] == "1"
            arg = f[2] if len(f) > 2 else ""
            if op == "type":
                show(f"guess_type({arg!r}{strict_arg(f[1])})", lambda: db.guess_type(arg, s))
            elif op == "ftype":
                show(f"guess_file_type({arg!r}{strict_arg(f[1])})", lambda: db.guess_file_type(arg, strict=s))
            elif op == "ext":
                show(f"guess_extension({arg!r}{strict_arg(f[1])})", lambda: db.guess_extension(arg, s))
            elif op == "exts":
                show(f"guess_all_extensions({arg!r}{strict_arg(f[1])})", lambda: db.guess_all_extensions(arg, s))
            elif op == "gtype":
                show(f"mimetypes.guess_type({arg!r}{strict_arg(f[1])})", lambda: mimetypes.guess_type(arg, s))
            else:
                show(f"mimetypes.guess_extension({arg!r}{strict_arg(f[1])})", lambda: mimetypes.guess_extension(arg, s))
        elif op == "add":
            db.add_type(f[2], f[3], f[1] == "1")
            print(f"add_type({f[2]!r}, {f[3]!r}{strict_arg(f[1])})")
        elif op == "gadd":
            mimetypes.add_type(f[2], f[3], f[1] == "1")
            print(f"mimetypes.add_type({f[2]!r}, {f[3]!r}{strict_arg(f[1])})")
        elif op == "read":
            path = "data/" + f[2]
            try:
                db.read(path, f[1] == "1")
                print(f"read({path!r}{strict_arg(f[1])})")
            except Exception as e:
                print(f"read({path!r}{strict_arg(f[1])}) -> {err(e)}")
        elif op == "readmt":
            path = "data/" + f[1]
            r = mimetypes.read_mime_types(path)
            if r is None:
                print(f"read_mime_types({path!r}) = None")
            else:
                print(f"read_mime_types({path!r}) = {len(r)} entries; from the file: {from_file(r, DEFAULTS)!r}")
        elif op == "init":
            files = ["data/" + x for x in f[1:]]
            if files:
                mimetypes.init(files)
                print(f"mimetypes.init({files!r})")
            else:
                mimetypes.init()
                print("mimetypes.init()")
        elif op == "maps":
            print(f"suffix_map = {mimetypes.suffix_map!r}")
            print(f"encodings_map = {mimetypes.encodings_map!r}")
            print(f"types_map: {len(mimetypes.types_map)} entries; from files: {from_file(mimetypes.types_map, DEFAULTS)!r}")
            print(f"common_types = {mimetypes.common_types!r}")
        elif op in ("new", "new0"):
            files = ["data/" + x for x in f[1:]]
            s = op == "new"
            try:
                db = MimeTypes(files, s)
                print(f"MimeTypes({files!r}{strict_arg('1' if s else '0')})")
            except Exception as e:
                print(f"MimeTypes({files!r}{strict_arg('1' if s else '0')}) -> {err(e)}")
        else:
            raise SystemExit("bad op " + op)


def run_cli(args):
    print(f"$ python -m mimetypes {' '.join(args)}".rstrip())
    reset_module()
    out = io.StringIO()
    old = sys.argv
    sys.argv = ["mimetypes.py"] + args
    code = 0
    try:
        with contextlib.redirect_stdout(out):
            mimetypes._main()
    except SystemExit as e:
        code = e.code
    finally:
        sys.argv = old
    for l in out.getvalue().split("\n")[:-1]:
        print(f"  {l}" if l else "")
    print(f"exit {code}")


# ------------------------------------------------------------ programs

def lines_of(path):
    out = []
    with open(path, encoding="utf-8") as fp:
        for l in fp.read().split("\n"):
            if l.strip() == "" or l.startswith("#"):
                continue
            out.append(l)
    return out


def site_db():
    db = MimeTypes()
    db.read("data/system/mime.types")
    db.read("data/apache/mime.types")
    db.read("data/local/mime.types", False)
    return db


TEXTISH = ("application/javascript", "text/javascript", "application/json",
           "application/xml", "image/svg+xml", "application/manifest+json")


def with_charset(t):
    if t.startswith("text/") or t in TEXTISH:
        return t + "; charset=utf-8"
    return t


# http.server.SimpleHTTPRequestHandler.guess_type, over the module db
HANDLER_MAP = {'.gz': 'application/gzip', '.Z': 'application/octet-stream',
               '.bz2': 'application/x-bzip2', '.xz': 'application/x-xz'}


def handler_guess(path):
    base, ext = posixpath.splitext(path)
    if ext in HANDLER_MAP:
        return HANDLER_MAP[ext]
    ext = ext.lower()
    if ext in HANDLER_MAP:
        return HANDLER_MAP[ext]
    guess, _ = mimetypes.guess_file_type(path)
    if guess:
        return guess
    return 'application/octet-stream'


def prog_server():
    print("== program: static file server")
    reset_module()
    mimetypes.init()
    print("Content-type, as http.server picks it:")
    for p in lines_of("data/server/requests.txt"):
        if p.endswith("/"):
            t = "text/html; charset=utf-8 (directory listing)"
        else:
            t = handler_guess(p)
        print(f"  {p:<36} {t}")
    db = site_db()
    disk = set(lines_of("data/server/precompressed.txt"))
    print("precompressed variants:")
    for l in lines_of("data/server/accept.txt"):
        path, ae = l.split("\t")
        toks = [t.split(";")[0].strip().lower() for t in ae.split(",")]
        rel = path[1:]
        enc = None
        for want, suf in (("br", ".br"), ("gzip", ".gz")):
            if (want in toks or "*" in toks) and rel + suf in disk:
                enc = (want, suf)
                break
        t, _ = db.guess_type(rel)
        ctype = with_charset(t) if t else "application/octet-stream"
        if enc:
            print(f"  {path} [{ae}] -> {rel}{enc[1]}: Content-Type {ctype}, Content-Encoding {enc[0]}, Vary: Accept-Encoding")
        else:
            print(f"  {path} [{ae}] -> {rel}: Content-Type {ctype}, Vary: Accept-Encoding")


def prog_nginx():
    print("== program: nginx types block")
    db = MimeTypes()
    order = []
    exts_of = {}
    stmts = 0
    with open("data/nginx/mime.types", encoding="utf-8") as fp:
        text = fp.read()
    inside = False
    for raw in text.split("\n"):
        l = raw.strip()
        if l == "" or l.startswith("#"):
            continue
        if l == "types {":
            inside = True
            continue
        if l == "}":
            inside = False
            continue
        if not inside or not l.endswith(";"):
            print(f"  skipped: {l!r}")
            continue
        words = l[:-1].split()
        stmts += 1
        t = words[0]
        if t not in exts_of:
            order.append(t)
            exts_of[t] = []
        for e in words[1:]:
            db.add_type(t, "." + e)
            exts_of[t].append(e)
    print(f"{stmts} statements, {len(order)} types")
    sysdb = site_db()
    print("where nginx and the site's mime.types disagree:")
    n = 0
    for t in order:
        for e in exts_of[t]:
            a = db.guess_type("x." + e)[0]
            b = sysdb.guess_type("x." + e)[0]
            if a != b:
                n += 1
                print(f"  .{e:<6} nginx {a}, mime.types {b}")
    print(f"  {n} extensions differ")
    out = []
    for t in order:
        out.append(f"{t:<40}{' '.join(exts_of[t])}")
    print(f"as a mime.types file ({len(out)} lines), the first five and the octet-stream line:")
    for l in out[:5]:
        print(f"  {l}")
    for l in out:
        if l.startswith("application/octet-stream"):
            print(f"  {l}")
    back = MimeTypes()
    back.readfp(io.StringIO("\n".join(out) + "\n"))
    same = 0
    for t in order:
        for e in exts_of[t]:
            if back.guess_type("x." + e) == db.guess_type("x." + e):
                same += 1
    total = sum(len(exts_of[t]) for t in order)
    print(f"read back: {same} of {total} extensions guess the same")
    print(f"guess_extension('application/octet-stream') nginx {db.guess_extension('application/octet-stream')}, read back {back.guess_extension('application/octet-stream')}")


def prog_uploads():
    print("== program: upload validator")
    db = site_db()
    policy = {}
    for l in lines_of("data/uploads/policy.conf"):
        t, n = l.split()
        policy[t] = int(n)
    ok = 0
    for i, l in enumerate(lines_of("data/uploads/uploads.tsv")):
        name, sent, size = l.split("\t")
        size = int(size)
        declared = sent.split(";")[0].strip().lower()
        t, enc = db.guess_type(name)
        base, ext = posixpath.splitext(name)
        inner = db.guess_type(base)[0] if ext else None
        if t is None:
            verdict = "reject: the name gives no known type"
        elif enc is not None:
            verdict = f"reject: {enc}-compressed {t}"
        elif inner is not None and t in ("application/x-msdownload", "application/octet-stream"):
            verdict = f"reject: an executable named like {inner}"
        elif t not in policy:
            verdict = f"reject: {t} is not accepted"
        elif declared != t:
            verdict = f"reject: sent as {declared} but the name says {t}"
        elif size > policy[t]:
            verdict = f"reject: {size} bytes, over the {policy[t]} limit"
        else:
            ok += 1
            verdict = f"accept as upload-{i + 1:03d}{db.guess_extension(t)}"
        print(f"  {name:<18} {verdict}")
    print(f"{ok} accepted")


def prog_objstore():
    print("== program: object store upload plan")
    db = site_db()
    by = {}
    for p in lines_of("data/objstore/manifest.txt"):
        t, enc = db.guess_type(p, strict=False)
        ctype = with_charset(t) if t else "application/octet-stream"
        if t is None:
            cache = "public, max-age=300"
        elif "/assets/" in p or t.startswith("font/") or t.startswith("image/"):
            cache = "public, max-age=31536000, immutable"
        elif t == "text/html":
            cache = "no-cache"
        else:
            cache = "public, max-age=300"
        extra = f"; Content-Encoding: {enc}" if enc in ("gzip", "br") else ""
        print(f"  {p}: Content-Type: {ctype}{extra}; Cache-Control: {cache}")
        major = (t or "application/octet-stream").split("/")[0]
        by[major] = by.get(major, 0) + 1
    print("objects by major type: " + ", ".join(f"{k} {by[k]}" for k in sorted(by)))


def prog_mail():
    print("== program: mail attachments")
    db = site_db()
    cls = {"text": "MIMEText", "image": "MIMEImage", "audio": "MIMEAudio"}
    for p in lines_of("data/mail/attachments.txt"):
        ctype, encoding = db.guess_type(p)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)
        c = cls.get(maintype, "MIMEBase")
        print(f"  {p!r}: {c}, Content-Type: {maintype}/{subtype}; name={p!r}")


def parse_accept(h):
    out = []
    for part in h.split(","):
        part = part.strip()
        if not part:
            continue
        bits = [b.strip() for b in part.split(";")]
        q = 1.0
        for b in bits[1:]:
            if b.startswith("q="):
                q = float(b[2:])
        out.append((bits[0].lower(), q))
    if not out:
        out.append(("*/*", 1.0))
    return out


def match_q(rng, t):
    best = None
    for r, q in rng:
        if r == t:
            spec = 3
        elif r.endswith("/*") and t.split("/")[0] == r[:-2]:
            spec = 2
        elif r == "*/*":
            spec = 1
        else:
            continue
        if best is None or spec > best[0]:
            best = (spec, q)
    return None if best is None else best[1]


def prog_negotiate():
    print("== program: content negotiation")
    db = site_db()
    variants = {}
    for l in lines_of("data/negotiate/variants.txt"):
        name, files = l.split("\t")
        variants[name] = files.split()
    for l in open("data/negotiate/requests.txt", encoding="utf-8").read().split("\n"):
        if l == "" or l.startswith("#"):
            continue
        name, accept = l.split("\t")
        rng = parse_accept(accept)
        best = None
        for f in variants[name]:
            t = db.guess_type(f)[0]
            if t is None:
                continue
            q = match_q(rng, t)
            if q is None or q <= 0:
                continue
            if best is None or q > best[1]:
                best = (f, q, t)
        if best is None:
            print(f"  {name} [{accept}] -> 406 Not Acceptable")
        else:
            print(f"  {name} [{accept}] -> {best[0]} ({best[2]}, q={best[1]:.3f})")


def prog_cdnlog():
    print("== program: CDN log by type")
    db = site_db()
    bytes_by = {}
    hits_by = {}
    naive_wrong = 0
    bad = 0
    for l in lines_of("data/cdnlog/access.log"):
        q1 = l.find('"')
        q2 = l.find('"', q1 + 1)
        req = l[q1 + 1:q2].split(" ")
        rest = l[q2 + 1:].split()
        if len(req) != 3 or len(rest) != 2:
            bad += 1
            continue
        target = req[1]
        naive = db.guess_type(target)[0]
        path = urllib.parse.urlsplit(target).path
        t = db.guess_type(path)[0]
        if naive != t:
            naive_wrong += 1
            print(f"  {target}: guess_type on the raw target says {naive}, on the path {t}")
        key = t or "(unknown)"
        bytes_by[key] = bytes_by.get(key, 0) + int(rest[1])
        hits_by[key] = hits_by.get(key, 0) + 1
    print(f"{bad} unparsable lines; {naive_wrong} targets need the query or fragment cut first")
    for k in sorted(bytes_by, key=lambda k: (-bytes_by[k], k)):
        print(f"  {k:<28} {hits_by[k]:>3} hits {bytes_by[k]:>10} bytes")


def prog_inventory():
    print("== program: shared-drive inventory")
    db = site_db()
    size_by = {}
    count_by = {}
    renames = []
    unknown = []
    for l in lines_of("data/inventory/files.txt"):
        path, size = l.rsplit(" ", 1)
        size = int(size)
        t, enc = db.guess_type(path)
        if t is None:
            unknown.append(path)
            major = "(unknown)"
        else:
            major = t.split("/")[0]
            if enc is None:
                canon = db.guess_extension(t)
                ext = posixpath.splitext(path)[1]
                if canon is not None and ext != canon:
                    renames.append((path, t, canon))
        size_by[major] = size_by.get(major, 0) + size
        count_by[major] = count_by.get(major, 0) + 1
    print("by major type:")
    for k in sorted(size_by):
        print(f"  {k:<12} {count_by[k]:>3} files {size_by[k]:>11} bytes")
    print(f"{len(renames)} files whose extension is not the type's first one:")
    for path, t, canon in renames:
        print(f"  {path} ({t}): {canon}")
    print(f"{len(unknown)} with no known type: {', '.join(unknown)}")


PROGRAMS = {"server": prog_server, "nginx": prog_nginx, "uploads": prog_uploads,
            "objstore": prog_objstore, "mail": prog_mail, "negotiate": prog_negotiate,
            "cdnlog": prog_cdnlog, "inventory": prog_inventory}


def main():
    jobs = open("data/jobs.tsv", encoding="utf-8").read().split("\n")[:-1]
    i = 0
    while i < len(jobs):
        f = jobs[i].split("\t")
        if f[0] == "job":
            body = []
            i += 1
            while i < len(jobs) and jobs[i].split("\t")[0] not in ("job", "cli", "program"):
                body.append(jobs[i])
                i += 1
            reset_module()
            run_job(f[1], body)
            continue
        if f[0] == "cli":
            run_cli(f[1:])
        elif f[0] == "program":
            PROGRAMS[f[1]]()
        i += 1


main()
