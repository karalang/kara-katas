# Writes data/: the jobs mini_barcode runs (data/jobs.jsonl) and the
# files its three programs read. Run with `python3 mk.py`.
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

JOBS = []


def job(name, *steps):
    JOBS.append({"name": name, "steps": [list(s) for s in steps]})


def new(var, kind, code, **kw):
    return ("new", var, kind, code, kw)


def show(var, *what):
    return ("show", var) + what


def render(var, opts=None, text=None, mode="brief"):
    return ("render", var, opts, text, mode)


ALL = ("repr", "str", "full", "build", "ascii")

# --- EAN-13 and its relatives

job("ean13 from twelve digits", new("b", "ean13", "400638133393"), show("b", *ALL, "checksum"),
    render("b", mode="full"))
job("ean13 with its check digit given", new("b", "ean13", "5901234123457"), show("b", "repr", "str"))
job("ean13 with a wrong check digit", new("b", "ean13", "5901234123450"), show("b", "repr"))
job("ean13 too long is cut", new("b", "ean13", "40063813339312345"), show("b", "repr", "str"))
job("ean13 too short", new("b", "ean13", "40063813339"))
job("ean13 with a letter", new("b", "ean13", "4006a8133393"))
job("ean13 letter after the twelfth digit", new("b", "ean13", "400638133393x"), show("b", "repr"))
job("ean13 empty", new("b", "ean13", ""))
job("ean13 no_checksum keeps the thirteenth", new("b", "ean13", "4006381333932", no_checksum=True),
    show("b", "repr", "checksum"))
job("ean13 no_checksum pads with zero", new("b", "ean13", "400638133393", no_checksum=True), show("b", "repr"))
job("ean13 no_checksum with a letter last", new("b", "ean13", "400638133393x", no_checksum=True), show("b", "repr"))
job("ean name is ean13", new("b", "EAN", "978014300723"), show("b", "repr"))
job("ean13 with guards", new("b", "ean13-guard", "590123412345"), show("b", *ALL), render("b", mode="full"))
job("ean13 guardbar keyword", new("b", "ean13", "400638133393", guardbar=True), show("b", "repr", "full"))
job("ean13-guard with guardbar turned off", new("b", "ean13-guard", "400638133393", guardbar=False),
    show("b", "repr", "full"))
job("ean13 unknown keyword", new("b", "ean13", "400638133393", make_ean=True))
job("ean8", new("b", "ean8", "5512345"), show("b", *ALL, "checksum"), render("b"))
job("ean8 with guards and human text", new("b", "ean8-guard", "4006381"), show("b", "full", "ascii"),
    render("b", {"human": "Milk 1L"}))
job("ean8 too short", new("b", "ean8", "551234"))
job("ean8-guard unknown keyword", new("b", "ean8-guard", "5512345", make_ean=True))
job("ean14", new("b", "ean14", "1234567890123"), show("b", *ALL, "checksum"), render("b"))
job("gtin is ean14", new("b", "gtin", "0950110153000"), show("b", "repr"))
job("ean14 with guards", new("b", "ean14", "0950110153000", guardbar=True), show("b", "full"),
    render("b"))
job("jan 490", new("b", "jan", "490123456789"), show("b", "repr", "build"))
job("jan 459", new("b", "JAN", "4591234567890"), show("b", "repr"))
job("jan outside Japan", new("b", "jan", "400638133393"))
job("jan with letters", new("b", "jan", "ab1234567890"))
job("jan with a space", new("b", "jan", " 49123456789"))
job("jan with underscores", new("b", "jan", "4_91234567890"))
job("jan unknown keyword", new("b", "jan", "490123456789", make_ean=True))

# --- ISBN and ISSN

job("isbn13 with hyphens", new("b", "isbn13", "978-0-13-235418-9"), show("b", "repr", "str", "full", "checksum"))
job("isbn is isbn13", new("b", "isbn", "9781593279288"), show("b", "repr"))
job("isbn13 979-10", new("b", "isbn13", "979-10-90636-07-1"), show("b", "repr"))
job("isbn13 979-8", new("b", "isbn13", "979-8-6024-0545-3"), show("b", "repr"))
job("isbn13 979-2", new("b", "isbn13", "979-2-12-345678-1"))
job("isbn13 not a book", new("b", "isbn13", "400638133393"))
job("gs1 is isbn13", new("b", "gs1", "5901234123457"))
job("isbn13 with guards", new("b", "isbn13", "9780132354189", guardbar=True), show("b", "repr", "full"),
    render("b", {"module_height": 20}))
