# mini_x509 in Python: OpenSSL 3.0's `x509`, `asn1parse` and `verify`
# commands, written from RFC 5280, X.690 (DER) and PKCS #1, over the
# certificates in data/. Each job's stdout comes first, then its stderr,
# as real.py captures them. Hashes come from hashlib and RSA from pow():
# the Kara program writes its own.
import base64, hashlib, os, sys

# ------------------------------------------------------------ DER


class Node:
    def __init__(self, tag, start, hl, length):
        self.tag = tag
        self.start = start  # offset of the tag byte
        self.hl = hl
        self.len = length
        self.kids = []

    def body(self, d):
        return d[self.start + self.hl:self.start + self.hl + self.len]

    def end(self):
        return self.start + self.hl + self.len


def parse_der(d, pos, end):
    # one TLV at pos, or None
    if pos + 2 > end:
        return None
    tag = d[pos]
    b = d[pos + 1]
    hl = 2
    if b < 0x80:
        length = b
    else:
        n = b & 0x7F
        if n == 0 or n > 4 or pos + 2 + n > end:
            return None
        length = 0
        for i in range(n):
            length = length << 8 | d[pos + 2 + i]
        hl = 2 + n
    if pos + hl + length > end:
        return None
    node = Node(tag, pos, hl, length)
    if tag & 0x20:
        p = pos + hl
        while p < pos + hl + length:
            k = parse_der(d, p, pos + hl + length)
            if k is None:
                return None
            node.kids.append(k)
            p = k.end()
    return node


OIDS = {
    "2.5.4.6": ("C", "countryName"), "2.5.4.8": ("ST", "stateOrProvinceName"), "2.5.4.7": ("L", "localityName"),
    "2.5.4.10": ("O", "organizationName"), "2.5.4.11": ("OU", "organizationalUnitName"),
    "2.5.4.3": ("CN", "commonName"), "1.2.840.113549.1.9.1": ("emailAddress", "emailAddress"),
    "1.2.840.113549.1.1.1": ("rsaEncryption", "rsaEncryption"),
    "1.2.840.113549.1.1.11": ("RSA-SHA256", "sha256WithRSAEncryption"),
    "1.2.840.10045.2.1": ("id-ecPublicKey", "id-ecPublicKey"),
    "1.2.840.10045.3.1.7": ("prime256v1", "prime256v1"),
    "2.5.29.17": ("subjectAltName", "X509v3 Subject Alternative Name"),
    "2.5.29.19": ("basicConstraints", "X509v3 Basic Constraints"),
    "2.5.29.15": ("keyUsage", "X509v3 Key Usage"),
    "2.5.29.37": ("extendedKeyUsage", "X509v3 Extended Key Usage"),
    "2.5.29.14": ("subjectKeyIdentifier", "X509v3 Subject Key Identifier"),
    "2.5.29.35": ("authorityKeyIdentifier", "X509v3 Authority Key Identifier"),
    "2.5.29.31": ("crlDistributionPoints", "X509v3 CRL Distribution Points"),
    "2.5.29.32": ("certificatePolicies", "X509v3 Certificate Policies"),
    "1.3.6.1.5.5.7.1.1": ("authorityInfoAccess", "Authority Information Access"),
    "1.3.6.1.5.5.7.3.1": ("serverAuth", "TLS Web Server Authentication"),
    "1.3.6.1.5.5.7.3.2": ("clientAuth", "TLS Web Client Authentication"),
    "1.3.6.1.5.5.7.3.3": ("codeSigning", "Code Signing"),
    "1.3.6.1.5.5.7.3.4": ("emailProtection", "E-mail Protection"),
    "1.3.6.1.5.5.7.3.8": ("timeStamping", "Time Stamping"),
    "1.3.6.1.5.5.7.3.9": ("OCSPSigning", "OCSP Signing"),
    "1.3.6.1.5.5.7.48.1": ("OCSP", "OCSP"),
    "1.3.6.1.5.5.7.48.2": ("caIssuers", "CA Issuers"),
}


