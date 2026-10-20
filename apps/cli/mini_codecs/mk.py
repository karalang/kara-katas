# Writes data/: jobs.tsv (calls into the codecs), the codec tables the
# port reads at startup, and the files for the programs. Run it from the
# app directory.
#
# jobs.tsv, one op per line, fields split by tabs:
#   job NAME                       start a job
#   lookup NAME                    codecs.lookup(NAME).name
#   decode ENCODING ERRORS BYTES   BYTES.decode(ENCODING, ERRORS)
#   encode ENCODING ERRORS TEXT    TEXT.encode(ENCODING, ERRORS)
#   feed ENCODING ERRORS BYTES...  an incremental decoder fed each piece,
#                                  final=True on the last one
# BYTES is a Python bytes literal and TEXT a str literal.
#
# The tables come from the Python that runs this script (3.13):
#   codecs.txt    each codec module this port knows and the name its
#                 CodecInfo gives
#   aliases.txt   encodings.aliases, for those modules
#   charmaps.txt  the decoding table of each 8-bit codec
#   names.txt     unicodedata names, for the characters the jobs encode
import encodings.aliases
import importlib
import os
import unicodedata

MODULES = ["ascii", "latin_1", "utf_8", "utf_8_sig", "utf_16", "utf_16_le",
           "utf_16_be", "utf_32", "utf_32_le", "utf_32_be", "unicode_escape",
           "raw_unicode_escape", "cp1252", "cp1251", "iso8859_15", "koi8_r",
           "mac_roman", "cp437", "cp850"]
CHARMAPS = ["cp1252", "cp1251", "iso8859_15", "koi8_r", "mac_roman", "cp437", "cp850"]

jobs = []


def job(name, *ops):
    jobs.append(["job", name])
    for op in ops:
        jobs.append(list(op))


def d(enc, err, lit):
    return ("decode", enc, err, lit)


def e(enc, err, lit):
    return ("encode", enc, err, lit)


job("lookup",
    *[("lookup", n) for n in [
        "utf-8", "UTF8", "utf_8", "U8", "UTF 8", " utf-8 ", "utf--8", "utf-8.x",
        "latin1", "Latin-1", "ISO-8859-1", "l1", "8859", "iso8859_15", "ISO-8859-15",
        "latin9", "cp-1252", "windows-1252", "CP1252", "cp1251", "windows_1251",
        "KOI8-R", "koi8_r", "macroman", "mac-roman", "MacRoman", "cp437",
        "IBM437", "437", "cp850", "IBM850", "ascii", "US-ASCII", "646", "ansi_x3.4_1968",
        "utf-16", "UTF16", "utf-16le", "UTF_16_BE", "utf32", "utf-32-le",
        "utf_8_sig", "utf8-sig", "unicode-escape", "unicode_escape",
        "raw-unicode-escape", "nope", "", "utf-8é"]])

