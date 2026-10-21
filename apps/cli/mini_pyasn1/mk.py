# Writes data/: the ASN.1 modules (schemas.json), the job list
# (jobs.json) and the inputs of the four programs. Binary inputs are
# made here with pyasn1's own encoders, the way a peer would send them.
import base64
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from schemas import DEFS  # noqa: E402

if os.path.isdir("data"):
    shutil.rmtree("data")
os.makedirs("data")


def write(path, text):
    os.makedirs(os.path.dirname(os.path.join("data", path)) or "data", exist_ok=True)
    with open(os.path.join("data", path), "w") as f:
        f.write(text)


write("schemas.json", json.dumps(DEFS, indent=1) + "\n")

J = []


def job(op, label, **kw):
    kw["op"] = op
    kw["id"] = label
    J.append(kw)


def H(s):
    return {"hex": s}


# ---- making values (the native decoder) and printing them ----------------
makes = [
    ("int", "Integer", 42), ("int-neg", "Integer", -129), ("int-big", "Integer", 2 ** 130 + 7),
    ("int-str", "Integer", "17"), ("int-bad", "Integer", "seventeen"),
    ("int-named", "Version", "v3"), ("int-named-num", "Version", 1), ("int-named-out", "Version", 7),
    ("int-named-bad", "Version", "v4"),
    ("bool-t", "Boolean", True), ("bool-f", "Boolean", False), ("bool-2", "Boolean", 2),
    ("bool-name", "Boolean", "True"),
    ("enum", "Colour", "green"), ("enum-num", "Colour", 2), ("enum-bad", "Colour", "purple"),
    ("pct", "Percent", 99), ("pct-hi", "Percent", 101), ("pct-neg", "Percent", -1),
    ("port-low", "Port", 22), ("port-alt", "Port", 8443), ("port-bad", "Port", 3000),
    ("nz", "NotZero", 5), ("nz-zero", "NotZero", 0),
    ("i32-max", "Integer32", 2147483647), ("i32-over", "Integer32", 2147483648),
    ("c64", "Counter64", 18446744073709551615), ("c64-over", "Counter64", 18446744073709551616),
    ("bits", "BitString", "101101"), ("bits-0b", "BitString", "0b1110"), ("bits-0x", "BitString", "0xA5"),
    ("bits-quote-b", "BitString", "'10011'B"), ("bits-quote-h", "BitString", "'7F'H"),
    ("bits-quote-bad", "BitString", "'7F'X"),
    ("bits-empty", "BitString", ""), ("bits-ctor-list", "BitString", {"ctor": [1, 0, 1, 1]}),
    ("bits-ctor-hex", "BitString", {"ctor": "0xA5"}), ("bits-ctor-quote", "BitString", {"ctor": "'10011'B"}),
    ("bits-ctor-quote-h", "BitString", {"ctor": "'7F'H"}), ("bits-ctor-bad", "BitString", {"ctor": "'7F'X"}),
    ("flags-ctor", "Flags", {"ctor": "urgent, deleted"}), ("flags-ctor-bad", "Flags", {"ctor": "urgent, lost"}), ("bits-badbin", "BitString", "10201"),
    ("bits-badhex", "BitString", "0xZZ"),
    ("flags", "Flags", "urgent, deleted"), ("flags-one", "Flags", "active"),
    ("flags-bad", "Flags", "urgent, lost"), ("flags-digits", "Flags", "101"),
    ("keyusage", "KeyUsage", "digitalSignature, keyCertSign, cRLSign"),
    ("octets-text", "OctetString", "hello"), ("octets-bin", "OctetString", H("00ff10")),
    ("octets-latin1", "OctetString", "café"), ("octets-wide", "OctetString", "€5"),
    ("octets-list", "OctetString", [104, 105]),
    ("null", "Null", None), ("null-empty", "Null", ""), ("null-text", "Null", "x"),
    ("oid", "ObjectIdentifier", "1.2.840.113549.1.1.11"), ("oid-list", "ObjectIdentifier", [2, 5, 4, 3]),
    ("oid-uuid", "ObjectIdentifier", "2.25.329800735698586629295641978511506172918"),
    ("oid-dash", "ObjectIdentifier", "1.2.-3"), ("oid-bad", "ObjectIdentifier", "1.two.3"),
    ("oid-neg", "ObjectIdentifier", [1, -2, 3]), ("oid-dots", "ObjectIdentifier", "1..3."),
    ("reloid", "RelativeOID", "8571.3.2"), ("reloid-bad", "RelativeOID", "8571.x"),
    ("real-dec", "Real", {"float": "3.25"}), ("real-int", "Real", 1000), ("real-zero", "Real", 0),
    ("real-half", "Real", {"float": "-0.5"}), ("real-inf", "Real", {"float": "inf"}),
    ("real-ninf", "Real", {"float": "-inf"}), ("real-b2", "Real", {"tuple": [3, 2, -4]}),
    ("real-b10", "Real", {"tuple": [1200, 10, -1]}), ("real-b3", "Real", {"tuple": [1, 3, 2]}),
    ("real-str", "Real", "2.5"), ("real-badstr", "Real", "two"),
    ("utf8", "UTF8String", "naïve ✓"), ("utf8-emoji", "UTF8String", "\U0001f600"),
    ("printable", "PrintableString", "Hello World"), ("printable-hi", "PrintableString", "café"),
    ("ia5", "IA5String", "user@example.org"), ("bmp", "BMPString", "日本"),
    ("universal", "UniversalString", "Aé\U0001f600"), ("teletex", "TeletexString", "År"),
    ("t61", "T61String", "ok"), ("visible", "VisibleString", "x-y"), ("iso646", "ISO646String", "z"),
    ("general", "GeneralString", "gen"), ("graphic", "GraphicString", "gr"),
    ("videotex", "VideotexString", "vt"), ("numeric", "NumericString", "0123 456"),
    ("digits", "Digits", "2024"), ("digits-long", "Digits", "123456789"), ("digits-alpha", "Digits", "12a4"),
    ("country", "X520countryName", "NZ"), ("country-bad", "X520countryName", "NZL"),
    ("objdesc", "ObjectDescriptor", "a descriptor"),
    ("utctime", "UTCTime", "240229235959Z"), ("gentime", "GeneralizedTime", "20240229235959.25Z"),
    ("seq", "Point", {"x": 3, "y": -4}), ("seq-label", "Point", {"x": 1, "y": 2, "label": "home"}),
    ("seq-missing", "Point", {"x": 1}), ("seq-extra", "Point", {"x": 1, "y": 2, "z": 3}),
    ("seq-badfield", "Point", {"x": "one", "y": 2}),
    ("choice", "Shape", {"point": {"x": 0, "y": 0}}),
    ("choice-circle", "Shape", {"circle": {"centre": {"x": 5, "y": 5}, "radius": 2}}),
    ("choice-poly", "Shape", {"polygon": [{"x": 0, "y": 0}, {"x": 4, "y": 0}, {"x": 0, "y": 3}]}),
    ("choice-none", "Shape", {"square": 1}),
    ("set", "Record", {"id": 7, "name": "seven", "tags": ["b", "a"], "colour": "blue"}),
    ("set-default", "Record", {"id": 8, "name": "eight", "active": False}),
    ("seqof", {"t": "SequenceOf", "of": "Integer"}, [3, 1, 2]),
    ("seqof-empty", {"t": "SequenceOf", "of": "Integer"}, []),
    ("setof", {"t": "SetOf", "of": "OctetString"}, ["b", "a", "ccc"]),
    ("rdn", "RelativeDistinguishedName", [{"type": "2.5.4.3", "value": H("0c034a6f65")}]),
    ("any", "Any", H("020105")),
    ("ext", "Extension", {"extnID": "2.5.29.19", "extnValue": H("30030101ff")}),
    ("varbind", "VarBind", {"name": "1.3.6.1.2.1.1.3.0", "": {"value": {"application-wide": {"timeticks-value": 123456}}}}),
    ("ip", "IpAddress", H("c0a80001")), ("ip-short", "IpAddress", H("c0a800")),
    ("ldap-bind", "LDAPMessage", {"messageID": 1, "protocolOp": {"bindRequest": {
        "version": 3, "name": "cn=admin,dc=example,dc=org", "authentication": {"simple": "secret"}}}}),
    ("ldap-version", "BindRequest", {"version": 200, "name": "", "authentication": {"simple": ""}}),
]
for label, t, v in makes:
    job("make", label, t=t, v=v)