def oid_str(b):
    parts = []
    v = 0
    first = True
    for c in b:
        v = v << 7 | (c & 0x7F)
        if c & 0x80 == 0:
            if first:
                x = 0 if v < 40 else 1 if v < 80 else 2
                parts += [x, v - 40 * x]
                first = False
            else:
                parts.append(v)
            v = 0
    return ".".join(str(p) for p in parts)


def short_name(oid):
    return OIDS[oid][0] if oid in OIDS else oid


def long_name(oid):
    return OIDS[oid][1] if oid in OIDS else oid


def hexc(b, upper=False):
    return ":".join(f"{x:02X}" if upper else f"{x:02x}" for x in b)


# ------------------------------------------------------------ certificates


class Cert:
    pass


def text_of(d, n):
    return bytes(n.body(d)).decode("utf-8", "replace")


# Distinguished names as OpenSSL's default `-nameopt oneline` prints them.
def dn(d, n):
    out = []
    for rdn in n.kids:
        for atv in rdn.kids:
            oid = oid_str(atv.kids[0].body(d))
            out.append(f"{short_name(oid)} = {text_of(d, atv.kids[1])}")
    return ", ".join(out)


MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


# (seconds since the epoch, printed form) of a UTCTime or GeneralizedTime
def time_of(d, n):
    s = text_of(d, n)
    if n.tag == 0x17:
        y = int(s[0:2])
        y += 2000 if y < 50 else 1900
        s = s[2:]
    else:
        y = int(s[0:4])
        s = s[4:]
    mo, da, hh, mi, ss = int(s[0:2]), int(s[2:4]), int(s[4:6]), int(s[6:8]), int(s[8:10])
    return epoch(y, mo, da, hh, mi, ss), f"{MONTHS[mo - 1]} {da:2} {hh:02}:{mi:02}:{ss:02} {y} GMT"


def epoch(y, mo, da, hh, mi, ss):
    # days from 1970-01-01, by Howard Hinnant's days_from_civil
    y -= mo <= 2
    era = y // 400
    yoe = y - era * 400
    doy = (153 * (mo + (-3 if mo > 2 else 9)) + 2) // 5 + da - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    days = era * 146097 + doe - 719468
    return days * 86400 + hh * 3600 + mi * 60 + ss


def load_cert(d):
    root = parse_der(d, 0, len(d))
    if root is None or root.tag != 0x30 or len(root.kids) != 3:
        return None
    c = Cert()
    c.der = d
    tbs = root.kids[0]
    c.tbs = d[tbs.start:tbs.end()]
    c.sig_alg = oid_str(root.kids[1].kids[0].body(d))
    c.sig = root.kids[2].body(d)[1:]
    k = tbs.kids
    i = 0
    c.version = 1
    if k[0].tag == 0xA0:
        c.version = k[0].kids[0].body(d)[0] + 1
        i = 1
    c.serial = k[i].body(d)
    c.tbs_alg = oid_str(k[i + 1].kids[0].body(d))
    c.issuer = dn(d, k[i + 2])
    c.issuer_der = d[k[i + 2].start:k[i + 2].end()]
    c.not_before, c.nb_text = time_of(d, k[i + 3].kids[0])
    c.not_after, c.na_text = time_of(d, k[i + 3].kids[1])
    c.subject = dn(d, k[i + 4])
    c.subject_der = d[k[i + 4].start:k[i + 4].end()]
    spki = k[i + 5]
    c.key_alg = oid_str(spki.kids[0].kids[0].body(d))
    c.curve = oid_str(spki.kids[0].kids[1].body(d)) if len(spki.kids[0].kids) > 1 and spki.kids[0].kids[1].tag == 6 else ""
    keybits = spki.kids[1].body(d)[1:]
    c.key_bytes = keybits
    c.n = b""
    c.e = 0
    if c.key_alg == "1.2.840.113549.1.1.1":
        kn = parse_der(keybits, 0, len(keybits))
        c.n = kn.kids[0].body(keybits)
        c.e = int.from_bytes(kn.kids[1].body(keybits), "big")
    c.exts = []
    for x in k[i + 6:]:
        if x.tag == 0xA3:
            for e in x.kids[0].kids:
                oid = oid_str(e.kids[0].body(d))
                crit = len(e.kids) == 3 and e.kids[1].body(d)[0] != 0
                val = e.kids[-1].body(d)
                c.exts.append((oid, crit, val))
    return c