job("utf-8",
    d("utf-8", "strict", "b'caf\\xc3\\xa9 \\xe2\\x82\\xac \\xf0\\x9f\\x8e\\x89'"),
    d("utf-8", "strict", "b'\\xef\\xbb\\xbfBOM kept'"),
    d("utf-8", "strict", "b'ab\\xffcd'"),
    d("utf-8", "strict", "b'ab\\x80cd'"),
    d("utf-8", "strict", "b'\\xc0\\xaf'"),
    d("utf-8", "strict", "b'\\xc2'"),
    d("utf-8", "strict", "b'\\xe2\\x82'"),
    d("utf-8", "strict", "b'\\xe2\\x28\\xa1'"),
    d("utf-8", "strict", "b'\\xe2\\x82\\x28'"),
    d("utf-8", "strict", "b'\\xe0\\x80\\x80'"),
    d("utf-8", "strict", "b'\\xed\\xa0\\x80'"),
    d("utf-8", "strict", "b'\\xed\\xa0'"),
    d("utf-8", "strict", "b'\\xf0\\x80\\x80\\x80'"),
    d("utf-8", "strict", "b'\\xf0\\x9f\\x8e'"),
    d("utf-8", "strict", "b'\\xf0\\x9f\\x8e('"),
    d("utf-8", "strict", "b'\\xf4\\x90\\x80\\x80'"),
    d("utf-8", "strict", "b'\\xf5\\x80'"),
    d("utf-8", "replace", "b'a\\xffb\\xe2\\x82c\\xf0\\x9f\\x8e\\xe2\\x28\\xa1'"),
    d("utf-8", "ignore", "b'a\\xffb\\xe2\\x82c\\xf0\\x9f\\x8e'"),
    d("utf-8", "backslashreplace", "b'a\\xffb\\xe2\\x82c\\xf0\\x9f\\x8e'"),
    d("utf-8", "surrogateescape", "b'a\\xffb\\xe2\\x82c\\xf0\\x9f\\x8e'"),
    d("utf-8", "surrogatepass", "b'\\xed\\xa0\\x80\\xed\\xb2\\xa9x'"),
    d("utf-8", "surrogatepass", "b'\\xed\\xa0'"),
    d("utf-8", "bogus", "b'ok'"),
    d("utf-8", "bogus", "b'\\xff'"),
    d("utf-8-sig", "strict", "b'\\xef\\xbb\\xbfBOM gone'"),
    d("utf-8-sig", "strict", "b'no BOM'"),
    d("utf-8-sig", "strict", "b'\\xef\\xbb'"),
    e("utf-8", "strict", "'caf\\xe9 \\u20ac \\U0001f389'"),
    e("utf-8", "strict", "'a\\ud800b'"),
    e("utf-8", "strict", "'a\\ud800\\udc00b'"),
    e("utf-8", "replace", "'a\\ud800\\udc00b'"),
    e("utf-8", "ignore", "'a\\ud800b'"),
    e("utf-8", "backslashreplace", "'a\\ud800b'"),
    e("utf-8", "xmlcharrefreplace", "'a\\ud800b'"),
    e("utf-8", "surrogatepass", "'a\\ud800\\udfffb'"),
    e("utf-8", "surrogateescape", "'a\\udcffb\\udc80'"),
    e("utf-8", "surrogateescape", "'a\\ud800b'"),
    e("utf-8-sig", "strict", "'x'"),
    e("utf-8-sig", "strict", "''"),
    )

job("ascii and latin-1",
    d("ascii", "strict", "b'plain'"),
    d("ascii", "strict", "b'caf\\xe9'"),
    d("ascii", "replace", "b'caf\\xe9\\xe9!'"),
    d("ascii", "surrogateescape", "b'caf\\xe9'"),
    d("latin-1", "strict", "b'caf\\xe9 \\x80\\xff'"),
    e("ascii", "strict", "'na\\xefve caf\\xe9'"),
    e("ascii", "strict", "'\\u201cquoted\\u201d'"),
    e("ascii", "strict", "'x\\u2014\\u2014\\u2014y'"),
    e("ascii", "replace", "'na\\xefve \\u2014 caf\\xe9'"),
    e("ascii", "ignore", "'na\\xefve \\u2014 caf\\xe9'"),
    e("ascii", "backslashreplace", "'na\\xefve \\u2014 \\U0001f600'"),
    e("ascii", "xmlcharrefreplace", "'na\\xefve \\u2014 \\U0001f600'"),
    e("ascii", "namereplace", "'na\\xefve \\u2014 \\U0001f600'"),
    e("ascii", "surrogateescape", "'a\\udce9b'"),
    e("ascii", "surrogateescape", "'a\\udce9\\u2014b'"),
    e("latin-1", "strict", "'caf\\xe9 \\xff'"),
    e("latin-1", "strict", "'caf\\xe9 \\u20ac'"),
    e("latin-1", "xmlcharrefreplace", "'5 \\u20ac'"),
    e("latin-1", "bogus", "'5 \\u20ac'"),
    )

