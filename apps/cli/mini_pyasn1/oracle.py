# Prints expected.out: runs data/jobs.json and the four programs through
# pyasn1 itself (the vendored copy in pyasn1/), the way mini_pyasn1.kara
# runs them through its port.
import base64
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pyasn1 import error  # noqa: E402
from pyasn1.codec.ber import decoder as ber_dec  # noqa: E402
from pyasn1.codec.ber import encoder as ber_enc  # noqa: E402
from pyasn1.codec.cer import decoder as cer_dec  # noqa: E402
from pyasn1.codec.cer import encoder as cer_enc  # noqa: E402
from pyasn1.codec.der import decoder as der_dec  # noqa: E402
from pyasn1.codec.der import encoder as der_enc  # noqa: E402
from pyasn1.codec.native import decoder as nat_dec  # noqa: E402
from pyasn1.codec.native import encoder as nat_enc  # noqa: E402
from pyasn1.type import char  # noqa: E402
from pyasn1.type import constraint  # noqa: E402
from pyasn1.type import namedtype  # noqa: E402
from pyasn1.type import namedval  # noqa: E402
from pyasn1.type import opentype  # noqa: E402
from pyasn1.type import tag  # noqa: E402
from pyasn1.type import univ  # noqa: E402
from pyasn1.type import useful  # noqa: E402

os.chdir(os.path.dirname(os.path.abspath(__file__)))

BASES = {}
for mod in (univ, char, useful):
    for name in dir(mod):
        obj = getattr(mod, name)
        if isinstance(obj, type) and issubclass(obj, univ.base.Asn1Type) and obj.typeId is not None:
            BASES[name] = obj
for name in ("SequenceOfAndSetOfBase", "SequenceAndSetBase"):
    BASES.pop(name, None)

TAG_CLASS = {"universal": tag.tagClassUniversal, "application": tag.tagClassApplication,
             "context": tag.tagClassContext, "private": tag.tagClassPrivate}

ENCODERS = {"ber": ber_enc.encode, "cer": cer_enc.encode, "der": der_enc.encode}
DECODERS = {"ber": ber_dec.decode, "cer": cer_dec.decode, "der": der_dec.decode}

CLASSES = dict(BASES)


def bound(x):
    if x == "MAX":
        return float("inf")
    if x == "MIN":
        return float("-inf")
    return x


def cons(c):
    if "range" in c:
        return constraint.ValueRangeConstraint(bound(c["range"][0]), bound(c["range"][1]))
    if "size" in c:
        return constraint.ValueSizeConstraint(bound(c["size"][0]), bound(c["size"][1]))
    if "single" in c:
        return constraint.SingleValueConstraint(*[pyval(v) for v in c["single"]])
    if "alpha" in c:
        return constraint.PermittedAlphabetConstraint(*c["alpha"])
    if "union" in c:
        return constraint.ConstraintsUnion(*[cons(x) for x in c["union"]])
    if "inter" in c:
        return constraint.ConstraintsIntersection(*[cons(x) for x in c["inter"]])
    if "excl" in c:
        return constraint.ConstraintsExclusion(cons(c["excl"]))
    raise ValueError(c)


def mktag(t):
    return tag.Tag(TAG_CLASS[t[0]], tag.tagFormatSimple, t[1])


def named_types(fields):
    out = []
    for f in fields:
        t = build(f["t"])
        ot = None
        if "open" in f:
            gov, mapping = f["open"]
            m = {}
            for k, v in mapping:
                key = univ.ObjectIdentifier(k) if isinstance(k, str) else univ.Integer(k)
                m[key] = build(v)
            ot = opentype.OpenType(gov, m)
        if f.get("opt"):
            out.append(namedtype.OptionalNamedType(f["n"], t, openType=ot))
        elif f.get("default"):
            out.append(namedtype.DefaultedNamedType(f["n"], t, openType=ot))
        else:
            out.append(namedtype.NamedType(f["n"], t, openType=ot))
    return namedtype.NamedTypes(*out)


