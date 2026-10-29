"""Writes data/: the workbooks the jobs read, each shaped like a file a
real program wrote, and data/jobs.txt, one job per line. oracle.py runs
each job on openpyxl and pandas, mini_read_excel.kara on its own port.

Most workbooks are built here part by part, as the program that wrote them
would have (Excel, Excel for Mac, the .NET Open XML SDK, a reporting tool
with a stale dimension), since openpyxl itself writes only one shape. One
is written by openpyxl. Every zip entry gets the same timestamp, so the
bytes are the same on every run.

Run: python3 -s -P -B mk.py"""
import datetime
import io
import os
import re
import shutil
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
shutil.rmtree(DATA, ignore_errors=True)
os.makedirs(DATA)

STAMP = (2024, 10, 1, 9, 30, 0)
MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
RNS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
DOC = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/"


def put_zip(name, parts, method=zipfile.ZIP_DEFLATED):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for path, text in parts:
            info = zipfile.ZipInfo(path, STAMP)
            info.compress_type = method
            data = text if isinstance(text, bytes) else text.encode("utf-8")
            z.writestr(info, data)
    with open(os.path.join(DATA, name), "wb") as f:
        f.write(buf.getvalue())


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def col_letter(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def content_types(sheets, strings=True, prefix=""):
    over = [
        f'<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        f'<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
    ]
    if strings:
        over.append('<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>')
    for i in range(sheets):
        over.append(f'<Override PartName="/xl/worksheets/sheet{i + 1}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>')
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
            f'<Types xmlns="{CT}"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            f'<Default Extension="xml" ContentType="application/xml"/>' + "".join(over) + "</Types>")


ROOT_RELS = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<Relationships xmlns="{PKG}">'
             f'<Relationship Id="rId1" Type="{DOC}officeDocument" Target="xl/workbook.xml"/></Relationships>')


def workbook_rels(sheets, strings=True):
    rels = [f'<Relationship Id="rId{i + 1}" Type="{DOC}worksheet" Target="worksheets/sheet{i + 1}.xml"/>' for i in range(sheets)]
    n = sheets
    rels.append(f'<Relationship Id="rId{n + 1}" Type="{DOC}styles" Target="styles.xml"/>')
    if strings:
        rels.append(f'<Relationship Id="rId{n + 2}" Type="{DOC}sharedStrings" Target="sharedStrings.xml"/>')
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<Relationships xmlns="{PKG}">' + "".join(rels) + "</Relationships>"


def workbook(names, date1904=False, defined="", states=None):
    pr = '<workbookPr date1904="1"/>' if date1904 else '<workbookPr defaultThemeVersion="164011"/>'
    sh = []
    for i, n in enumerate(names):
        st = ""
        if states and states[i] != "visible":
            st = f' state="{states[i]}"'
        sh.append(f'<sheet name="{esc(n)}" sheetId="{i + 1}"{st} r:id="rId{i + 1}"/>')
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
            f'<workbook xmlns="{MAIN}" xmlns:r="{RNS}">{pr}<bookViews><workbookView xWindow="0" yWindow="0" windowWidth="28800" windowHeight="12300"/></bookViews>'
            f'<sheets>{"".join(sh)}</sheets>{defined}<calcPr calcId="191029"/></workbook>')


def styles(numfmts, xfs):
    """numfmts: [(id, code)]; xfs: [numFmtId] for cellXfs in order."""
    nf = ""
    if numfmts:
        nf = f'<numFmts count="{len(numfmts)}">' + "".join(
            f'<numFmt numFmtId="{i}" formatCode="{esc(c).replace(chr(34), "&quot;")}"/>' for i, c in numfmts) + "</numFmts>"
    xf = "".join(f'<xf numFmtId="{i}" fontId="0" fillId="0" borderId="0" xfId="0"' +
                 (' applyNumberFormat="1"' if i else "") + "/>" for i in xfs)
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<styleSheet xmlns="{MAIN}">{nf}'
            '<fonts count="1"><font><sz val="11"/><name val="Calibri"/><family val="2"/></font></fonts>'
            '<fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills>'
            '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
            '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
            f'<cellXfs count="{len(xfs)}">{xf}</cellXfs>'
            '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>')


class Strings:
    """A shared string table in first-use order, as Excel builds it."""

    def __init__(self):
        self.items = []
        self.index = {}
        self.count = 0

    def add(self, s, xml=None):
        self.count += 1
        key = xml or s
        if key not in self.index:
            self.index[key] = len(self.items)
            self.items.append(xml or f"<t{' xml:space=\"preserve\"' if s != s.strip() or chr(10) in s else ''}>{esc(s)}</t>")
        return self.index[key]

    def xml(self):
        body = "".join(f"<si>{x}</si>" for x in self.items)
        return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
                f'<sst xmlns="{MAIN}" count="{self.count}" uniqueCount="{len(self.items)}">{body}</sst>')


