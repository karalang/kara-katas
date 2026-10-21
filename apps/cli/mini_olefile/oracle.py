# Runs data/jobs.txt through the copy of olefile 0.47 in olefile.py and
# prints what it does; expected.out is this program's output.
import os
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import olefile  # noqa: E402

KINDS = {0: "empty", 1: "storage", 2: "stream", 3: "lockbytes", 4: "property", 5: "root"}
CLSIDS = {
    "00020906-0000-0000-C000-000000000046": "word",
    "00020820-0000-0000-C000-000000000046": "excel",
    "00020D0B-0000-0000-C000-000000000046": "outlook",
}


def err(e):
    return "! %s: %r" % (type(e).__name__, str(e))


def path(name):
    return os.path.join("data", name)


def unescape(p):
    return p.replace("\\x05", "\x05").replace("\\x01", "\x01").replace("\\x03", "\x03")


def level_of(args, i):
    if len(args) > i and args[i].isdigit():
        return int(args[i])
    return olefile.DEFECT_FATAL


def issues(ole):
    if ole.parsing_issues:
        print("  issues:")
        for t, m in ole.parsing_issues:
            print("    %s: %s" % (t.__name__, m))


def job_open(args):
    ole = olefile.OleFileIO(path(args[0]), raise_defects=level_of(args, 1))
    print("  sectors %d/%d cutoff %d nb_sect %d fat %d entries %d loaded %d" % (
        ole.sector_size, ole.mini_sector_size, ole.minisectorcutoff, ole.nb_sect,
        len(ole.fat), len(ole.direntries), sum(1 for e in ole.direntries if e is not None)))
    print("  version %d.%d byte order %04X difat %d/%d" % (
        ole.minor_version, ole.dll_version, ole.byte_order, ole.num_fat_sectors,
        ole.num_difat_sectors))
    print("  header clsid %r root %r root clsid %r" % (
        ole.header_clsid, ole.get_rootentry_name(), ole.root.clsid))
    return ole


def walk(e, depth, onpath):
    line = "  " + "  " * depth + repr(e.name) + " " + KINDS.get(e.entry_type, "type %d" % e.entry_type)
    if e.entry_type in (olefile.STGTY_STREAM, olefile.STGTY_ROOT):
        line += " %d" % e.size
        if e.is_minifat:
            line += " mini"
    if e.clsid:
        line += " {%s}" % e.clsid
    if e.sid in onpath:
        print(line + " (again)")
        return
    print(line)
    for k in e.kids:
        walk(k, depth + 1, onpath + [e.sid])


def job_tree(args):
    ole = olefile.OleFileIO(path(args[0]), raise_defects=level_of(args, 1))
    walk(ole.root, 0, [])
    return ole


def job_list(args):
    ole = olefile.OleFileIO(path(args[0]), raise_defects=level_of(args, 2))
    mode = args[1] if len(args) > 1 else "streams"
    try:
        for p in ole.listdir(streams=mode != "storages", storages=mode != "streams"):
            print("  " + repr(p))
    except Exception as e:
        print("  " + err(e))
    return ole


def attempt(label, f):
    try:
        v = f()
        print("  %s %s" % (label, str(v) if hasattr(v, "year") else repr(v)))
    except Exception as e:
        print("  %s %s" % (label, err(e)))


def job_entry(args):
    ole = olefile.OleFileIO(path(args[0]))
    p = unescape(args[1])
    print("  exists %r type %r" % (ole.exists(p), ole.get_type(p)))
    attempt("size", lambda: ole.get_size(p))
    attempt("clsid", lambda: ole.getclsid(p))
    attempt("mtime", lambda: ole.getmtime(p))
    attempt("ctime", lambda: ole.getctime(p))
    return ole


def job_stream(args):
    ole = olefile.OleFileIO(path(args[0]))
    p = unescape(args[1])
    ole._raise_defects_level = level_of(args, 2)
    try:
        data = ole.openstream(p).read()
        print("  %d bytes adler32 %08x" % (len(data), zlib.adler32(data)))
        print("  head " + data[:24].hex())
    except Exception as e:
        print("  " + err(e))
    return ole


def job_props(args, user=False):
    ole = olefile.OleFileIO(path(args[0]))
    p = unescape(args[1])
    convert = "convert" in args[2:]
    ole._raise_defects_level = level_of(args, len(args) - 1)
    try:
        if user:
            props = ole.get_userdefined_properties(p, convert_time=convert, no_conversion=[10])
            print("  %d properties" % len(props))
            for d in props:
                print("  %r: %r" % (d["property_name"], d["value"]))
        else:
            props = ole.getproperties(p, convert_time=convert, no_conversion=[10])
            print("  %d properties" % len(props))
            for k, v in props.items():
                print("  %d: %r" % (k, v))
    except Exception as e:
        print("  " + err(e))
    return ole


def job_meta(args):
    ole = olefile.OleFileIO(path(args[0]))
    try:
        md = ole.get_metadata()
        for attr in md.SUMMARY_ATTRIBS + md.DOCSUM_ATTRIBS:
            v = getattr(md, attr)
            if v is not None:
                print("  %s: %r" % (attr, v))
    except Exception as e:
        print("  " + err(e))
    return ole