# ---- reprs and type printing ---------------------------------------------
for label, t in [("Integer", "Integer"), ("Version", "Version"), ("Percent", "Percent"),
                 ("Port", "Port"), ("NotZero", "NotZero"), ("Digits", "Digits"),
                 ("Null", "Null"), ("Any", "Any"), ("Flags", "Flags"), ("Counter32", "Counter32"),
                 ("tagged", {"t": "Integer", "impl": ["context", 5]}),
                 ("explicit", {"t": "OctetString", "expl": ["application", 9]}),
                 ("double", {"t": "Integer", "impl": ["context", 1], "expl": ["context", 2]}),
                 ("sub-named", {"t": "Integer", "named": [["one", 1], ["two", 2]]}),
                 ("sub-cons", {"t": "Percent", "sub": [{"range": [10, 20]}]}),
                 ("seqof", {"t": "SequenceOf", "of": "Integer"}),
                 ("seqof-size", {"t": "SequenceOf", "of": "Integer", "size": [{"size": [1, 3]}]}),
                 ("validity", "Validity"), ("point", "Point"),
                 ("time", "Time"), ("long-named", "ResultCode")]:
    job("repr", label, t=t)
job("repr", "value-long", t="OctetString", v="a fairly long octet string value to trim")
job("repr", "value-int", t="Percent", v=55)
job("repr", "value-point", t="Point", v={"x": 1, "y": 2})
job("repr", "value-bits", t="Flags", v={"ctor": "urgent"})
for t in ["Integer", "Version", "Point", "Shape", "Record", "Certificate",
          "LDAPMessage", "Name", "VarBind"]:
    job("ptype", t, t=t)

# ---- BIT STRING and OID operations --------------------------------------
for label, v in [("b1", "1011001"), ("b2", "0x0F0"), ("b3", "'1'B"), ("b4", "")]:
    job("bits", label, v=v)
job("bits", "flags", v="urgent, deleted", t="Flags")
for a, b in [("1.3.6.1", "1.3.6.1.2.1"), ("1.3.6.1.2.1", "1.3.6.1"), ("1.3.6", "1.3.7.1"),
             ("2.5.4", "2.5.4")]:
    job("oid", a + " " + b, a=a, b=b)