def build(t):
    if isinstance(t, str):
        return CLASSES[t]()
    cls = CLASSES[t["t"]]
    kw = {}
    if "of" in t:
        kw["componentType"] = build(t["of"])
    if "fields" in t:
        kw["componentType"] = named_types(t["fields"])
    obj = cls(**kw)
    sub = {}
    if "impl" in t:
        sub["implicitTag"] = mktag(t["impl"])
    if "expl" in t:
        sub["explicitTag"] = mktag(t["expl"])
    if "sub" in t:
        c = constraint.ConstraintsIntersection()
        for x in t["sub"]:
            c += cons(x)
        sub["subtypeSpec"] = c
    if "size" in t:
        c = constraint.ConstraintsIntersection()
        for x in t["size"]:
            c += cons(x)
        sub["sizeSpec"] = c
    if "named" in t:
        sub["namedValues"] = namedval.NamedValues(*[tuple(x) for x in t["named"]])
    if sub:
        obj = obj.subtype(**sub)
    if "value" in t:
        obj = obj.clone(pyval(t["value"]))
    return obj


def define(d):
    base = CLASSES[d["class"]]
    attrs = {}
    if "tag" in d:
        if "impl" in d["tag"]:
            attrs["tagSet"] = base.tagSet.tagImplicitly(mktag(d["tag"]["impl"]))
        else:
            attrs["tagSet"] = base.tagSet.tagExplicitly(mktag(d["tag"]["expl"]))
    if "named" in d:
        attrs["namedValues"] = namedval.NamedValues(*[tuple(x) for x in d["named"]])
    if "cons" in d:
        spec = base.subtypeSpec
        for c in d["cons"]:
            spec = spec + cons(c)
        attrs["subtypeSpec"] = spec
    if "of" in d:
        attrs["componentType"] = build(d["of"])
    if "fields" in d:
        attrs["componentType"] = named_types(d["fields"])
    if "sizeSpec" in d:
        for c in d["sizeSpec"]:
            attrs["sizeSpec"] = cons(c)
    CLASSES[d["def"]] = type(d["def"], (base,), attrs)


def pyval(v):
    if isinstance(v, dict):
        if "hex" in v:
            return bytes.fromhex(v["hex"])
        if "tuple" in v:
            return tuple(pyval(x) for x in v["tuple"])
        if "float" in v:
            return float(v["float"])
        return {k: pyval(x) for k, x in v.items()}
    if isinstance(v, list):
        return [pyval(x) for x in v]
    return v


def err(e):
    return "%s: %s" % (type(e).__name__, e)


def hexs(b):
    return bytes(b).hex()


def opts(o):
    out = {}
    for k, v in (o or {}).items():
        if k == "openTypes":
            continue
        out[k] = v
    return out


for d in json.load(open("data/schemas.json")):
    define(d)


def make(t, v):
    spec = build(t)
    if isinstance(v, dict) and "ctor" in v:
        return spec.clone(pyval(v["ctor"]))
    return nat_dec.decode(pyval(v), asn1Spec=spec)


def show(obj):
    if isinstance(obj, univ.base.SimpleAsn1Type):
        print("repr: %r" % (obj,))
    print("pretty: %s" % obj.prettyPrint())
    try:
        print("native: %r" % (nat_enc.encode(obj),))
    except Exception as e:
        print("native: " + err(e))


def job_make(j):
    try:
        v = make(j["t"], j["v"])
    except Exception as e:
        print(err(e))
        return
    show(v)


def job_repr(j):
    try:
        if "v" in j:
            obj = make(j["t"], j["v"])
        else:
            obj = build(j["t"])
        print(repr(obj))
    except Exception as e:
        print(err(e))


def job_ptype(j):
    print(build(j["t"]).prettyPrintType())


def job_bits(j):
    try:
        b = make(j.get("t", "BitString"), {"ctor": j["v"]})
        print("str=%s int=%d octets=%s len=%d bits=%s" % (
            str(b), b.asInteger(), b.asOctets().hex(), len(b), list(b)))
        if len(b) > 2:
            print("b[0]=%d b[-1]? %s b[1:3]=%s" % (b[0], b[len(b) - 1], b[1:3]))
        print("shifted: %s %s" % (b << 2, b >> 1))
        print("plus: %s" % (b + "11"))
        print("cmp: %s %s" % (b == "1011001", b < "11"))
    except Exception as e:
        print(err(e))


def job_oid(j):
    a = univ.ObjectIdentifier(j["a"])
    b = univ.ObjectIdentifier(j["b"])
    print("a=%s b=%s len=%d prefix=%s eq=%s a+b=%s a[1:]=%s" % (
        a, b, len(a), a.isPrefixOf(b), a == b, a + tuple(b), a[1:]))