job("isbn10", new("b", "isbn10", "0132354187"), show("b", "repr", "str", "full"))
job("isbn10 with hyphens", new("b", "isbn10", "0-306-40615-2"), show("b", "repr", "str"))
job("isbn10 with X", new("b", "isbn10", "080442957X"), show("b", "repr", "str"))
job("isbn10 wrong check digit", new("b", "isbn10", "0306406153"), show("b", "str"))
job("isbn10 too short", new("b", "isbn10", "12345"))
job("isbn10 keyword", new("b", "isbn10", "0132354187", guardbar=True))
job("issn", new("b", "issn", "0317-8471"), show("b", "repr", "str", "full", "build"))
job("issn check digit 10", new("b", "issn", "2434-561X"), show("b", "repr", "str"))
job("issn check digit 11", new("b", "issn", "0000000"), show("b", "repr", "str"))
job("issn real 0378-5955", new("b", "issn", "03785955"), show("b", "repr", "str"))
job("issn with a letter past the seventh digit", new("b", "issn", "0317-847a"))
job("issn too short", new("b", "issn", "123"))

# --- UPC-A

job("upca", new("b", "upca", "03600029145"), show("b", *ALL, "checksum"), render("b"))
job("upc twelve digits are cut", new("b", "upc", "036000291452"), show("b", "repr", "str"))
job("upc make_ean", new("b", "upc", "03600029145", make_ean=True), show("b", "repr", "str", "full"))
job("upc too short", new("b", "upc", "0360002914"))
job("upc with a letter", new("b", "upc", "03600a29145"))
job("upc check digit zero", new("b", "upc", "01234567895"), show("b", "str", "checksum"))

# --- Code 39 and PZN

job("code39", new("b", "code39", "WIKIPEDIA"), show("b", *ALL, "checksum"), render("b"))
job("code39 lower case", new("b", "code39", "hello world"), show("b", "repr", "str"))
job("code39 without checksum", new("b", "code39", "CODE-39", add_checksum=False), show("b", "repr", "build"))
job("code39 bad character in the checksum", new("b", "code39", "abc@"))
job("code39 bad characters", new("b", "code39", "A@B#", add_checksum=False))
job("code39 sharp s", new("b", "code39", "straße"), show("b", "repr"))
job("code39 empty", new("b", "code39", ""), show("b", "repr", "build"))
job("code39 small render", new("b", "code39", "LOT 42"),
    render("b", {"quiet_zone": 1, "module_height": 5, "font_size": 0}, mode="full"))
job("pzn", new("b", "pzn", "123456"), show("b", "repr", "str", "full"))
job("pzn cut to six", new("b", "pzn", "6543217"), show("b", "repr"))
job("pzn check 10", new("b", "pzn", "222222"))
job("pzn too short", new("b", "pzn", "12345"))
job("pzn letter", new("b", "pzn", "12a456"))

# --- Code 128 and GS1-128

job("code128 text", new("b", "code128", "Wikipedia"), show("b", "repr", "encoded", "build", "ascii"))
job("code128 digits", new("b", "code128", "123456"), show("b", "encoded", "build"))
job("code128 odd digits", new("b", "code128", "12345"), show("b", "encoded"))
job("code128 one digit", new("b", "code128", "7"), show("b", "encoded"))
job("code128 remembers its charset", new("b", "code128", "12a"), show("b", "encoded", "encoded", "build"))
job("code128 into C and back", new("b", "code128", "AB12345C"), show("b", "encoded", "encoded"))
job("code128 four digits switch", new("b", "code128", "ab1234cd123ef"), show("b", "encoded"))
job("code128 control characters", new("b", "code128", "\tTab\nNL"), show("b", "repr", "encoded", "encoded"))
job("code128 lower then control", new("b", "code128", "a\n"), show("b", "encoded", "encoded"))
job("code128 FNC characters", new("b", "code128", "xó1ò"), show("b", "repr", "encoded"))
job("code128 empty", new("b", "code128", ""), show("b", "repr", "build"))
job("code128 bad characters", new("b", "code128", "café €5"))
job("code128 render twice", new("b", "code128", "12a"), render("b"), render("b"))
job("gs1_128", new("b", "gs1_128", "0109501101530003172012311000A1"),
    show("b", "repr", "str", "full", "encoded"), render("b"))
job("gs1_128 with a separator", new("b", "gs1_128", "10ABC123ñ21123"), show("b", "repr", "encoded"))
job("gs1_128 separator after an odd digit", new("b", "gs1_128", "123ñ45"), show("b", "encoded"))
job("gs1_128 in charset A", new("b", "gs1_128", "\nñ1"), show("b", "encoded"))

