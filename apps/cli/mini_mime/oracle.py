# The reference: the same program written with Python 3.13's base64,
# binascii and quopri. quopri is made to use its own pure-Python codec
# (the one the Kara port follows) rather than binascii's C one.
import base64, binascii, os, quopri

quopri.b2a_qp = None
quopri.a2b_qp = None


def unescape(s):
    out = bytearray()
    b = s.encode("utf-8")
    i = 0
    while i < len(b):
        c = b[i]
        if c == 0x5C and i + 1 < len(b):
            n = chr(b[i + 1])
            if n in "tnr\\":
                out.append({"t": 9, "n": 10, "r": 13, "\\": 92}[n]); i += 2; continue
            if n == "x":
                out.append(int(b[i + 2:i + 4], 16)); i += 4; continue
        out.append(c)
        i += 1
    return bytes(out)


def err(e):
    name = "binascii.Error" if isinstance(e, binascii.Error) else type(e).__name__
    return f"Error: {name}: {e}"


def run_case(name, opts, data):
    if name == "b64encode":
        return base64.b64encode(data, altchars=opts["alt"].encode() if "alt" in opts else None)
    if name == "urlsafe_b64encode":
        return base64.urlsafe_b64encode(data)
    if name == "b64decode":
        return base64.b64decode(data, altchars=opts["alt"].encode() if "alt" in opts else None,
                                validate="validate" in opts)
    if name == "urlsafe_b64decode":
        return base64.urlsafe_b64decode(data)
    if name == "encodebytes":
        return base64.encodebytes(data)
    if name == "decodebytes":
        return base64.decodebytes(data)
    if name == "b32encode":
        return base64.b32encode(data)
    if name == "b32hexencode":
        return base64.b32hexencode(data)
    if name == "b32decode":
        return base64.b32decode(data, casefold="casefold" in opts, map01=opts.get("map01"))
    if name == "b32hexdecode":
        return base64.b32hexdecode(data, casefold="casefold" in opts)
    if name == "b16encode":
        return base64.b16encode(data)
    if name == "b16decode":
        return base64.b16decode(data, casefold="casefold" in opts)
    if name == "a85encode":
        return base64.a85encode(data, foldspaces="foldspaces" in opts, wrapcol=int(opts.get("wrapcol", 0)),
                                pad="pad" in opts, adobe="adobe" in opts)
    if name == "a85decode":
        return base64.a85decode(data, foldspaces="foldspaces" in opts, adobe="adobe" in opts)
    if name == "b85encode":
        return base64.b85encode(data, pad="pad" in opts)
    if name == "b85decode":
        return base64.b85decode(data)
    if name == "z85encode":
        return base64.z85encode(data)
    if name == "z85decode":
        return base64.z85decode(data)
    if name == "hexlify":
        if "sep" in opts:
            return binascii.hexlify(data, opts["sep"], int(opts.get("n", 1)))
        return binascii.hexlify(data)
    if name == "unhexlify":
        return binascii.unhexlify(data)
    if name == "crc32":
        return binascii.crc32(data, int(opts.get("value", 0)))
    if name == "crc_hqx":
        return binascii.crc_hqx(data, int(opts.get("value", 0)))
    if name == "qp_encode":
        return quopri.encodestring(data, quotetabs="quotetabs" in opts, header="header" in opts)
    if name == "qp_decode":
        return quopri.decodestring(data, header="header" in opts)
    raise SystemExit(f"unknown case {name}")


def show_codecs():
    print("== codecs")
    for line in open("data/cases.txt", encoding="utf-8").read().splitlines():
        spec, _, raw = line.partition(" | ")
        words = spec.split()
        opts = {}
        for w in words[1:]:
            k, _, v = w.partition("=")
            opts[k] = v
        print(line)
        try:
            r = run_case(words[0], opts, unescape(raw))
        except (ValueError, binascii.Error) as e:
            print("  " + err(e))
            continue
        print(f"  -> {r!r}")


# ------------------------------------------------------------ mail

BOUNDARY = "==kara-0001=="


def content_type_for(name):
    ext = name.rpartition(".")[2]
    return {"txt": "text/plain", "csv": "text/csv", "png": "image/png"}.get(ext, "application/octet-stream")


def encoded_word_b(s):
    if s.isascii():
        return s
    return "=?utf-8?b?" + base64.b64encode(s.encode()).decode() + "?="


def make_icon():
    out = bytearray()
    x = 12345
    for _ in range(300):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append((x >> 16) & 0xFF)
    return bytes(out)


def build_message():
    names = sorted(os.listdir("data/outbox"))
    subject = "Nightly build — café branch, all green"
    out = []
    out.append("From: build-bot <bot@example.com>")
    out.append("To: team@example.com")
    out.append("Subject: =?utf-8?q?" + quopri.encodestring(subject.encode(), header=True).decode() + "?=")
    out.append("MIME-Version: 1.0")
    out.append(f'Content-Type: multipart/mixed; boundary="{BOUNDARY}"')
    out.append("")
    out.append("This is a multi-part message in MIME format.")
    for name in names:
        data = open(f"data/outbox/{name}", "rb").read()
        out.append(f"--{BOUNDARY}")
        if name == "note.txt":
            out.append('Content-Type: text/plain; charset="utf-8"')
            out.append("Content-Transfer-Encoding: quoted-printable")
            out.append("")
            out.append(quopri.encodestring(data).decode())
        else:
            fname = encoded_word_b(name)
            out.append(f'Content-Type: {content_type_for(name)}; name="{fname}"')
            out.append("Content-Transfer-Encoding: base64")
            out.append(f'Content-Disposition: attachment; filename="{fname}"')
            out.append("")
            out.append(base64.encodebytes(data).decode())
    out.append(f"--{BOUNDARY}--")
    return "\n".join(out) + "\n"