def ext(c, oid):
    for o, crit, v in c.exts:
        if o == oid:
            return v
    return None


# ------------------------------------------------------------ extension values

KU_NAMES = ["Digital Signature", "Non Repudiation", "Key Encipherment", "Data Encipherment", "Key Agreement",
            "Certificate Sign", "CRL Sign", "Encipher Only", "Decipher Only"]


def key_usage(v):
    n = parse_der(v, 0, len(v))
    b = n.body(v)
    # bit k of the BIT STRING is the k'th from the top of the first byte
    out = []
    for k in range(9):
        byte = k // 8
        if byte < len(b) - 1 and b[1 + byte] & (0x80 >> (k % 8)):
            out.append(k)
    return out


def basic_constraints(v):
    n = parse_der(v, 0, len(v))
    ca = False
    plen = -1
    for k in n.kids:
        if k.tag == 1:
            ca = k.body(v)[0] != 0
        elif k.tag == 2:
            plen = int.from_bytes(k.body(v), "big")
    return ca, plen


def ip_text(b):
    if len(b) == 4:
        return ".".join(str(x) for x in b)
    return ":".join(f"{b[i] << 8 | b[i + 1]:X}" for i in range(0, 16, 2))


# general names as (kind, text, raw bytes)
def general_names(v, n):
    out = []
    for g in n.kids:
        t = g.tag & 0x1F
        body = g.body(v)
        if t == 1:
            out.append(("email", bytes(body).decode()))
        elif t == 2:
            out.append(("DNS", bytes(body).decode()))
        elif t == 6:
            out.append(("URI", bytes(body).decode()))
        elif t == 7:
            out.append(("IP Address", ip_text(body), body))
        else:
            out.append(("othername", "<unsupported>"))
    return out


def gn_text(g):
    return f"{g[0]}:{g[1]}"


def eku(v):
    n = parse_der(v, 0, len(v))
    return [oid_str(k.body(v)) for k in n.kids]


def ext_lines(oid, v):
    if oid == "2.5.29.17":
        n = parse_der(v, 0, len(v))
        return [", ".join(gn_text(g) for g in general_names(v, n))]
    if oid == "2.5.29.19":
        ca, plen = basic_constraints(v)
        if not ca:
            return ["CA:FALSE"]
        return ["CA:TRUE" + (f", pathlen:{plen}" if plen >= 0 else "")]
    if oid == "2.5.29.15":
        return [", ".join(KU_NAMES[k] for k in key_usage(v))]
    if oid == "2.5.29.37":
        return [", ".join(long_name(o) for o in eku(v))]
    if oid == "2.5.29.14":
        n = parse_der(v, 0, len(v))
        return [hexc(n.body(v), True)]
    if oid == "2.5.29.35":
        n = parse_der(v, 0, len(v))
        for k in n.kids:
            if k.tag == 0x80:
                return [hexc(k.body(v), True)]
        return []
    if oid == "2.5.29.31":
        n = parse_der(v, 0, len(v))
        out = []
        for dp in n.kids:
            for f in dp.kids:
                if f.tag == 0xA0:
                    out.append("Full Name:")
                    for g in general_names(v, f.kids[0]):
                        out.append("  " + gn_text(g))
        return out
    if oid == "1.3.6.1.5.5.7.1.1":
        n = parse_der(v, 0, len(v))
        out = []
        for ad in n.kids:
            method = oid_str(ad.kids[0].body(v))
            g = general_names(v, wrap(ad.kids[1]))[0]
            out.append(f"{long_name(method)} - {gn_text(g)}")
        return out
    if oid == "2.5.29.32":
        n = parse_der(v, 0, len(v))
        return [f"Policy: {oid_str(p.kids[0].body(v))}" for p in n.kids]
    return [hexc(v)]