def sheet(rows, dim=None, merges=(), cols="", extra="", prefix="", ns_decl=None):
    p = prefix
    out = []
    for r in rows:
        out.append(r)
    d = f'<{p}dimension ref="{dim}"/>' if dim else ""
    m = ""
    if merges:
        m = f'<{p}mergeCells count="{len(merges)}">' + "".join(f'<{p}mergeCell ref="{x}"/>' for x in merges) + f"</{p}mergeCells>"
    decl = ns_decl if ns_decl is not None else f'xmlns="{MAIN}" xmlns:r="{RNS}"'
    root = f"{p}worksheet"
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<{root} {decl}>{d}'
            f'<{p}sheetViews><{p}sheetView workbookViewId="0"/></{p}sheetViews><{p}sheetFormatPr defaultRowHeight="15"/>{cols}'
            f'<{p}sheetData>{"".join(out)}</{p}sheetData>{m}{extra}'
            f'<{p}pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/></{root}>')


def row(n, cells, spans=None, attrs=""):
    sp = f' spans="{spans}"' if spans else ""
    return f'<row r="{n}"{sp}{attrs}>' + "".join(cells) + "</row>"


def excel_serial(d, epoch=datetime.datetime(1899, 12, 30)):
    if isinstance(d, datetime.date) and not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)
    delta = d - epoch
    return delta.days + delta.seconds / 86400


def num(v):
    if isinstance(v, float):
        r = repr(v)
        if r.endswith(".0"):
            r = r[:-2]
        return r
    return str(v)


class Lcg:
    def __init__(self, seed):
        self.s = seed

    def next(self, n):
        self.s = (self.s * 6364136223846793005 + 1442695040888963407) % (1 << 64)
        return (self.s >> 33) % n


# ---------------------------------------------------------------- 1
# sales_q3.xlsx: a sales team's quarter, saved by Excel 365 on Windows.
# Orders has a shared formula down Total with its cached values, a
# percentage that is often blank, a [h]:mm duration, booleans, an error
# in one Total, notes with rich text runs, a _x000D_ escape and a
# number typed as text with its leading zeros, and one blank row.
# Summary is a printed report: a merged title, a note, a blank row, then
# the table with a totals row. Lookups holds two tables side by side.
S = Strings()
fmts = [(164, '"$"#,##0.00'), (165, "[h]:mm"), (166, "yyyy\\-mm\\-dd"), (167, '[$-409]mmmm\\ d\\,\\ yyyy;@')]
# style ids: 0 general, 1 date(14), 2 money(164), 3 pct(9), 4 dur(165), 5 iso date(166), 6 long date(167), 7 int with sep (3), 8 text(49)
xfs = [0, 14, 164, 9, 165, 166, 167, 3, 49]
r = Lcg(2024)
reps = ["Ana Lima", "Bo Chen", "Cy Okafor", "Dee Varga"]
regions = ["North", "South", "East", "West"]
notes = [None, None, None, "rush", "call first", None, "repeat customer", None]
hdr = ["Order ID", "Order Date", "Region", "Rep", "Units", "Unit Price", "Discount", "Total", "Shipped", "Ship Time", "Notes"]
rows = [row(1, [f'<c r="{col_letter(i + 1)}1" t="s"><v>{S.add(h)}</v></c>' for i, h in enumerate(hdr)], "1:11")]
rn = 2
first = None
for i in range(30):
    if i == 17:
        rn += 1  # a row deleted by hand leaves nothing behind but a gap
    oid = 10301 + i
    d = datetime.date(2024, 7, 1) + datetime.timedelta(days=i * 3 + r.next(3))
    reg = regions[r.next(4)]
    rep = reps[r.next(4)]
    units = 1 + r.next(40)
    price = [12.5, 19.99, 7.25, 149.0, 0.85][r.next(5)]
    disc = [None, None, 0.05, 0.1, 0.15][r.next(5)]
    total = units * price * (1 - (disc or 0))
    shipped = r.next(4) != 0
    hours = r.next(70) + r.next(60) / 60
    c = [f'<c r="A{rn}"><v>{oid}</v></c>',
         f'<c r="B{rn}" s="1"><v>{excel_serial(d):g}</v></c>',
         f'<c r="C{rn}" t="s"><v>{S.add(reg)}</v></c>',
         f'<c r="D{rn}" t="s"><v>{S.add(rep)}</v></c>',
         f'<c r="E{rn}"><v>{units}</v></c>',
         f'<c r="F{rn}" s="2"><v>{num(price)}</v></c>']
    c.append(f'<c r="G{rn}" s="3"><v>{num(disc)}</v></c>' if disc is not None else f'<c r="G{rn}" s="3"/>')
    if i == 0:
        c.append(f'<c r="H{rn}" s="2"><f t="shared" ref="H2:H32" si="0">E2*F2*(1-G2)</f><v>{num(total)}</v></c>')
    elif i == 11:
        c.append(f'<c r="H{rn}" s="2" t="e"><f>VLOOKUP(A{rn},Lookups!A:B,2,FALSE)</f><v>#N/A</v></c>')
    else:
        c.append(f'<c r="H{rn}" s="2"><f t="shared" si="0"/><v>{num(total)}</v></c>')
    c.append(f'<c r="I{rn}" t="b"><v>{1 if shipped else 0}</v></c>')
    c.append(f'<c r="J{rn}" s="4"><v>{num(hours / 24)}</v></c>')
    note = notes[r.next(8)]
    if i == 4:
        c.append(f'<c r="K{rn}" t="s"><v>{S.add("x", "<r><rPr><b/><sz val=\"11\"/></rPr><t>URGENT</t></r><r><rPr><sz val=\"11\"/></rPr><t xml:space=\"preserve\"> - ship today</t></r>")}</v></c>')
    elif i == 9:
        c.append(f'<c r="K{rn}" t="s"><v>{S.add("Dock 4_x000D_" + chr(10) + "Gate B")}</v></c>')
    elif i == 13:
        c.append(f'<c r="K{rn}" s="8" t="s"><v>{S.add("007")}</v></c>')
    elif i == 21:
        c.append(f'<c r="K{rn}" t="s"><v>{S.add("Fish & Chips Ltd <wholesale>")}</v></c>')
    elif note:
        c.append(f'<c r="K{rn}" t="s"><v>{S.add(note)}</v></c>')
    rows.append(row(rn, c, "1:11"))
    rn += 1
