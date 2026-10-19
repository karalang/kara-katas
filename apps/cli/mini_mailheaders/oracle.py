# Runs data/jobs.jsonl and reads data/mail/ (as mk.py writes them) through
# Python 3.13's real email.utils and email.header, and prints what
# mini_mailheaders.kara prints.
import json
import os
from email import utils
from email.header import Header, decode_header, make_header


def err(e):
    return f"{type(e).__name__}: {e}"


def call(j):
    fn, args, kw = j["fn"], j["args"], j["kw"]
    if fn == "parseaddr":
        return repr(utils.parseaddr(*args, **kw))
    if fn == "getaddresses":
        return repr(utils.getaddresses(*args, **kw))
    if fn == "formataddr":
        return repr(utils.formataddr(tuple(args[0]), **kw))
    if fn in ("quote", "unquote", "parsedate_tz", "parsedate", "decode_rfc2231", "encode_rfc2231"):
        return repr(getattr(utils, fn)(*args, **kw))
    if fn == "parsedate_to_datetime":
        return utils.parsedate_to_datetime(*args).isoformat()
    if fn == "mktime_tz":
        return repr(utils.mktime_tz(utils.parsedate_tz(args[0])))
    if fn == "formatdate":
        return repr(utils.formatdate(args[0], **kw))
    if fn == "collapse_rfc2231_value":
        v = args[0]
        return repr(utils.collapse_rfc2231_value(tuple(v) if isinstance(v, list) else v))
    if fn == "decode_header":
        return repr(decode_header(args[0]))
    if fn == "str_make_header":
        return repr(str(make_header(decode_header(args[0]))))
    if fn == "encode_make_header":
        return repr(make_header(decode_header(args[0])).encode())
    if fn == "header":
        h = Header(**kw["init"])
        out = [repr(str(h))]
        try:
            out.append(repr(h.encode(**kw["encode"])))
        except Exception as e:
            out.append(err(e))
        return "\n  ".join(out)
    if fn == "header_parts":
        h = Header()
        for s, cs in args[0]:
            h.append(s, cs)
        return "\n  ".join([repr(str(h)), repr(h.encode()), repr(decode_header(h))])
    raise AssertionError(fn)


for line in open("data/jobs.jsonl", encoding="utf-8"):
    line = line.rstrip("\n")
    print("== " + line)
    try:
        print("  " + call(json.loads(line)))
    except Exception as e:
        print("  " + err(e))


# The mailbox: a header block per file, folded lines kept with their
# line break, as the message file has them.
def headers_of(text):
    head = text.replace("\r\n", "\n").split("\n\n", 1)[0]
    out = []
    for line in head.split("\n"):
        if line[:1] in (" ", "\t") and out:
            out[-1][1] += "\n" + line
        elif ":" in line:
            name, value = line.split(":", 1)
            out.append([name, value.lstrip(" \t")])
    return out


def get(hs, name):
    for k, v in hs:
        if k.lower() == name.lower():
            return v
    return None


def decoded(s):
    try:
        return repr(str(make_header(decode_header(s))))
    except Exception as e:
        return err(e)


book = {}
for f in sorted(os.listdir("data/mail")):
    print(f"== mail/{f}")
    hs = headers_of(open(f"data/mail/{f}", encoding="utf-8").read())
    name, addr = utils.parseaddr(get(hs, "From") or "")
    print(f"  from: {decoded(name)} {addr!r}")
    rcpts = utils.getaddresses([v for k, v in hs if k.lower() in ("to", "cc")])
    for n, a in rcpts:
        print(f"  to: {decoded(n)} {a!r}")
    for n, a in [(name, addr)] + rcpts:
        if a and a.lower() not in book:
            book[a.lower()] = n
    date = get(hs, "Date") or ""
    ts = None
    try:
        print(f"  date: {utils.parsedate_to_datetime(date).isoformat()}")
    except Exception as e:
        print(f"  date: {err(e)}")
    t = utils.parsedate_tz(date)
    if t is not None:
        ts = utils.mktime_tz(t)
        print(f"  utc: {ts}")
    subject = get(hs, "Subject") or ""
    print(f"  subject: {decoded(subject)}")
    try:
        text = str(make_header(decode_header(subject)))
    except Exception:
        text = subject
    reply = "Re: " + text if not text.lower().startswith("re:") else text
    try:
        to = utils.formataddr((str(make_header(decode_header(name))), addr))
    except Exception as e:
        to = err(e)
    print(f"  reply To: {to}")
    try:
        enc = Header(reply, "utf-8", header_name="Subject").encode()
    except Exception as e:
        enc = err(e)
    print("  reply Subject: " + enc.replace("\n", "\n  "))
    if ts is not None:
        print(f"  reply Date: {utils.formatdate(ts + 3600, usegmt=True)}")
print("== address book")
for a in sorted(book):
    print(f"  {a} {decoded(book[a])}")
