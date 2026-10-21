"""Writes data/: the compound files (OLE2 / CFB) a law firm's records
office finds in a matter's intake folder, and jobs.txt.

The files are written by the small CFB writer below, the way Word 97,
Excel 97 and Outlook lay them out: a header, the FAT, the directory as a
red-black tree (all black), the MiniFAT and the mini stream for small
streams, and normal sectors for streams of 4096 bytes or more. The
property set streams (SummaryInformation and DocumentSummaryInformation
with its user-defined section) are written as [MS-OLEPS] lays them out,
padding included. The broken files are good files with one part
damaged after layout, the way a bad copy, a crashed save or a hostile
sender leaves them."""
import datetime
import os
import struct
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

ENDOFCHAIN = 0xFFFFFFFE
FREESECT = 0xFFFFFFFF
FATSECT = 0xFFFFFFFD
DIFSECT = 0xFFFFFFFC
NOSTREAM = 0xFFFFFFFF
MAGIC = b"\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1"


def guid(s):
    return uuid.UUID(s).bytes_le


WORD = guid("00020906-0000-0000-C000-000000000046")
EXCEL = guid("00020820-0000-0000-C000-000000000046")
MSG = guid("00020D0B-0000-0000-C000-000000000046")
PACKAGE = guid("0003000C-0000-0000-C000-000000000046")
FMTID_SUMMARY = guid("F29F85E0-4FF9-1068-AB91-08002B27B3D9")
FMTID_DOCSUM = guid("D5CDD502-2E9C-101B-9397-08002B2CF9AE")
FMTID_USER = guid("D5CDD505-2E9C-101B-9397-08002B2CF9AE")


def filetime(y, mo, d, h=0, mi=0, s=0, us=0):
    delta = datetime.datetime(y, mo, d, h, mi, s, us) - datetime.datetime(1601, 1, 1)
    return (delta.days * 86400 + delta.seconds) * 10000000 + delta.microseconds * 10


# ------------------------------------------------------------ property sets

def pad4(b):
    return b + b"\0" * (-len(b) % 4)


def vt_i2(v):
    return struct.pack("<IhH", 2, v, 0)


def vt_i4(v):
    return struct.pack("<Ii", 3, v)


def vt_bool(v):
    return struct.pack("<IHH", 11, 0xFFFF if v else 0, 0)


def lpstr_body(s):
    b = s.encode("latin-1") + b"\0"
    return pad4(struct.pack("<I", len(b)) + b)


def vt_lpstr(s):
    return struct.pack("<I", 30) + lpstr_body(s)


def vt_lpwstr(s):
    b = (s + "\0").encode("utf-16-le")
    return pad4(struct.pack("<II", 31, len(s) + 1) + b)


def vt_filetime(ft):
    return struct.pack("<IQ", 64, ft)


def vt_cf(fmt, data):
    body = struct.pack("<i", fmt) + data
    return pad4(struct.pack("<II", 71, len(body)) + body)


def vt_blob(data):
    return pad4(struct.pack("<II", 65, len(data)) + data)


def vt_clsid(g):
    return struct.pack("<I", 72) + g


def vt_raw(t, body):
    return struct.pack("<I", t) + body


def vt_vector_lpstr(items):
    out = struct.pack("<II", 0x101E, len(items))
    for s in items:
        out += lpstr_body(s)
    return out


def vt_vector_variant(items):
    out = struct.pack("<II", 0x100C, len(items))
    for it in items:
        out += it
    return out


def section(props, dictionary=None):
    """props: list of (id, typed value bytes). The dictionary (property
    0 of a user-defined section) goes first, right after the table."""
    rows = []
    if dictionary is not None:
        d = struct.pack("<I", len(dictionary))
        for pid, name in dictionary:
            b = name.encode("latin-1") + b"\0"
            d += struct.pack("<II", pid, len(b)) + b
        rows.append((0, pad4(d)))
    rows += props
    table_len = 8 + 8 * len(rows)
    offset = table_len
    table = b""
    values = b""
    for pid, val in rows:
        table += struct.pack("<II", pid, offset)
        values += val
        offset += len(val)
    return struct.pack("<II", table_len + len(values), len(rows)) + table + values


def propset(sections):
    """sections: list of (fmtid, section bytes)."""
    head = struct.pack("<HHI", 0xFFFE, 0, 0x00020006) + b"\0" * 16 + struct.pack("<I", len(sections))
    off = len(head) + 20 * len(sections)
    lst = b""
    body = b""
    for fmtid, sec in sections:
        lst += fmtid + struct.pack("<I", off)
        body += sec
        off += len(sec)
    return head + lst + body