last = rn - 1
orders = sheet(rows, dim=f"A1:K{last}", cols='<cols><col min="1" max="1" width="10.7" customWidth="1"/><col min="11" max="11" width="24" customWidth="1"/></cols>')

title = S.add("Q3 Sales Summary")
srows = [row(1, [f'<c r="A1" t="s"><v>{title}</v></c>', '<c r="B1"/>', '<c r="C1"/>', '<c r="D1"/>'], "1:4", ' ht="21" customHeight="1"'),
         row(2, [f'<c r="A2" t="s"><v>{S.add("Generated 2024-10-01 from the CRM export")}</v></c>'], "1:4"),
         row(4, [f'<c r="{x}4" t="s"><v>{S.add(h)}</v></c>' for x, h in zip("ABCD", ["Region", "Orders", "Revenue", "Share"])], "1:4")]
totals = {}
for i in range(30):
    pass
rev = [38211.4, 27450.0, 19980.55, 31002.1]
cnt = [9, 6, 7, 8]
tot = sum(rev)
for k, reg in enumerate(regions):
    n = 5 + k
    srows.append(row(n, [f'<c r="A{n}" t="s"><v>{S.add(reg)}</v></c>',
                         f'<c r="B{n}"><f>COUNTIF(Orders!C:C,A{n})</f><v>{cnt[k]}</v></c>',
                         f'<c r="C{n}" s="2"><f>SUMIF(Orders!C:C,A{n},Orders!H:H)</f><v>{num(rev[k])}</v></c>',
                         f'<c r="D{n}" s="3"><f>C{n}/$C$9</f><v>{num(rev[k] / tot)}</v></c>'], "1:4"))
srows.append(row(9, [f'<c r="A9" t="s"><v>{S.add("Total")}</v></c>',
                     f'<c r="B9"><f>SUM(B5:B8)</f><v>30</v></c>',
                     f'<c r="C9" s="2"><f>SUM(C5:C8)</f><v>{num(tot)}</v></c>',
                     f'<c r="D9" s="3"><f>SUM(D5:D8)</f><v>1</v></c>'], "1:4"))
summary = sheet(srows, dim="A1:D9", merges=["A1:D1"])

lrows = [row(1, [f'<c r="A1" t="s"><v>{S.add("Code")}</v></c>', f'<c r="B1" t="s"><v>{S.add("Region")}</v></c>',
                 f'<c r="D1" t="s"><v>{S.add("Rep")}</v></c>', f'<c r="E1" t="s"><v>{S.add("Quota")}</v></c>', f'<c r="F1" t="s"><v>{S.add("Start")}</v></c>'], "1:6")]
codes = [("N", "North"), ("S", "South"), ("E", "East"), ("W", "West")]
quota = [120000, 95000, 101500.5, 88000]
starts = [datetime.date(2019, 4, 1), datetime.date(2021, 1, 11), datetime.date(2016, 9, 5), datetime.date(1900, 2, 28)]
for k in range(4):
    n = k + 2
    lrows.append(row(n, [f'<c r="A{n}" t="s"><v>{S.add(codes[k][0])}</v></c>', f'<c r="B{n}" t="s"><v>{S.add(codes[k][1])}</v></c>',
                         f'<c r="D{n}" t="s"><v>{S.add(reps[k])}</v></c>', f'<c r="E{n}" s="7"><v>{num(quota[k])}</v></c>',
                         f'<c r="F{n}" s="6"><v>{excel_serial(starts[k]) if k != 3 else 59:g}</v></c>'], "1:6"))
lrows.append(row(6, [f'<c r="A6" t="s"><v>{S.add("C")}</v></c>', f'<c r="B6" t="s"><v>{S.add("Central")}</v></c>'], "1:6"))
lookups = sheet(lrows, dim="A1:F6")

defined = ('<definedNames><definedName name="_xlnm._FilterDatabase" localSheetId="0" hidden="1">Orders!$A$1:$K$32</definedName>'
           '<definedName name="Quotas">Lookups!$D$1:$E$5</definedName></definedNames>')
put_zip("sales_q3.xlsx", [
    ("[Content_Types].xml", content_types(3)),
    ("_rels/.rels", ROOT_RELS),
    ("xl/workbook.xml", workbook(["Orders", "Summary", "Lookups"], defined=defined)),
    ("xl/_rels/workbook.xml.rels", workbook_rels(3)),
    ("xl/worksheets/sheet1.xml", orders),
    ("xl/worksheets/sheet2.xml", summary),
    ("xl/worksheets/sheet3.xml", lookups),
    ("xl/styles.xml", styles(fmts, xfs)),
    ("xl/sharedStrings.xml", S.xml()),
])