def wrap(g):
    w = Node(0x30, 0, 0, 0)
    w.kids = [g]
    return w


# ------------------------------------------------------------ printing

def hex_block(b, per, indent):
    out = []
    for i in range(0, len(b), per):
        chunk = b[i:i + per]
        line = ":".join(f"{x:02x}" for x in chunk)
        if i + per < len(b):
            line += ":"
        out.append(" " * indent + line + "\n")
    return "".join(out)


def serial_text(s):
    neg = s[0] & 0x80
    v = s
    while len(v) > 1 and v[0] == 0:
        v = v[1:]
    if len(v) <= 8 and not neg:
        n = int.from_bytes(v, "big")
        return f" {n} (0x{n:x})\n"
    return "\n" + " " * 12 + hexc(v) + "\n"


def print_text(c):
    s = "Certificate:\n    Data:\n"
    s += f"        Version: {c.version} (0x{c.version - 1:x})\n"
    s += "        Serial Number:" + serial_text(c.serial)
    s += f"        Signature Algorithm: {long_name(c.tbs_alg)}\n"
    s += f"        Issuer: {c.issuer}\n"
    s += "        Validity\n"
    s += f"            Not Before: {c.nb_text}\n"
    s += f"            Not After : {c.na_text}\n"
    s += f"        Subject: {c.subject}\n"
    s += "        Subject Public Key Info:\n"
    s += f"            Public Key Algorithm: {long_name(c.key_alg)}\n"
    if c.n:
        n = c.n
        while len(n) > 1 and n[0] == 0 and n[1] & 0x80 == 0:
            n = n[1:]
        bits = (len(n) - 1) * 8 + n[0].bit_length() if n[0] else (len(n) - 1) * 8
        s += f"                Public-Key: ({bits} bit)\n"
        s += "                Modulus:\n" + hex_block(n, 15, 20)
        s += f"                Exponent: {c.e} (0x{c.e:x})\n"
    else:
        s += "                Public-Key: (256 bit)\n"
        s += "                pub:\n" + hex_block(c.key_bytes, 15, 20)
        s += f"                ASN1 OID: {long_name(c.curve)}\n"
        s += "                NIST CURVE: P-256\n"
    if c.exts:
        s += "        X509v3 extensions:\n"
        for oid, crit, v in c.exts:
            s += f"            {long_name(oid)}: {'critical' if crit else ''}\n"
            for l in ext_lines(oid, v):
                s += " " * 16 + l + "\n"
    s += f"    Signature Algorithm: {long_name(c.sig_alg)}\n"
    s += "    Signature Value:\n" + hex_block(c.sig, 18, 8)
    return s


# ------------------------------------------------------------ files

class Job:
    def __init__(self):
        self.out = ""
        self.err = ""
        self.status = 0


def read_certs(path):
    # every certificate in a PEM file, or the one in a DER file; None when
    # the file cannot be opened
    if not os.path.isfile("data/" + path):
        return None
    data = open("data/" + path, "rb").read()
    certs = []
    if b"-----BEGIN CERTIFICATE-----" not in data:
        c = load_cert(data)
        return [c] if c else []
    text = data.decode("latin-1")
    for block in text.split("-----BEGIN CERTIFICATE-----")[1:]:
        if "-----END CERTIFICATE-----" not in block:
            break
        body = block.split("-----END CERTIFICATE-----")[0]
        b64 = "".join(body.split())
        try:
            der = base64.b64decode(b64, validate=True)
        except Exception:
            break
        c = load_cert(der)
        if c is None:
            break
        certs.append(c)
    return certs