def decode_charset(b, cs):
    cs = cs.lower()
    if cs in ("utf-8", "utf8"):
        return b.decode("utf-8", "replace")
    if cs in ("iso-8859-1", "latin-1", "latin1"):
        return b.decode("iso-8859-1")
    return b.decode("ascii", "replace")


def decode_header(v):
    # RFC 2047 encoded words; white space between two of them is dropped
    out = []
    i = 0
    last_was_word = False
    pending_ws = ""
    while i < len(v):
        if v.startswith("=?", i):
            q1 = v.find("?", i + 2)
            q2 = v.find("?", q1 + 1) if q1 >= 0 else -1
            end = v.find("?=", q2 + 1) if q2 >= 0 else -1
            if q1 >= 0 and q2 == q1 + 2 and end >= 0:
                cs = v[i + 2:q1]
                enc = v[q1 + 1].lower()
                text = v[q2 + 1:end].encode()
                try:
                    if enc == "q":
                        raw = quopri.decodestring(text, header=True)
                    elif enc == "b":
                        raw = base64.b64decode(text)
                    else:
                        raw = None
                except binascii.Error:
                    raw = None
                if raw is not None:
                    if not last_was_word:
                        out.append(pending_ws)
                    pending_ws = ""
                    out.append(decode_charset(raw, cs))
                    last_was_word = True
                    i = end + 2
                    continue
        c = v[i]
        if c in " \t":
            pending_ws += c
        else:
            out.append(pending_ws)
            pending_ws = ""
            out.append(c)
            last_was_word = False
        i += 1
    out.append(pending_ws)
    return "".join(out)


def parse_headers(lines):
    headers = []
    i = 0
    while i < len(lines) and lines[i] != "":
        line = lines[i]
        if line[:1] in (" ", "\t") and headers:
            headers[-1][1] += " " + line.strip()
        else:
            k, _, v = line.partition(":")
            headers.append([k.strip(), v.strip()])
        i += 1
    return headers, lines[i + 1:]


def header(headers, name):
    for k, v in headers:
        if k.lower() == name.lower():
            return v
    return ""


def params(value):
    parts = value.split(";")
    main = parts[0].strip().lower()
    ps = {}
    for p in parts[1:]:
        k, _, v = p.strip().partition("=")
        v = v.strip()
        if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
            v = v[1:-1]
        ps[k.strip().lower()] = v
    return main, ps


def split_parts(body, boundary):
    parts = []
    cur = None
    for line in body:
        if line == f"--{boundary}--":
            if cur is not None:
                parts.append(cur)
            return parts
        if line == f"--{boundary}":
            if cur is not None:
                parts.append(cur)
            cur = []
            continue
        if cur is not None:
            cur.append(line)
    if cur is not None:
        parts.append(cur)
    return parts


def receive(path, outdir):
    text = open(path, "rb").read().decode("ascii", "replace")
    lines = [l.removesuffix("\r") for l in text.split("\n")]
    if lines and lines[-1] == "":
        lines.pop()
    headers, body = parse_headers(lines)
    print(f"From: {decode_header(header(headers, 'From'))}")
    print(f"Subject: {decode_header(header(headers, 'Subject'))}")
    ctype, ps = params(header(headers, "Content-Type") or "text/plain")
    if ctype.startswith("multipart/"):
        parts = split_parts(body, ps["boundary"])
    else:
        parts = [lines]
    files = []
    for n, plines in enumerate(parts, 1):
        ph, pbody = parse_headers(plines)
        pt, pps = params(header(ph, "Content-Type") or "text/plain")
        cte = header(ph, "Content-Transfer-Encoding").lower() or "7bit"
        _, dps = params(header(ph, "Content-Disposition"))
        fname = decode_header(dps.get("filename", pps.get("name", "")))
        raw = "\n".join(pbody).encode()
        try:
            if cte == "base64":
                data = base64.b64decode(raw)
            elif cte == "quoted-printable":
                data = quopri.decodestring(raw)
            else:
                data = raw
        except binascii.Error as e:
            print(f"part {n}: {pt} {cte} {fname!r}: {err(e)}")
            continue
        dump = binascii.hexlify(data[:16], " ").decode()
        print(f"part {n}: {pt} {cte} {fname!r}: {len(data)} bytes, crc32 {binascii.crc32(data):08x}, {dump}")
        if pt.startswith("text/") and not fname:
            for tl in decode_charset(data, pps.get("charset", "us-ascii")).split("\n"):
                print(f"  | {tl}")
        if fname:
            os.makedirs(outdir, exist_ok=True)
            open(f"{outdir}/{fname}", "wb").write(data)
        files.append(data)
    return files


def show_mail():
    print("== send")
    open("data/outbox/café-logo.png", "wb").write(make_icon())
    msg = build_message()
    os.makedirs("data/out", exist_ok=True)
    open("data/out/message.eml", "w").write(msg)
    print(open("data/out/message.eml").read(), end="")
    print("== receive")
    print("-- data/out/message.eml")
    got = receive("data/out/message.eml", "data/out/received/message")
    names = sorted(os.listdir("data/outbox"))
    for name, back in zip(names, got):
        mine = open(f"data/outbox/{name}", "rb").read()
        print(f"round trip {name}: {'same' if back == mine else 'DIFFERENT'}")
    for name in sorted(os.listdir("data/inbox")):
        print(f"-- data/inbox/{name}")
        receive(f"data/inbox/{name}", "data/out/received/" + name.rpartition(".")[0])


show_codecs()
show_mail()