def job_time(j):
    try:
        t = CLASSES[j["t"]](j["v"])
        print(t.asDateTime.isoformat())
    except Exception as e:
        print(err(e))


def job_enc(j):
    try:
        v = make(j["t"], j["v"])
    except Exception as e:
        print("make: " + err(e))
        return
    kw = opts(j.get("opts"))
    if j.get("spec"):
        kw["asn1Spec"] = build(j["t"])
    try:
        print(hexs(ENCODERS[j["codec"]](v, **kw)))
    except Exception as e:
        print(err(e))
    print("after: %s" % v.prettyPrint())


def job_dec(j):
    kw = opts(j.get("opts"))
    if j.get("t"):
        kw["asn1Spec"] = build(j["t"])
    try:
        obj, tail = DECODERS[j["codec"]](bytes.fromhex(j["hex"]), **kw)
    except Exception as e:
        print(err(e))
        return
    if obj is None:
        print("None")
    elif isinstance(obj, bytes):
        print("bytes %s" % hexs(obj))
    else:
        print("%s %s" % (type(obj).__name__, obj.tagSet))
        show(obj)
    if tail:
        print("tail: %s" % hexs(tail))


def job_rt(j):
    v = make(j["t"], j["v"])
    spec = build(j["t"])
    for c in ("ber", "cer", "der"):
        b = ENCODERS[c](v)
        try:
            obj, tail = DECODERS[c](b, asn1Spec=spec)
        except Exception as e:
            print("%s %s %s" % (c, hexs(b), err(e)))
            continue
        same = der_enc.encode(obj) == der_enc.encode(v)
        print("%s %s %s" % (c, hexs(b), same and "same" or "differs"))
    print(obj.prettyPrint())


JOBS = {"make": job_make, "repr": job_repr, "ptype": job_ptype, "bits": job_bits, "oid": job_oid,
        "time": job_time, "enc": job_enc, "dec": job_dec, "rt": job_rt}


def run_jobs():
    for j in json.load(open("data/jobs.json")):
        print("== %s %s" % (j["op"], j["id"]))
        JOBS[j["op"]](j)


# ---- the programs ---------------------------------------------------------

NAMES = {
    "2.5.4.3": "CN", "2.5.4.5": "serialNumber", "2.5.4.6": "C", "2.5.4.7": "L", "2.5.4.8": "ST",
    "2.5.4.10": "O", "2.5.4.11": "OU", "2.5.4.97": "organizationIdentifier",
    "1.2.840.113549.1.9.1": "emailAddress", "0.9.2342.19200300.100.1.25": "DC",
    "1.2.840.113549.1.1.1": "rsaEncryption", "1.2.840.113549.1.1.5": "sha1WithRSAEncryption",
    "1.2.840.113549.1.1.11": "sha256WithRSAEncryption", "1.2.840.113549.1.1.12": "sha384WithRSAEncryption",
    "1.2.840.113549.1.1.13": "sha512WithRSAEncryption", "1.2.840.10045.2.1": "ecPublicKey",
    "1.2.840.10045.4.3.2": "ecdsa-with-SHA256", "1.2.840.10045.4.3.3": "ecdsa-with-SHA384",
    "1.3.132.0.34": "secp384r1", "1.2.840.10045.3.1.7": "prime256v1",
    "2.5.29.14": "subjectKeyIdentifier", "2.5.29.15": "keyUsage", "2.5.29.16": "privateKeyUsagePeriod",
    "2.5.29.17": "subjectAltName", "2.5.29.19": "basicConstraints", "2.5.29.31": "cRLDistributionPoints",
    "2.5.29.32": "certificatePolicies", "2.5.29.35": "authorityKeyIdentifier", "2.5.29.37": "extKeyUsage",
    "1.3.6.1.5.5.7.1.1": "authorityInfoAccess", "1.3.6.1.5.5.7.48.1": "ocsp", "1.3.6.1.5.5.7.48.2": "caIssuers",
    "1.3.6.1.5.5.7.2.1": "cps", "1.3.6.1.5.5.7.2.2": "unotice", "2.5.29.32.0": "anyPolicy",
    "1.3.6.1.5.5.7.3.1": "serverAuth", "1.3.6.1.5.5.7.3.2": "clientAuth",
    "1.2.840.113549.1.9.14": "extensionRequest",
}


def oname(oid):
    return NAMES.get(str(oid), str(oid))


