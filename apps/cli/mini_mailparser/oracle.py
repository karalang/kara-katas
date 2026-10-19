# Reads data/ (as mk.py writes it) through Python 3.13's real email
# package -- the compat32 parser, Message, Generator and email.mime -- and
# prints what mini_mailparser.kara prints.
import binascii
import json
import os
from email import message_from_string
from email.generator import Generator
from email.header import decode_header, make_header
from email.mime.application import MIMEApplication
from email.mime.message import MIMEMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, getaddresses, parseaddr
from io import StringIO


def err(e):
    return f"{type(e).__name__}: {e}"


def read(name):
    with open("data/mail/" + name, encoding="utf-8", newline="") as f:
        return f.read()


def defects(m):
    out = []
    for d in m.defects:
        out.append(type(d).__name__ + (f"({str(d)!r})" if d.args else ""))
    return "[" + ", ".join(out) + "]"


def show_text(b, charset):
    try:
        return repr(b.decode(charset or "us-ascii", "replace"))
    except LookupError as e:
        return err(e)


def show_parts(m):
    for i, p in enumerate(m.walk()):
        print(f"  [{i}] {p.get_content_type()} default={p.get_default_type()} multipart={p.is_multipart()}")
        print(f"      params {p.get_params()!r}")
        print(f"      filename {p.get_filename()!r} charset {p.get_content_charset()!r} disposition {p.get_content_disposition()!r}")
        if p.defects:
            print(f"      defects {defects(p)}")
        if p.preamble is not None or p.epilogue is not None:
            print(f"      preamble {p.preamble!r} epilogue {p.epilogue!r}")
        if not p.is_multipart():
            raw = p.get_payload()
            print(f"      payload {raw!r}")
            b = p.get_payload(decode=True)
            print(f"      decoded {b!r}")
            if p.defects:
                print(f"      defects after decode {defects(p)}")
            if p.get_content_maintype() == "text":
                print(f"      text {show_text(b, p.get_content_charset())}")


def flatten(m, **kw):
    s = StringIO()
    Generator(s, **kw).flatten(m)
    return s.getvalue()


def show_lines(text):
    for line in text.splitlines(keepends=True):
        print("    | " + repr(line))


def parse_job(name):
    text = read(name)
    m = message_from_string(text)
    print("== parse " + name)
    print(f"  unixfrom {m.get_unixfrom()!r}")
    print(f"  headers {m.items()!r}")
    show_parts(m)
    print(f"  charsets {m.get_charsets()!r}")
    out = m.as_string()
    if out == text:
        print("  as_string: same as the file")
    else:
        print("  as_string:")
        show_lines(out)
    print("  folded at 40, From_ lines mangled:")
    show_lines(flatten(message_from_string(text), maxheaderlen=40))


def value(v):
    if isinstance(v, list):
        return tuple(v)
    return v


def edit_job(j):
    m = message_from_string(read(j["file"]))
    p = list(m.walk())[j["part"]]
    print(f"== edit {j['file']} part {j['part']}")
    for op in j["ops"]:
        name, args = op[0], op[1:]
        try:
            if name == "get_param":
                r = p.get_param(args[0], **args[1])
            elif name == "get_params":
                r = p.get_params(**args[0])
            elif name == "set_param":
                r = p.set_param(args[0], value(args[1]), **args[2])
            elif name == "del_param":
                r = p.del_param(args[0], **args[1])
            elif name == "set_type":
                r = p.set_type(args[0])
            elif name == "set_boundary":
                r = p.set_boundary(args[0])
            elif name == "get_boundary":
                r = p.get_boundary()
            elif name == "get_filename":
                r = p.get_filename()
            elif name == "get_content_charset":
                r = p.get_content_charset()
            elif name == "get_content_disposition":
                r = p.get_content_disposition()
            elif name == "get_content_type":
                r = p.get_content_type()
            elif name == "get_charsets":
                r = p.get_charsets()
            elif name == "get_all":
                r = p.get_all(args[0])
            elif name == "get":
                r = p.get(args[0])
            elif name == "replace_header":
                r = p.replace_header(args[0], args[1])
            elif name == "add_header":
                r = p.add_header(args[0], args[1], **{k: value(v) for k, v in args[2].items()})
            elif name == "set":
                p[args[0]] = args[1]
                r = None
            elif name == "del":
                del p[args[0]]
                r = None
            else:
                raise AssertionError(name)
            print(f"  {name} {args!r} -> {r!r}")
        except Exception as e:
            print(f"  {name} {args!r} -> {err(e)}")
    print(f"  headers {p.items()!r}")
    print("  header block:")
    out = p.as_string()
    show_lines(out[:out.index("\n\n") + 1] if "\n\n" in out else out)