for t, v in [("UTCTime", "240229235959Z"), ("UTCTime", "9912312359Z"), ("UTCTime", "240101120000+0530"),
             ("UTCTime", "240101120000-08"), ("GeneralizedTime", "20240229235959.250Z"),
             ("GeneralizedTime", "2024022923Z"), ("GeneralizedTime", "202402292359-0130"),
             ("GeneralizedTime", "20240229235959,5+02"), ("GeneralizedTime", "20241301000000Z"),
             ("GeneralizedTime", "20240101000000.xZ"), ("UTCTime", "2401011200+5")]:
    job("time", t + " " + v, t=t, v=v)

# ---- encoding ------------------------------------------------------------
encs = [
    ("Integer", 0), ("Integer", 127), ("Integer", 128), ("Integer", -128), ("Integer", -129),
    ("Integer", 256), ("Integer", 2 ** 64), ("Integer", -(2 ** 64)), ("Integer", 2 ** 130 + 7),
    ("Boolean", True), ("Boolean", False), ("Colour", "blue"),
    ("BitString", ""), ("BitString", "1"), ("BitString", "10110"), ("BitString", {"ctor": "0xABCD"}),
    ("BitString", "1" * 70), ("Flags", {"ctor": "urgent, deleted"}), ("KeyUsage", {"ctor": "keyCertSign, cRLSign"}),
    ("KeyUsage", {"ctor": "digitalSignature"}), ("ReasonFlags", {"ctor": "aACompromise"}),
    ("OctetString", ""), ("OctetString", "hello world"), ("OctetString", H("00" * 200)),
    ("Null", None), ("ObjectIdentifier", "1.2.840.113549.1.1.11"),
    ("ObjectIdentifier", "2.5.4.3"), ("ObjectIdentifier", "2.999.3"), ("ObjectIdentifier", "0.39"),
    ("ObjectIdentifier", "1.40"), ("ObjectIdentifier", "3.1"), ("ObjectIdentifier", "1"),
    ("ObjectIdentifier", "2.25.329800735698586629295641978511506172918"),
    ("RelativeOID", "8571.3.2"), ("Real", 0), ("Real", {"float": "3.25"}), ("Real", 1000),
    ("Real", {"float": "-0.5"}), ("Real", {"float": "inf"}), ("Real", {"float": "-inf"}),
    ("Real", {"tuple": [3, 2, -4]}), ("Real", {"tuple": [-5, 2, 300]}), ("Real", {"tuple": [1, 2, 0]}),
    ("Real", {"tuple": [24, 2, -1]}), ("Real", {"tuple": [255, 2, 1000]}), ("Real", {"tuple": [1, 2, -129]}),
    ("UTF8String", "naïve ✓"), ("BMPString", "日本"), ("UniversalString", "A\U0001f600"),
    ("PrintableString", "Hello"), ("IA5String", "a@b.c"), ("T61String", "t61"),
    ("ISO646String", "iso"), ("NumericString", "12 34"),
    ("UTCTime", "240229235959Z"), ("GeneralizedTime", "20240229235959Z"),
    ("GeneralizedTime", "20240229235959.500Z"), ("GeneralizedTime", "20240229235959.000Z"),
    ("GeneralizedTime", "20240229235959.120Z"), ("GeneralizedTime", "20240229235959+0100"),
    ("GeneralizedTime", "20240229235959,5Z"), ("GeneralizedTime", "202402292359Z"),
    ("GeneralizedTime", "20240229235959"), ("UTCTime", "2402292359Z"), ("UTCTime", "24022923Z"),
    ("Point", {"x": 3, "y": -4}), ("Point", {"x": 1, "y": 2, "label": "home"}), ("Point", {"x": 1}),
    ("Shape", {"point": {"x": 0, "y": 0}}), ("Shape", {}),
    ("Shape", {"circle": {"centre": {"x": 5, "y": 5}, "radius": 2}}),
    ("Shape", {"polygon": [{"x": 0, "y": 0}, {"x": 4, "y": 0}, {"x": 0, "y": 3}]}),
    ("Record", {"id": 7, "name": "seven", "tags": ["b", "a", "ab"], "colour": "blue"}),
    ("Record", {"id": 8, "name": "eight", "active": False}),
    ("Record", {"id": 9, "name": "nine", "active": True}),
    ({"t": "SequenceOf", "of": "Integer"}, [3, 1, 2]), ({"t": "SequenceOf", "of": "Integer"}, []),
    ({"t": "SetOf", "of": "Integer"}, [300, 2, 1, 256]),
    ({"t": "SetOf", "of": "OctetString"}, ["b", "a", "ccc", ""]),
    ({"t": "SetOf", "of": "OctetString", "impl": ["context", 4]}, ["zz", "y"]),
    ({"t": "SequenceOf", "of": "Integer", "size": [{"size": [1, 2]}]}, [1, 2, 3]),
    ({"t": "SequenceOf", "of": "Integer", "size": [{"size": [1, 2]}]}, [1]),
    ("Extension", {"extnID": "2.5.29.19", "critical": True, "extnValue": H("30030101ff")}),
    ("Extension", {"extnID": "2.5.29.15", "critical": False, "extnValue": H("03020186")}),
    ("BasicConstraints", {"cA": True, "pathLenConstraint": 0}), ("BasicConstraints", {}),
    ("AlgorithmIdentifier", {"algorithm": "1.2.840.113549.1.1.11", "parameters": H("0500")}),
    ("AlgorithmIdentifier", {"algorithm": "1.2.840.10045.4.3.2"}),
    ({"t": "Integer", "impl": ["context", 5]}, 5), ({"t": "Integer", "expl": ["context", 5]}, 5),
    ({"t": "Integer", "impl": ["context", 31]}, 1), ({"t": "Integer", "impl": ["private", 1000]}, 1),
    ({"t": "Integer", "impl": ["application", 200000]}, 1),
    ({"t": "Integer", "impl": ["context", 1], "expl": ["context", 2]}, 1),
    ({"t": "OctetString", "expl": ["application", 9]}, "x"),
    ({"t": "Point", "expl": ["context", 0]}, {"x": 1, "y": 1}),
    ("Any", H("020105")), ({"t": "Any", "expl": ["context", 1]}, H("020105")),
    ("VarBind", {"name": "1.3.6.1.2.1.1.3.0", "": {"value": {"application-wide": {"timeticks-value": 123456}}}}),
    ("VarBind", {"name": "1.3.6.1.2.1.1.9.0", "": {"noSuchInstance": None}}),
    ("Message", {"version": "version-2c", "community": "public", "data": {"get-request": {
        "request-id": 1, "error-status": 0, "error-index": 0, "variable-bindings": [
            {"name": "1.3.6.1.2.1.1.1.0", "": {"unSpecified": None}}]}}}),
    ("LDAPMessage", {"messageID": 1, "protocolOp": {"bindRequest": {
        "version": 3, "name": "cn=admin,dc=example,dc=org", "authentication": {"simple": "secret"}}}}),
    ("LDAPMessage", {"messageID": 2, "protocolOp": {"unbindRequest": None}}),
    ("LDAPMessage", {"messageID": 3, "protocolOp": {"bindResponse": {
        "resultCode": "success", "matchedDN": "", "diagnosticMessage": ""}},
        "controls": [{"controlType": "1.2.840.113556.1.4.319", "controlValue": H("3005020100 0400".replace(" ", ""))}]}),
]
CODECS = ["ber", "cer", "der"]
for i, (t, v) in enumerate(encs):
    for c in CODECS:
        job("enc", "e%d-%s" % (i, c), t=t, v=v, codec=c)