def text(v):
    if isinstance(v, univ.Choice):
        v = v.getComponent()
    if isinstance(v, univ.Any):
        return "#" + hexs(v.asOctets())
    return str(v)


def dn(name):
    rdns = []
    for rdn in name["rdnSequence"]:
        rdns.append("+".join("%s=%s" % (oname(atv["type"]), text(atv["value"])) for atv in rdn))
    return ", ".join(rdns)


def general_name(g):
    kind = g.getName()
    v = g.getComponent()
    if kind == "directoryName":
        return "DirName:" + dn(v)
    if kind == "iPAddress":
        return "IP:" + ".".join(str(b) for b in v.asOctets())
    if kind == "registeredID":
        return "RID:" + str(v)
    if kind == "otherName":
        return "othername:" + str(v["type-id"])
    return {"rfc822Name": "email", "dNSName": "DNS", "uniformResourceIdentifier": "URI"}[kind] + ":" + str(v)


def decode_ext(oid, raw):
    spec = {"2.5.29.19": "BasicConstraints", "2.5.29.15": "KeyUsage", "2.5.29.14": "SubjectKeyIdentifier",
            "2.5.29.35": "AuthorityKeyIdentifier", "2.5.29.32": "CertificatePolicies",
            "2.5.29.31": "CRLDistributionPoints", "1.3.6.1.5.5.7.1.1": "AuthorityInfoAccessSyntax",
            "2.5.29.17": "GeneralNames", "2.5.29.37": "ExtKeyUsageSyntax",
            "2.5.29.16": "PrivateKeyUsagePeriod"}.get(oid)
    if spec is None:
        return ["%d bytes" % len(raw)]
    v, tail = der_dec.decode(raw, asn1Spec=CLASSES[spec](), decodeOpenTypes=True)
    if spec == "BasicConstraints":
        out = "CA:%s" % ("TRUE" if v["cA"] else "FALSE")
        if v["pathLenConstraint"].isValue:
            out += ", pathlen:%d" % v["pathLenConstraint"]
        return [out]
    if spec == "KeyUsage":
        names = [n for n, pos in CLASSES["KeyUsage"].namedValues.items() if pos < len(v) and v[pos]]
        return [", ".join(names) + " (%s)" % v.prettyPrint()]
    if spec == "SubjectKeyIdentifier":
        return [":".join("%02X" % b for b in v.asOctets())]
    if spec == "AuthorityKeyIdentifier":
        out = []
        if v["keyIdentifier"].isValue:
            out.append("keyid:" + ":".join("%02X" % b for b in v["keyIdentifier"].asOctets()))
        if v["authorityCertIssuer"].isValue:
            out.extend(general_name(g) for g in v["authorityCertIssuer"])
        if v["authorityCertSerialNumber"].isValue:
            out.append("serial:%x" % int(v["authorityCertSerialNumber"]))
        return out
    if spec == "CertificatePolicies":
        out = []
        for pi in v:
            out.append("Policy: " + oname(pi["policyIdentifier"]))
            if pi["policyQualifiers"].isValue:
                for q in pi["policyQualifiers"]:
                    qid = str(q["policyQualifierId"])
                    if qid == "1.3.6.1.5.5.7.2.1":
                        uri, _ = der_dec.decode(q["qualifier"].asOctets(), asn1Spec=char.IA5String())
                        out.append("  CPS: " + str(uri))
                    else:
                        out.append("  %s: %d bytes" % (oname(qid), len(q["qualifier"])))
        return out
    if spec == "CRLDistributionPoints":
        out = []
        for dp in v:
            if dp["distributionPoint"].isValue:
                dpn = dp["distributionPoint"]
                if dpn.getName() == "fullName":
                    out.extend("Full Name: " + general_name(g) for g in dpn["fullName"])
                else:
                    out.append("Relative Name: %d attributes" % len(dpn["nameRelativeToCRLIssuer"]))
            if dp["reasons"].isValue:
                out.append("Reasons: " + dp["reasons"].prettyPrint())
        return out
    if spec == "AuthorityInfoAccessSyntax":
        return ["%s - %s" % (oname(ad["accessMethod"]), general_name(ad["accessLocation"])) for ad in v]
    if spec == "GeneralNames":
        return [", ".join(general_name(g) for g in v)]
    if spec == "ExtKeyUsageSyntax":
        return [", ".join(oname(k) for k in v)]
    return [v.prettyPrint()]