def job_extract(args):
    ole = olefile.OleFileIO(path(args[0]))
    p = unescape(args[1])
    try:
        data = ole.openstream(p).read()
        with open(path("out/" + args[2]), "wb") as f:
            f.write(data)
        print("  wrote out/%s, %d bytes adler32 %08x" % (args[2], len(data), zlib.adler32(data)))
    except Exception as e:
        print("  " + err(e))
    return ole


# ------------------------------------------------------------ the intake report

def text(b):
    return b.decode("latin-1") if isinstance(b, bytes) else str(b)


def kind_of(ole):
    k = CLSIDS.get(ole.root.clsid)
    if k:
        return k
    if ole.exists("WordDocument"):
        return "word"
    if ole.exists("Workbook") or ole.exists("Book"):
        return "excel"
    if ole.exists("__substg1.0_0037001F"):
        return "outlook"
    return "unknown"


def utf16_stream(ole, p):
    if not ole.exists(p):
        return None
    return ole.openstream(p).read().decode("utf-16-le", "replace")


def report_one(name, manifest):
    print("  " + name)
    try:
        ole = olefile.OleFileIO(path(name))
    except Exception as e:
        print("    rejected: " + err(e))
        manifest.append((name, "-", "rejected", "", 0))
        return "rejected"
    kind = kind_of(ole)
    flags = []
    title = ""
    try:
        if kind == "outlook":
            subject = utf16_stream(ole, "__substg1.0_0037001F")
            sender = utf16_stream(ole, "__substg1.0_0C1A001F")
            addr = utf16_stream(ole, "__substg1.0_0C1F001F")
            title = subject or ""
            print("    outlook message %r from %s <%s>" % (subject, sender, addr))
            atts = [p[0] for p in ole.listdir(streams=False, storages=True)
                    if len(p) == 1 and p[0].startswith("__attach_version1.0_#")]
            for a in atts:
                fn = utf16_stream(ole, a + "/__substg1.0_3707001F")
                size = ole.get_size(a + "/__substg1.0_37010102")
                print("    attachment %s, %d bytes" % (fn, size))
            if atts:
                flags.append("%d attachments" % len(atts))
        else:
            md = ole.get_metadata()
            title = text(md.title) if md.title is not None else ""
            print("    %s document %r by %s, last saved by %s" % (
                kind, title, text(md.author), text(md.last_saved_by)))
            if md.create_time is not None or md.last_saved_time is not None:
                print("    created %s, saved %s" % (md.create_time, md.last_saved_time))
            if md.num_pages:
                print("    %d pages, %d words" % (md.num_pages, md.num_words))
            if md.company is not None:
                print("    company %s" % text(md.company))
            if kind == "word" and ole.exists("WordDocument"):
                fib = ole.openstream("WordDocument").read(12)
                if len(fib) >= 12 and fib[0] == 0xEC and fib[1] == 0xA5 and fib[11] & 0x01:
                    flags.append("encrypted")
        if ole.exists("Macros") or ole.exists("_VBA_PROJECT_CUR") or ole.exists("VBA"):
            flags.append("macros")
        if ole.exists("ObjectPool"):
            flags.append("embedded objects")
    except Exception as e:
        print("    unreadable: " + err(e))
        flags.append("unreadable")
    n = len(ole.parsing_issues)
    if n:
        flags.append("%d defects" % n)
        for t, m in ole.parsing_issues[:3]:
            print("    defect %s: %s" % (t.__name__, m))
    try:
        olefile.OleFileIO(path(name), raise_defects=olefile.DEFECT_INCORRECT)
        strict = "ok"
    except Exception as e:
        strict = "rejected"
        print("    strict open: " + err(e))
    if "macros" in flags or "encrypted" in flags or "unreadable" in flags or strict == "rejected":
        decision = "quarantine"
    elif n:
        decision = "review"
    else:
        decision = "archive"
    print("    flags: %s; strict %s; %s" % (", ".join(flags) or "none", strict, decision))
    manifest.append((name, kind, decision, title, n))
    return decision


def job_report(args):
    manifest = []
    counts = {}
    for name in args:
        d = report_one(name, manifest)
        counts[d] = counts.get(d, 0) + 1
    print("  " + ", ".join("%s %d" % (k, counts[k]) for k in ("archive", "review", "quarantine", "rejected") if k in counts))
    lines = ["file,kind,decision,title,defects"]
    for name, kind, decision, title, n in manifest:
        t = title.replace('"', '""')
        if "," in t or '"' in t:
            t = '"' + t + '"'
        lines.append("%s,%s,%s,%s,%d" % (name, kind, decision, t, n))
    data = ("\r\n".join(lines) + "\r\n").encode("utf-8")
    with open(path("out/manifest.csv"), "wb") as f:
        f.write(data)
    print("  wrote out/manifest.csv, %d bytes adler32 %08x" % (len(data), zlib.adler32(data)))
    return None


JOBS = {
    "open": job_open, "tree": job_tree, "list": job_list, "entry": job_entry,
    "stream": job_stream, "props": job_props,
    "userprops": lambda a: job_props(a, True), "meta": job_meta,
    "extract": job_extract, "report": job_report,
}


def main():
    with open(path("jobs.txt")) as f:
        lines = f.read().splitlines()
    for line in lines:
        if not line.strip():
            continue
        words = line.split()
        print("== " + line)
        try:
            ole = JOBS[words[0]](words[1:])
            if ole is not None:
                issues(ole)
        except Exception as e:
            print("  " + err(e))


main()