long_text = "Kara " * 210
for t, v in [("OctetString", "abcdefghij"), ("BitString", "1" * 40 + "0" * 9), ("UTF8String", "ascii only"),
             ("IA5String", "chunky"), ("OctetString", "abcd")]:
    job("enc", "chunk4 " + t, t=t, v=v, codec="ber", opts={"maxChunkSize": 4})
    job("enc", "chunk4-indef " + t, t=t, v=v, codec="ber", opts={"maxChunkSize": 4, "defMode": False})
for t, v in [("OctetString", long_text), ("UTF8String", long_text), ("BitString", "10" * 4100),
             ("GeneralizedTime", "20240229235959Z")]:
    for c in CODECS:
        job("enc", "long %s %s" % (t, c), t=t, v=v, codec=c)
for t, v in [("Point", {"x": 3, "y": -4}), ("Record", {"id": 7, "name": "seven", "tags": ["b"]}),
             ("Shape", {"polygon": [{"x": 0, "y": 0}]}), ("Integer", 5), ("OctetString", "abc"),
             ({"t": "Integer", "expl": ["context", 5]}, 5), ("Any", H("020105")),
             ({"t": "Any", "expl": ["context", 1]}, H("020105")), ("Null", None)]:
    job("enc", "indef %s" % json.dumps(t), t=t, v=v, codec="ber", opts={"defMode": False})
for t, v in [("Point", {"x": 3, "y": -4}), ("Shape", {"point": {"x": 0, "y": 0}}),
             ("Record", {"id": 7, "name": "seven", "tags": ["b", "a"]}), ("Integer", 5),
             ("BitString", "1011"), ("OctetString", "abc"), ("ObjectIdentifier", "1.2.3"),
             ("Real", 1000), ("Any", H("020105")), ("Extension", {"extnID": "2.5.29.19", "extnValue": H("3000")})]:
    for c in CODECS:
        job("enc", "spec %s %s" % (json.dumps(t), c), t=t, v=v, codec=c, spec=True)
job("enc", "omit-empty", t="LDAPMessage", v={"messageID": 4, "protocolOp": {"unbindRequest": None}, "controls": []},
    codec="ber")
job("enc", "omit-empty-cer", t="LDAPMessage", v={"messageID": 4, "protocolOp": {"unbindRequest": None}, "controls": []},
    codec="cer")
job("enc", "omit-empty-opt", t="LDAPMessage", v={"messageID": 4, "protocolOp": {"unbindRequest": None}, "controls": []},
    codec="ber", opts={"omitEmptyOptionals": True})