def when(t):
    return t.getComponent().asDateTime.isoformat()


def key_info(spki):
    alg = spki["algorithm"]
    bits = spki["subjectPublicKey"]
    name = oname(alg["algorithm"])
    if name == "rsaEncryption":
        rsa, _ = der_dec.decode(bits.asOctets(), asn1Spec=CLASSES["RSAPublicKey"]())
        n = int(rsa["modulus"])
        return "RSA %d bit, exponent %d, modulus %s...%s" % (
            n.bit_length(), int(rsa["publicExponent"]), ("%x" % n)[:8], ("%x" % n)[-8:])
    if name == "ecPublicKey":
        curve = alg["parameters"]["namedCurve"]
        return "EC %s, point %d bytes, first byte %02x" % (oname(curve), len(bits) // 8, bits.asOctets()[0])
    return name


def pem_body(text, label):
    lines = text.strip().splitlines()
    if lines[0] != "-----BEGIN %s-----" % label or lines[-1] != "-----END %s-----" % label:
        raise ValueError("not a %s PEM block" % label)
    return base64.b64decode("".join(lines[1:-1]))


def prog_certinfo():
    for fn in sorted(os.listdir("data/certs")):
        print("== certinfo %s" % fn)
        der = pem_body(open("data/certs/" + fn).read(), "CERTIFICATE")
        cert, tail = der_dec.decode(der, asn1Spec=CLASSES["Certificate"](), decodeOpenTypes=True)
        tbs = cert["tbsCertificate"]
        print("version: %s" % tbs["version"].prettyPrint())
        print("serial: %x" % int(tbs["serialNumber"]))
        print("signature: %s" % oname(tbs["signature"]["algorithm"]))
        print("issuer: %s" % dn(tbs["issuer"]))
        print("subject: %s" % dn(tbs["subject"]))
        print("valid: %s .. %s (%s, %s)" % (when(tbs["validity"]["notBefore"]), when(tbs["validity"]["notAfter"]),
                                             tbs["validity"]["notBefore"].getName(),
                                             tbs["validity"]["notAfter"].getName()))
        print("key: %s" % key_info(tbs["subjectPublicKeyInfo"]))
        if tbs["extensions"].isValue:
            for ext in tbs["extensions"]:
                oid = str(ext["extnID"])
                print("ext %s%s:" % (oname(oid), " critical" if ext["critical"] else ""))
                for line in decode_ext(oid, ext["extnValue"].asOctets()):
                    print("    " + line)
        print("signature bits: %d" % len(cert["signature"]))
        print("self-signed name: %s" % (der_enc.encode(tbs["issuer"]) == der_enc.encode(tbs["subject"])))
        print("DER round trip: %s, %d bytes, tail %d" % (der_enc.encode(cert) == der, len(der), len(tail)))
    smallest = min(sorted(os.listdir("data/certs")), key=lambda f: os.path.getsize("data/certs/" + f))
    der = pem_body(open("data/certs/" + smallest).read(), "CERTIFICATE")
    print("== certinfo schemaless %s" % smallest)
    print(ber_dec.decode(der)[0].prettyPrint())


def bits_of(b):
    return "".join("%08d" % int(bin(x)[2:]) for x in b)


def pem(der, label):
    b = base64.b64encode(der).decode()
    return "-----BEGIN %s-----\n%s\n-----END %s-----\n" % (
        label, "\n".join(b[i:i + 64] for i in range(0, len(b), 64)), label)


RDN_TYPES = {}
for d in json.load(open("data/schemas.json")):
    if d["def"] == "AttributeTypeAndValue":
        for k, t in d["fields"][1]["open"][1]:
            RDN_TYPES[k] = build(t)


def prog_csr():
    os.makedirs("data/out", exist_ok=True)
    for fn in sorted(os.listdir("data/csr")):
        print("== csr %s" % fn)
        req = json.load(open("data/csr/" + fn))
        try:
            rdns = []
            for oid, val in req["subject"]:
                spec = RDN_TYPES[oid]
                if isinstance(spec, univ.Choice):
                    val = {"utf8String": val}
                enc = der_enc.encode(nat_dec.decode(val, asn1Spec=spec))
                rdns.append([{"type": oid, "value": enc}])
            key = der_enc.encode(make("RSAPublicKey", {"modulus": int(req["modulus"], 16),
                                                       "publicExponent": req["exponent"]}))
            san = der_enc.encode(make("GeneralNames", [{"dNSName": d} for d in req["dns"]]))
            exts = der_enc.encode(make("Extensions", [{"extnID": "2.5.29.17", "extnValue": san}]))
            csr = make("CertificationRequest", {
                "certificationRequestInfo": {
                    "version": "v1", "subject": {"rdnSequence": rdns},
                    "subjectPKInfo": {"algorithm": {"algorithm": "1.2.840.113549.1.1.1", "parameters": b"\x05\x00"},
                                      "subjectPublicKey": bits_of(key)},
                    "attributes": [{"type": "1.2.840.113549.1.9.14", "values": [exts]}]},
                "signatureAlgorithm": {"algorithm": "1.2.840.113549.1.1.11", "parameters": b"\x05\x00"},
                "signature": bits_of(bytes.fromhex(req["signature"]))})
            der = der_enc.encode(csr)
        except Exception as e:
            print("error: " + err(e))
            continue
        out = "data/out/" + fn.replace(".json", ".csr")
        with open(out, "w") as f:
            f.write(pem(der, "CERTIFICATE REQUEST"))
        print("wrote %s, %d bytes DER" % (out, len(der)))
        text_ = open(out).read()
        print(text_, end="")
        back, tail = der_dec.decode(pem_body(text_, "CERTIFICATE REQUEST"),
                                    asn1Spec=CLASSES["CertificationRequest"](), decodeOpenTypes=True)
        info = back["certificationRequestInfo"]
        print("subject: %s" % dn(info["subject"]))
        print("key: %s" % key_info(info["subjectPKInfo"]))
        for attr in info["attributes"]:
            print("attribute %s, %d value(s)" % (oname(attr["type"]), len(attr["values"])))
            for raw in attr["values"]:
                exts_, _ = der_dec.decode(raw.asOctets(), asn1Spec=CLASSES["Extensions"]())
                for ext in exts_:
                    print("  %s: %s" % (oname(ext["extnID"]),
                                        "; ".join(decode_ext(str(ext["extnID"]), ext["extnValue"].asOctets()))))
        print("same DER: %s" % (der_enc.encode(back) == der))


def mib_value(kind, v):
    return {"string": lambda: {"simple": {"string-value": v}},
            "integer": lambda: {"simple": {"integer-value": v}},
            "oid": lambda: {"simple": {"objectID-value": v}},
            "timeticks": lambda: {"application-wide": {"timeticks-value": v}},
            "counter32": lambda: {"application-wide": {"counter-value": v}},
            "gauge32": lambda: {"application-wide": {"gauge32-value": v}},
            "counter64": lambda: {"application-wide": {"big-counter-value": v}},
            "ipaddress": lambda: {"application-wide": {"ipAddress-value": bytes.fromhex(v)}}}[kind]()


def oid_key(s):
    return tuple(int(x) for x in s.split("."))


def bind_text(bv):
    kind = bv.getName()
    if kind != "value":
        return kind
    syn = bv["value"].getComponent()
    inner = syn.getComponent()
    name = syn.getName()
    if name == "string-value":
        return "STRING: %s" % inner.prettyPrint()
    if name == "ipAddress-value":
        return "IpAddress: %s" % ".".join(str(b) for b in inner.asOctets())
    return "%s: %s" % (type(inner).__name__ if type(inner).__name__ != "Integer32" else "INTEGER",
                       inner.prettyPrint())


def prog_snmp():
    mib = {}
    for oid, kind, value, writable in json.load(open("data/snmp/mib.json")):
        mib[oid] = [kind, value, writable]
    order = sorted(mib, key=oid_key)

    def lookup(oid):
        if oid in mib:
            return mib[oid][0], mib[oid][1]
        prefix = oid + "."
        for o in order:
            if o.startswith(prefix) or oid.startswith(o.rsplit(".", 1)[0] + "."):
                return None, "noSuchInstance"
        return None, "noSuchObject"

    def after(oid):
        k = oid_key(oid)
        for o in order:
            if oid_key(o) > k:
                return o
        return None

    def bind(oid, kind, value):
        if kind is None:
            return {"name": oid, "": {value: None}}
        return {"name": oid, "": {"value": mib_value(kind, value)}}

    def nextbind(oid):
        o = after(oid)
        if o is None:
            return {"name": oid, "": {"endOfMibView": None}}
        return bind(o, mib[o][0], mib[o][1])

    for r in json.load(open("data/snmp/requests.json")):
        print("== snmp %s" % r["name"])
        try:
            msg, tail = ber_dec.decode(bytes.fromhex(r["hex"]), asn1Spec=CLASSES["Message"]())
        except Exception as e:
            print("dropped: " + err(e))
            continue
        if tail:
            print("dropped: %d trailing bytes" % len(tail))
            continue
        if int(msg["version"]) != 1:
            print("dropped: version %s" % msg["version"].prettyPrint())
            continue
        community = msg["community"].asOctets()
        if community not in (b"public", b"private"):
            print("dropped: unknown community %r" % community)
            continue
        kind = msg["data"].getName()
        pdu = msg["data"].getComponent()
        rid = int(pdu["request-id"])
        names = [str(b["name"]) for b in pdu["variable-bindings"]]
        status, index, binds = "noError", 0, []
        if kind == "get-request":
            for oid in names:
                binds.append(bind(oid, *lookup(oid)))
        elif kind == "get-next-request":
            binds = [nextbind(oid) for oid in names]
        elif kind == "get-bulk-request":
            nr = min(int(pdu["non-repeaters"]), len(names))
            binds = [nextbind(oid) for oid in names[:nr]]
            cur = names[nr:]
            for _ in range(int(pdu["max-repetitions"])):
                step = [nextbind(oid) for oid in cur]
                binds.extend(step)
                cur = [b["name"] for b in step]
                if all("endOfMibView" in b[""] for b in step):
                    break
        elif kind == "set-request":
            binds = [{"name": str(b["name"]), "": nat_enc.encode(b[""])} for b in pdu["variable-bindings"]]
            if community != b"private":
                status, index = "noAccess", 1
            else:
                for i, b in enumerate(pdu["variable-bindings"]):
                    oid = str(b["name"])
                    if oid not in mib:
                        status, index = "noCreation", i + 1
                        break
                    if not mib[oid][2]:
                        status, index = "notWritable", i + 1
                        break
                    syn = b[""]["value"].getComponent()
                    if mib[oid][0] != "string" or syn.getName() != "string-value":
                        status, index = "wrongType", i + 1
                        break
                if status == "noError":
                    for b in pdu["variable-bindings"]:
                        mib[str(b["name"])][1] = str(b[""]["value"].getComponent().getComponent())
        else:
            print("dropped: %s is not a request" % kind)
            continue
        resp = make("Message", {"version": "version-2c", "community": msg["community"].asOctets(),
                                "data": {"response": {"request-id": rid, "error-status": status,
                                                      "error-index": index, "variable-bindings": binds}}})
        out = ber_enc.encode(resp)
        print("response %d bytes: %s" % (len(out), hexs(out)))
        rp = resp["data"]["response"]
        print("status %s index %d" % (rp["error-status"].prettyPrint(), rp["error-index"]))
        for b in rp["variable-bindings"]:
            print("  %s = %s" % (b["name"], bind_text(b[""])))


def ldap_norm(dn_):
    return ",".join(p.strip().lower() for p in dn_.split(","))


def attr_get(entry, name):
    for k, v in entry["attrs"].items():
        if k.lower() == name.lower():
            return v
    return None


def match(entry, f):
    kind = f.getName()
    v = f.getComponent()
    if kind == "and":
        return all(match(entry, x) for x in v)
    if kind == "or":
        return any(match(entry, x) for x in v)
    if kind == "not":
        return not match(entry, v)
    if kind == "present":
        name = str(v)
        return name.lower() == "objectclass" or attr_get(entry, name) is not None
    if kind == "substrings":
        vals = attr_get(entry, str(v["type"])) or []
        for val in vals:
            s, pos, ok = val.lower(), 0, True
            for part in v["substrings"]:
                p = str(part.getComponent()).lower()
                which = part.getName()
                if which == "initial":
                    ok = s.startswith(p)
                    pos = len(p)
                elif which == "any":
                    i = s.find(p, pos)
                    ok = i >= 0
                    pos = i + len(p)
                else:
                    ok = s.endswith(p) and len(s) - len(p) >= pos
                if not ok:
                    break
            if ok:
                return True
        return False
    vals = attr_get(entry, str(v["attributeDesc"])) or []
    want = str(v["assertionValue"]).lower()
    if kind == "equalityMatch":
        return any(x.lower() == want for x in vals)
    if kind == "greaterOrEqual":
        return any(x.lower() >= want for x in vals)
    return any(x.lower() <= want for x in vals)


def ldap_reply(mid, op, body):
    out = ber_enc.encode(make("LDAPMessage", {"messageID": mid, "protocolOp": {op: body}}))
    print("  -> %s %s" % (op, hexs(out)))


def result(code, matched="", msg=""):
    return {"resultCode": code, "matchedDN": matched, "diagnosticMessage": msg}


def prog_ldap():
    directory = json.load(open("data/ldap/directory.json"))
    for sess in json.load(open("data/ldap/sessions.json")):
        print("== ldap %s" % sess["name"])
        bound = None
        for raw in sess["msgs"]:
            try:
                m, tail = ber_dec.decode(bytes.fromhex(raw), asn1Spec=CLASSES["LDAPMessage"]())
            except Exception as e:
                print("<- undecodable: %s" % type(e).__name__)
                print("  -> notice of disconnection")
                break
            mid = int(m["messageID"])
            op = m["protocolOp"].getName()
            body = m["protocolOp"].getComponent()
            if m["controls"].isValue:
                for c in m["controls"]:
                    print("<- control %s critical=%s" % (c["controlType"], bool(c["criticality"])))
            if op == "bindRequest":
                name = str(body["name"])
                auth = body["authentication"]
                print("<- %d bind %r %s" % (mid, name, auth.getName()))
                if int(body["version"]) != 3:
                    ldap_reply(mid, "bindResponse", result("protocolError", "", "only LDAPv3 is supported"))
                elif auth.getName() != "simple":
                    ldap_reply(mid, "bindResponse", result("authMethodNotSupported", "",
                                                           "SASL %s is not supported" % auth["sasl"]["mechanism"]))
                elif name == "" and auth["simple"].asOctets() == b"":
                    bound = ""
                    ldap_reply(mid, "bindResponse", result("success"))
                else:
                    entry = [e for e in directory if ldap_norm(e["dn"]) == ldap_norm(name)]
                    pw = attr_get(entry[0], "userPassword") if entry else None
                    if pw and str(auth["simple"]) in pw:
                        bound = entry[0]["dn"]
                        ldap_reply(mid, "bindResponse", result("success"))
                    else:
                        ldap_reply(mid, "bindResponse", result("invalidCredentials"))
            elif op == "searchRequest":
                base = ldap_norm(str(body["baseObject"]))
                scope = body["scope"].prettyPrint()
                attrs = [str(a) for a in body["attributes"]]
                print("<- %d search %r %s attrs=%s" % (mid, str(body["baseObject"]), scope, ",".join(attrs)))
                if bound is None:
                    ldap_reply(mid, "searchResDone", result("operationsError", "", "bind first"))
                    continue
                if not any(ldap_norm(e["dn"]) == base for e in directory):
                    matched = base
                    while matched and not any(ldap_norm(e["dn"]) == matched for e in directory):
                        matched = matched.split(",", 1)[1] if "," in matched else ""
                    ldap_reply(mid, "searchResDone", result("noSuchObject", matched))
                    continue
                sent, code = 0, "success"
                for e in directory:
                    d = ldap_norm(e["dn"])
                    if scope == "baseObject":
                        inside = d == base
                    elif scope == "singleLevel":
                        inside = "," in d and d.split(",", 1)[1] == base
                    else:
                        inside = d == base or d.endswith("," + base)
                    if not inside or not match(e, body["filter"]):
                        continue
                    if int(body["sizeLimit"]) and sent == int(body["sizeLimit"]):
                        code = "sizeLimitExceeded"
                        break
                    pas = []
                    for k, vals in e["attrs"].items():
                        if k == "userPassword":
                            continue
                        if attrs and k.lower() not in [a.lower() for a in attrs]:
                            continue
                        pas.append({"type": k, "vals": [] if bool(body["typesOnly"]) else vals})
                    ldap_reply(mid, "searchResEntry", {"objectName": e["dn"], "attributes": pas})
                    sent += 1
                ldap_reply(mid, "searchResDone", result(code))
            elif op == "unbindRequest":
                print("<- %d unbind" % mid)
                break
            else:
                print("<- %d unexpected %s" % (mid, op))
                ldap_reply(mid, "searchResDone", result("protocolError"))


if __name__ == "__main__":
    run_jobs()
    prog_certinfo()
    prog_csr()
    prog_snmp()
    prog_ldap()
