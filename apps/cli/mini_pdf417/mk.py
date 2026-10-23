"""Write data/jobs.tsv and the input files the jobs read.

PDF417 is the stacked bar code on airline boarding passes (IATA BCBP),
North American driver's licences (AAMVA), shipping labels and many
invoices and ID cards. The inputs are made-up records in those shapes.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

FILES = {
    "in/boarding.txt": (
        "M1DESMARAIS/LUC       EABC123 YULFRAAC 0834 226F001A0025 100"
    ).encode("ascii"),
    "in/licence.txt": (
        "@\n\x1e\rANSI 636014040002DL00410278ZC03190008DL"
        "DAQD1234562\nDCSPUBLIC\nDDEN\nDACJOHN\nDDFN\nDADQUINCY\nDDGN"
        "\nDCAD\nDCBNONE\nDCDNONE\nDBD08312013\nDBB08311977\nDBA08312022"
        "\nDBC1\nDAU069 in\nDAYGRN\nDAG789 E OAK ST\nDAIANYTOWN\nDAJCA"
        "\nDAK902230000  \nDCF00/00/0000NNNAN/ANFD/YY\nDCGUSA\nDCK"
        "D1234562 XXXXXXXXXX\r"
    ).encode("ascii"),
    "in/invoice.txt": (
        "INVOICE 2024-0815\tACME Tools Ltd.\n"
        "Bill to: Rivera & Sons, 12 Harbour Rd.\n"
        "Items: 4 x M8 bolts @ 0.35; 2 x drill bits (5mm) @ 4.20\n"
        "Total EUR 9.80 -- due 30 days\n"
    ).encode("ascii"),
    "in/vcard.txt": (
        "BEGIN:VCARD\nVERSION:3.0\nN:Okafor;Adaeze\nORG:Lagos Port Authority"
        "\nTEL;TYPE=work:+234-1-555-0199\nEMAIL:a.okafor@example.org\n"
        "END:VCARD\n"
    ).encode("ascii"),
    "in/parcel.txt": (
        "[)>\x1e01\x1d02\x1d840\x1d001\x1d1Z12345E0205271688\x1dUPSN\x1d"
        "12345E\x1d089\x1d\x1d1/1\x1d10.1\x1dY\x1d\x1dSAN DIEGO\x1dCA\x1e\x04"
    ).encode("ascii"),
    "in/utf8.txt": "Zürich – Ελλάδα – 東京 ✓\n".encode("utf-8"),
    "in/digits.txt": ("0123456789" * 9 + "42").encode("ascii"),
    "in/blob.bin": bytes(range(256)) + bytes((i * 37 + 11) % 256 for i in range(120)),
    "in/empty.txt": b"",
}

JOBS = []


def job(*fields):
    JOBS.append("\t".join(str(f) for f in fields))


def section(title):
    JOBS.append("# " + title)


section("compaction")
for spec in ["text:Hello, world!", "text:ABC abc 123 ABC", "text:hello",
             "text:0123456789012", "text:01234567890123", "text:abc0123456789012def",
             "text:abc01234567890123def", "text:\\t\\n\\r", "text:a~b{c}d|e",
             "text:email: a@b.co", "text:MiXeD CaSe; with (punct)!",
             "text:\\u00e9t\\u00e9", "hex:000102030405", "hex:00010203040506",
             "hex:ff", "text:", "file:in/digits.txt", "file:in/blob.bin",
             "file:in/parcel.txt", "text:x" + "9" * 50 + "y",
             "text:1234567890123456789012345678901234567890123456789"]:
    job("compact", spec)

section("compaction modes")
for spec in ["text:PDF417", "text:pdf417", "text:a.b.c", "text:A;B;C",
             "text:Ab", "text:aB!C", "text:#$%&", "text:.", "text:?",
             "text:hello world", "text:a b", "text:a\\nb", "hex:41e942"]:
    job("text", spec)
for spec in ["text:0", "text:1", "text:000", "text:999999", "text:1234567890",
             "text:" + "9" * 44, "text:" + "1" * 45, "text:" + "0" * 50,
             "text:", "text:12a"]:
    job("numeric", spec)
for spec in ["hex:00", "hex:010203", "hex:ffffffffffff", "hex:000000000000",
             "hex:0102030405060708090a0b0c", "hex:6162636465666768", "hex:"]:
    job("bytes", spec)

section("error correction and bases")
for level in range(0, 9):
    job("ec", "16,902,1,278,827,900,295,902,2,326,823,544,900,149,900,900", level)
job("ec", "-", 2)
job("ec", "5,453,178,121,239", 0)
job("ec", "5,453,178,121,239", 9)
job("ec", "5,453,178,121,239", -1)
job("ec", "928,928,928,928", 1)
job("base", "1,2,3", 10, 2)
job("base", "255,255,255,255,255,255", 256, 900)
job("base", "0,0,1", 256, 900)
job("base", "-", 10, 900)
job("base", "1,0,0,0", 900, 256)
job("base", "8,9,9", 10, 16)
for rows, cols, level in [(3, 1, 0), (5, 2, 2), (10, 6, 5), (90, 30, 8)]:
    if rows <= 10:
        job("rowwords", rows, cols, level)
job("rowwords", 7, 3, 8)

section("encoding")
for spec, opts in [
        ("text:Hello, world!", []),
        ("text:Hello, world!", ["columns=3"]),
        ("text:Hello, world!", ["columns=1", "security_level=0"]),
        ("text:Hello, world!", ["security_level=5"]),
        ("text:PDF417 bar code", ["columns=4", "security_level=1"]),
        ("text:01234567890123456789", ["columns=2"]),
        ("hex:deadbeefcafe", ["columns=2"]),
        ("text:\\u00e9t\\u00e9", ["encoding=latin-1"]),
        ("text:\\u00e9t\\u00e9", ["encoding=utf-8"]),
        ("text:\\u00e9t\\u00e9", ["encoding=ascii"]),
        ("text:caf\\u00e9", ["encoding=ascii"]),
        ("text:\\u20ac", ["encoding=latin-1"]),
        ("text:\\u20ac 5", ["encoding=utf-8", "columns=3"]),
        ("text:x", ["columns=0"]),
        ("text:x", ["columns=31"]),
        ("text:x", ["security_level=9"]),
        ("text:x", ["security_level=-1"]),
        ("text:x", ["columns=30", "security_level=0"]),
        ("text:x", ["columns=12", "security_level=0"]),
        ("text:x", ["columns=11", "security_level=0"]),
        ("text:", ["columns=1"]),
        ("int:42", []),
        ("text:x", ["colour=red"]),
        ("file:in/boarding.txt", ["columns=8"]),
        ("file:in/vcard.txt", ["columns=10", "security_level=3"]),
        ("file:in/utf8.txt", ["columns=5"]),
        ("file:in/empty.txt", ["columns=2"]),
        ("file:in/digits.txt", ["columns=1", "security_level=0"]),
        ("text:" + "Z" * 1900, ["columns=30", "security_level=0"]),
        ("text:" + "Zz" * 600, ["columns=30", "security_level=0"]),
        ("text:" + "ab" * 50, ["columns=1"]),
        ("text:" + "ab" * 100, ["columns=1"]),
        ("text:" + "a" * 2000, ["columns=30", "security_level=8"])]:
    job("encode", spec, *opts)
job("encode", "file:in/licence.txt", "columns=12", "security_level=4")
job("encode", "file:in/invoice.txt", "columns=9", "security_level=3")
job("encode", "file:in/parcel.txt", "columns=6", "security_level=4")
job("encode", "textfile:in/utf8.txt", "columns=7", "encoding=utf-8")
job("encode", "textfile:in/utf8.txt", "encoding=latin-1")
job("encode", "file:in/missing.txt")

section("module grids")
job("grid", "text:Hi", "columns=1", "security_level=0")
job("grid", "text:PDF417", "columns=2", "security_level=1")
job("grid", "hex:00ff00ff", "columns=1", "security_level=1")
job("grid", "text:0123456789012345", "columns=2", "security_level=0")

section("colours")
for spec in ["#000", "#FFF", "#1a2B3c", "#12345678", "#abcd", "rgb(10, 20, 30)",
             "rgb(100%,50%,0%)", "rgba(1,2,3,4)", "hsl(120, 100%, 25%)",
             "hsl(0,0%,50%)", "hsv(240, 50%, 100%)", "hsb(60,100%,100%)",
             "hsl(300.5, 20.5%, 80%)", "#12", "#ggg", "rgb(1,2)", "#000000 ",
             " #000", "RGB(1,2,3)", "#" + "0" * 120, "hsl(10,200%,50%)"]:
    job("color", spec)

section("svg")
job("svg", "hello.svg", "text:Hello, world!")
job("svg", "small.svg", "text:Hi", "columns=1", "security_level=0", "scale=1",
    "ratio=1")
job("svg", "boarding.svg", "file:in/boarding.txt", "columns=8", "scale=2",
    "color=#1a2b3c", "description=IATA BCBP <YUL> & \"FRA\"")
job("svg", "licence.svg", "file:in/licence.txt", "columns=12",
    "security_level=4", "color=rgb(0,0,128)", "description=AAMVA été\\tTAB")
job("svg", "vcard.svg", "file:in/vcard.txt", "columns=10", "ratio=4",
    "color=hsl(200, 80%, 30%)")
job("svg", "bad.svg", "text:x", "columns=1", "color=chartreuse-ish")
job("svg", "nodesc.svg", "text:x", "columns=2", "description=")

section("images")
job("image", "hello.ppm", "text:Hello, world!")
job("image", "tiny.ppm", "text:Hi", "columns=1", "security_level=0", "scale=1",
    "ratio=1", "padding=0")
job("image", "boarding.ppm", "file:in/boarding.txt", "columns=8", "scale=2",
    "padding=10", "fg_color=#1a2b3c", "bg_color=#fafafa")
job("image", "invoice.ppm", "file:in/invoice.txt", "columns=9",
    "security_level=3", "scale=1", "ratio=2", "padding=4",
    "fg_color=rgb(128,0,0)", "bg_color=hsv(60, 10%, 100%)")
job("image", "parcel.ppm", "file:in/parcel.txt", "columns=6", "ratio=1",
    "padding=1", "bg_color=#ffe")
job("image", "bad.ppm", "text:x", "columns=1", "fg_color=nope")
job("image", "badbg.ppm", "text:x", "columns=1", "fg_color=nope", "bg_color=#12")
job("image", "toolong.ppm", "text:" + "9" * 3000, "columns=1")


def main():
    for path, body in FILES.items():
        full = os.path.join(DATA, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "wb") as fh:
            fh.write(body)
    os.makedirs(os.path.join(DATA, "out"), exist_ok=True)
    with open(os.path.join(DATA, "jobs.tsv"), "w", encoding="utf-8") as fh:
        for line in JOBS:
            fh.write(line + "\n")
    with open(os.path.join(DATA, "files.txt"), "w", encoding="utf-8") as fh:
        for path in FILES:
            fh.write(path + "\n")


main()