# ---- decoding ------------------------------------------------------------
decs = [
    ("020100", None), ("0201ff", None), ("02020080", None), ("020900ffffffffffffffff", None),
    ("0200", None), ("02810105", None), ("0283000001 05".replace(" ", ""), None), ("0101ff", None),
    ("010100", None), ("010101", None), ("01020000", None), ("0a0102", None),
    ("030100", None), ("0303066e5c", None), ("0300", None), ("030108", None),
    ("23 80 0303000a3b 030204f0 0000", None), ("2309 0303000a3b 030204f0", None),
    ("0403616263", None), ("2480 0403616263 04026465 0000", None),
    ("240b 0403616263 2404 04026465", None), ("0500", None), ("050101", None),
    ("06062a864886f70d", None), ("0603550403", None), ("06028837", None), ("0600", None),
    ("06028001", None), ("060188", None), ("060169", None),
    ("0d03c21b03", None), ("090380fd01", None), ("090403314532", None), ("0900", None),
    ("090140", None), ("090141", None), ("0901 80", None), ("0902 0100", None),
    ("090783ff00000001ff".replace(" ", ""), None), ("0904 1331452b", None), ("0903 0331a2", None),
    ("0902 c001", None), ("0903 a0 0101", None),
    ("0c06c3a9746521", None), ("0c01ff", None), ("1e04 65e5 672c", None), ("1c08 00000041 0001f600", None),
    ("1c03 000000", None), ("13026869", None), ("130180", None), ("1603612e62", None), ("170d3234303232393233353935395a", None),
    ("180f32303234303232393233353935395a", None), ("12023132", None), ("14 02 c5 72", None),
    ("3006 020101 020102", None), ("3006 020101 0c0161", None), ("3000", None),
    ("3080 020101 020102 0000", None), ("3180 020101 0101ff 0000", None), ("3106 020101 020102", None),
    ("a003020105", None), ("bf810103020105", None), ("8001ff", None), ("4100", None),
    ("6080 020101 0000", None), ("1f8101 0105", None),
    ("02050102", None), ("0284", None), ("02", None), ("", None),
    ("0201050201", None), ("020105 0000 ff", None), ("3004 020101 0000", None),
    ("3082000a 020101 020102 020103 0000", None),
    # with a schema
    ("3006020103020104", "Point"), ("300c02010302010c040468 6f6d65", "Point"),
    ("300c0201030201040c04686f6d65", "Point"), ("3003020103", "Point"),
    ("30090201030201040201ff", "Point"), ("3080 020103 020104 0000", "Point"),
    ("30800201030201040c80", "Point"), ("a0060201000201 00", "Shape"),
    ("a0060201000201000000", "Shape"),
    ("a10b 3006020105020105 020102", "Shape"), ("a2 08 3006020100020100", "Shape"),
    ("a3 00", "Shape"), ("3006020100020100", "Shape"),
    ("31 0e 020107 8005736576656e 0a0102 0101ff".replace(" ", ""), "Record"),
    ("31 0b 0a0102 8005736576656e 020107".replace(" ", ""), "Record"),
    ("31 06 8001 61 020101", "Record"), ("31 03 020107", "Record"),
    ("3108 020101 020101 020101", "Point"),
    ("020105", "Percent"), ("020165", "Percent"), ("0a0101", "Colour"), ("0a0107", "Colour"),
    ("0101ff", "Boolean"), ("010101", "Boolean"), ("02010a", "Boolean"),
    ("030207 80", "Flags"), ("0302 0390", "KeyUsage"), ("0403 616263", "OctetString"),
    ("2480 0403616263 0000", "OctetString"), ("0c03 616263", "OctetString"),
    ("0403 616263", "UTF8String"), ("0c03 616263", "UTF8String"),
    ("0500", "Null"), ("0403 616263", "Any"), ("a003020105", "Any"),
    ("a003020105", {"t": "Any", "expl": ["context", 0]}), ("a0 80 020105 0000", {"t": "Any", "expl": ["context", 0]}),
    ("a0 80 020105 0000", "Any"), ("8501 05", {"t": "Integer", "impl": ["context", 5]}),
    ("a503 020105", {"t": "Integer", "expl": ["context", 5]}), ("a503 020105", {"t": "Integer", "impl": ["context", 5]}),
    ("020105", {"t": "Integer", "expl": ["context", 5]}),
    ("3009 020101 020102 020103", {"t": "SequenceOf", "of": "Integer"}),
    ("3009 020101 020102 020103", {"t": "SequenceOf", "of": "Integer", "size": [{"size": [1, 2]}]}),
    ("3003 0c0161", {"t": "SequenceOf", "of": "Integer"}),
    ("3080 020101 0000", {"t": "SequenceOf", "of": "Integer"}),
    ("310a 040162 040161 0403636363", {"t": "SetOf", "of": "OctetString"}),
    ("0406c0a80001ff", "IpAddress"), ("4004c0a80001", "IpAddress"), ("4003c0a800", "IpAddress"),
    ("4304 0001e240", "TimeTicks"), ("4609 00ffffffffffffffff", "Counter64"),
    ("300b 0603 2b0601 4304 0001e240", "VarBind"), ("3007 0603 2b0601 8100", "VarBind"),
    ("3007 0603 2b0601 0500", "VarBind"), ("3008 0603 2b0601 0401 41", "VarBind"),
    ("3007 0603 2b0601 8800", "VarBind"),
    ("3009 060355 1d13 0402 3000", "Extension"), ("300c 0603551d13 0101ff 04023000", "Extension"),
    ("300c 0603551d13 010100 04023000", "Extension"),
    ("3000", "BasicConstraints"), ("3006 0101ff 020100", "BasicConstraints"), ("3003 020105", "BasicConstraints"),
    ("300d06092a864886f70d01010b0500", "AlgorithmIdentifier"), ("300a06082a8648ce3d040302", "AlgorithmIdentifier"),
    ("3013 06072a8648ce3d0201 06082a8648ce3d030107", "AlgorithmIdentifier"),
    ("3006 0201 07 0201 08", {"t": "Envelope"}),
    ("0101ff", "ProtocolOp"), ("4200", "ProtocolOp"), ("4200", "LDAPMessage"),
    ("3005 020102 4200", "LDAPMessage"),
]
for i, (h, t) in enumerate(decs):
    h = h.replace(" ", "")
    for c in CODECS:
        if t is None or c == "ber":
            job("dec", "d%d-%s" % (i, c), hex=h, codec=c, t=t)
        else:
            job("dec", "d%d-%s" % (i, c), hex=h, codec=c, t=t)