def first_cert(job, path):
    certs = read_certs(path)
    if certs is None:
        job.err += f"Could not open file or uri for loading certificate from {path}\nUnable to load certificate\n"
        job.status = 1
        return None
    if not certs:
        job.err += f"Could not read certificate from {path}\nUnable to load certificate\n"
        job.status = 1
        return None
    return certs[0]


# ------------------------------------------------------------ matching

def host_match(pattern, host):
    p = pattern.lower()
    h = host.lower()
    if p == h:
        return True
    if p.startswith("*.") and p.count(".") >= 2:
        dot = h.find(".")
        return dot > 0 and h[dot:] == p[1:]
    return False


def sans(c):
    v = ext(c, "2.5.29.17")
    if v is None:
        return []
    return general_names(v, parse_der(v, 0, len(v)))


def check_host(c, host):
    dns = [g for g in sans(c) if g[0] == "DNS"]
    if dns:
        return any(host_match(g[1], host) for g in dns)
    cn = [p[5:] for p in c.subject.split(", ") if p.startswith("CN = ")]
    return any(host_match(x, host) for x in cn)


def parse_ip(s):
    if ":" not in s:
        return bytes(int(x) for x in s.split("."))
    head, _, tail = s.partition("::")
    h = [int(x, 16) for x in head.split(":") if x]
    t = [int(x, 16) for x in tail.split(":") if x] if "::" in s else []
    groups = h + [0] * (8 - len(h) - len(t)) + t
    return b"".join(g.to_bytes(2, "big") for g in groups)


def x509_cmd(job, args):
    path = ""
    inform = "PEM"
    actions = []
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("-in", "-inform", "-ext", "-checkhost", "-checkip", "-checkemail"):
            if a == "-in":
                path = args[i + 1]
            elif a == "-inform":
                inform = args[i + 1]
            else:
                actions.append((a, args[i + 1]))
            i += 2
            continue
        if a != "-noout":
            actions.append((a, ""))
        i += 1
    c = first_cert(job, path)
    if c is None:
        return
    digest = "sha1"
    for a, v in actions:
        if a in ("-sha256", "-sha1"):
            digest = a[1:]
    for a, v in actions:
        if a == "-text":
            job.out += print_text(c)
        elif a == "-subject":
            job.out += f"subject={c.subject}\n"
        elif a == "-issuer":
            job.out += f"issuer={c.issuer}\n"
        elif a == "-serial":
            s = c.serial
            while len(s) > 1 and s[0] == 0:
                s = s[1:]
            job.out += "serial=" + "".join(f"{x:02X}" for x in s) + "\n"
        elif a == "-dates":
            job.out += f"notBefore={c.nb_text}\nnotAfter={c.na_text}\n"
        elif a == "-enddate":
            job.out += f"notAfter={c.na_text}\n"
        elif a == "-fingerprint":
            h = hashlib.new(digest, c.der).digest()
            job.out += f"{'SHA1' if digest == 'sha1' else digest} Fingerprint={hexc(h, True)}\n"
        elif a == "-ext":
            want = v.split(",")
            for oid, crit, val in c.exts:
                if short_name(oid) in want:
                    job.out += f"{long_name(oid)}: {'critical' if crit else ''}\n"
                    for l in ext_lines(oid, val):
                        job.out += "    " + l + "\n"
        elif a == "-checkhost":
            job.out += f"Hostname {v} does{'' if check_host(c, v) else ' NOT'} match certificate\n"
        elif a == "-checkip":
            ok = any(g[0] == "IP Address" and g[2] == parse_ip(v) for g in sans(c))
            job.out += f"IP {v} does{'' if ok else ' NOT'} match certificate\n"
        elif a == "-checkemail":
            ok = any(g[0] == "email" and g[1].lower() == v.lower() for g in sans(c))
            job.out += f"Email {v} does{'' if ok else ' NOT'} match certificate\n"


# ------------------------------------------------------------ asn1parse

