# Runs data/jobs.tsv (as mk.py writes it) through Python 3.13's real
# mailbox module, on copies under data/work/, and prints what
# mini_mailbox.kara prints.
import calendar
import mailbox
import os
import shutil
import time
from email.header import decode_header, make_header
from email.utils import parseaddr, parsedate_tz, mktime_tz

DATA = os.path.abspath("data")

KINDS = {
    "mbox": (mailbox.mbox, mailbox.mboxMessage),
    "mmdf": (mailbox.MMDF, mailbox.MMDFMessage),
    "babyl": (mailbox.Babyl, mailbox.BabylMessage),
    "mh": (mailbox.MH, mailbox.MHMessage),
    "maildir": (mailbox.Maildir, mailbox.MaildirMessage),
    "plain": (None, mailbox.Message),
}


def err(e):
    return f"error: {type(e).__name__}: {str(e).replace(DATA, '<data>')}"


def dpath(p):
    return os.path.join("data", p)


def subject(m):
    s = m["Subject"]
    if s is None:
        return "-"
    return str(make_header(decode_header(s)))


def kind_name(m):
    return type(m).__name__


def state(m):
    out = [kind_name(m)]
    if isinstance(m, mailbox.MaildirMessage):
        out.append(f"subdir={m.get_subdir()!r} info={m.get_info()!r} flags={m.get_flags()!r}")
    elif isinstance(m, mailbox._mboxMMDFMessage):
        out.append(f"from={m.get_from()!r} flags={m.get_flags()!r}")
    elif isinstance(m, mailbox.MHMessage):
        out.append(f"sequences={m.get_sequences()!r}")
    elif isinstance(m, mailbox.BabylMessage):
        out.append(f"labels={m.get_labels()!r} visible={m.get_visible().items()!r}")
    return " ".join(out)


def describe(m, ind="  "):
    print(ind + state(m))
    print(ind + f"unixfrom {m.get_unixfrom()!r}")
    print(ind + f"headers {m.items()!r}")
    if m.is_multipart():
        print(ind + f"parts {[p.get_content_type() for p in m.walk()]!r}")
    else:
        print(ind + f"body {m.get_payload()!r}")


def show_lines(b):
    if isinstance(b, bytes):
        b = b.decode("ascii")
    # Lines end at "\n" only (str.splitlines would also split at \x1f).
    start = 0
    while start < len(b):
        end = b.find("\n", start)
        end = len(b) if end < 0 else end + 1
        print("    | " + repr(b[start:end]))
        start = end


def keys_of(box):
    ks = box.keys()
    if isinstance(box, mailbox.Maildir):
        return sorted(ks)
    return ks


def tree(path):
    out = []
    for root, dirs, files in os.walk(dpath(path)):
        for d in dirs:
            out.append(os.path.relpath(os.path.join(root, d), dpath(path)) + "/")
        for f in files:
            out.append(os.path.relpath(os.path.join(root, f), dpath(path)))
    return sorted(out)


def copy(src, dst):
    s, d = dpath(src), dpath(dst)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    if os.path.isdir(s):
        shutil.copytree(s, d)
    else:
        shutil.copyfile(s, d)


def key_arg(box, k):
    if isinstance(box, (mailbox.Maildir,)):
        return k
    return int(k)


def envelope_from(m):
    # The envelope sender and date, from the From and Date headers.
    addr = parseaddr(m.get("From", ""))[1] or "MAILER-DAEMON"
    t = parsedate_tz(m.get("Date", ""))
    if t is None:
        return addr + " Thu Jan  1 00:00:00 1970"
    return addr + " " + time.asctime(time.gmtime(mktime_tz(t)))


def convert(kind, m, redate):
    c = KINDS[kind][1](m)
    if redate and isinstance(c, mailbox._mboxMMDFMessage):
        c.set_from(envelope_from(m))
    return c


def parse_seqs(spec):
    out = {}
    if spec == "-":
        return out
    for part in spec.split(";"):
        name, ks = part.split("=")
        out[name] = [int(k) for k in ks.split(",") if k]
    return out