job("dec", "open-types", hex="3013 06072a8648ce3d0201 06082a8648ce3d030107".replace(" ", ""), codec="der",
    t="AlgorithmIdentifier", opts={"decodeOpenTypes": True})
job("dec", "open-types-rsa", hex="300d06092a864886f70d0101010500", codec="der",
    t="AlgorithmIdentifier", opts={"decodeOpenTypes": True})
job("dec", "open-types-unknown", hex="300d06092a864886f70d0101020500", codec="der",
    t="AlgorithmIdentifier", opts={"decodeOpenTypes": True})
job("dec", "open-types-attr", hex="300a0603550403 0c034a6f65".replace(" ", ""), codec="der",
    t="AttributeTypeAndValue", opts={"decodeOpenTypes": True})
job("dec", "open-types-attr-c", hex="30090603550406 13024e5a".replace(" ", ""), codec="der",
    t="AttributeTypeAndValue", opts={"decodeOpenTypes": True})
job("dec", "open-types-attr-bad", hex="300a0603550406 13034e5a4c".replace(" ", ""), codec="der",
    t="AttributeTypeAndValue", opts={"decodeOpenTypes": True})
job("dec", "open-types-off", hex="300a0603550403 0c034a6f65".replace(" ", ""), codec="der",
    t="AttributeTypeAndValue")

# ---- round trips ---------------------------------------------------------
for t, v in [("Point", {"x": 300, "y": -70000, "label": "été"}),
             ("Record", {"id": 1, "name": "one", "tags": ["x", "yy", "a"], "active": False, "colour": "red"}),
             ("Shape", {"circle": {"centre": {"x": -1, "y": 1}, "radius": 1000000}}),
             ("Message", {"version": "version-2c", "community": "private", "data": {"set-request": {
                 "request-id": 99, "error-status": 0, "error-index": 0, "variable-bindings": [
                     {"name": "1.3.6.1.2.1.1.5.0", "": {"value": {"simple": {"string-value": "router-1"}}}},
                     {"name": "1.3.6.1.2.1.1.7.0", "": {"value": {"simple": {"integer-value": 72}}}}]}}}),
             ("LDAPMessage", {"messageID": 9, "protocolOp": {"searchRequest": {
                 "baseObject": "dc=example,dc=org", "scope": "wholeSubtree", "derefAliases": "neverDerefAliases",
                 "sizeLimit": 0, "timeLimit": 30, "typesOnly": False,
                 "filter": {"and": [{"equalityMatch": {"attributeDesc": "objectClass", "assertionValue": "person"}},
                                    {"present": "mail"}]},
                 "attributes": ["cn", "mail"]}}}),
             ("BasicConstraints", {"cA": True, "pathLenConstraint": 3}),
             ("Real", {"tuple": [-7, 2, -10]}),
             ("GeneralizedTime", "20240229235959.5Z")]:
    job("rt", json.dumps(t), t=t, v=v)

write("jobs.json", json.dumps(J, indent=0) + "\n")

# ---- program inputs -------------------------------------------------------
CERTS = ["ISRG_Root_X1", "ISRG_Root_X2", "Amazon_Root_CA_3", "Entrust_Root_Certification_Authority",
         "D-TRUST_Root_Class_3_CA_2_2009", "GlobalSign_Root_CA_-_R3", "SecureSign_Root_CA12",
         "ACCVRAIZ1", "Atos_TrustedRoot_2011", "Certigna_Root_CA", "Izenpe.com"]
for name in CERTS:
    write("certs/%s.pem" % name, open("/etc/ssl/certs/%s.pem" % name).read())

import oracle  # noqa: E402  (reads data/schemas.json, written above)

# A made-up 1024-bit modulus: the CSR tool only lays the key out, it
# never does arithmetic with it.
MOD = "c3" + "".join("%02x" % ((i * 37 + 11) % 256) for i in range(127))
write("csr/web.json", json.dumps({
    "subject": [["2.5.4.6", "NZ"], ["2.5.4.8", "Canterbury"], ["2.5.4.7", "Ōtautahi"],
                ["2.5.4.10", "Example Ltd"], ["2.5.4.3", "www.example.nz"]],
    "dns": ["www.example.nz", "example.nz", "api.example.nz"],
    "modulus": MOD, "exponent": 65537, "signature": "00" * 8}, indent=1) + "\n")
write("csr/mail.json", json.dumps({
    "subject": [["2.5.4.3", "mail"], ["1.2.840.113549.1.9.1", "postmaster@example.org"],
                ["0.9.2342.19200300.100.1.25", "example"], ["0.9.2342.19200300.100.1.25", "org"]],
    "dns": ["mail.example.org"],
    "modulus": MOD[::-1], "exponent": 3, "signature": "5a" * 4}, indent=1) + "\n")
write("csr/bad.json", json.dumps({
    "subject": [["2.5.4.6", "NZL"], ["2.5.4.3", "x"]],
    "dns": [], "modulus": "01", "exponent": 3, "signature": ""}, indent=1) + "\n")