TAG_NAMES = {1: "BOOLEAN", 2: "INTEGER", 3: "BIT STRING", 4: "OCTET STRING", 5: "NULL", 6: "OBJECT",
             12: "UTF8STRING", 16: "SEQUENCE", 17: "SET", 19: "PRINTABLESTRING", 22: "IA5STRING",
             23: "UTCTIME", 24: "GENERALIZEDTIME"}


def asn1_lines(d, n, depth, out):
    cls = n.tag & 0xC0
    if cls == 0x80:
        name = f"cont [ {n.tag & 0x1F} ]"
    else:
        name = TAG_NAMES.get(n.tag & 0x1F, f"<ASN1 {n.tag & 0x1F}>")
    kind = "cons" if n.tag & 0x20 else "prim"
    line = f"{n.start:5}:d={depth:<2} hl={n.hl} l={n.len:4} {kind}: {' ' * depth}{name:<18}"
    b = n.body(d)
    t = n.tag
    if t == 2:
        line += ":" + "".join(f"{x:02X}" for x in b)
    elif t == 6:
        line += ":" + long_name(oid_str(b))
    elif t in (12, 19, 22, 23, 24):
        line += ":" + bytes(b).decode("utf-8", "replace")
    out.append(line + "\n")
    for k in n.kids:
        asn1_lines(d, k, depth + 1, out)


def asn1parse_cmd(job, args):
    path = args[args.index("-in") + 1]
    certs = read_certs(path)
    if not certs:
        job.err += "Error reading certificate\n"
        job.status = 1
        return
    d = certs[0].der
    out = []
    asn1_lines(d, parse_der(d, 0, len(d)), 0, out)
    job.out += "".join(out)


# ------------------------------------------------------------ verify

ERRORS = {
    7: "certificate signature failure",
    9: "certificate is not yet valid",
    10: "certificate has expired",
    18: "self-signed certificate",
    19: "self-signed certificate in certificate chain",
    20: "unable to get local issuer certificate",
    25: "path length constraint exceeded",
    26: "unsuitable certificate purpose",
    32: "key usage does not include certificate signing",
    62: "hostname mismatch",
    79: "invalid CA certificate",
}
# the errors the verify command's callback lets the check continue past
CONTINUE = {9, 10, 18, 25, 26, 79}

SHA256_PREFIX = bytes.fromhex("3031300d060960864801650304020105000420")


def rsa_verify(issuer, c):
    n = int.from_bytes(issuer.n, "big")
    s = int.from_bytes(c.sig, "big")
    k = (n.bit_length() + 7) // 8
    if s >= n or len(c.sig) != k:
        return False
    em = pow(s, issuer.e, n).to_bytes(k, "big")
    want = b"\x00\x01" + b"\xff" * (k - 3 - len(SHA256_PREFIX) - 32) + b"\x00" + SHA256_PREFIX + hashlib.sha256(c.tbs).digest()
    return em == want


def self_issued(c):
    return c.subject_der == c.issuer_der


def ku_has(c, bit):
    v = ext(c, "2.5.29.15")
    return v is None or bit in key_usage(v)


def is_ca(c):
    v = ext(c, "2.5.29.19")
    return v is not None and basic_constraints(v)[0]


def path_len(c):
    v = ext(c, "2.5.29.19")
    return basic_constraints(v)[1] if v is not None else -1


def eku_allows(c, oid):
    v = ext(c, "2.5.29.37")
    return v is None or oid in eku(v)


class Verify:
    def __init__(self, job):
        self.job = job
        self.failed = False

    # report an error at depth i; True to keep going
    def error(self, c, i, code):
        self.job.err += f"{c.subject}\nerror {code} at {i} depth lookup: {ERRORS[code]}\n"
        self.failed = True
        return code in CONTINUE