job("utf-16 and utf-32",
    e("utf-16", "strict", "'hi \\U0001f600'"),
    e("utf-16-le", "strict", "'hi \\U0001f600'"),
    e("utf-16-be", "strict", "'hi \\U0001f600'"),
    e("utf-16-le", "strict", "'a\\ud800b'"),
    e("utf-16-le", "surrogatepass", "'a\\ud800b'"),
    e("utf-16-le", "replace", "'a\\ud800b'"),
    e("utf-32", "strict", "'hi \\U0001f600'"),
    e("utf-32-be", "strict", "'hi'"),
    e("utf-32-le", "backslashreplace", "'a\\udfffb'"),
    d("utf-16", "strict", "b'\\xff\\xfeh\\x00i\\x00'"),
    d("utf-16", "strict", "b'\\xfe\\xff\\x00h\\x00i'"),
    d("utf-16", "strict", "b'h\\x00i\\x00'"),
    d("utf-16", "strict", "b'\\xff\\xfe\\xff\\xfeh\\x00'"),
    d("utf-16-le", "strict", "b'\\xff\\xfeh\\x00'"),
    d("utf-16-le", "strict", "b'=\\xd8\\x00\\xde'"),
    d("utf-16-be", "strict", "b'\\xd8=\\xde\\x00'"),
    d("utf-16-le", "strict", "b'a\\x00\\x00\\xdcb\\x00'"),
    d("utf-16-le", "strict", "b'a\\x00\\x00\\xd8b\\x00'"),
    d("utf-16-le", "strict", "b'a\\x00\\x00\\xd8'"),
    d("utf-16-le", "strict", "b'a\\x00\\x00\\xd8b'"),
    d("utf-16-le", "strict", "b'a\\x00b'"),
    d("utf-16", "strict", "b'\\xfe\\xff\\x00a\\x00'"),
    d("utf-16-le", "replace", "b'a\\x00\\x00\\xdcb\\x00\\x00\\xd8c\\x00d'"),
    d("utf-16-le", "surrogatepass", "b'a\\x00\\x00\\xdcb\\x00'"),
    d("utf-16-le", "backslashreplace", "b'a\\x00\\x00\\xdcb'"),
    d("utf-32", "strict", "b'\\xff\\xfe\\x00\\x00h\\x00\\x00\\x00'"),
    d("utf-32", "strict", "b'\\x00\\x00\\xfe\\xff\\x00\\x00\\x00h'"),
    d("utf-32-le", "strict", "b'\\x00\\x00\\x11\\x00'"),
    d("utf-32-le", "strict", "b'\\x00\\xd8\\x00\\x00'"),
    d("utf-32-le", "strict", "b'a\\x00\\x00\\x00b\\x00'"),
    d("utf-32-be", "replace", "b'\\x00\\x00\\x00a\\x00\\x11\\x00\\x00\\x00\\x00\\x00b'"),
    d("utf-32-le", "surrogatepass", "b'\\x00\\xd8\\x00\\x00'"),
    )

job("8-bit code pages",
    d("cp1252", "strict", "b'\\x93smart\\x94 \\x80 5 \\x96 caf\\xe9'"),
    d("cp1252", "strict", "b'a\\x81b'"),
    d("cp1252", "replace", "b'a\\x81\\x8d\\x8fb'"),
    d("cp1252", "backslashreplace", "b'a\\x81b'"),
    d("cp1252", "surrogateescape", "b'a\\x81b'"),
    d("cp1251", "strict", "b'\\xcf\\xf0\\xe8\\xe2\\xe5\\xf2'"),
    d("koi8-r", "strict", "b'\\xf0\\xd2\\xc9\\xd7\\xc5\\xd4'"),
    d("iso8859-15", "strict", "b'5 \\xa4 \\xbd'"),
    d("mac-roman", "strict", "b'caf\\x8e \\xa5 \\xf0'"),
    d("cp437", "strict", "b'\\xc9\\xcd\\xbb\\xba\\xb0\\xb1\\xb2\\x01\\x02'"),
    d("cp850", "strict", "b'\\x82\\x90\\xd0'"),
    e("cp1252", "strict", "'\\u201csmart\\u201d \\u20ac \\u2013 caf\\xe9'"),
    e("cp1252", "strict", "'\\u0442\\u0435\\u043a\\u0441\\u0442'"),
    e("cp1252", "replace", "'x \\u0442\\u0435 y \\u2192'"),
    e("cp1252", "xmlcharrefreplace", "'x \\u2192 y'"),
    e("cp1252", "namereplace", "'x \\u2192 y'"),
    e("cp1252", "surrogateescape", "'a\\udc81b'"),
    e("cp1251", "strict", "'\\u041f\\u0440\\u0438\\u0432\\u0435\\u0442'"),
    e("koi8-r", "strict", "'\\u041f\\u0440\\u0438\\u0432\\u0435\\u0442'"),
    e("koi8-r", "strict", "'caf\\xe9'"),
    e("iso8859-15", "strict", "'5 \\u20ac'"),
    e("iso8859-15", "strict", "'\\xa4'"),
    e("mac-roman", "strict", "'caf\\xe9 \\uf8ff'"),
    e("cp437", "strict", "'\\u2554\\u2550\\u2557 \\u263a'"),
    )