def unread(box, m):
    if isinstance(m, mailbox._mboxMMDFMessage):
        return "R" not in m.get_flags()
    if isinstance(m, mailbox.MaildirMessage):
        return "S" not in m.get_flags()
    if isinstance(m, mailbox.MHMessage):
        return "unseen" in m.get_sequences()
    if isinstance(m, mailbox.BabylMessage):
        return "unseen" in m.get_labels()
    return False


def text_of(m):
    for p in m.walk():
        if p.get_content_type() == "text/plain":
            b = p.get_payload(decode=True)
            return b.decode("ascii", "replace")
    return ""


boxes = {}


def op(a):
    name = a[0]
    if name == "copy":
        copy(a[1], a[2])
    elif name == "rmfile":
        os.remove(dpath(a[1]))
    elif name == "open":
        cls = KINDS[a[2]][0]
        create = len(a) < 5 or a[4] != "nocreate"
        boxes[a[1]] = cls(dpath(a[3]), create=create)
        print(f"  opened {a[1]}")
    elif name == "keys":
        print(f"  keys {keys_of(boxes[a[1]])!r}")
    elif name == "len":
        print(f"  len {len(boxes[a[1]])}")
    elif name == "has":
        box = boxes[a[1]]
        print(f"  has {a[2]} {key_arg(box, a[2]) in box}")
    elif name == "get":
        box = boxes[a[1]]
        describe(box[key_arg(box, a[2])])
    elif name == "bytes":
        box = boxes[a[1]]
        if len(a) > 3:
            show_lines(box.get_bytes(key_arg(box, a[2]), True))
        else:
            show_lines(box.get_bytes(key_arg(box, a[2])))
    elif name == "string":
        box = boxes[a[1]]
        if len(a) > 3:
            show_lines(box.get_string(key_arg(box, a[2]), True))
        else:
            show_lines(box.get_string(key_arg(box, a[2])))
    elif name == "summary":
        box = boxes[a[1]]
        for k in keys_of(box):
            m = box[k]
            print(f"  {k!r}: {subject(m)!r} | {state(m)}")
    elif name in ("flag", "label", "seq"):
        box = boxes[a[1]]
        k = key_arg(box, a[2])
        m = box[k]
        what = {"flag": "flag", "label": "label", "seq": "sequence"}[name]
        if a[3] == "set":
            m.set_flags(a[4])
        else:
            getattr(m, f"{a[3]}_{what}")(a[4])
        box[k] = m
        print(f"  {k!r} now {state(m)}")
    elif name == "remove":
        box = boxes[a[1]]
        box.remove(key_arg(box, a[2]))
        print(f"  removed {a[2]}")
    elif name == "discard":
        box = boxes[a[1]]
        box.discard(key_arg(box, a[2]))
        print(f"  discarded {a[2]}")
    elif name == "flush":
        boxes[a[1]].flush()
        print(f"  flushed {a[1]}")
    elif name == "close":
        boxes.pop(a[1]).close()
        print(f"  closed {a[1]}")
    elif name == "add":
        box = boxes[a[1]]
        with open(dpath(a[2]), "rb") as f:
            k = box.add(f.read())
        print(f"  added {'<new>' if isinstance(box, mailbox.Maildir) else k}")
    elif name == "replace":
        box = boxes[a[1]]
        with open(dpath(a[3]), "rb") as f:
            box[key_arg(box, a[2])] = f.read()
        print(f"  replaced {a[2]}")
    elif name in ("convert", "move"):
        src = boxes[a[1]]
        m = src[key_arg(src, a[2])]
        c = convert(a[3] if name == "convert" else a[4], m, a[-1] == "redate")
        if name == "move":
            dst = boxes[a[3]]
            k = dst.add(c)
            print(f"  added {'<new>' if isinstance(dst, mailbox.Maildir) else k}")
        describe(c)
    elif name == "file":
        with open(dpath(a[1]), "rb") as f:
            show_lines(f.read())
    elif name == "tree":
        for t in tree(a[1]):
            print(f"    {t}")
    elif name == "seqs":
        print(f"  sequences {boxes[a[1]].get_sequences()!r}")
    elif name == "setseqs":
        boxes[a[1]].set_sequences(parse_seqs(a[2]))
        print("  sequences set")
    elif name == "pack":
        boxes[a[1]].pack()
        print("  packed")
    elif name == "folders":
        print(f"  folders {sorted(boxes[a[1]].list_folders())!r}")
    elif name == "folder":
        boxes[a[3]] = boxes[a[1]].get_folder(a[2])
        print(f"  opened {a[3]}")
    elif name == "addfolder":
        boxes[a[3]] = boxes[a[1]].add_folder(a[2])
        print(f"  opened {a[3]}")
    elif name == "rmfolder":
        boxes[a[1]].remove_folder(a[2])
        print(f"  removed folder {a[2]}")
    elif name == "info":
        print(f"  info {boxes[a[1]].get_info(a[2])!r} flags {boxes[a[1]].get_flags(a[2])!r}")
    elif name == "setinfo":
        boxes[a[1]].set_info(a[2], a[3] if len(a) > 3 else "")
        print("  info set")
    elif name in ("set_flags", "add_flag", "remove_flag"):
        getattr(boxes[a[1]], name)(a[2], a[3])
        print(f"  {name} done")
    elif name == "labels":
        print(f"  labels {sorted(boxes[a[1]].get_labels(), key=repr)!r}")
    elif name == "unread":
        total = 0
        for n in a[1:]:
            box = boxes[n]
            c = 0
            for k in keys_of(box):
                if unread(box, box[k]):
                    c += 1
            total += c
            print(f"  {n}: {c} unread of {len(box)}")
        print(f"  total {total}")
    elif name == "search":
        needle = a[-1].lower()
        for n in a[1:-1]:
            box = boxes[n]
            for k in keys_of(box):
                m = box[k]
                if needle in subject(m).lower() or needle in text_of(m).lower():
                    print(f"  {n} {k!r}: {subject(m)}")
    elif name == "digest":
        box = boxes[a[1]]
        for k in keys_of(box):
            m = box[k]
            t = parsedate_tz(m.get("Date", ""))
            when = "-" if t is None else time.asctime(time.gmtime(mktime_tz(t)))
            print(f"  {k!r:>3} {when}  {parseaddr(m.get('From', ''))[1]:<28} {subject(m)}")
    elif name == "dedupe":
        seen = set()
        for k in keys_of(boxes[a[1]]):
            seen.add(boxes[a[1]][k]["Message-ID"])
        box = boxes[a[2]]
        for k in keys_of(box):
            mid = box[k]["Message-ID"]
            if mid in seen:
                box.remove(k)
                print(f"  dropped {k!r} {mid}")
            else:
                seen.add(mid)
    elif name == "archive":
        src, dst = boxes[a[1]], boxes[a[2]]
        cutoff = calendar.timegm(time.strptime(a[3], "%Y-%m-%d"))
        for k in keys_of(src):
            m = src[k]
            t = parsedate_tz(m.get("Date", ""))
            if t is not None and mktime_tz(t) < cutoff:
                nk = dst.add(convert(a[4], m, False))
                src.remove(k)
                print(f"  archived {k!r} as {'<new>' if isinstance(dst, mailbox.Maildir) else nk!r}: {subject(m)}")
    elif name == "date":
        t = parsedate_tz(a[1])
        print(f"  date {a[1]!r}: {t!r}" + ("" if t is None else f" -> {mktime_tz(t)} {time.asctime(time.gmtime(mktime_tz(t)))}"))
    else:
        raise AssertionError(name)


with open("data/jobs.tsv", encoding="ascii") as f:
    for line in f:
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        a = line.split("\t")
        if a[0] == "job":
            print("== " + a[1])
            boxes.clear()
            continue
        try:
            op(a)
        except Exception as e:
            print("  " + err(e))