def verify_one(job, path, trusted, untrusted, at, purpose, host):
    certs = read_certs(path)
    if not certs:
        job.err += f"Could not read certificate from {path}\nUnable to load certificate\n" if certs is not None else \
            f"Could not open file or uri for loading certificate from {path}\n"
        job.err += f"error {path}: verification failed\n"
        return False
    leaf = certs[0]
    v = Verify(job)
    # build the chain: untrusted issuers first, then a trusted one
    chain = [leaf]
    anchored = False
    while True:
        top = chain[-1]
        tr = [t for t in trusted if t.subject_der == top.issuer_der]
        if tr:
            if not (self_issued(top) and any(t.der == top.der for t in trusted)):
                chain.append(tr[0])
            anchored = True
            break
        if self_issued(top):
            break
        un = [u for u in untrusted if u.subject_der == top.issuer_der and u not in chain]
        if not un:
            break
        chain.append(un[0])
    if not anchored:
        top = chain[-1]
        if self_issued(top):
            code = 18 if len(chain) == 1 else 19
            if not v.error(top, len(chain) - 1, code):
                job.err += f"error {path}: verification failed\n"
                return False
        else:
            v.error(top, len(chain) - 1, 20)
            job.err += f"error {path}: verification failed\n"
            return False
    # extensions: CA flags, purpose, path lengths
    plen = 0
    for i, c in enumerate(chain):
        if i > 0 and not is_ca(c):
            if not v.error(c, i, 79):
                return fail(job, path)
        if purpose and i == 0 and not eku_allows(c, "1.3.6.1.5.5.7.3.1"):
            if not v.error(c, i, 26):
                return fail(job, path)
        if i > 1 and path_len(c) >= 0 and plen > path_len(c):
            if not v.error(c, i, 25):
                return fail(job, path)
        if i > 0 and not self_issued(c):
            plen += 1
    if host and not check_host(leaf, host):
        if not v.error(leaf, 0, 62):
            return fail(job, path)
    # signatures and validity, from the anchor down
    for i in range(len(chain) - 1, -1, -1):
        c = chain[i]
        issuer = chain[i + 1] if i + 1 < len(chain) else None
        if issuer is not None:
            if not ku_has(issuer, 5):
                if not v.error(issuer, i + 1, 32):
                    return fail(job, path)
            if not rsa_verify(issuer, c):
                if not v.error(c, i, 7):
                    return fail(job, path)
        if at < c.not_before:
            if not v.error(c, i, 9):
                return fail(job, path)
        if at > c.not_after:
            if not v.error(c, i, 10):
                return fail(job, path)
    if v.failed:
        return fail(job, path)
    job.out += f"{path}: OK\n"
    return True


def fail(job, path):
    job.err += f"error {path}: verification failed\n"
    return False


def verify_cmd(job, args):
    trusted = []
    untrusted = []
    at = 0
    purpose = ""
    host = ""
    files = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "-CAfile":
            trusted += read_certs(args[i + 1]) or []
            i += 2
        elif a == "-untrusted":
            untrusted += read_certs(args[i + 1]) or []
            i += 2
        elif a == "-attime":
            at = int(args[i + 1])
            i += 2
        elif a == "-purpose":
            purpose = args[i + 1]
            i += 2
        elif a == "-verify_hostname":
            host = args[i + 1]
            i += 2
        else:
            files.append(a)
            i += 1
    ok = True
    for f in files:
        if not verify_one(job, f, trusted, untrusted, at, purpose, host):
            ok = False
    if not ok:
        job.status = 2


def main():
    for line in open("data/jobs.txt").read().splitlines():
        if not line or line.startswith("#"):
            continue
        job = Job()
        w = line.split(" ")
        if w[0] == "x509":
            x509_cmd(job, w[1:])
        elif w[0] == "asn1parse":
            asn1parse_cmd(job, w[1:])
        elif w[0] == "verify":
            verify_cmd(job, w[1:])
        text = f"$ openssl {line}\n" + job.out + job.err
        if job.status:
            text += f"[exit status {job.status}]\n"
        sys.stdout.write(text + "\n")


main()