job("escape codecs",
    d("unicode_escape", "strict", "b'tab\\\\there \\\\x41 \\\\u20ac \\\\U0001f600 \\\\101 \\\\n\\xe9'"),
    d("unicode_escape", "strict", "b'a\\\\x4'"),
    d("unicode_escape", "strict", "b'a\\\\'"),
    d("unicode_escape", "strict", "b'a\\\\U00110000b'"),
    d("unicode_escape", "strict", "b'a\\\\u12z'"),
    d("unicode_escape", "replace", "b'a\\\\x4zb\\\\u12'"),
    d("unicode_escape", "backslashreplace", "b'a\\\\x4zb'"),
    d("unicode_escape", "strict", "b'\\\\\\\\ \\\\\\' \\\\\" \\\\a\\\\b\\\\f\\\\v\\\\0\\\\377'"),
    d("raw_unicode_escape", "strict", "b'a\\\\x41 \\\\u20ac \\\\U0001f600 \\xe9'"),
    d("raw_unicode_escape", "strict", "b'a\\\\u12'"),
    d("raw_unicode_escape", "strict", "b'a\\\\\\\\u0041'"),
    e("unicode_escape", "strict", "'tab\\there \\\\ \\'q\\' caf\\xe9 \\u20ac \\U0001f600 \\x7f\\x00'"),
    e("raw_unicode_escape", "strict", "'caf\\xe9 \\u20ac \\U0001f600 \\\\u'"),
    )

job("incremental decoding",
    ("feed", "utf-8", "strict", "b'caf\\xc3'", "b'\\xa9 \\xe2\\x82'", "b'\\xac'", "b' \\xf0\\x9f'", "b'\\x8e'", "b'\\x89!'"),
    ("feed", "utf-8", "strict", "b'ab\\xe2\\x82'", "b''"),
    ("feed", "utf-8", "replace", "b'ab\\xe2'", "b'('", "b'\\xf0\\x9f\\x8e'"),
    ("feed", "utf-8", "strict", "b'ab\\xe2('"),
    ("feed", "utf-8-sig", "strict", "b'\\xef'", "b'\\xbb'", "b'\\xbfhi'"),
    ("feed", "utf-8-sig", "strict", "b'\\xef'", "b'x'"),
    ("feed", "utf-16", "strict", "b'\\xff'", "b'\\xfeh'", "b'\\x00i'", "b'\\x00=\\xd8'", "b'\\x00\\xde'"),
    ("feed", "utf-16", "strict", "b'\\x00'", "b'h\\x00'", "b'i'"),
    ("feed", "utf-16-le", "strict", "b'h\\x00='", "b'\\xd8'", "b''"),
    ("feed", "utf-32", "strict", "b'\\x00\\x00\\xfe'", "b'\\xff\\x00\\x00'", "b'\\x00h'"),
    ("feed", "cp1252", "strict", "b'\\x93a'", "b'\\x94'"),
    ("feed", "unicode_escape", "strict", "b'a\\\\'", "b'x4'", "b'1b'"),
    ("feed", "ascii", "strict", "b'ok'", "b'\\xff'"),
    )


# ------------------------------------------------------------ programs

legacy = {
    "notes-win.txt": ("cp1252", "“Quarterly” notes – café budget €1,200\r\nNext: naïve forecast\r\n"),
    "menu-mac.txt": ("mac_roman", "Crème brûlée • 7,50\rCafé crème • 3,20\r"),
    "report-ru.txt": ("koi8_r", "Отчёт за март\nИтого: 42\n"),
    "invoice-1251.txt": ("cp1251", "Счёт № 17\nСумма: 9 900 ₽\n"),
    "banner-dos.txt": ("cp437", "╔════╗\n║ OK ║\n╚════╝\n"),
    "price-l9.txt": ("iso8859_15", "Prix: 12 € – œuvre\n"),
}
legacy_bytes = {}
for name, (enc, text) in legacy.items():
    try:
        legacy_bytes[name] = text.encode(enc)
    except UnicodeEncodeError:
        legacy_bytes[name] = text.encode(enc, "replace")
