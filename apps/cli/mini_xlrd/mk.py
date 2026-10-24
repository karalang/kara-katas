#!/usr/bin/env python3
"""Writes data/ for mini_xlrd: workbooks saved by the vendored xlwt,
BIFF8 streams built record by record, compound documents built sector by
sector, damaged copies, a few ZIP files and data/jobs.txt. data/files.txt
lists every input file.

Run from this directory: python3 -s -P -B mk.py"""
import datetime
import os
import struct
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
import xlwt  # noqa: E402

DATA = os.path.join(HERE, "data")
pack = struct.pack
FILES = []


def put(name, data):
    path = os.path.join(DATA, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    FILES.append(name)


def save(wb, name):
    path = os.path.join(DATA, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wb.save(path)
    FILES.append(name)
    with open(path, "rb") as f:
        return f.read()


# ------------------------------------------------------------ xlwt books

def book_basic():
    wb = xlwt.Workbook()
    ws = wb.add_sheet("Stock")
    date = xlwt.easyxf(num_format_str="yyyy-mm-dd")
    stamp = xlwt.easyxf(num_format_str="yyyy-mm-dd hh:mm:ss")
    money = xlwt.easyxf(num_format_str="#,##0.00")
    for c, h in enumerate(["Item", "Qty", "Price", "Added", "In stock", "Note"]):
        ws.write(0, c, h)
    rows = [
        ("Bolt M6", 120, 0.15, datetime.date(2024, 3, 1), True, ""),
        ("Nut M6", 0, 0.05, datetime.date(2024, 3, 2), False, "reorder"),
        ("Washer", -3, 0.02, datetime.date(2023, 12, 31), True, "count again"),
        ("Hinge", 15, 3.99, datetime.datetime(2024, 2, 29, 13, 45, 30), True, None),
        ('Bracket "L"', 7, 12.5, "2024-04-01", True, "date typed as text"),
        ("Spring, long", 2500, 0.004, datetime.date(1900, 3, 1), False, "tab\there"),
    ]
    for r, row in enumerate(rows, 1):
        for c, v in enumerate(row):
            if v is None:
                continue
            if c == 3 and not isinstance(v, str):
                ws.write(r, c, v, stamp if isinstance(v, datetime.datetime) else date)
            elif c == 2:
                ws.write(r, c, v, money)
            else:
                ws.write(r, c, v)
    ws.row(7).set_cell_error(1, "#DIV/0!")
    ws.row(7).set_cell_error(2, 0x2A)  # xlwt has no "#N/A" key
    ws.row(7).set_cell_error(3, "#VALUE!")  # which xlwt maps to code 36
    ws.write(7, 0, "Totals")
    ws.write(8, 3, None, date)
    ws.write(8, 5, "")
    ws.write(9, 0, 1 / 3)
    ws.write(9, 1, 2 ** 31)
    ws.write(9, 2, -0.5)
    ws.write(9, 4, False)
    return save(wb, "books/basic.xls")


SALES = [
    # date, region, product, units, price
    ("Q1", datetime.date(2024, 1, 5), "North", "Widget", 12, 2.5),
    ("Q1", datetime.date(2024, 1, 9), "South", "Gadget", 3, 19.99),
    ("Q1", datetime.date(2024, 1, 17), "North", "Gadget", 1, 19.99),
    ("Q1", datetime.date(2024, 2, 2), "East", "Widget", 40, 2.25),
    ("Q1", datetime.date(2024, 2, 14), "West", "Gizmo", 5, 7.0),
    ("Q1", datetime.date(2024, 2, 29), "South", "Widget", "n/a", 2.5),
    ("Q1", datetime.date(2024, 3, 3), "East", "Gizmo", 8, 7.0),
    ("Q1", datetime.date(2024, 3, 21), "North", "Widget", 20, 2.4),
    ("Q1", datetime.date(2024, 3, 30), "Ost", "Gizmo", 2, 7.0),
    ("Q2", datetime.datetime(2024, 4, 2, 9, 30), "West", "Widget", 15, 2.5),
    ("Q2", datetime.date(2024, 4, 11), "South", "Gizmo", None, 7.0),
    ("Q2", datetime.date(2024, 4, 28), "North", "Gadget", 6, 18.5),
    ("Q2", datetime.date(2024, 5, 6), "East", "Widget", 33, 2.25),
    ("Q2", datetime.date(2024, 5, 19), "West", "Gadget", "#N/A", 18.5),
    ("Q2", datetime.date(2024, 6, 1), "North", "Gizmo", 9, 6.75),
    ("Q2", datetime.date(2024, 6, 15), "South", "Widget", 11, 2.5),
    ("Q2", datetime.date(2024, 6, 30), "East", "Gadget", 2, 18.5),
]


def book_sales():
    wb = xlwt.Workbook()
    date = xlwt.easyxf(num_format_str="dd/mm/yyyy")
    stamp = xlwt.easyxf(num_format_str="dd/mm/yyyy hh:mm")
    head = xlwt.easyxf("font: bold on")
    for q in ("Q1", "Q2"):
        ws = wb.add_sheet(q)
        for c, h in enumerate(["Date", "Region", "Product", "Units", "Unit price"]):
            ws.write(0, c, h, head)
        r = 1
        for row in SALES:
            if row[0] != q:
                continue
            d, region, product, units, price = row[1:]
            ws.write(r, 0, d, stamp if isinstance(d, datetime.datetime) else date)
            ws.write(r, 1, region)
            ws.write(r, 2, product)
            if units == "#N/A":
                ws.row(r).set_cell_error(3, 0x2A)
            elif units is not None:
                ws.write(r, 3, units)
            ws.write(r, 4, price)
            r += 1
    lk = wb.add_sheet("Lookup")
    lk.visibility = 1
    for r, (a, b) in enumerate([("Ost", "East"), ("Nord", "North"), ("Sud", "South")]):
        lk.write(r, 0, a)
        lk.write(r, 1, b)
    notes = wb.add_sheet("Notes")
    notes.write_merge(0, 0, 0, 3, "Sales notes", xlwt.easyxf("font: bold on, height 280; align: horiz center"))
    bold = xlwt.Font()
    bold.bold = True
    notes.write_rich_text(2, 0, [("Units ", bold), "of ", ("n/a", bold), " mean the count was lost."])
    notes.write(3, 0, "Prices are per unit, before tax.")
    return save(wb, "books/sales.xls")


NUMBERS = [
    0, 1, -1, 7, 536870911, -536870912, 536870912, 2 ** 31, 2 ** 53, -2 ** 40,
    12.34, -0.01, 1234567.89, 0.5, 1.5, -2.5, 100.25, 0.1, 1 / 3, 3.14159,
    1e300, -1e-300, 5e-324, 1e16, 123456789012345678.0, 2.5e-7, 65536.0,
    float("inf"), float("-inf"), -0.0,
]


def book_numbers():
    wb = xlwt.Workbook()
    ws = wb.add_sheet("Column")
    for r, v in enumerate(NUMBERS):
        ws.write(r, 0, v)
    ws2 = wb.add_sheet("Rows")
    for r in range(4):
        for c in range(6):
            ws2.write(r, c, (r * 6 + c) * [1, 0.25, 100.5, 1e9][r])
    ws2.write(5, 0, 10)
    ws2.write(5, 1, 0.1)
    ws2.write(5, 2, 20)
    ws2.write(5, 3, 30)
    return save(wb, "books/numbers.xls")


def book_text():
    wb = xlwt.Workbook()
    ws = wb.add_sheet("Unicode")
    words = [
        "plain ascii", "café crème", "Größe", "naïve façade", "Ελληνικά",
        "Русский текст", "日本語のテキスト", "한국어", "עברית", "العربية",
        "emoji 📦 box", "math 𝐀𝐁", "tab\tand\nnewline", "quote ' and \"",
        "back\\slash", "", " leading", "trailing ", "€ 9.99", "ÿ",
    ]
    for r, w in enumerate(words):
        ws.write(r, 0, w)
        ws.write(r, 1, len(w))
    ws.write(0, 2, "plain ascii")
    long = wb.add_sheet("Long")
    text = "".join("line %04d: the quick brown fox; " % i for i in range(320))
    long.write(0, 0, text)
    mixed = "".join(("Ω%d " % i) if i % 3 else ("w%d " % i) for i in range(2600))
    long.write(1, 0, mixed)
    for i in range(400):
        long.write(2 + i // 8, i % 8, "s%03d %s" % (i, "äöü" if i % 5 == 0 else "x"))
    return save(wb, "books/text.xls")


def book_1904():
    wb = xlwt.Workbook()
    wb.dates_1904 = True
    ws = wb.add_sheet("Dates")
    fmts = ["yyyy-mm-dd", "hh:mm:ss", "d mmm yyyy h:mm", "mm:ss", "[h]:mm", "0.00"]
    vals = [
        datetime.date(1904, 1, 1), datetime.date(1904, 1, 2), datetime.date(2024, 2, 29),
        datetime.datetime(1999, 12, 31, 23, 59, 59), datetime.time(6, 30), datetime.time(23, 59, 59),
        datetime.datetime(2000, 1, 1, 12, 0), datetime.date(9999, 12, 31),
    ]
    for r, v in enumerate(vals):
        for c, f in enumerate(fmts):
            ws.write(r, c, v, xlwt.easyxf(num_format_str=f))
    ws.write(len(vals), 0, 0.0, xlwt.easyxf(num_format_str="yyyy-mm-dd"))
    ws.write(len(vals), 1, -1.0, xlwt.easyxf(num_format_str="yyyy-mm-dd"))
    ws.write(len(vals), 2, 0.99999999, xlwt.easyxf(num_format_str="hh:mm:ss"))
    ws.write(len(vals), 3, 3000000.0, xlwt.easyxf(num_format_str="yyyy-mm-dd"))
    return save(wb, "books/d1904.xls")


def book_1900():
    wb = xlwt.Workbook()
    ws = wb.add_sheet("Dates")
    style = xlwt.easyxf(num_format_str="yyyy-mm-dd hh:mm:ss")
    vals = [0.0, 0.5, 1.0, 59.0, 60.0, 61.0, 61.25, 366.0, 45351.999988, 45351.9999999,
            2958465.0, 2958466.0, -0.25, 43831.000005787]
    for r, v in enumerate(vals):
        ws.write(r, 0, v, style)
        ws.write(r, 1, v)
    return save(wb, "books/d1900.xls")


def book_layout():
    wb = xlwt.Workbook()
    ws = wb.add_sheet("Report")
    title = xlwt.easyxf("font: name Courier New, bold on, height 320, colour dark_blue; align: horiz center, vert center")
    head = xlwt.easyxf("font: bold on, italic on; borders: bottom thick; pattern: pattern solid, fore_colour light_yellow")
    pct = xlwt.easyxf("font: colour red", num_format_str="0.0%")
    wrap = xlwt.easyxf("align: wrap on, vert top", num_format_str="@")
    under = xlwt.easyxf("font: underline single, struck_out on", num_format_str='"Total: "#,##0')
    red = xlwt.easyxf("pattern: pattern solid, fore_colour red", num_format_str="[Red]0.00;[Blue]-0.00")
    ws.write_merge(0, 1, 0, 4, "Quarterly report", title)
    for c, h in enumerate(["Team", "Share", "Comment", "Total", "Delta"]):
        ws.write(2, c, h, head)
    data = [("Ops", 0.25, "steady, no change in headcount", 1200, 3.5),
            ("Sales", 0.5, "two new hires", 34000, -1.25),
            ("R&D", 0.125, "prototype shipped", 98765, 0.0)]
    for r, (a, b, c, d, e) in enumerate(data, 3):
        ws.write(r, 0, a)
        ws.write(r, 1, b, pct)
        ws.write(r, 2, c, wrap)
        ws.write(r, 3, d, under)
        ws.write(r, 4, e, red)
    ws.write_merge(6, 6, 0, 2, None, head)
    ws.write(7, 1, None, red)
    ws.col(0).width = 256 * 12
    ws.col(2).width = 256 * 30
    ws.col(4).hidden = True
    ws.row(3).height_mismatch = True
    ws.row(3).height = 600
    ws.panes_frozen = True
    ws.horz_split_pos = 3
    ws.horz_split_first_visible = 3
    italic = xlwt.Font()
    italic.italic = True
    big = xlwt.Font()
    big.height = 400
    ws.write_rich_text(9, 0, ["normal ", ("italic", italic), " and ", ("big", big)])
    other = wb.add_sheet("Other")
    other.write(0, 0, "second sheet")
    other.set_selected(True)
    other.normal_magn = 150
    return save(wb, "books/layout.xls")


def book_sparse():
    wb = xlwt.Workbook()
    ws = wb.add_sheet("Sparse")
    ws.write(0, 0, "origin")
    ws.write(0, 3, 4)
    ws.write(5, 1, "row six")
    ws.write(2, 255, "last column")
    ws.write(300, 200, 301.0)
    ws.write(301, 0, None, xlwt.easyxf("font: bold on"))
    return save(wb, "books/sparse.xls")


def book_formulas():
    wb = xlwt.Workbook()
    ws = wb.add_sheet("Calc")
    for r, v in enumerate([3, 4, 5]):
        ws.write(r, 0, v)
    ws.write(3, 0, xlwt.Formula("SUM(A1:A3)"))
    ws.write(4, 0, xlwt.Formula('"a"&"b"'))
    ws.write(5, 0, xlwt.Formula("1/0"))
    ws.write(6, 0, xlwt.Formula("A1>A2"), xlwt.easyxf(num_format_str="yyyy-mm-dd"))
    return save(wb, "books/formulas.xls")


def book_owner():
    wb = xlwt.Workbook()
    wb.owner = "Zoe Analyst"
    wb.country_code = 44
    ws = wb.add_sheet("Ünïcode name")
    ws.write(0, 0, "owner test")
    wb.add_sheet("x" * 31).write(0, 0, 1)
    return save(wb, "books/owner.xls")


def book_split_pair():
    wb = xlwt.Workbook()
    ws = wb.add_sheet("Pair")
    # 8202 characters of filler put the second string's astral character
    # across the SST/CONTINUE boundary.
    filler = "f" * 8202
    ws.write(0, 0, filler)
    ws.write(1, 0, "Ωab📦cd")
    return save(wb, "books/split_pair.xls")


# ------------------------------------------------------------ raw BIFF8

def rec(code, data=b""):
    return pack("<HH", code, len(data)) + data


def bof(stype, vers=0x0600, build=0x0DBB, year=0x07CC):
    return rec(0x0809, pack("<HHHHII", vers, stype, build, year, 0, 6))


EOF = rec(0x000A)


def ustr(s, lenlen=2, flag=None):
    try:
        b = s.encode("latin1")
        f, n = 0, len(s)
    except UnicodeEncodeError:
        b = s.encode("utf_16_le")
        f, n = 1, len(b) // 2
    if flag == 1 and f == 0:
        b = s.encode("utf_16_le")
        f = 1
    return pack("<H" if lenlen == 2 else "<B", n) + bytes([f]) + b


def fmt_rec(key, s):
    return rec(0x041E, pack("<H", key) + ustr(s))


def xf_rec(fmtkey, font=0):
    return rec(0x00E0, pack("<HHHBBBBIiH", font, fmtkey, 0x0001, 0x20, 0, 0, 0, 0, 0, 0x20C0))


def dims(r1, c1):
    return rec(0x0200, pack("<iiHHH", 0, r1, 0, c1, 0))


def number(r, c, xf, v):
    return rec(0x0203, pack("<HHHd", r, c, xf, v))


def rk_bytes(v):
    if isinstance(v, tuple):
        kind, x = v
    else:
        kind, x = "int", v
    if kind == "int":
        return pack("<i", (x << 2) | 2)
    if kind == "int100":
        return pack("<i", (x << 2) | 3)
    raw = pack("<d", x)
    hi = struct.unpack("<I", raw[4:])[0] & ~3
    if kind == "float100":
        hi |= 1
    return pack("<I", hi)


def rk(r, c, xf, v):
    return rec(0x027E, pack("<HHH", r, c, xf) + rk_bytes(v))


def mulrk(r, c0, xf, vals):
    body = b"".join(pack("<H", xf) + rk_bytes(v) for v in vals)
    return rec(0x00BD, pack("<HH", r, c0) + body + pack("<H", c0 + len(vals) - 1))


def label(r, c, xf, s, flag=None):
    return rec(0x0204, pack("<HHH", r, c, xf) + ustr(s, 2, flag))


def labelsst(r, c, xf, i):
    return rec(0x00FD, pack("<HHHi", r, c, xf, i))


def boolerr(r, c, xf, v, err):
    return rec(0x0205, pack("<HHHBB", r, c, xf, v, err))


TINT1 = pack("<H", 3) + b"\x1e\x01\x00"


def formula(r, c, xf, result):
    return rec(0x0006, pack("<HHH8sHI", r, c, xf, result, 0, 0) + TINT1)


def fres_num(v):
    return pack("<d", v)


def fres(kind, val=0):
    return bytes([kind, 0, val, 0, 0, 0, 0xFF, 0xFF])


def string_rec(s, flag=None):
    body = ustr(s, 2, flag)
    return rec(0x0207, body)


def rstring(r, c, xf, s, runs):
    body = pack("<HHH", r, c, xf) + ustr(s, 2) + pack("<H", len(runs))
    body += b"".join(pack("<HH", a, b) for a, b in runs)
    return rec(0x00D6, body)


STD_XFS = [0, 14, 22, 0x31, 164, 165, 999]


def globals_pre(extra=b"", datemode=0, codepage=1200, formats=None):
    out = b""
    if codepage is not None:
        out += rec(0x0042, pack("<H", codepage))
    out += rec(0x0022, pack("<H", datemode))
    for key, s in (formats or [(164, "yyyy-mm-dd hh:mm"), (165, '0.00 "kg"')]):
        out += fmt_rec(key, s)
    for k in STD_XFS:
        out += xf_rec(k)
    return out + extra


def raw_book(sheets, pre=None, sst=b"", post=b"", first=None):
    """sheets: (name, sheet_type, visibility, body) with body a whole
    substream; offsets in BOUNDSHEET are filled in here."""
    if pre is None:
        pre = globals_pre()
    head = first if first is not None else bof(5)
    bs_len = sum(4 + 6 + len(ustr(s[0], 1)) for s in sheets)
    off = len(head) + len(pre) + bs_len + len(sst) + len(post) + len(EOF)
    bsr = b""
    for name, typ, vis, body in sheets:
        bsr += rec(0x0085, pack("<iBB", off, vis, typ) + ustr(name, 1))
        off += len(body)
    return head + pre + bsr + sst + post + EOF + b"".join(s[3] for s in sheets)


def sheet(cells, r1=None, c1=None, extra=b""):
    body = bof(0x10)
    if r1 is not None:
        body += dims(r1, c1)
    return body + b"".join(cells) + extra + EOF


def sst_records(items, count=None):
    """items: list of pieces; bytes go into the current record, "|" starts a
    CONTINUE record. Returns the SST record followed by its CONTINUEs."""
    chunks = [b""]
    for it in items:
        if it == "|":
            chunks.append(b"")
        else:
            chunks[-1] += it
    return chunks


def sst(strings_pieces, nstr):
    chunks = sst_records(strings_pieces)
    out = rec(0x00FC, pack("<ii", nstr, nstr) + chunks[0])
    for ch in chunks[1:]:
        out += rec(0x003C, ch)
    return out


def raw_files():
    # every cell record type, with the formula result kinds
    cells = [
        label(0, 0, 0, "label record"),
        label(0, 1, 0, "Größe", flag=1),
        label(0, 2, 0, "Ωmega"),
        number(1, 0, 0, 2.75),
        number(1, 1, 1, 45000.5),
        number(1, 2, 4, 45000.25),
        number(1, 3, 5, 12.5),
        number(1, 4, 6, 7.0),
        number(1, 5, 3, 8.0),
        rk(2, 0, 0, 1234),
        rk(2, 1, 0, ("int100", 1234)),
        rk(2, 2, 0, ("float", 1.5)),
        rk(2, 3, 0, ("float100", 1.5)),
        rk(2, 4, 1, -5),
        rk(2, 5, 2, ("float", 45000.0)),
        mulrk(3, 1, 0, [1, ("int100", -250), ("float", 0.75), 3]),
        boolerr(4, 0, 0, 1, 0),
        boolerr(4, 1, 0, 0, 0),
        boolerr(4, 2, 0, 0x07, 1),
        boolerr(4, 3, 0, 0x2A, 1),
        boolerr(4, 4, 0, 0x99, 1),
        formula(5, 0, 0, fres_num(42.5)),
        formula(5, 1, 1, fres_num(45000.75)),
        formula(5, 2, 0, fres(1, 1)),
        formula(5, 3, 0, fres(2, 0x0F)),
        formula(5, 4, 0, fres(3)),
        formula(5, 5, 0, fres(0)),
        string_rec("formula text"),
        formula(6, 0, 0, fres(0)),
        rec(0x0207, pack("<H", 13) + b"\x00split "),
        rec(0x003C, b"\x01" + "över".encode("utf_16_le")),
        rec(0x003C, b"\x00 ok"),
        formula(6, 1, 0, fres(0)),
        rec(0x04BC, pack("<HHBBxBH", 6, 6, 1, 1, 1, 3) + b"\x1e\x01\x00"),
        string_rec("after SHRFMLA"),
        rstring(7, 0, 0, "rich string", [(0, 1), (5, 2)]),
        rec(0x0201, pack("<HHH", 7, 1, 0)),
        rec(0x00BE, pack("<HHHHH", 7, 2, 0, 0, 3)),
    ]
    sst_body = [ustr("one"), ustr("two")]
    book = raw_book([("Records", 0, 0, sheet(cells, 8, 6)),
                     ("SST", 0, 0, sheet([labelsst(0, 0, 0, 1), labelsst(0, 1, 0, 0)], 1, 2))],
                    sst=sst(sst_body, 2))
    put("raw/records.xls", book)

    # SST strings split across CONTINUE records in every way unpack_SST_table reads
    pieces = [
        ustr("short"),
        pack("<HB", 10, 0) + b"compr", "|", b"\x01" + "essed".encode("utf_16_le"),
        pack("<HB", 6, 1) + "Ωαβ".encode("utf_16_le"), "|", b"\x00def",
        pack("<HBH", 4, 8, 2) + b"rich" + pack("<HH", 0, 1), "|", pack("<HH", 2, 3),
        pack("<HBi", 5, 4, 6) + b"phone" + b"\x01\x02\x03", "|", b"\x04\x05\x06",
        pack("<HBHi", 3, 12, 1, 2) + b"\xe9t\xe9" + pack("<HH", 1, 1) + b"\x00\x00",
        ustr("last"),
    ]
    put("raw/sst_split.xls", raw_book([("Split", 0, 0, sheet([labelsst(0, c, 0, c) for c in range(7)], 1, 7))],
                                     sst=sst(pieces, 7)))
    put("raw/sst_short.xls", raw_book([("S", 0, 0, sheet([labelsst(0, 0, 0, 0)], 1, 1))],
                                     sst=sst([ustr("only")], 3)))
    put("raw/sst_index.xls", raw_book([("S", 0, 0, sheet([labelsst(0, 0, 0, 5)], 1, 1))],
                                     sst=sst([ustr("only")], 1)))

    # sheet kinds and visibility
    put("raw/sheet_types.xls", raw_book([
        ("Chart1", 2, 0, sheet([], 0, 0)),
        ("Data", 0, 0, sheet([number(0, 0, 0, 1.0)], 1, 1)),
        ("Macro", 1, 0, sheet([], 0, 0)),
        ("Hidden", 0, 1, sheet([number(0, 0, 0, 2.0)], 1, 1)),
        ("VeryHidden", 0, 2, sheet([], 0, 0)),
        ("VBA", 6, 0, sheet([], 0, 0)),
        ("Empty", 0, 0, sheet([])),
    ]))

    # records xlrd reports on, even without verbosity
    odd = [
        number(0, 0, 0, 1.0),
        bof(0x20) + rec(0x0203, pack("<HHHd", 9, 9, 0, 9.0)) + EOF,
        bof(0x40) + EOF,
        rec(0x00A0, pack("<HH", 1, 20)),
        rec(0x0225, pack("<H", 300)),
        rec(0x0099, pack("<HH", 8, 0)),
        rec(0x023E, pack("<HHHHxxHH", 0x06B6 | 0x800, 2, 1, 64, 0, 500)),
        rec(0x0041, pack("<HHHHB", 2, 4, 4, 2, 3)),
        number(1, 1, 0, 2.0),
    ]
    put("raw/oddities.xls", raw_book([("Odd", 0, 0, sheet(odd, 2, 2)),
                                      ("Odd2", 0, 0, sheet([rec(0x0225, pack("<HHH", 1, 2, 3)),
                                                            rec(0x00A0, pack("<HH", 3, 0)),
                                                            rec(0x023E, pack("<HHHHxxHH", 0x06B6, 0, 0, 64, 700, 0))], 0, 0))]))

    # globals variations
    put("raw/datemode1.xls", raw_book([("D", 0, 0, sheet([number(0, 0, 1, 1.5), number(0, 1, 1, 0.0)], 1, 2))],
                                     pre=globals_pre(datemode=1)))
    put("raw/datemode2.xls", raw_book([("D", 0, 0, sheet([], 0, 0))], pre=globals_pre(datemode=2)))
    for cp in (1252, 32768, 10007, 9999, 1999, 437, 424, None):
        name = "raw/codepage_%s.xls" % ("none" if cp is None else cp)
        put(name, raw_book([("C", 0, 0, sheet([label(0, 0, 0, "text")], 1, 1))], pre=globals_pre(codepage=cp)))
    put("raw/encrypted.xls", raw_book([("E", 0, 0, sheet([], 0, 0))],
                                     pre=globals_pre(extra=rec(0x002F, pack("<HHH", 1, 1, 1) + b"\x00" * 48))))
    put("raw/writeaccess.xls", raw_book([("W", 0, 0, sheet([], 0, 0))],
                                       pre=rec(0x005C, ustr("Ada Lovelace") + b" " * 20) + rec(0x008C, pack("<HH", 1, 49)) + globals_pre()))
    formats = [(164, "General"), (165, "[$-409]mmmm d, yyyy"), (166, '"Week "0'), (167, "d \"days\""),
               (168, "\\d0"), (169, "h0"), (170, "[h]:mm:ss"), (171, "0.00E+00"), (172, "_(* #,##0_)"),
               (173, "yyyy;@"), (174, "@"), (175, "[Red]0.0"), (176, "ss.0"), (177, "\"m\"0"),
               (178, "#,##0.00\\ \"€\""), (179, "[")]
    pre = globals_pre(formats=formats, extra=b"".join(xf_rec(k) for k, _ in formats))
    cells = [number(i // 4, i % 4, 7 + i, 45123.5) for i in range(len(formats))]
    put("raw/formats.xls", raw_book([("Formats", 0, 0, sheet(cells, 4, 4))], pre=pre))

    # BOF problems
    put("raw/workspace.xls", raw_book([], first=bof(0x100)))
    put("raw/chart_bof.xls", raw_book([], first=bof(0x20)))
    put("raw/biff_unknown.xls", raw_book([], first=bof(5, vers=0x0700)))
    put("raw/biff5_old.xls", rec(0x0809, pack("<HHHH", 0x0500, 5, 2412, 1993)) + b"\x00" * 40)
    put("raw/bof_len.xls", rec(0x0809, b"\x00\x06") + b"\x00" * 30)
    put("raw/bof_short.xls", pack("<HH", 0x0809, 16) + b"\x00\x06\x05\x00")
    put("raw/bof_cut.xls", b"\x09\x08\x10")
    put("raw/no_sheet_bof.xls", raw_book([("S", 0, 0, number(0, 0, 0, 1.0) + EOF)]))
    put("raw/sheet_no_eof.xls", raw_book([("S", 0, 0, bof(0x10) + number(0, 0, 0, 1.0))]))
    put("raw/globals_no_eof.xls", bof(5) + globals_pre())
    put("raw/formula_kind.xls", raw_book([("F", 0, 0, sheet([formula(0, 0, 0, fres(4))], 1, 1))]))
    put("raw/formula_nostring.xls", raw_book([("F", 0, 0, sheet([formula(0, 0, 0, fres(0)), number(0, 1, 0, 1.0)], 1, 2))]))
    put("raw/formula_shr_nostring.xls", raw_book([("F", 0, 0, sheet([
        formula(0, 0, 0, fres(0)), rec(0x04BC, pack("<HHBBxBH", 0, 0, 0, 0, 1, 3) + b"\x1e\x01\x00"),
        number(0, 1, 0, 1.0)], 1, 2))]))
    put("raw/string_long.xls", raw_book([("F", 0, 0, sheet([formula(0, 0, 0, fres(0)),
                                                            rec(0x0207, pack("<H", 2) + b"\x00abc")], 1, 1))]))
    put("raw/string_cont.xls", raw_book([("F", 0, 0, sheet([formula(0, 0, 0, fres(0)),
                                                            rec(0x0207, pack("<H", 6) + b"\x00abc"),
                                                            number(0, 1, 0, 1.0)], 1, 2))]))
    put("raw/xf_missing.xls", raw_book([("X", 0, 0, sheet([number(0, 0, 40, 1.0)], 1, 1))]))
    put("raw/biff_stream.xls", raw_book([("Data", 0, 0, sheet([label(0, 0, 0, "raw stream, no OLE2")], 1, 1))]))
    return book


# ------------------------------------------------------------ OLE2 files

def dirent(name, etype, child=-1, left=-1, right=-1, first=-2, size=0):
    if name:
        nb = name.encode("utf_16_le") + b"\x00\x00"
    else:
        nb = b""
    e = nb.ljust(64, b"\x00")
    e += pack("<HBBiii", len(nb), etype, 1, left, right, child)
    e += b"\x00" * 16 + pack("<I", 0) + b"\x00" * 16
    e += pack("<ii", first, size) + b"\x00" * 4
    assert len(e) == 128
    return e


def ole(streams, order=None, mini=(), ssz=9, sssz=6, marker=b"\xfe\xff", patch=None, extra_dirs=(), tail=b""):
    """streams: (name, bytes) kept in regular sectors; mini: (name, bytes)
    kept in the short-stream container. order permutes the data sectors."""
    sec = 512
    data_secs = []  # (stream index, sector index)
    blobs = []
    for i, (name, b) in enumerate(streams):
        n = (len(b) + sec - 1) // sec
        blobs.append(b + b"\x00" * (n * sec - len(b)))
        for k in range(n):
            data_secs.append((i, k))
    sscs = b""
    mini_first = []
    for name, b in mini:
        mini_first.append(len(sscs) // 64)
        n = (len(b) + 63) // 64
        sscs += b + b"\x00" * (n * 64 - len(b))
    ssat = []
    for (name, b), f in zip(mini, mini_first):
        n = (len(b) + 63) // 64
        for k in range(n):
            ssat.append(f + k + 1 if k < n - 1 else -2)
    sscs_secs = (len(sscs) + sec - 1) // sec
    ssat_secs = (len(ssat) * 4 + sec - 1) // sec
    ndir = 1 + len(streams) + len(mini) + len(extra_dirs)
    dir_secs = (ndir * 128 + sec - 1) // sec
    if order is not None:
        data_secs = [data_secs[i] for i in order]
    layout = ["sat"] + ["dir"] * dir_secs + ["ssat"] * ssat_secs + ["sscs"] * sscs_secs + data_secs
    nsat = 1
    total = len(layout)
    assert total <= 128
    sat = [-1] * 128
    sat[0] = -3
    pos_of = {}
    for p, what in enumerate(layout):
        pos_of.setdefault(what if isinstance(what, str) else what, []).append(p)
    for kind in ("dir", "ssat", "sscs"):
        ps = pos_of.get(kind, [])
        for j, p in enumerate(ps):
            sat[p] = ps[j + 1] if j + 1 < len(ps) else -2
    first_of = {}
    for i, (name, b) in enumerate(streams):
        n = len(blobs[i]) // sec
        ps = [layout.index((i, k)) for k in range(n)]
        for j, p in enumerate(ps):
            sat[p] = ps[j + 1] if j + 1 < len(ps) else -2
        first_of[i] = ps[0] if ps else -2
    entries = []
    kids = list(range(1, ndir))
    dir_first = pos_of["dir"][0]
    root_first = pos_of["sscs"][0] if sscs_secs else -2
    entries.append(dirent("Root Entry", 5, child=kids[0] if kids else -1, first=root_first, size=len(sscs)))
    did = 1
    for i, (name, b) in enumerate(streams):
        entries.append(dirent(name, 2, right=did + 1 if did + 1 < ndir else -1, first=first_of[i], size=len(b)))
        did += 1
    for (name, b), f in zip(mini, mini_first):
        entries.append(dirent(name, 2, right=did + 1 if did + 1 < ndir else -1, first=f, size=len(b)))
        did += 1
    for name, etype in extra_dirs:
        entries.append(dirent(name, etype, right=did + 1 if did + 1 < ndir else -1))
        did += 1
    dirb = b"".join(entries)
    dirb += b"\x00" * (dir_secs * sec - len(dirb))
    ssatb = b"".join(pack("<i", x) for x in ssat)
    ssatb += pack("<i", -1) * ((ssat_secs * sec - len(ssatb)) // 4)
    sscsb = sscs + b"\x00" * (sscs_secs * sec - len(sscs))
    if patch:
        sat = patch(sat, layout, entries)
    body = b""
    di = si = ci = 0
    for what in layout:
        if what == "sat":
            body += b"".join(pack("<i", x) for x in sat)
        elif what == "dir":
            body += dirb[di * sec:(di + 1) * sec]
            di += 1
        elif what == "ssat":
            body += ssatb[si * sec:(si + 1) * sec]
            si += 1
        elif what == "sscs":
            body += sscsb[ci * sec:(ci + 1) * sec]
            ci += 1
        else:
            i, k = what
            body += blobs[i][k * sec:(k + 1) * sec]
    msat = [0] + [-1] * 108
    head = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" + b"\x00" * 16
    head += pack("<HH", 0x3E, 3) + marker + pack("<HH", ssz, sssz) + b"\x00" * 6
    head += pack("<iiiiiiiii", 0, nsat, dir_first, 0, 4096,
                 pos_of["ssat"][0] if ssat_secs else -2, ssat_secs, -2, 0)
    head += b"".join(pack("<i", x) for x in msat)
    assert len(head) == 512
    return head + body + tail


def pad_stream(b, size):
    return b + b"\x00" * (size - len(b))


def ole_files(records_book, basic):
    wbk = pad_stream(records_book, 4608)
    junk = b"JUNK" * 256
    n = (len(wbk) + 511) // 512
    m = 2
    order = []
    for k in range(n):
        order.append(k)
        if k < m:
            order.append(n + k)
    put("ole/split.xls", ole([("Workbook", wbk), ("Junk", junk[:1024])], order=order))
    put("ole/plain.xls", ole([("Workbook", wbk)]))
    small = raw_book([("Mini", 0, 0, sheet([label(0, 0, 0, "from the short-stream container"), rk(0, 1, 0, 99)], 1, 2))])
    put("ole/mini.xls", ole([], mini=[("Workbook", small)]))
    put("ole/book.xls", ole([("Book", wbk)]))
    put("ole/upper.xls", ole([("WORKBOOK", wbk)]))
    put("ole/both.xls", ole([("Book", pad_stream(small, 4096)), ("Workbook", wbk)]))
    put("ole/no_workbook.xls", ole([("Data", wbk)]))
    put("ole/storage.xls", ole([("Other", wbk)], extra_dirs=[("Workbook", 1)]))
    put("ole/odd_entry.xls", ole([("Other", wbk)], extra_dirs=[("Workbook", 3)]))
    put("ole/sector_shift.xls", ole([("Workbook", wbk)], ssz=21))
    put("ole/short_shift.xls", ole([("Workbook", wbk)], sssz=10))
    put("ole/big_endian.xls", ole([("Workbook", wbk)], marker=b"\xff\xfe"))

    def loop(sat, layout, entries):
        ps = [p for p, w in enumerate(layout) if isinstance(w, tuple) and w[0] == 0]
        sat[ps[-1]] = ps[1]
        return sat
    put("ole/sat_loop.xls", ole([("Workbook", wbk)], patch=loop))

    def short(sat, layout, entries):
        ps = [p for p, w in enumerate(layout) if isinstance(w, tuple) and w[0] == 0]
        sat[ps[3]] = -2
        return sat
    put("ole/chain_short.xls", ole([("Workbook", wbk)], patch=short))

    def oob(sat, layout, entries):
        ps = [p for p, w in enumerate(layout) if isinstance(w, tuple) and w[0] == 0]
        sat[ps[2]] = 200
        return sat
    put("ole/chain_oob.xls", ole([("Workbook", wbk)], patch=oob))

    # the directory sector follows the SAT sector; patch the Workbook entry
    good = ole([("Workbook", wbk)])
    dir_pos = 512 + 512

    def with_size(b, size, first=None):
        b = bytearray(b)
        off = dir_pos + 128 + 120
        b[off:off + 4] = pack("<i", size)
        if first is not None:
            b[off - 4:off] = pack("<i", first)
        return bytes(b)
    put("ole/size_large.xls", with_size(good, 999999))
    put("ole/size_small.xls", with_size(good, 4096))
    put("ole/size_short_stream.xls", with_size(good, 2000))
    put("ole/neg_first.xls", with_size(good, 4608, first=-1))
    put("ole/tail.xls", ole([("Workbook", wbk)], tail=b"\x00" * 100))

    def ssat_loop(sat, layout, entries):
        p = layout.index("ssat")
        sat[p] = p
        return sat
    put("ole/ssat_loop.xls", ole([], mini=[("Workbook", small)], patch=ssat_loop))

    # damaged copies of an xlwt file
    for cut in (7, 40, 600, 3000, 5000):
        put("bad/cut_%d.xls" % cut, basic[:cut])
    put("bad/empty.xls", b"")
    put("bad/one_byte.xls", b"\x09")
    put("bad/text.xls", b"name,qty\nbolt,12\n")
    put("bad/html.xls", b"<html><body><table><tr><td>1</td></tr></table></body></html>\n")
    put("bad/signature_only.xls", b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1")
    flipped = bytearray(basic)
    flipped[0] ^= 0xFF
    put("bad/flipped.xls", bytes(flipped))


def zip_bytes(names):
    import io
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_STORED) as z:
        for n in names:
            info = zipfile.ZipInfo(n, date_time=(2024, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o644 << 16
            z.writestr(info, b"<x/>")
    return buf.getvalue()


def zip_files():
    put("zip/report.xlsx", zip_bytes(["[Content_Types].xml", "_rels/.rels", "xl/workbook.xml", "xl/worksheets/sheet1.xml"]))
    put("zip/report.xlsb", zip_bytes(["[Content_Types].xml", "xl/workbook.bin"]))
    put("zip/sheet.ods", zip_bytes(["mimetype", "content.xml", "styles.xml"]))
    put("zip/archive.zip", zip_bytes(["readme.txt", "data/rows.csv"]))
    put("zip/windows.xlsx", zip_bytes(["XL\\Workbook.XML"]))
    full = zip_bytes(["xl/workbook.xml"])
    put("zip/commented.xlsx", full[:-2] + pack("<H", 9) + b"a comment")
    put("zip/truncated.xlsx", full[:60])
    put("zip/empty.zip", zip_bytes([]))


# ------------------------------------------------------------ jobs

def jobs():
    j = []
    sec = lambda s: j.append("# " + s)  # noqa: E731
    sec("xlwt workbooks: every cell, as open_workbook reads it")
    for f in ["basic", "sales", "numbers", "text", "d1900", "d1904", "formulas", "owner", "sparse"]:
        j.append("dump books/%s.xls" % f)
    j.append("dump books/sparse.xls ragged")
    j.append("dump books/split_pair.xls")
    sec("formatting_info=True: fonts, formats, XFs, merges, rows and columns")
    for f in ["layout", "sales", "sparse", "basic"]:
        j.append("fmt books/%s.xls" % f)
    j.append("dump books/layout.xls")
    sec("BIFF8 streams built record by record")
    for f in ["records", "sst_split", "sst_short", "sst_index", "sheet_types", "oddities", "datemode1",
              "datemode2", "codepage_1252", "codepage_32768", "codepage_10007", "codepage_9999",
              "codepage_1999", "codepage_437", "codepage_424", "codepage_none", "encrypted", "writeaccess", "formats",
              "workspace", "chart_bof", "biff_unknown", "biff5_old", "bof_len", "bof_short", "bof_cut",
              "no_sheet_bof", "sheet_no_eof", "globals_no_eof", "formula_kind", "formula_nostring",
              "formula_shr_nostring", "string_long", "string_cont", "xf_missing", "biff_stream"]:
        j.append("dump raw/%s.xls" % f)
    j.append("dump raw/sheet_types.xls ondemand")
    j.append("fmt raw/records.xls")
    sec("compound documents built sector by sector")
    for f in ["plain", "split", "mini", "book", "upper", "both", "no_workbook", "storage", "odd_entry",
              "sector_shift", "short_shift", "big_endian", "sat_loop", "chain_short", "chain_oob",
              "size_large", "size_small", "size_short_stream", "neg_first", "tail", "ssat_loop"]:
        j.append("dump ole/%s.xls" % f)
    sec("damaged files")
    for f in ["cut_7", "cut_40", "cut_600", "cut_3000", "cut_5000", "empty", "one_byte", "text", "html",
              "signature_only", "flipped"]:
        j.append("dump bad/%s.xls" % f)
    sec("file format sniffing")
    for f in ["report.xlsx", "report.xlsb", "sheet.ods", "archive.zip", "windows.xlsx", "commented.xlsx",
              "truncated.xlsx", "empty.zip"]:
        j.append("dump zip/%s" % f)
    j.append("!inspect books/basic.xls zip/report.xlsx zip/report.xlsb zip/sheet.ods zip/archive.zip "
             "zip/truncated.xlsx raw/records.xls bad/text.xls bad/empty.xls")
    sec("xldate conversions")
    for x, m in [("0.0", 0), ("0.5", 0), ("1.0", 0), ("60.0", 0), ("61.0", 0), ("61.5", 0), ("43831.75", 0),
                 ("43831.999994", 0), ("43831.9999999", 0), ("2958465.5", 0), ("2958466.0", 0),
                 ("1.0", 1), ("1461.0", 1), ("2957003.0", 1), ("-1.0", 0), ("1.5", 2), ("45351.123456789", 0),
                 ("0.000005787", 0), ("100000000.0", 1), ("59.99", 0)]:
        j.append("xldate %s %d" % (x, m))
    for y, mo, d, m in [(2024, 2, 29, 0), (2023, 2, 29, 0), (1900, 3, 1, 0), (1900, 2, 28, 0),
                        (1904, 1, 1, 1), (1904, 1, 2, 1), (0, 0, 0, 0), (1899, 12, 31, 0),
                        (10000, 1, 1, 0), (2024, 13, 1, 0), (2024, 4, 31, 1), (2000, 2, 29, 1), (2024, 1, 1, 3)]:
        j.append("fromdate %d %d %d %d" % (y, mo, d, m))
    for h, mi, s in [(0, 0, 0), (12, 0, 0), (23, 59, 59), (6, 30, 15), (24, 0, 0), (1, 60, 0)]:
        j.append("fromtime %d %d %d" % (h, mi, s))
    sec("cell and column names")
    j.append("names 0 1 25 26 27 51 52 255 701 702")
    j.append("cells 0,0 9,2 65535,255 99,26")
    j.append("ranges 0,1,0,1 0,3,0,2 4,5,26,28 0,65536,0,256")
    sec("programs on top of xlrd")
    j.append("!csv books/sales.xls Q1")
    j.append("!csv books/sales.xls Q2")
    j.append("!csv books/basic.xls Stock")
    j.append("!csv books/text.xls Unicode")
    j.append("!csv books/sales.xls Missing")
    j.append("!report books/sales.xls")
    j.append("!report books/basic.xls")
    j.append("!find books/sales.xls Widget")
    j.append("!find books/text.xls äöü")
    with open(os.path.join(DATA, "jobs.txt"), "w") as f:
        f.write("\n".join(j) + "\n")


def main():
    basic = book_basic()
    book_sales()
    book_numbers()
    book_text()
    book_1900()
    book_1904()
    book_layout()
    book_sparse()
    book_formulas()
    book_owner()
    book_split_pair()
    records = raw_files()
    ole_files(records, basic)
    zip_files()
    jobs()
    with open(os.path.join(DATA, "files.txt"), "w") as f:
        f.write("\n".join(FILES) + "\n")
    print("%d files" % len(FILES))


main()