# The SNMP agent's MIB: a few system and interface objects.
MIB = [
    ["1.3.6.1.2.1.1.1.0", "string", "mini_pyasn1 agent v0.1", False],
    ["1.3.6.1.2.1.1.2.0", "oid", "1.3.6.1.4.1.8072.3.2.10", False],
    ["1.3.6.1.2.1.1.3.0", "timeticks", 123456, False],
    ["1.3.6.1.2.1.1.4.0", "string", "ops@example.org", True],
    ["1.3.6.1.2.1.1.5.0", "string", "router-1", True],
    ["1.3.6.1.2.1.1.7.0", "integer", 72, False],
    ["1.3.6.1.2.1.2.1.0", "integer", 2, False],
    ["1.3.6.1.2.1.2.2.1.2.1", "string", "lo", False],
    ["1.3.6.1.2.1.2.2.1.2.2", "string", "eth0", False],
    ["1.3.6.1.2.1.2.2.1.5.1", "gauge32", 10000000, False],
    ["1.3.6.1.2.1.2.2.1.5.2", "gauge32", 4294967295, False],
    ["1.3.6.1.2.1.2.2.1.10.1", "counter32", 3735928559, False],
    ["1.3.6.1.2.1.2.2.1.10.2", "counter32", 17, False],
    ["1.3.6.1.2.1.4.20.1.1.10.0.0.1", "ipaddress", "0a000001", False],
    ["1.3.6.1.2.1.31.1.1.1.6.2", "counter64", 18446744073709551615, False],
]
write("snmp/mib.json", json.dumps(MIB, indent=0) + "\n")


def snmp(name, pdu, body, version="version-2c", community="public"):
    m = oracle.make("Message", {"version": version, "community": community, "data": {pdu: body}})
    return {"name": name, "hex": oracle.ber_enc.encode(m).hex()}


def vb(*oids):
    return [{"name": o, "": {"unSpecified": None}} for o in oids]


def req(rid, binds):
    return {"request-id": rid, "error-status": 0, "error-index": 0, "variable-bindings": binds}


def sval(kind, v):
    return {"name": kind[0], "": {"value": {kind[1]: v}}}


SNMP = [
    snmp("get sysDescr", "get-request", req(1, vb("1.3.6.1.2.1.1.1.0"))),
    snmp("get several", "get-request", req(2, vb("1.3.6.1.2.1.1.5.0", "1.3.6.1.2.1.1.3.0",
                                                  "1.3.6.1.2.1.4.20.1.1.10.0.0.1", "1.3.6.1.2.1.1.2.0"))),
    snmp("get missing", "get-request", req(3, vb("1.3.6.1.2.1.1.9.0", "1.3.6.1.2.1.2.2.1.2.7", "1.3.6.1.2.1.1"))),
    snmp("getnext walk", "get-next-request", req(4, vb("1.3.6.1.2.1.1", "1.3.6.1.2.1.2.2.1.10.2",
                                                        "1.3.6.1.2.1.31.1.1.1.6.2"))),
    snmp("getbulk", "get-bulk-request", {"request-id": 5, "non-repeaters": 1, "max-repetitions": 3,
                                         "variable-bindings": vb("1.3.6.1.2.1.1.7", "1.3.6.1.2.1.2.2.1.2",
                                                                 "1.3.6.1.2.1.2.2.1.10")}),
    snmp("getbulk past end", "get-bulk-request", {"request-id": 6, "non-repeaters": 0, "max-repetitions": 4,
                                                  "variable-bindings": vb("1.3.6.1.2.1.31")}),
    snmp("set sysName", "set-request", req(7, [
        {"name": "1.3.6.1.2.1.1.5.0", "": {"value": {"simple": {"string-value": "core-router"}}}}]), community="private"),
    snmp("get after set", "get-request", req(8, vb("1.3.6.1.2.1.1.5.0"))),
    snmp("set read-only", "set-request", req(9, [
        {"name": "1.3.6.1.2.1.1.5.0", "": {"value": {"simple": {"string-value": "x"}}}},
        {"name": "1.3.6.1.2.1.1.7.0", "": {"value": {"simple": {"integer-value": 4}}}}]), community="private"),
    snmp("set wrong type", "set-request", req(10, [
        {"name": "1.3.6.1.2.1.1.4.0", "": {"value": {"simple": {"integer-value": 4}}}}]), community="private"),
    snmp("set missing", "set-request", req(11, [
        {"name": "1.3.6.1.2.1.1.99.0", "": {"value": {"simple": {"string-value": "x"}}}}]), community="private"),
    snmp("set public", "set-request", req(16, [
        {"name": "1.3.6.1.2.1.1.4.0", "": {"value": {"simple": {"string-value": "me"}}}}])),
    snmp("bad community", "get-request", req(12, vb("1.3.6.1.2.1.1.1.0")), community="secret"),
    snmp("version 1", "get-request", req(13, vb("1.3.6.1.2.1.1.1.0")), version="version-1"),
    snmp("not a request", "response", req(14, vb("1.3.6.1.2.1.1.1.0"))),
    snmp("private community", "get-request", req(15, vb("1.3.6.1.2.1.1.4.0")), community="private"),
]
SNMP.append({"name": "truncated", "hex": SNMP[0]["hex"][:-6]})
SNMP.append({"name": "trailing bytes", "hex": SNMP[0]["hex"] + "0500"})
SNMP.append({"name": "not snmp", "hex": "302a020101"})
SNMP.append({"name": "empty", "hex": ""})
SNMP.append({"name": "wrong inner tag", "hex": "3011020101040670756" + "26c6963a1040201010000"})
write("snmp/requests.json", json.dumps(SNMP, indent=0) + "\n")