# ---------------------------------------------------------------- 2
# stock_mac.xlsx: a warehouse count from Excel 2011 for Mac, on the 1904
# date system, with every kind of number format a date test has to get
# right or wrong: builtin dates, times and datetimes, a builtin id the
# table does not have (31, an East Asian date), and custom codes with an
# escaped dash, a locale prefix, a colour, a literal, minutes:seconds and
# a negative-in-red that is not a date at all.
S = Strings()
fmts = [(164, "yyyy\\-mm\\-dd"), (165, "[$-F800]dddd\\,\\ mmmm\\ dd\\,\\ yyyy"), (166, "[Red]#,##0"),
        (167, '"Bin "0'), (168, "mm:ss.0"), (169, "0.00_);[Red]\\(0.00\\)"), (170, "d/m/yyyy h:mm:ss"), (171, "General")]
# ids: 0 gen, 1 date 14, 2 time 21, 3 dt 22, 4 id31, 5 iso 164, 6 long 165, 7 red 166, 8 bin 167, 9 mmss 168, 10 neg 169, 11 dmy 170, 12 hmm 20, 13 "General" custom
xfs = [0, 14, 21, 22, 31, 164, 165, 166, 167, 168, 169, 170, 20, 171]
mac = datetime.datetime(1904, 1, 1)
hdr = ["SKU", "Counted", "At", "Last move", "Lot date", "Expires", "Received", "On hand", "Bin", "Cycle", "Variance", "Logged", "Shift start", "Batch"]
rows = [row(1, [f'<c r="{col_letter(i + 1)}1" t="s"><v>{S.add(h)}</v></c>' for i, h in enumerate(hdr)], "1:14")]
r = Lcg(1904)
for i in range(12):
    n = i + 2
    d = datetime.datetime(2023, 11, 6) + datetime.timedelta(days=i, hours=r.next(10) + 7, minutes=r.next(60), seconds=r.next(60))
    c = [f'<c r="A{n}" t="s"><v>{S.add("SKU-%04d" % (311 + i * 7))}</v></c>',
         f'<c r="B{n}" s="1"><v>{excel_serial(d.date(), mac):g}</v></c>',
         f'<c r="C{n}" s="2"><v>{num((d - datetime.datetime(d.year, d.month, d.day)).seconds / 86400)}</v></c>',
         f'<c r="D{n}" s="3"><v>{num(excel_serial(d, mac))}</v></c>',
         f'<c r="E{n}" s="4"><v>{excel_serial(d.date(), mac) - 40:g}</v></c>',
         f'<c r="F{n}" s="5"><v>{excel_serial(d.date(), mac) + 365:g}</v></c>',
         f'<c r="G{n}" s="6"><v>{excel_serial(d.date(), mac) - 3:g}</v></c>',
         f'<c r="H{n}" s="7"><v>{r.next(900) - 50}</v></c>',
         f'<c r="I{n}" s="8"><v>{100 + r.next(40)}</v></c>',
         f'<c r="J{n}" s="9"><v>{num(round((r.next(5000) + 0.5) / 864000, 9))}</v></c>',
         f'<c r="K{n}" s="10"><v>{num((r.next(400) - 200) / 8)}</v></c>',
         f'<c r="L{n}" s="11"><v>{num(excel_serial(d, mac) + 0.25)}</v></c>',
         f'<c r="M{n}" s="12"><v>{num([0.25, 0.5833333333333334, 0.9166666666666666][i % 3])}</v></c>',
         f'<c r="N{n}" s="13"><v>{4400 + i}</v></c>']
    rows.append(row(n, c, "1:14"))
# a midnight-exact time of 0, a first-day date, the 1904 epoch itself
rows.append(row(14, [f'<c r="A14" t="s"><v>{S.add("SKU-EDGE")}</v></c>', '<c r="B14" s="1"><v>0</v></c>', '<c r="C14" s="2"><v>0</v></c>',
                     '<c r="D14" s="3"><v>1.5</v></c>', '<c r="E14" s="4"><v>0</v></c>', '<c r="F14" s="5"><v>-1</v></c>'], "1:14"))
stock = sheet(rows, dim="A1:N14")
put_zip("stock_mac.xlsx", [
    ("[Content_Types].xml", content_types(1)),
    ("_rels/.rels", ROOT_RELS),
    ("xl/workbook.xml", workbook(["Count"], date1904=True)),
    ("xl/_rels/workbook.xml.rels", workbook_rels(1)),
    ("xl/worksheets/sheet1.xml", stock),
    ("xl/styles.xml", styles(fmts, xfs)),
    ("xl/sharedStrings.xml", S.xml()),
])

# ---------------------------------------------------------------- 3
# crm_contacts.xlsx: a CRM's export written with the .NET Open XML SDK:
# every element prefixed x:, inline strings and no shared string table,
# no dimension, a run of rows and cells with no r attribute, t="str" and
# t="d" (ISO dates, as strict-mode writers do), a phone number, a zip
# code with a leading zero, a padded name, a number in exponent form and
# a value that looks like a date but is text.
X = "x:"
decl = f'xmlns:x="{MAIN}" xmlns:r="{RNS}"'