# --- Codabar and ITF

job("codabar", new("b", "codabar", "A40156B"), show("b", "repr", "str", "build", "ascii"), render("b"))
job("nw-7 money", new("b", "nw-7", "C$1.00+D"), show("b", "build"))
job("codabar one letter", new("b", "codabar", "A"), show("b", "build"))
job("codabar narrow and wide", new("b", "codabar", "A12B", narrow=1, wide=3), show("b", "build"))
job("codabar bad start", new("b", "codabar", "a1b"), show("b", "repr", "build"))
job("codabar bad end", new("b", "codabar", "A12"), show("b", "build"))
job("codabar bad middle", new("b", "codabar", "A1x9B"), show("b", "build"))
job("codabar empty", new("b", "codabar", ""), show("b", "build"))
job("itf", new("b", "itf", "1234567"), show("b", "repr", "str", "build"), render("b"))
job("itf narrow 1 wide 2", new("b", "itf", "12", narrow=1, wide=2), show("b", "build", "ascii"))
job("itf with a letter", new("b", "itf", "12a"))
job("itf empty", new("b", "itf", ""))
job("itf narrow zero", new("b", "itf", "12", narrow=0), show("b", "build"), render("b"))

# --- names

job("unknown barcode", new("b", "qr", "hello"))
job("names ignore case", new("b", "Code128", "x"), new("c", "UPCA", "03600029145"), show("b", "repr"), show("c", "repr"))

# --- the SVG writer's options

job("svg without doctype", new("b", "itf", "12"), render("b", {"with_doctype": False}))
job("svg compressed", new("b", "codabar", "A1B"), render("b", {"compress": True}, mode="full"))
job("svg no text", new("b", "ean8", "5512345"), render("b", {"write_text": False}))
job("svg own text without write_text", new("b", "ean8", "5512345"), render("b", {"write_text": False}, "custom"))
job("svg text with lines", new("b", "code39", "A1"),
    render("b", {"text_line_distance": 2}, "Line one\nLine two", "full"))
job("svg text ending in a newline", new("b", "code39", "A1"), render("b", None, "x\n"))
job("svg text not centred", new("b", "code39", "A1"), render("b", {"center_text": False}))
job("svg same colours", new("b", "code39", "A1"), render("b", {"foreground": "white"}, mode="full"))
job("svg no background", new("b", "code39", "A1"), render("b", {"background": None}))
job("svg awkward colours", new("b", "code39", "A1"),
    render("b", {"background": "#fff\"><", "foreground": "rgb(0, 0, 0)&\t"}))
job("svg font sizes", new("b", "code39", "A1"), render("b", {"font_size": 8.5}), render("b", {"font_size": 12.0}))
job("svg underscore option", new("b", "code39", "A1"), render("b", {"_quiet_zone": 0, "_unknown": 3, "dpi": 600}))
job("svg sixteenth modules", new("b", "codabar", "A1B"), render("b", {"module_width": 0.0625}, mode="full"))
job("svg margins", new("b", "code39", "A1"), render("b", {"margin_top": 0, "margin_bottom": 3, "text_distance": 1}))
job("svg escaped text", new("b", "code128", "a<b&c>\"d'"), render("b", {"human": "<&>\"'"}))
job("svg guard blocks with less text", new("b", "ean13-guard", "400638133393"), render("b", None, "ABC"))
job("svg guard blocks with more text", new("b", "ean13-guard", "400638133393"), render("b", None, "a b c d e f"))
job("svg guards at height 1", new("b", "ean13-guard", "400638133393"), render("b", {"guard_height_factor": 1}))
job("svg guard height 1.5", new("b", "ean8-guard", "5512345"), render("b", {"guard_height_factor": 1.5}))
job("svg options stay on the writer", new("b", "code39", "A1"),
    render("b", {"human": "first", "center_text": False}), render("b"), render("b", {"human": ""}))

# --- save and generate

job("save", new("b", "ean13", "400638133393"), ("save", "b", "data/out/jobs/ean13", None, None),
    ("save", "b", "data/out/jobs/ean13-small", {"module_height": 5}, "small"))
job("save to a missing directory", new("b", "ean8", "5512345"), ("save", "b", "data/out/nowhere/x", None, None))
job("generate", ("generate", "isbn10", "0132354187", "data/out/jobs/book", {"module_height": 8}, None),
    ("generate", "itf", "1234", "data/out/jobs/itf", None, None),
    ("generate", "code128", "LOT-7", "data/out/jobs/lot", None, ""),
    ("generate", "code128", "LOT-7", "data/out/jobs/lot-text", None, "Lot seven"))