def compose():
    print("== compose")
    agenda = open("data/outbox/agenda.txt", encoding="utf-8").read()
    logo = open("data/outbox/logo.bin", "rb").read()

    texts = [
        ("Plain ASCII note.\n", "plain", None),
        ("Grüße aus Köln — bis bald!\n", "plain", None),
        ("Résumé attached, café at noon.\n" + "x" * 90 + "é\nend", "plain", "iso-8859-1"),
        ("Price: 10 € = 10 euros\n", "plain", "iso-8859-15"),
        ("<p>Grüße</p>", "html", "utf-8"),
        ("Grüße", "plain", "us-ascii"),
        ("", "plain", "utf-8"),
    ]
    for text, sub, cs in texts:
        try:
            t = MIMEText(text, sub, cs)
            print(f"  MIMEText {text!r} {sub!r} {cs!r}")
            show_lines(t.as_string())
        except Exception as e:
            print(f"  MIMEText {text!r} {sub!r} {cs!r} -> {err(e)}")

    outer = MIMEMultipart("mixed", boundary="===============1234567890==")
    outer["From"] = formataddr(("Dörte Müller", "doerte@example.de"))
    outer["To"] = ", ".join([formataddr(("Ben Okafor", "ben@example.net")), formataddr(("Chen, Wei", "wei.chen@example.com"))])
    outer["Subject"] = "Agenda für Montag — please review the attached files before the meeting starts"
    outer["Date"] = "Mon, 26 Oct 2026 09:00:00 +0100"
    outer.preamble = "You will not see this in a MIME-aware mail reader.\n"
    alt = MIMEMultipart("alternative", boundary="alt-b")
    alt.attach(MIMEText("Hi all,\nsee the agenda.\n"))
    alt.attach(MIMEText("<p>Hi all,</p><p>see the <i>agenda</i>.</p>", "html", "utf-8"))
    outer.attach(alt)
    a = MIMEText(agenda, "plain", "utf-8")
    a.add_header("Content-Disposition", "attachment", filename="agenda.txt")
    outer.attach(a)
    b = MIMEApplication(logo, "octet-stream", Name="logo.bin")
    b.add_header("Content-Disposition", "attachment", filename=("utf-8", "", "Logo für Präsentation.bin"))
    outer.attach(b)
    fwd = message_from_string(read("05.eml"))
    inner = fwd.get_payload(1).get_payload(0)
    outer.attach(MIMEMessage(inner))
    out = outer.as_string()
    print("  multipart:")
    show_lines(out)
    back = message_from_string(out)
    print("  parsed back:")
    show_parts(back)
    print(f"  same again: {back.as_string() == out}")


def report():
    print("== mailbox report")
    os.makedirs("data/saved", exist_ok=True)
    for name in sorted(os.listdir("data/mail")):
        m = message_from_string(read(name))
        frm = parseaddr(m.get("from", ""))
        subj = m.get("subject")
        try:
            subj = str(make_header(decode_header(subj))) if subj is not None else None
        except Exception as e:
            subj = err(e)
        parts = list(m.walk())
        print(f"  {name} from {frm!r} subject {subj!r} parts {len(parts)} defects {sum(len(p.defects) for p in parts)}")
        body = None
        for i, p in enumerate(parts):
            if p.is_multipart():
                continue
            fn = p.get_filename()
            if fn is not None or p.get_content_disposition() == "attachment":
                data = p.get_payload(decode=True)
                safe = "".join(c if c.isalnum() or c in "._-" else "_" for c in (fn or f"part{i}"))
                path = f"data/saved/{name[:2]}-{safe}"
                with open(path, "wb") as f:
                    f.write(data)
                print(f"    saved {path} {len(data)} bytes crc32 {binascii.crc32(data):08x}")
            elif body is None and p.get_content_type() == "text/plain":
                cs = p.get_content_charset() or "us-ascii"
                try:
                    text = p.get_payload(decode=True).decode(cs, "replace")
                except LookupError:
                    text = p.get_payload(decode=True).decode("us-ascii", "replace")
                body = text.strip().split("\n")[0] if text.strip() else ""
        print(f"    first line {body!r}")
        to = getaddresses(m.get_all("to", []) + m.get_all("cc", []))
        print(f"    recipients {to!r}")
    print("  saved files:")
    for n in sorted(os.listdir("data/saved")):
        print(f"    {n} {os.path.getsize('data/saved/' + n)}")


for name in sorted(os.listdir("data/mail")):
    parse_job(name)
for line in open("data/jobs.jsonl", encoding="utf-8"):
    edit_job(json.loads(line))
compose()
report()