def istr(ref, s):
    a = f' r="{ref}"' if ref else ""
    sp = ' xml:space="preserve"' if s != s.strip() else ""
    return f'<x:c{a} t="inlineStr"><x:is><x:t{sp}>{esc(s)}</x:t></x:is></x:c>'


def xnum(ref, v, s=None):
    a = f' r="{ref}"' if ref else ""
    st = f' s="{s}"' if s is not None else ""
    return f"<x:c{a}{st}><x:v>{v}</x:v></x:c>"


people = [
    ("Okonkwo, Ada", "ada.okonkwo@example.com", "+1 415 555 0134", "02134", "2021-03-04", "true", "1E3", "Gold"),
    ("  Rui Tanaka ", "rui@example.org", "415-555-0199", "94107", "2022-11-30T08:15:00", "false", "250", "Silver"),
    ("Marta Nowak", "", "(212) 555-0100", "10001", "2020-01-15", "true", "0.5", ""),
    ("Lee & Partners", "office@example.net", "", "00501", "2019-07-04", "0", "-12.75", "Bronze"),
    ("Zoë Ångström", "zoe@example.se", "+46 8 555 010 00", "11122", "2023-05-09T23:59:59.5", "1", "1.25e-2", "Gold"),
]
xrows = [f'<x:row r="1">' + "".join(istr(f"{col_letter(i + 1)}1", h) for i, h in enumerate(
    ["Name", "Email", "Phone", "Zip", "Since", "Opt in", "Score", "Tier", "Signed"])) + "</x:row>"]
for k, (nm, em, ph, zp, since, opt, score, tier) in enumerate(people):
    n = k + 2
    use_r = k < 3
    ref = (lambda c: f"{c}{n}") if use_r else (lambda c: None)
    cells = [istr(ref("A"), nm)]
    cells.append(istr(ref("B"), em) if em else (f'<x:c r="B{n}"/>' if use_r else "<x:c/>"))
    cells.append(f'<x:c{" r=" + chr(34) + ref("C") + chr(34) if use_r else ""} t="str"><x:v>{esc(ph)}</x:v></x:c>' if ph else (f'<x:c r="C{n}"/>' if use_r else "<x:c/>"))
    cells.append(istr(ref("D"), zp))
    cells.append(f'<x:c{" r=" + chr(34) + ref("E") + chr(34) if use_r else ""} t="d"><x:v>{since}</x:v></x:c>')
    bit = {"true": "1", "false": "0"}.get(opt, opt)
    cells.append(f'<x:c{" r=" + chr(34) + ref("F") + chr(34) if use_r else ""} t="b"><x:v>{bit}</x:v></x:c>')
    cells.append(xnum(ref("G"), score))
    cells.append(istr(ref("H"), tier) if tier else (f'<x:c r="H{n}"/>' if use_r else "<x:c/>"))
    cells.append(istr(ref("I"), ["2021-03-04", "n/a", "2022-12-01", "NA", "-"][k]))
    if use_r:
        xrows.append(f'<x:row r="{n}">' + "".join(cells) + "</x:row>")
    else:
        xrows.append("<x:row>" + "".join(cells) + "</x:row>")
crm = sheet(xrows, prefix=X, ns_decl=decl)
crm_ct = content_types(1, strings=False)
crm_wb = (f'<?xml version="1.0" encoding="utf-8"?><x:workbook {decl}><x:sheets>'
          f'<x:sheet name="Contacts" sheetId="1" r:id="R5a1"/></x:sheets></x:workbook>')
crm_rels = (f'<?xml version="1.0" encoding="utf-8"?><Relationships xmlns="{PKG}">'
            f'<Relationship Type="{DOC}worksheet" Target="/xl/worksheets/sheet1.xml" Id="R5a1"/>'
            f'<Relationship Type="{DOC}styles" Target="/xl/styles.xml" Id="R9c2"/></Relationships>')
put_zip("crm_contacts.xlsx", [
    ("[Content_Types].xml", crm_ct),
    ("_rels/.rels", ROOT_RELS),
    ("xl/workbook.xml", crm_wb),
    ("xl/_rels/workbook.xml.rels", crm_rels),
    ("xl/worksheets/sheet1.xml", crm),
    ("xl/styles.xml", styles([], [0])),
])