job("generate errors", ("generate", "qr", "x", "data/out/jobs/qr", None, None),
    ("generate", "ean13", "12", "data/out/jobs/short", None, None),
    ("generate", "ean13", "400638133393", None, None, None))

# --- the python-barcode command

job("cli list", ("cli", ["list"]))
job("cli version", ("cli", ["-v"]), ("cli", ["--version"]))
job("cli create code39", ("cli", ["create", "WIKIPEDIA", "data/out/cli/wiki"]))
job("cli create ean13", ("cli", ["create", "-b", "EAN13", "400638133393", "data/out/cli/ean"]))
job("cli create isbn10 with text",
    ("cli", ["create", "--barcode=isbn10", "0132354187", "data/out/cli/./sub/../book", "--text", "ISBN 0-13-235418-7"]))
job("cli create abbreviated", ("cli", ["create", "--barc", "upca", "--tex", "UPC", "03600029145", "data/out/cli/upc"]))
job("cli create attached short option", ("cli", ["create", "-bitf", "1234", "data/out/cli/itf"]))
job("cli create empty text", ("cli", ["create", "--text", "", "-b", "ean", "590123412345", "data/out/cli/empty-text"]))
job("cli errors", ("cli", []), ("cli", ["frob"]), ("cli", ["create", "x"]),
    ("cli", ["create", "x", "o", "--bogus"]), ("cli", ["create", "-b", "qr", "x", "o"]),
    ("cli", ["create", "x", "o", "--text"]), ("cli", ["create", "-b", "ean13", "12", "data/out/cli/bad"]))


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


shutil.rmtree("data", ignore_errors=True)
write("data/jobs.jsonl", "".join(json.dumps(j, ensure_ascii=False) + "\n" for j in JOBS))

# A shop's shelf labels: the code column is whatever the supplier sent.
write("data/products.csv", """sku,name,price,code
MLK-1L,Whole milk 1 L,1.19,4006381333931
BRD-500,Rye bread 500 g,2.49,5901234123457
EGG-10,Free-range eggs x10,3.29,4006381-333932
CHO-100,Dark chocolate 100 g,1.79,55123457
CHO-101,Milk chocolate 100 g,1.79,55123450
SOD-033,Cola 0.33 L,0.89,036000291452
SOD-050,Cola 0.5 L,1.29,0360 0029 1453
TEA-025,Green tea 25 bags,2.99,10950110153003
TEA-026,Black tea 25 bags,2.99,10950110153004
JAM-450,Strawberry jam 450 g,2.69,4006381-33393
OIL-750,Olive oil 0.75 L,6.99,40063813339A1
SPC-001,Salt & pepper set,4.50,
""")

# Pallets and cartons leaving the warehouse.
write("data/shipments.jsonl", "".join(json.dumps(s) + "\n" for s in [
    {"id": "PAL-0001", "sscc": "03765432100000001", "gtin": "0950110153000", "batch": "B2024-11", "expiry": "261231", "count": 48},
    {"id": "PAL-0002", "sscc": "03765432100000002", "gtin": "0400638133393", "batch": "L7", "expiry": "270115", "count": 120},
    {"id": "CTN-0450", "sscc": None, "gtin": "1950110153000", "batch": "X1", "expiry": None, "count": None, "serial": "SN000451"},
    {"id": "CTN-0451", "sscc": None, "gtin": "195011015300", "batch": "X1", "expiry": None, "count": None},
    {"id": "PAL-0003", "sscc": "0376543210000003", "gtin": "0950110153000", "batch": "B2024-12", "expiry": "261301", "count": 12},
]))

# A small library's catalogue.
write("data/books.txt", """# kind  number  title
isbn10  0-13-235418-7  Clean Code
isbn10  0-306-40615-2  A sample book
isbn10  0-8044-2957-X  The Old Man and the Sea
isbn10  0-8044-2957-5  The same book, mistyped
isbn13  978-1-59327-928-8  The Rust Programming Language
isbn13  979-10-90636-07-1  Un livre
isbn13  979-2-12-345678-1  An old 979 number
isbn13  978-0-13-235418-0  Clean Code, wrong check digit
issn    0317-8471  Journal of Things
issn    2434-561X  Bulletin of Ten
issn    0378-5955  Hearing Research
issn    0378-5950  Hearing Research, mistyped
issn    0000-0000  Placeholder
""")
print(f"wrote data/: {len(JOBS)} jobs")