def summary(title, subject, author, keywords, comments, template, last_by, rev,
            edit_secs, printed, created, saved, pages, words, chars, app, security,
            thumb=None):
    p = [(1, vt_i2(1252))]
    for pid, s in ((2, title), (3, subject), (4, author), (5, keywords), (6, comments),
                   (7, template), (8, last_by), (9, rev)):
        if s is not None:
            p.append((pid, vt_lpstr(s)))
    p.append((10, vt_filetime(edit_secs * 10000000)))
    if printed:
        p.append((11, vt_filetime(printed)))
    p.append((12, vt_filetime(created)))
    p.append((13, vt_filetime(saved)))
    p.append((14, vt_i4(pages)))
    p.append((15, vt_i4(words)))
    p.append((16, vt_i4(chars)))
    if thumb is not None:
        p.append((17, vt_cf(-1, thumb)))
    p.append((18, vt_lpstr(app)))
    p.append((19, vt_i4(security)))
    return propset([(FMTID_SUMMARY, section(p))])


def docsum(company, manager, category, lines, paras, parts, user=None):
    p = [(1, vt_i2(1252))]
    if category:
        p.append((2, vt_lpstr(category)))
    p.append((5, vt_i4(lines)))
    p.append((6, vt_i4(paras)))
    p.append((11, vt_bool(False)))
    p.append((12, vt_vector_variant([vt_lpstr("Title"), vt_i4(1),
                                     vt_lpstr("Headings"), vt_i4(len(parts) - 1)])))
    p.append((13, vt_vector_lpstr(parts)))
    if manager:
        p.append((14, vt_lpstr(manager)))
    p.append((15, vt_lpstr(company)))
    p.append((16, vt_bool(False)))
    p.append((17, vt_i4(lines * 61)))
    p.append((19, vt_bool(False)))
    p.append((22, vt_bool(False)))
    p.append((23, vt_i4(0x000B0000)))
    secs = [(FMTID_DOCSUM, section(p))]
    if user is not None:
        names = [(i + 2, n) for i, (n, _) in enumerate(user)]
        up = [(1, vt_i2(1252))] + [(i + 2, v) for i, (_, v) in enumerate(user)]
        secs.append((FMTID_USER, section(up, names)))
    return propset(secs)


# ------------------------------------------------------------ the CFB writer

class Node:
    def __init__(self, name, kind, data=b"", clsid=b"\0" * 16, ctime=0, mtime=0, kids=None):
        self.name = name
        self.kind = kind          # 1 storage, 2 stream, 5 root
        self.data = data
        self.clsid = clsid
        self.ctime = ctime
        self.mtime = mtime
        self.kids = kids or []
        self.sid = None


def stream(name, data, mtime=0):
    return Node(name, 2, data, mtime=mtime)


def storage(name, kids, clsid=b"\0" * 16, ctime=0, mtime=0):
    return Node(name, 1, clsid=clsid, ctime=ctime, mtime=mtime, kids=kids)


def cfb_key(n):
    return (len(n.name), n.name.upper())


class Layout:
    pass