# ---------------------------------------------------------------- 4
# ledger_stale.xlsx: a reporting tool that writes the dimension once,
# before the data, and never updates it: it claims A1:C4 but the sheet
# runs to F12. openpyxl's read-only iteration believes the dimension;
# pandas resets it first. A hidden sheet and a very hidden one follow.
S = Strings()
fmts = [(164, "dd/mm/yyyy")]
xfs = [0, 164, 4]
lr = [row(1, [f'<c r="{c}1" t="s"><v>{S.add(h)}</v></c>' for c, h in zip("ABCDEF", ["Date", "Account", "Memo", "Debit", "Credit", "Balance"])])]
bal = 1000.0
r = Lcg(77)
accts = ["4000 Sales", "5100 Freight", "6200 Rent", "1200 Receivables"]
for i in range(11):
    n = i + 2
    d = datetime.date(2024, 9, 2) + datetime.timedelta(days=i * 2)
    deb = round(r.next(90000) / 100, 2) if r.next(2) else None
    cre = None if deb is not None else round(r.next(50000) / 100, 2)
    bal = round(bal + (deb or 0) - (cre or 0), 2)
    c = [f'<c r="A{n}" s="1"><v>{excel_serial(d):g}</v></c>', f'<c r="B{n}" t="s"><v>{S.add(accts[r.next(4)])}</v></c>']
    if i % 4 == 1:
        c.append(f'<c r="C{n}" t="s"><v>{S.add(["INV-2291 partial", "reversal of 9/3", "  "][i // 4])}</v></c>')
    c.append(f'<c r="D{n}" s="2"><v>{num(deb)}</v></c>' if deb is not None else f'<c r="D{n}" s="2"/>')
    c.append(f'<c r="E{n}" s="2"><v>{num(cre)}</v></c>' if cre is not None else f'<c r="E{n}" s="2"/>')
    # one shared formula down Balance, typed with a double space
    if n == 3:
        c.append(f'<c r="F{n}" s="2"><f t="shared" ref="F3:F12" si="0">ROUND(F2 +  D3-E3,2)</f><v>{num(bal)}</v></c>')
    elif n > 3:
        c.append(f'<c r="F{n}" s="2"><f t="shared" si="0"/><v>{num(bal)}</v></c>')
    else:
        c.append(f'<c r="F{n}" s="2"><v>{num(bal)}</v></c>')
    lr.append(row(n, c))
ledger = sheet(lr, dim="A1:C4")
hid = sheet([row(1, [f'<c r="A1" t="s"><v>{S.add("internal")}</v></c>'])], dim="A1")
vhid = sheet([row(1, [f'<c r="B2" t="s"><v>{S.add("secret sauce")}</v></c>'])], dim="B2")
put_zip("ledger_stale.xlsx", [
    ("[Content_Types].xml", content_types(3)),
    ("_rels/.rels", ROOT_RELS),
    ("xl/workbook.xml", workbook(["Ledger", "Scratch", "Config"], states=["visible", "hidden", "veryHidden"])),
    ("xl/_rels/workbook.xml.rels", workbook_rels(3)),
    ("xl/worksheets/sheet1.xml", ledger),
    ("xl/worksheets/sheet2.xml", hid),
    ("xl/worksheets/sheet3.xml", vhid),
    ("xl/styles.xml", styles(fmts, xfs)),
    ("xl/sharedStrings.xml", S.xml()),
])

# ---------------------------------------------------------------- 5
# survey.xlsx: a form tool's export with two header rows (question group
# and question), answers that mix numbers and words in one column,
# "N/A" and "-" for no answer, duplicated column titles, an empty title
# and trailing empty cells that carry only a style.
S = Strings()
xfs = [0, 1]
g = ["", "About you", "About you", "Ratings", "Ratings", "Ratings", "Ratings", ""]
q = ["Respondent", "Age", "Team", "Tools", "Support", "Tools", "", "Comment"]
srows = [row(1, [f'<c r="{col_letter(i + 1)}1" t="s"><v>{S.add(x)}</v></c>' if x else f'<c r="{col_letter(i + 1)}1" s="1"/>' for i, x in enumerate(g)]),
         row(2, [f'<c r="{col_letter(i + 1)}2" t="s"><v>{S.add(x)}</v></c>' if x else f'<c r="{col_letter(i + 1)}2" s="1"/>' for i, x in enumerate(q)])]
answers = [
    (101, 34, "Ops", 4, 5, 3, 2, "fine"),
    (102, "N/A", "Dev", 5, "N/A", 4, 4, None),
    (103, 51, "Dev", 2, 3, "-", 1, "slow laptop"),
    (104, 28, None, 3, 4, 5, None, None),
    (105, "41", "Sales", "five", 2, 3, 3, "more training"),
    (106, 39.5, "Ops", 4, 4, 4, 4, "N/A"),
]
for k, a in enumerate(answers):
    n = k + 3
    cells = []
    for i, v in enumerate(a):
        ref = f"{col_letter(i + 1)}{n}"
        if v is None:
            continue
        if isinstance(v, str):
            cells.append(f'<c r="{ref}" t="s"><v>{S.add(v)}</v></c>')
        else:
            cells.append(f'<c r="{ref}"><v>{num(v)}</v></c>')
    cells.append(f'<c r="{col_letter(10)}{n}" s="1"/>')
    srows.append(row(n, cells))
srows.append(row(10, ['<c r="A10" s="1"/>', '<c r="B10" s="1"/>']))
survey = sheet(srows, dim="A1:J10")
put_zip("survey.xlsx", [
    ("[Content_Types].xml", content_types(1)),
    ("_rels/.rels", ROOT_RELS),
    ("xl/workbook.xml", workbook(["Responses"])),
    ("xl/_rels/workbook.xml.rels", workbook_rels(1)),
    ("xl/worksheets/sheet1.xml", survey),
    ("xl/styles.xml", styles([], xfs)),
    ("xl/sharedStrings.xml", S.xml()),
])