# a manifest that names the wrong codec for one file and none for another
manifest = [
    ("notes-win.txt", "windows-1252"),
    ("menu-mac.txt", "macintosh"),
    ("report-ru.txt", "KOI8-R"),
    ("invoice-1251.txt", "latin-1"),
    ("banner-dos.txt", "ibm437"),
    ("price-l9.txt", "ISO-8859-15"),
    ("missing.txt", "utf-8"),
    ("notes-win.txt", "cp-1252"),
]

uploads = {
    "a-utf8.csv": "name,city\nZoë,München\n".encode("utf-8"),
    "b-utf8-bom.csv": "name,city\nJosé,São Paulo\n".encode("utf-8-sig"),
    "c-utf16le-bom.csv": "name,city\n李雷,北京\n".encode("utf-16"),
    "d-utf16be-bom.csv": b"\xfe\xff" + "name,city\nAnna,Kraków\n".encode("utf-16-be"),
    "e-cp1252.csv": "name,city\nFrançois,“Paris”\n".encode("cp1252"),
    "f-utf32-bom.csv": "name,city\n\U0001f600,Tokyo\n".encode("utf-32"),
    "g-broken.csv": b"name,city\nBj\xc3\xb6rk,Reykjav\xc3\xadk\nOops,\xff\xfe\n",
}

log = (b"2026-10-20 12:00:01 user=zo\xc3\xab path=/caf\xc3\xa9 status=200\n"
       b"2026-10-20 12:00:02 user=\xff\xfeadmin path=/x\x80y status=404\n"
       b"2026-10-20 12:00:03 user=bob path=/\xe2\x82 status=500\n")

mojibake = [
    "café",
    "naïve résumé",
    "“smart quotes”",
    "München – Zürich",
    "plain ascii",
    "Łódź",
]

os.makedirs("data/legacy", exist_ok=True)
os.makedirs("data/uploads", exist_ok=True)


def write(path, data):
    with open(path, "wb") as f:
        f.write(data)


write("data/jobs.tsv", "".join("\t".join(line) + "\n" for line in jobs).encode("utf-8"))
for name, b in legacy_bytes.items():
    write("data/legacy/" + name, b)
write("data/legacy/manifest.tsv", "".join("%s\t%s\n" % m for m in manifest).encode())
for name, b in uploads.items():
    write("data/uploads/" + name, b)
write("data/server.log", log)
# the mojibake a UTF-8 page shows when it is read as cp1252, one a line
moji = []
for s in mojibake:
    moji.append(s.encode("utf-8").decode("cp1252", "replace"))
write("data/mojibake.txt", ("\n".join(moji) + "\n").encode("utf-8"))

# the tables
lines = []
for m in MODULES:
    mod = importlib.import_module("encodings." + m)
    lines.append("%s\t%s\n" % (m, mod.getregentry().name))
write("data/codecs.txt", "".join(lines).encode())
lines = []
for alias, target in sorted(encodings.aliases.aliases.items()):
    if target in MODULES:
        lines.append("%s\t%s\n" % (alias, target))
write("data/aliases.txt", "".join(lines).encode())
lines = []
for m in CHARMAPS:
    mod = importlib.import_module("encodings." + m)
    table = mod.decoding_table
    lines.append(m + "\t" + " ".join("-" if c == "￾" else "%x" % ord(c) for c in table) + "\n")
write("data/charmaps.txt", "".join(lines).encode())
names = set()
for op in jobs:
    if op[0] == "encode":
        import ast
        for c in ast.literal_eval(op[3]):
            names.add(c)
lines = []
for c in sorted(names):
    n = unicodedata.name(c, None)
    if n is not None and ord(c) > 127:
        lines.append("%x\t%s\n" % (ord(c), n))
write("data/names.txt", "".join(lines).encode())