def build(root_kids, root_clsid=b"\0" * 16, root_mtime=0, shift=9, extra_fat=0):
    """Lays the tree out and returns (bytes, layout). layout records
    where everything went, for the damage done afterwards."""
    ss = 1 << shift
    root = Node("Root Entry", 5, clsid=root_clsid, mtime=root_mtime, kids=root_kids)
    order = []

    def number(n):
        n.sid = len(order)
        order.append(n)
        for k in sorted(n.kids, key=cfb_key):
            number(k)
    number(root)

    # mini stream and big streams
    mini = b""
    minifat = []
    for n in order:
        if n.kind == 2 and 0 < len(n.data) < 4096:
            n.mini = True
            n.start = len(mini) // 64
            count = (len(n.data) + 63) // 64
            for i in range(count):
                minifat.append(n.start + i + 1 if i < count - 1 else ENDOFCHAIN)
            mini += n.data + b"\0" * (-len(n.data) % 64)
        else:
            n.mini = False
    dir_sects = (len(order) * 128 + ss - 1) // ss
    minifat_sects = (len(minifat) * 4 + ss - 1) // ss if minifat else 0
    mini_sects = (len(mini) + ss - 1) // ss
    big = [n for n in order if n.kind == 2 and not n.mini and len(n.data) > 0]
    big_sects = sum((len(n.data) + ss - 1) // ss for n in big)
    per = ss // 4
    nfat = 1
    while nfat * per < nfat + extra_fat + dir_sects + minifat_sects + mini_sects + big_sects:
        nfat += 1
    nfat += extra_fat
    fat = []
    lay = Layout()
    lay.ss = ss
    lay.fat_sects = list(range(nfat))
    fat += [FATSECT] * nfat

    def chain(count):
        first = len(fat)
        for i in range(count):
            fat.append(first + i + 1 if i < count - 1 else ENDOFCHAIN)
        return first if count else ENDOFCHAIN

    lay.dir_start = chain(dir_sects)
    lay.dir_sects = list(range(lay.dir_start, lay.dir_start + dir_sects))
    lay.minifat_start = chain(minifat_sects)
    lay.mini_start = chain(mini_sects)
    for n in big:
        n.start = chain((len(n.data) + ss - 1) // ss)
    nsect = len(fat)
    fat += [FREESECT] * (nfat * per - len(fat))

    def entry(n):
        if n is None:
            return b"\0" * 64 + struct.pack("<HBBIII16sIQQIII", 0, 0, 0, NOSTREAM, NOSTREAM,
                                             NOSTREAM, b"\0" * 16, 0, 0, 0, 0, 0, 0)
        nm = (n.name + "\0").encode("utf-16-le")
        start = 0
        size = 0
        if n.kind == 5:
            start = lay.mini_start
            size = len(mini)
        elif n.kind == 2:
            start = n.start if n.data else ENDOFCHAIN
            size = len(n.data)
        return nm + b"\0" * (64 - len(nm)) + struct.pack(
            "<HBBIII16sIQQIII", len(nm), n.kind, 1, n.left, n.right, n.child,
            n.clsid, 0, n.ctime, n.mtime, start, size, 0)

    # red-black tree of each storage's kids, as a balanced binary tree
    def tree(nodes):
        if not nodes:
            return NOSTREAM
        mid = len(nodes) // 2
        n = nodes[mid]
        n.left = tree(nodes[:mid])
        n.right = tree(nodes[mid + 1:])
        return n.sid
    for n in order:
        n.left = n.right = NOSTREAM
    for n in order:
        n.child = tree(sorted(n.kids, key=cfb_key)) if n.kind != 2 else NOSTREAM

    dirb = b"".join(entry(n) for n in order)
    dirb += entry(None) * ((dir_sects * ss - len(dirb)) // 128)
    lay.entries = {}
    for n in order:
        lay.entries[path_of(n, order)] = n

    head = MAGIC + b"\0" * 16 + struct.pack(
        "<HHHHHHIIIIIIIIII", 0x3E, 3 if shift == 9 else 4, 0xFFFE, shift, 6, 0, 0,
        dir_sects if shift != 9 else 0, nfat, lay.dir_start, 0, 4096,
        lay.minifat_start if minifat else ENDOFCHAIN, minifat_sects, ENDOFCHAIN, 0)
    difat = list(lay.fat_sects[:109]) + [FREESECT] * (109 - min(nfat, 109))
    head += struct.pack("<109I", *difat)
    head += b"\0" * (ss - len(head))
    body = struct.pack("<%dI" % len(fat), *fat)
    body += dirb
    mfb = struct.pack("<%dI" % len(minifat), *minifat) if minifat else b""
    mfb += struct.pack("<I", FREESECT) * ((minifat_sects * ss - len(mfb)) // 4)
    body += mfb
    body += mini + b"\0" * (mini_sects * ss - len(mini))
    for n in big:
        body += n.data + b"\0" * (-len(n.data) % ss)
    lay.nsect = nsect
    return bytearray(head + body), lay


def path_of(n, order):
    return n.name


# --- damage helpers

def put32(b, off, v):
    b[off:off + 4] = struct.pack("<I", v)


def put16(b, off, v):
    b[off:off + 2] = struct.pack("<H", v)


def sect_off(lay, s):
    return lay.ss * (s + 1)


def entry_off(lay, sid):
    per = lay.ss // 128
    return sect_off(lay, lay.dir_sects[sid // per]) + (sid % per) * 128


def fat_entry_off(lay, s):
    per = lay.ss // 4
    return sect_off(lay, lay.fat_sects[s // per]) + (s % per) * 4


def find(lay, name):
    return lay.entries[name]


# ------------------------------------------------------------ content

def text_bytes(seed, n):
    words = ("the parties agree that clause schedule notice payment term lease "
             "landlord tenant premises rent review counterpart executed witness "
             "deed default interest arrears completion vacant possession").split()
    out = []
    i = seed
    size = 0
    while size < n:
        w = words[(i * 7 + 3) % len(words)]
        i += 1
        out.append(w)
        size += len(w) + 1
    return (" ".join(out))[:n].encode("latin-1")


def fib(text, encrypted=False):
    """The start of a Word 97 FIB, then the text: enough for the report
    to read wIdent, nFib and the fEncrypted flag."""
    flags = 0x0200 | (0x0100 if encrypted else 0)
    head = struct.pack("<HHHHHH", 0xA5EC, 0x00C1, 0x6A62, 0x0409, 0, flags)
    head += b"\0" * (0x200 - len(head))
    return head + text


def compobj(name, prog):
    a = (name + "\0").encode("latin-1")
    b = "MSWordDoc\0".encode("latin-1")
    c = (prog + "\0").encode("latin-1")
    return (struct.pack("<HHI", 1, 0xFFFE, 0x0A03) + b"\xff\xff\xff\xff" + WORD +
            struct.pack("<I", len(a)) + a + struct.pack("<I", len(b)) + b +
            struct.pack("<I", len(c)) + c + b"\0" * 12)


def biff(n):
    out = struct.pack("<HHHHHHII", 0x0809, 16, 0x0600, 0x0005, 0x2775, 0x07CD, 0x000100C1, 0x00000406)
    i = 0
    while len(out) < n - 4:
        rec = struct.pack("<HHHHHd", 0x0203, 14, i // 6, i % 6, 0x0F, 1000.0 + i * 37.5)
        out += rec
        i += 1
    return out[:n - 4] + struct.pack("<HH", 0x000A, 0)


def utf16(s):
    return s.encode("utf-16-le")


T_CREATED = filetime(2019, 3, 4, 9, 12, 0)
T_SAVED = filetime(2019, 10, 2, 14, 31, 7)
T_PRINTED = filetime(2019, 10, 1, 17, 45, 30, 500000)


def board_report(big=True):
    text = text_bytes(3, 4700 if big else 2600)
    return [
        stream("WordDocument", fib(text)),
        stream("1Table", text_bytes(11, 1300)),
        stream("\x01CompObj", compobj("Microsoft Word 97-2003 Document", "Word.Document.8")),
        stream("\x05SummaryInformation", summary(
            "Q3 Board Report", "Quarterly results", "M. Okafor", "board; q3; results",
            "Draft for the October meeting", "Normal.dotm", "J. Lindqvist", "14",
            12840, T_PRINTED, T_CREATED, T_SAVED, 7, 2210, 12608,
            "Microsoft Office Word", 0, thumb=b"\x08\x00\x10\x00thumbnail")),
        stream("\x05DocumentSummaryInformation", docsum(
            "Harwell & Co", "R. Achebe", "Board papers", 211, 58,
            ["Q3 Board Report", "Results", "Outlook", "Risks"],
            user=[("Client", vt_lpstr("Harwell & Co")), ("Matter No", vt_i4(4471)),
                  ("Reviewed", vt_bool(True)), ("Due", vt_filetime(filetime(2019, 10, 15, 12))),
                  ("Office", vt_lpwstr("Leeds"))])),
        storage("ObjectPool", [
            storage("_1632925377", [
                stream("\x01Ole10Native", struct.pack("<I", 60) + b"\x02\x00chart.png\0C:\\tmp\\chart.png\0" + b"\x89PNG\r\n\x1a\n" + b"\0" * 21),
                stream("\x03ObjInfo", b"\x00\x00\x03\x00\x04\x00"),
            ], clsid=PACKAGE, ctime=T_CREATED, mtime=T_SAVED),
        ], ctime=T_CREATED, mtime=T_SAVED),
    ]


def budget_sheet():
    return [
        stream("Workbook", biff(5200)),
        stream("\x05SummaryInformation", summary(
            "FY2019 Budget", None, "P. Varga", None, None, None, "P. Varga", None,
            0, 0, filetime(2018, 11, 20, 8), filetime(2019, 1, 7, 16, 2, 44), 0, 0, 0,
            "Microsoft Excel", 0)),
        stream("\x05DocumentSummaryInformation", docsum(
            "Harwell & Co", None, None, 0, 0, ["Sheet1", "Budget", "Notes"])),
    ]


def macro_invoice():
    return [
        stream("WordDocument", fib(text_bytes(29, 1900))),
        stream("1Table", text_bytes(5, 700)),
        stream("\x05SummaryInformation", summary(
            "Invoice 2291", None, "accounts", None, None, "Normal.dotm", "accounts", "2",
            60, 0, filetime(2019, 9, 30, 23, 58), filetime(2019, 9, 30, 23, 59, 1), 1, 120, 700,
            "Microsoft Office Word", 0)),
        storage("Macros", [
            storage("VBA", [
                stream("dir", b"\x01" + text_bytes(41, 300)),
                stream("ThisDocument", b"Attribute VB_Name = \"ThisDocument\"\r\n" +
                       b"Sub AutoOpen()\r\n    Shell \"cmd /c echo opened\"\r\nEnd Sub\r\n"),
                stream("_VBA_PROJECT", b"\xcc\x61\xff\xff\x00\x00\x00"),
            ]),
            stream("PROJECT", b"ID=\"{00000000-0000-0000-0000-000000000000}\"\r\nDocument=ThisDocument/&H00000000\r\n"),
            stream("PROJECTwm", b"ThisDocument\0T\0h\0i\0s\0D\0o\0c\0u\0m\0e\0n\0t\0\0\0\0\0"),
        ], ctime=filetime(2019, 9, 30, 23, 57), mtime=filetime(2019, 9, 30, 23, 59)),
    ]


def client_msg():
    body = ("Dear Ms Okafor,\r\n\r\nFurther to our call this morning, I attach the signed "
            "counterpart of the lease and the schedule of condition. The completion date "
            "remains the 15th. Please confirm receipt.\r\n\r\nKind regards,\r\nT. Brennan\r\n")
    body = body * 12
    props = struct.pack("<QIIII", 0, 1, 1, 2, 2) + b"\0" * 8
    props += struct.pack("<IIQ", 0x0E070003, 6, 1) + struct.pack("<IIQ", 0x0E080003, 6, 9876)
    return [
        stream("__substg1.0_001A001F", utf16("IPM.Note")),
        stream("__substg1.0_0037001F", utf16("RE: Unit 4 lease - signed counterpart")),
        stream("__substg1.0_0C1A001F", utf16("Tom Brennan")),
        stream("__substg1.0_0C1F001F", utf16("t.brennan@brennan-law.example")),
        stream("__substg1.0_0E04001F", utf16("Okafor, Miriam")),
        stream("__substg1.0_1000001F", utf16(body)),
        stream("__properties_version1.0", props),
        storage("__nameid_version1.0", [
            stream("__substg1.0_00020102", b"\0" * 16),
            stream("__substg1.0_00030102", b""),
            stream("__substg1.0_00040102", b""),
        ]),
        storage("__recip_version1.0_#00000000", [
            stream("__substg1.0_3001001F", utf16("Okafor, Miriam")),
            stream("__substg1.0_39FE001F", utf16("m.okafor@harwell.example")),
            stream("__properties_version1.0", b"\0" * 8 + struct.pack("<IIQ", 0x0C150003, 6, 1)),
        ]),
        storage("__attach_version1.0_#00000000", [
            stream("__substg1.0_3707001F", utf16("Lease - Unit 4 (signed).pdf")),
            stream("__substg1.0_37010102", b"%PDF-1.4\n" + text_bytes(17, 2200) + b"\n%%EOF\n"),
            stream("__properties_version1.0", b"\0" * 8 + struct.pack("<IIQ", 0x37050003, 6, 1)),
        ]),
        storage("__attach_version1.0_#00000001", [
            stream("__substg1.0_3707001F", utf16("Schedule of condition.docx")),
            stream("__substg1.0_37010102", b"PK\x03\x04" + text_bytes(23, 900)),
            stream("__properties_version1.0", b"\0" * 8 + struct.pack("<IIQ", 0x37050003, 6, 1)),
        ]),
    ]


def write(name, b):
    with open(os.path.join(DATA, name), "wb") as f:
        f.write(bytes(b))


def main():
    os.makedirs(os.path.join(DATA, "out"), exist_ok=True)
    for n in os.listdir(os.path.join(DATA, "out")):
        os.remove(os.path.join(DATA, "out", n))

    # --- good files
    b, lay = build(board_report(), WORD, T_SAVED)
    write("q3_board_report.doc", b)
    board, board_lay = b, lay

    b, lay = build(budget_sheet(), EXCEL)
    write("budget_2019.xls", b)
    budget, budget_lay = b, lay

    b, lay = build(macro_invoice(), WORD)
    write("invoice_2291.doc", b)

    b, lay = build(client_msg(), MSG)
    write("re_unit4_lease.msg", b)

    kids = board_report(big=False)
    kids[0] = stream("WordDocument", fib(text_bytes(31, 2100), encrypted=True))
    del kids[5]
    b, lay = build(kids, WORD)
    write("locked_minutes.doc", b)

    b, lay = build([stream("WordDocument", fib(text_bytes(37, 3000))),
                    stream("\x05SummaryInformation", summary(
                        "Site survey", None, "K. Mensah", None, None, None, "K. Mensah", "1",
                        300, 0, filetime(2020, 2, 3, 10), filetime(2020, 2, 3, 11, 20), 2, 900, 5100,
                        "Microsoft Office Word", 0))], WORD, shift=12)
    write("site_survey_4k.doc", b)

    # --- broken files

    write("not_ole.doc", b"{\\rtf1\\ansi\\deff0 {\\fonttbl {\\f0 Times New Roman;}}\\f0\\fs24 "
          b"Draft heads of terms\\par }" + b" " * 1600)
    write("short.doc", board[:400])

    # header oddities: CLSID, byte order, reserved, transaction number, cutoff
    q = bytearray(budget)
    q[8:24] = EXCEL
    put16(q, 0x1C, 0xFEFF)
    put16(q, 0x22, 7)
    put32(q, 0x34, 3)
    put32(q, 0x38, 0x800)
    write("odd_header.xls", q)

    # only a transaction number: a potential defect
    q = bytearray(budget)
    put32(q, 0x34, 1)
    write("transacted.xls", q)

    # a copy that stopped part way through
    write("cut_short.doc", board[:len(board) * 7 // 10])

    # the WordDocument chain loops back on itself after three sectors
    q = bytearray(board)
    wd = find(board_lay, "WordDocument")
    put32(q, fat_entry_off(board_lay, wd.start + 2), wd.start)
    write("looped_chain.doc", q)

    # WordDocument points out of the FAT; 1Table's mini chain too
    q = bytearray(board)
    put32(q, fat_entry_off(board_lay, wd.start + 3), 4000)
    t1 = find(board_lay, "1Table")
    mf = sect_off(board_lay, board_lay.minifat_start) + (t1.start + 5) * 4
    put32(q, mf, 900)
    write("bad_chain.doc", q)

    # stream sizes that lie: too large, and an empty stream with a start
    q = bytearray(board)
    put32(q, entry_off(board_lay, wd.sid) + 120, 0x00100000)
    cs = find(board_lay, "\x01CompObj")
    put32(q, entry_off(board_lay, cs.sid) + 120, 0)
    write("bad_sizes.doc", q)

    # directory damage, one kind per file
    q = bytearray(board)
    q[entry_off(board_lay, t1.sid) + 66] = 7                # an unknown entry type
    write("dir_badtype.doc", q)

    q = bytearray(board)
    put16(q, entry_off(board_lay, cs.sid) + 64, 90)
    write("dir_longname.doc", q)

    q = bytearray(board)
    si = find(board_lay, "\x05SummaryInformation")
    name = (("worddocument") + "\0").encode("utf-16-le")
    o = entry_off(board_lay, si.sid)
    q[o:o + 64] = name + b"\0" * (64 - len(name))
    put16(q, o + 64, len(name))
    write("dir_dupname.doc", q)

    q = bytearray(board)
    op = find(board_lay, "ObjectPool")
    put32(q, entry_off(board_lay, op.sid) + 76, 0)        # ObjectPool's child is the root
    put32(q, entry_off(board_lay, op.sid) + 120, 64)      # and the storage has a size
    put32(q, entry_off(board_lay, wd.sid) + 124, 1)       # sizeHigh set on a 512 file
    write("dir_loop.doc", q)

    q = bytearray(board)
    put32(q, entry_off(board_lay, op.sid) + 76, 999)
    ds = find(board_lay, "\x05DocumentSummaryInformation")
    put32(q, entry_off(board_lay, ds.sid) + 116, wd.start)  # shares WordDocument's sectors
    put32(q, entry_off(board_lay, ds.sid) + 120, 4096 + 200)
    write("dir_range.doc", q)

    q = bytearray(board)
    q[entry_off(board_lay, si.sid) + 66] = 3              # lockbytes in the tree
    q[entry_off(board_lay, 0) + 66] = 1                   # root written as a storage
    write("dir_kinds.doc", q)

    q = bytearray(board)
    put32(q, 0x30, ENDOFCHAIN)
    write("no_directory.doc", q)

    # no MiniFAT although small streams use it
    q = bytearray(board)
    put32(q, 0x3C, ENDOFCHAIN)
    put32(q, 0x40, 0)
    write("no_minifat.doc", q)

    # times out of range
    q = bytearray(board)
    o = entry_off(board_lay, op.sid)
    q[o + 108:o + 116] = struct.pack("<Q", 0xFFFFFFFFFFFFFFFF)
    q[o + 100:o + 108] = struct.pack("<Q", 116444736000000000)
    write("bad_times.doc", q)

    # DIFAT: the FAT listed only through a DIFAT sector
    b, lay = build(budget_sheet(), EXCEL, extra_fat=1)
    q = bytearray(b)
    difat_sect = lay.fat_sects[-1]
    fat0 = lay.fat_sects[0]
    put32(q, 0x4C, FREESECT)
    for i in range(1, 109):
        put32(q, 0x4C + 4 * i, FREESECT)
    put32(q, 0x2C, 110)
    put32(q, 0x44, difat_sect)
    put32(q, 0x48, 1)
    o = sect_off(lay, difat_sect)
    q[o:o + 512] = struct.pack("<128I", *([fat0] + [FREESECT] * 126 + [ENDOFCHAIN]))
    put32(q, fat_entry_off(lay, difat_sect), DIFSECT)
    write("difat.xls", q)
    difat = q

    q = bytearray(difat)
    put32(q, 0x48, 2)
    write("difat_count.xls", q)

    q = bytearray(difat)
    o = sect_off(lay, difat_sect)
    put32(q, o + 127 * 4, 3)
    write("difat_end.xls", q)

    q = bytearray(difat)
    put32(q, 0x44, 500)
    write("difat_range.xls", q)

    q = bytearray(difat)
    put32(q, 0x2C, 12)
    write("difat_few.xls", q)

    # property sets with damage, in one file
    bad = []
    bad.append(stream("\x05BrokenHeader", b"\xfe\xff\x00\x00\x06\x00\x02\x00"))
    s = summary("Lease", None, "T. Brennan", None, None, None, None, None, 0, 0,
                T_CREATED, T_SAVED, 1, 10, 50, "Word", 0)
    q = bytearray(s)
    put32(q, 28 + 16, 9000)                                 # section offset past the end
    bad.append(stream("\x05BadOffset", bytes(q)))
    sec = section([
        (1, vt_i2(-535)),
        (2, vt_raw(5, struct.pack("<d", 2.5))),             # VT_R8: not parsed
        (3, vt_raw(18, struct.pack("<HH", 65535, 0))),       # VT_UI2
        (4, vt_raw(19, struct.pack("<I", 0xDEADBEEF))),      # VT_UI4
        (5, vt_raw(17, b"\x2a\0\0\0")),                       # VT_UI1
        (6, vt_raw(10, struct.pack("<I", 0x80070005))),      # VT_ERROR
        (7, vt_filetime(0xFFFFFFFFFFFFFFF0)),                # far past year 9999
        (8, vt_filetime(filetime(1999, 12, 31, 23, 59, 59, 999999))),
        (9, vt_clsid(MSG)),
        (10, vt_blob(b"\x00\x01binary\xff")),
        (11, vt_raw(0x1003, struct.pack("<Iiii", 3, 10, -20, 30))),     # vector of I4
        (12, vt_raw(0x1002, struct.pack("<IhhH", 2, -1, 7, 0))),        # vector of I2
        (13, vt_vector_lpstr(["Lot", "Lot 4", "Unit 4a"])),             # padding olefile skips
        (14, vt_raw(0x1040, struct.pack("<IQ", 1, filetime(2001, 1, 1)))),
        (15, vt_raw(0x100C, struct.pack("<I", 2) + vt_i4(5) + vt_bool(True))),
        (16, vt_raw(66, b"\0\0\0\0")),                        # VT_STREAM: not parsed
        (17, vt_raw(0x2003, b"\0\0\0\0")),                    # VT_ARRAY: not parsed
        (0x80000000, vt_raw(72, b"short")),                    # a CLSID that runs on
        (20, vt_raw(11, b"")),                                 # a bool with no value
        (18, vt_lpwstr("Leeds office")),                      # LPWSTR as olefile reads it
    ])
    sec = bytearray(sec)
    put32(sec, 8 + 8 * 18 + 4, 0x10000)                      # property 21 is past the end
    sec[8 + 8 * 18:8 + 8 * 18 + 4] = struct.pack("<I", 21)
    bad.append(stream("\x05Kinds", propset([(FMTID_SUMMARY, bytes(sec))])))
    sec = bytearray(section([(1, vt_i2(1252)), (2, vt_lpstr("Ann")), (3, vt_filetime(T_SAVED))]))
    put32(sec, 0, len(sec) - 4)                              # the size cuts the time in half
    bad.append(stream("\x05TruncTime", propset([(FMTID_SUMMARY, bytes(sec))])))
    sec = bytearray(section([(1, vt_i2(1252)), (2, vt_raw(17, b"\x07\0\0\0"))]))
    put32(sec, 0, len(sec) - 4)                              # the size stops before the byte
    bad.append(stream("\x05TruncByte", propset([(FMTID_SUMMARY, bytes(sec))])))
    sec = bytearray(section([(1, vt_i2(1252)), (2, vt_lpstr("x"))]))
    put32(sec, 4, 0x7FFFFFFF)                                # property count far too big
    bad.append(stream("\x05Clamped", propset([(FMTID_SUMMARY, bytes(sec))])))
    sec = bytearray(section([(1, vt_i2(1252)), (2, vt_lpstr("Title")), (3, vt_i4(9))]))
    put32(sec, 8 + 8 + 4, 0x1000)                            # second offset past the end
    put32(sec, 0, 3)                                         # section size below 4
    bad.append(stream("\x05TinySection", propset([(FMTID_SUMMARY, bytes(sec))])))
    ds = docsum("Brennan Law", None, None, 4, 2, ["Lease", "Recitals"],
                user=[("Matter", vt_lpstr("Unit 4")), ("Fee", vt_i4(-1200)),
                      ("Billable", vt_bool(False)), ("Opened", vt_filetime(filetime(2019, 2, 1, 9))),
                      ("Partner", vt_lpwstr("A. Rahman")), ("Ref", vt_raw(1, struct.pack("<II", 0, 4) + b"R-9\0")),
                      ("Rate", vt_raw(5, struct.pack("<d", 1.5)))])
    bad.append(stream("\x05DocumentSummaryInformation", ds))
    q = bytearray(ds)
    pos = bytes(q).find(b"Billable\0")
    q[pos + 1] = 0xC3
    q[pos + 2] = 0x28
    bad.append(stream("\x05BadDictionary", bytes(q)))
    q = bytearray(ds)
    pos = bytes(q).find(b"Billable\0")
    put32(q, pos - 4, 400)                                   # a name length past the end
    bad.append(stream("\x05LongName", bytes(q)))
    bad.append(stream("WordDocument", fib(text_bytes(43, 600))))
    b, lay = build(bad, WORD)
    write("damaged_props.doc", b)

    jobs = []
    good = ["q3_board_report.doc", "budget_2019.xls", "invoice_2291.doc", "re_unit4_lease.msg",
            "locked_minutes.doc", "site_survey_4k.doc"]
    broken = ["not_ole.doc", "short.doc", "odd_header.xls", "transacted.xls", "cut_short.doc",
              "looped_chain.doc", "bad_chain.doc", "bad_sizes.doc", "dir_badtype.doc",
              "dir_longname.doc", "dir_dupname.doc", "dir_loop.doc", "dir_range.doc",
              "dir_kinds.doc", "no_directory.doc", "no_minifat.doc", "bad_times.doc",
              "difat.xls", "difat_count.xls", "difat_end.xls", "difat_range.xls",
              "difat_few.xls", "damaged_props.doc"]
    for f in good + broken:
        jobs.append("open %s" % f)
    for f in ["odd_header.xls", "transacted.xls", "dir_loop.doc", "dir_range.doc", "bad_sizes.doc"]:
        for lvl in (30, 20, 10):
            jobs.append("open %s %d" % (f, lvl))
    for f in good + ["dir_loop.doc", "dir_kinds.doc", "dir_dupname.doc", "dir_badtype.doc",
                     "dir_range.doc", "cut_short.doc", "difat.xls"]:
        jobs.append("tree %s" % f)
    jobs += [
        "list q3_board_report.doc",
        "list q3_board_report.doc storages",
        "list q3_board_report.doc both",
        "list invoice_2291.doc both",
        "list re_unit4_lease.msg",
        "list re_unit4_lease.msg storages",
        "list dir_kinds.doc",
        "list dir_kinds.doc both 30",
        "list dir_loop.doc both",
        "list dir_badtype.doc",
    ]
    jobs += [
        "entry q3_board_report.doc WordDocument",
        "entry q3_board_report.doc worddocument",
        "entry q3_board_report.doc ObjectPool",
        "entry q3_board_report.doc ObjectPool/_1632925377",
        "entry q3_board_report.doc objectpool/_1632925377/\\x01ole10native",
        "entry q3_board_report.doc Macros",
        "entry q3_board_report.doc ObjectPool/Missing",
        "entry q3_board_report.doc ObjectPool/",
        "entry q3_board_report.doc /WordDocument",
        "entry invoice_2291.doc Macros/VBA/ThisDocument",
        "entry invoice_2291.doc Macros/VBA",
        "entry invoice_2291.doc Macros/VBA/ThisDocument/x",
        "entry re_unit4_lease.msg __attach_version1.0_#00000000/__substg1.0_37010102",
        "entry bad_times.doc ObjectPool",
        "entry dir_longname.doc \\x01CompObj",
        "entry dir_dupname.doc WordDocument",
    ]
    jobs += [
        "stream q3_board_report.doc WordDocument",
        "stream q3_board_report.doc 1Table",
        "stream q3_board_report.doc \\x01CompObj",
        "stream q3_board_report.doc ObjectPool",
        "stream q3_board_report.doc Nothing",
        "stream q3_board_report.doc ObjectPool/_1632925377/\\x03ObjInfo",
        "stream re_unit4_lease.msg __substg1.0_1000001F",
        "stream re_unit4_lease.msg __nameid_version1.0/__substg1.0_00030102",
        "stream site_survey_4k.doc WordDocument",
        "stream looped_chain.doc WordDocument",
        "stream bad_chain.doc WordDocument",
        "stream bad_chain.doc 1Table",
        "stream bad_chain.doc 1Table 30",
        "stream bad_sizes.doc WordDocument",
        "stream bad_sizes.doc \\x01CompObj",
        "stream cut_short.doc WordDocument",
        "stream cut_short.doc 1Table",
        "stream no_minifat.doc 1Table",
        "stream no_minifat.doc WordDocument",
        "stream dir_range.doc \\x05DocumentSummaryInformation",
        "stream difat.xls Workbook",
    ]
    jobs += [
        "props q3_board_report.doc \\x05SummaryInformation",
        "props q3_board_report.doc \\x05SummaryInformation convert",
        "props q3_board_report.doc \\x05DocumentSummaryInformation convert",
        "props budget_2019.xls \\x05SummaryInformation convert",
        "props damaged_props.doc \\x05BrokenHeader",
        "props damaged_props.doc \\x05BrokenHeader 30",
        "props damaged_props.doc \\x05BadOffset",
        "props damaged_props.doc \\x05Kinds",
        "props damaged_props.doc \\x05Kinds convert",
        "props damaged_props.doc \\x05Kinds convert 30",
        "props damaged_props.doc \\x05TruncTime",
        "props damaged_props.doc \\x05TruncTime convert",
        "props damaged_props.doc \\x05TruncByte",
        "props damaged_props.doc \\x05TruncByte 30",
        "props damaged_props.doc \\x05Clamped",
        "props damaged_props.doc \\x05TinySection",
        "props damaged_props.doc Missing",
        "props q3_board_report.doc ObjectPool",
        "props cut_short.doc \\x05SummaryInformation",
        "userprops q3_board_report.doc \\x05DocumentSummaryInformation",
        "userprops budget_2019.xls \\x05DocumentSummaryInformation",
        "userprops damaged_props.doc \\x05DocumentSummaryInformation",
        "userprops damaged_props.doc \\x05DocumentSummaryInformation convert",
        "userprops damaged_props.doc \\x05BadDictionary",
        "userprops damaged_props.doc \\x05LongName",
        "userprops damaged_props.doc \\x05LongName 30",
        "userprops damaged_props.doc \\x05BrokenHeader",
        "userprops damaged_props.doc \\x05SummaryInformation",
    ]
    for f in good + ["damaged_props.doc", "cut_short.doc"]:
        jobs.append("meta %s" % f)
    jobs += [
        "extract re_unit4_lease.msg __attach_version1.0_#00000000/__substg1.0_37010102 lease_signed.pdf",
        "extract re_unit4_lease.msg __attach_version1.0_#00000001/__substg1.0_37010102 schedule.docx",
        "extract invoice_2291.doc Macros/VBA/ThisDocument ThisDocument.vba",
        "extract q3_board_report.doc ObjectPool/_1632925377/\\x01Ole10Native chart.bin",
        "extract cut_short.doc WordDocument cut_short.WordDocument",
        "extract q3_board_report.doc Missing missing.bin",
    ]
    jobs.append("report " + " ".join(good + broken))
    with open(os.path.join(DATA, "jobs.txt"), "w") as f:
        f.write("\n".join(jobs) + "\n")


main()