# ---------------------------------------------------------------- 6
# timesheet.xlsx, written by openpyxl itself from Python values: dates,
# datetimes, times, timedeltas, None, a formula with no cached value
# (openpyxl never computes one), a merged header and a second sheet with
# a header only. Rewritten with fixed timestamps afterwards.
import openpyxl  # noqa: E402

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Week 41"
ws.append(["Timesheet", None, None, None, None, None])
ws.merge_cells("A1:F1")
ws.append(["Employee", "Day", "In", "Out", "Break", "Hours"])
staff = ["Priya", "Tomasz", "Kwame"]
r = Lcg(41)
for k in range(9):
    day = datetime.date(2024, 10, 7) + datetime.timedelta(days=k // 3)
    tin = datetime.time(7 + r.next(3), 15 * r.next(4))
    tout = datetime.time(15 + r.next(3), 15 * r.next(4), 30 if k == 4 else 0)
    brk = datetime.timedelta(minutes=30 + 15 * r.next(3))
    n = ws.max_row + 1
    ws.append([staff[k % 3], day, tin, tout, brk if k != 5 else None, f"=(D{n}-C{n})*24-E{n}*24"])
ws.append(["Total", None, None, None, None, "=SUM(F3:F11)"])
ws.append(["Signed off", datetime.datetime(2024, 10, 11, 17, 42, 9, 250000)])
ws2 = wb.create_sheet("Week 42")
ws2.append(["Employee", "Day", "In", "Out", "Break", "Hours"])
wb.properties.creator = "payroll-export"
wb.properties.created = datetime.datetime(2024, 10, 11, 18, 0, 0)
wb.properties.modified = datetime.datetime(2024, 10, 11, 18, 0, 0)
buf = io.BytesIO()
wb.save(buf)
src = zipfile.ZipFile(io.BytesIO(buf.getvalue()))
# openpyxl stamps docProps/core.xml with the time of the save; pin it.
parts = []
for n in src.namelist():
    b = src.read(n)
    if n == "docProps/core.xml":
        b = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*<", rb"\g<1>2024-10-11T18:00:00Z<", b)
    parts.append((n, b))
put_zip("timesheet.xlsx", parts)

# ---------------------------------------------------------------- 7
# A stored (uncompressed) workbook, as some streaming writers produce,
# with one empty sheet and one that has only a header row.
S = Strings()
put_zip("stored.xlsx", [
    ("[Content_Types].xml", content_types(2)),
    ("_rels/.rels", ROOT_RELS),
    ("xl/workbook.xml", workbook(["Empty", "Header only"])),
    ("xl/_rels/workbook.xml.rels", workbook_rels(2)),
    ("xl/worksheets/sheet1.xml", sheet([], dim="A1")),
    ("xl/worksheets/sheet2.xml", sheet([row(1, [f'<c r="{c}1" t="s"><v>{S.add(h)}</v></c>' for c, h in zip("ABC", ["id", "name", "amount"])])], dim="A1:C1")),
    ("xl/styles.xml", styles([], [0])),
    ("xl/sharedStrings.xml", S.xml()),
], method=zipfile.ZIP_STORED)

# ---------------------------------------------------------------- 8
# Files that are not workbooks: a CSV someone renamed, a zip with no
# workbook in it, and a legacy .xls name.
with open(os.path.join(DATA, "renamed.xlsx"), "wb") as f:
    f.write(b"id,name\r\n1,widget\r\n")
put_zip("photos.xlsx", [("[Content_Types].xml", f'<?xml version="1.0"?><Types xmlns="{CT}"><Default Extension="jpg" ContentType="image/jpeg"/></Types>'),
                        ("img/1.jpg", b"\xff\xd8\xff\xe0 not really a jpeg")])
with open(os.path.join(DATA, "old.xls"), "wb") as f:
    f.write(bytes.fromhex("d0cf11e0a1b11ae1") + bytes(24))

# ---------------------------------------------------------------- jobs
jobs = []
J = jobs.append
# openpyxl, read-only as pandas opens it
for f in ["sales_q3.xlsx", "stock_mac.xlsx", "crm_contacts.xlsx", "ledger_stale.xlsx", "survey.xlsx", "timesheet.xlsx", "stored.xlsx"]:
    J(f"sheets {f}")
J("rows sales_q3.xlsx Orders")
J("rows sales_q3.xlsx Orders formulas")
J("rows sales_q3.xlsx Orders min_row=1 max_row=4 min_col=6 max_col=9 formulas")
J("cells sales_q3.xlsx Orders max_row=6")
J("cells sales_q3.xlsx Orders min_row=12 max_row=20 min_col=7 max_col=11 formulas")
J("rows sales_q3.xlsx Summary")
J("rows sales_q3.xlsx Summary formulas")
J("cells sales_q3.xlsx Summary formulas")
J("rows sales_q3.xlsx Lookups")
J("cells sales_q3.xlsx Lookups min_col=5")
J("rows stock_mac.xlsx Count")
J("cells stock_mac.xlsx Count")
J("rows crm_contacts.xlsx Contacts")
J("cells crm_contacts.xlsx Contacts")
J("rows ledger_stale.xlsx Ledger")
J("rows ledger_stale.xlsx Ledger reset")
J("rows ledger_stale.xlsx Ledger reset formulas")
J("rows ledger_stale.xlsx Ledger max_row=20 max_col=7")
J("rows ledger_stale.xlsx Config")
J("rows survey.xlsx Responses")
J("rows timesheet.xlsx Week\\s41")
J("rows timesheet.xlsx Week\\s41 formulas")
J("cells timesheet.xlsx Week\\s41 min_row=3 max_row=4")
J("rows timesheet.xlsx Week\\s42")
J("rows stored.xlsx Empty")
J("rows stored.xlsx Header\\sonly")
J("rows sales_q3.xlsx Missing")
for f in ["renamed.xlsx", "photos.xlsx", "old.xls", "nowhere.xlsx"]:
    J(f"sheets {f}")
# pandas.read_excel
R = lambda f, a="": J(f"read {f} {a}".rstrip())
R("sales_q3.xlsx")
R("sales_q3.xlsx", "sheet_name=Orders usecols=A:E nrows=5")
R("sales_q3.xlsx", "usecols=A,C,H:I")
R("sales_q3.xlsx", "usecols=Order\\sID,Rep,Total")
R("sales_q3.xlsx", "usecols=0,4,5")
R("sales_q3.xlsx", "index_col=0 usecols=A,E,K nrows=12")
R("sales_q3.xlsx", "dtype=Order\\sID:str,Units:float")
R("sales_q3.xlsx", "dtype=Notes:object usecols=A,K")
R("sales_q3.xlsx", "na_values=rush usecols=A,K")
R("sales_q3.xlsx", "keep_default_na=False usecols=A,G,K nrows=8")
R("sales_q3.xlsx", "keep_default_na=False na_values=#N/A usecols=A,H")
R("sales_q3.xlsx", "skiprows=1,2,3 nrows=4 usecols=A:D")
R("sales_q3.xlsx", "header=None nrows=3 usecols=A:D")
R("sales_q3.xlsx", "header=None names=id,day,where,who skiprows=1 nrows=3 usecols=A:D")
R("sales_q3.xlsx", "names=id,day,where usecols=A:C nrows=2")
R("sales_q3.xlsx", "skipfooter=25 usecols=A,B,J")
R("sales_q3.xlsx", "sheet_name=1")
R("sales_q3.xlsx", "sheet_name=Summary skiprows=3")
R("sales_q3.xlsx", "sheet_name=Summary header=3 skipfooter=1")
R("sales_q3.xlsx", "sheet_name=Summary header=3 index_col=Region")
R("sales_q3.xlsx", "sheet_name=Lookups")
R("sales_q3.xlsx", "sheet_name=Lookups usecols=D:F")
R("sales_q3.xlsx", "sheet_name=Lookups usecols=A:B true_values=N false_values=S")
R("sales_q3.xlsx", "sheet_name=Summary,Lookups header=3 nrows=2")
R("sales_q3.xlsx", "sheet_name=Missing")
R("sales_q3.xlsx", "sheet_name=7")
R("sales_q3.xlsx", "usecols=Order\\sID,Price")
R("sales_q3.xlsx", "usecols=A:Z nrows=1")
R("sales_q3.xlsx", "header=40")
R("sales_q3.xlsx", "index_col=0 dtype=Units:int")
R("sales_q3.xlsx", "dtype=Discount:int usecols=A,G")
R("stock_mac.xlsx")
R("stock_mac.xlsx", "usecols=A:D parse_dates=False")
R("stock_mac.xlsx", "usecols=A,E,F,G nrows=4")
R("stock_mac.xlsx", "usecols=H:N")
R("stock_mac.xlsx", "index_col=0 usecols=A,B,C")
R("crm_contacts.xlsx")
R("crm_contacts.xlsx", "dtype=Zip:str usecols=A,D")
R("crm_contacts.xlsx", "usecols=Name,Signed na_values=n/a")
R("crm_contacts.xlsx", "keep_default_na=False usecols=Email,Tier,Signed")
R("crm_contacts.xlsx", "usecols=Opt\\sin,Score true_values=1 false_values=0")
R("ledger_stale.xlsx")
R("ledger_stale.xlsx", "sheet_name=None")
R("ledger_stale.xlsx", "usecols=Memo")
R("ledger_stale.xlsx", "index_col=0 usecols=A,D,E")
R("ledger_stale.xlsx", "nrows=3")
R("survey.xlsx")
R("survey.xlsx", "header=1")
R("survey.xlsx", "header=1 na_values=-")
R("survey.xlsx", "header=1 index_col=0 usecols=A:E")
R("survey.xlsx", "header=1 dtype=Age:float usecols=A,B")
R("survey.xlsx", "header=1 dtype=Tools:str")
R("survey.xlsx", "skiprows=2 header=None")
R("timesheet.xlsx")
R("timesheet.xlsx", "header=1")
R("timesheet.xlsx", "header=1 nrows=4")
R("timesheet.xlsx", "header=1 usecols=Employee,Break skipfooter=2")
R("timesheet.xlsx", "sheet_name=Week\\s42")
R("timesheet.xlsx", "sheet_name=Week\\s42 index_col=0")
R("stored.xlsx")
R("stored.xlsx", "sheet_name=1")
R("stored.xlsx", "sheet_name=None")
R("renamed.xlsx")
R("old.xls")
R("nowhere.xlsx")
with open(os.path.join(DATA, "jobs.txt"), "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(jobs) + "\n")
print(len(jobs), "jobs")