# The LDAP server's directory.
DIR = [
    {"dn": "dc=example,dc=org", "attrs": {"objectClass": ["top", "domain"], "dc": ["example"]}},
    {"dn": "ou=people,dc=example,dc=org", "attrs": {"objectClass": ["organizationalUnit"], "ou": ["people"]}},
    {"dn": "uid=ana,ou=people,dc=example,dc=org", "attrs": {
        "objectClass": ["person", "inetOrgPerson"], "uid": ["ana"], "cn": ["Ana Silva"], "sn": ["Silva"],
        "mail": ["ana@example.org", "a.silva@example.org"], "userPassword": ["correct horse"]}},
    {"dn": "uid=bo,ou=people,dc=example,dc=org", "attrs": {
        "objectClass": ["person"], "uid": ["bo"], "cn": ["Bo Lindqvist"], "sn": ["Lindqvist"],
        "employeeNumber": ["0042"], "userPassword": ["battery staple"]}},
    {"dn": "uid=chidi,ou=people,dc=example,dc=org", "attrs": {
        "objectClass": ["person", "inetOrgPerson"], "uid": ["chidi"], "cn": ["Chidi Okafor"], "sn": ["Okafor"],
        "mail": ["chidi@example.org"], "employeeNumber": ["0107"]}},
    {"dn": "ou=groups,dc=example,dc=org", "attrs": {"objectClass": ["organizationalUnit"], "ou": ["groups"]}},
    {"dn": "cn=admins,ou=groups,dc=example,dc=org", "attrs": {
        "objectClass": ["groupOfNames"], "cn": ["admins"], "member": ["uid=ana,ou=people,dc=example,dc=org"]}},
]
write("ldap/directory.json", json.dumps(DIR, indent=1) + "\n")


def ldap(mid, op, body, controls=None):
    v = {"messageID": mid, "protocolOp": {op: body}}
    if controls is not None:
        v["controls"] = controls
    return oracle.ber_enc.encode(oracle.make("LDAPMessage", v)).hex()


def search(base, scope, flt, attrs=(), size=0, types=False):
    return {"baseObject": base, "scope": scope, "derefAliases": "neverDerefAliases", "sizeLimit": size,
            "timeLimit": 0, "typesOnly": types, "filter": flt, "attributes": list(attrs)}


EQ = lambda a, v: {"equalityMatch": {"attributeDesc": a, "assertionValue": v}}  # noqa: E731
PEOPLE = "ou=people,dc=example,dc=org"
SESSIONS = [
    {"name": "anonymous", "msgs": [
        ldap(1, "bindRequest", {"version": 3, "name": "", "authentication": {"simple": ""}}),
        ldap(2, "searchRequest", search("dc=example,dc=org", "baseObject", {"present": "objectClass"})),
        ldap(3, "searchRequest", search(PEOPLE, "singleLevel", EQ("objectClass", "PERSON"), ["cn", "mail"])),
        ldap(4, "unbindRequest", None)]},
    {"name": "ana", "msgs": [
        ldap(1, "bindRequest", {"version": 3, "name": "uid=ana,ou=people,dc=example,dc=org",
                                "authentication": {"simple": "correct horse"}}),
        ldap(2, "searchRequest", search("dc=example,dc=org", "wholeSubtree", {"and": [
            EQ("objectClass", "person"), {"present": "mail"}]}, ["uid", "mail"])),
        ldap(3, "searchRequest", search("dc=example,dc=org", "wholeSubtree", {"substrings": {
            "type": "cn", "substrings": [{"initial": "b"}, {"any": "lind"}]}}, ["cn"])),
        ldap(4, "searchRequest", search(PEOPLE, "wholeSubtree", {"or": [
            EQ("uid", "bo"), {"greaterOrEqual": {"attributeDesc": "employeeNumber", "assertionValue": "0100"}}]},
            ["uid", "employeeNumber"])),
        ldap(5, "searchRequest", search(PEOPLE, "singleLevel", {"not": {"present": "mail"}}, [], types=True)),
        ldap(6, "searchRequest", search("dc=example,dc=org", "wholeSubtree", {"present": "objectClass"},
                                        ["dn"], size=3)),
        ldap(7, "searchRequest", search("ou=nobody,dc=example,dc=org", "baseObject", {"present": "objectClass"})),
        ldap(8, "searchRequest", search("cn=admins,ou=groups,dc=example,dc=org", "baseObject",
                                        {"substrings": {"type": "member", "substrings": [{"final": "DC=ORG"}]}},
                                        ["member"]), controls=[{"controlType": "1.2.840.113556.1.4.319",
                                                                "criticality": True, "controlValue": "3006020103040"}]),
        ldap(9, "unbindRequest", None)]},
    {"name": "wrong password", "msgs": [
        ldap(1, "bindRequest", {"version": 3, "name": "uid=bo,ou=people,dc=example,dc=org",
                                "authentication": {"simple": "tr0ub4dor"}}),
        ldap(2, "bindRequest", {"version": 3, "name": "uid=nobody,ou=people,dc=example,dc=org",
                                "authentication": {"simple": "x"}}),
        ldap(3, "bindRequest", {"version": 2, "name": "uid=bo,ou=people,dc=example,dc=org",
                                "authentication": {"simple": "battery staple"}}),
        ldap(4, "bindRequest", {"version": 3, "name": "", "authentication": {"sasl": {"mechanism": "EXTERNAL"}}}),
        ldap(5, "searchRequest", search(PEOPLE, "baseObject", {"lessOrEqual": {
            "attributeDesc": "ou", "assertionValue": "people"}})),
        "300c020107" + "4207" + "616e6f6e796d",
        ldap(8, "unbindRequest", None)]},
    {"name": "no operation", "msgs": ["3005020106"]},
    {"name": "unknown operation", "msgs": ["30070201096a020500"]},
]
write("ldap/sessions.json", json.dumps(SESSIONS, indent=1) + "\n")

print("%d jobs" % len(J))
