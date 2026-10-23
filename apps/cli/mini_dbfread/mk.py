#!/usr/bin/env python3
"""Writes the inputs of mini_dbfread to data/: the tables and memo files of
a town archive's legacy systems (dBase III, dBase IV, FoxBASE and Visual
FoxPro, in eight code pages), the damaged files other tools left behind,
and the script data/jobs.tsv that oracle.py and mini_dbfread.kara replay.

The files are written here, byte by byte, by a small DBF / FPT / DBT
writer, so every header field, flag byte and memo block is chosen on
purpose. A job is one tab-separated line; see oracle.py for the verbs.

Run: python3 -s -P -B mk.py"""
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
LEGACY = os.path.join(DATA, "legacy")
BROKEN = os.path.join(LEGACY, "broken")

FILES = []  # paths under data/, in the order they are written


def put(rel, data):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    FILES.append(rel)


# ------------------------------------------------------------ field values

def c(text, n, enc="ascii"):
    b = text.encode(enc) if isinstance(text, str) else text
    assert len(b) <= n, (text, n)
    return b + b" " * (n - len(b))


def num(text, n):
    b = text.encode("ascii")
    assert len(b) <= n, (text, n)
    return b" " * (n - len(b)) + b


def i4(v):
    return struct.pack("<i", v)


def y8(v):
    return struct.pack("<q", v)


def d8(v):
    return struct.pack("<d", v)


def julian(y, m, d):
    import datetime
    return datetime.date(y, m, d).toordinal() + 1721425


def t8(day, ms):
    return struct.pack("<LL", day, ms)


def ptr(n):
    return struct.pack("<I", n)


# ------------------------------------------------------------ the writers

def field(name, ftype, length, dec=0, address=0, name_raw=None, extra=b""):
    raw = name_raw if name_raw is not None else name.encode("ascii")
    raw = raw + b"\0" * (11 - len(raw))
    assert len(raw) == 11
    tail = extra if extra else b"\0" * 14
    assert len(tail) == 14
    return raw + ftype.encode("latin-1") + struct.pack("<LBB", address, length, dec) + tail


def dbf(version, fields, records, lang=0x00, date=(124, 3, 15), backlink=0,
        recordlen=None, headerlen=None, numrecords=None, end=b"\r",
        eof=b"\x1a", flags=(0, 0, 0)):
    """fields: (name, type, length, dec) tuples or raw 32-byte descriptors.
    records: (flag, bytes) pairs."""
    descs = b""
    total = 1
    for f in fields:
        if isinstance(f, bytes):
            descs += f
            total += f[16]
        else:
            name, ftype, length, dec = f
            descs += field(name, ftype, length & 0xFF,
                           (length >> 8) if ftype == "C" else dec,
                           address=total if version >= 0x30 else 0)
            total += length
    hl = 32 + len(descs) + len(end) + backlink
    if headerlen is None:
        headerlen = hl
    if recordlen is None:
        recordlen = total
    if numrecords is None:
        numrecords = len(records)
    head = struct.pack("<BBBBLHHHBBLLLBBH", version, date[0], date[1],
                       date[2], numrecords, headerlen, recordlen, 0,
                       flags[0], flags[1], 0, 0, 0, flags[2], lang, 0)
    body = b"".join(flag + data for flag, data in records)
    return head + descs + end + b"\0" * backlink + body + eof


def fpt(blocksize, memos):
    """Visual FoxPro memo file. memos: (index, type, data); index is in
    blocks and must leave room for the earlier memos."""
    out = bytearray(struct.pack(">LHH", 0, 0, blocksize) + b"\0" * 504)
    nextblock = len(out) // blocksize
    for index, mtype, data in memos:
        at = index * blocksize
        assert at >= len(out), index
        out += b"\0" * (at - len(out))
        block = struct.pack(">LL", mtype, len(data)) + data
        if len(block) % blocksize:
            block += b"\0" * (blocksize - len(block) % blocksize)
        out += block
        nextblock = len(out) // blocksize
    out[0:4] = struct.pack(">L", nextblock)
    return bytes(out)


def dbt3(memos, last_open=False):
    """dBase III memo file: 512-byte blocks, each memo ends in 0x1a 0x1a.
    With last_open the final memo has no end marker and runs to EOF."""
    out = bytearray(b"\0" * 512)
    for k, (index, data) in enumerate(memos):
        at = index * 512
        assert at >= len(out), index
        out += b"\0" * (at - len(out))
        last = k == len(memos) - 1
        out += data if (last and last_open) else data + b"\x1a\x1a"
        if not (last and last_open) and len(out) % 512:
            out += b"\0" * (512 - len(out) % 512)
    out[0:4] = struct.pack("<L", len(out) // 512 + 1)
    return bytes(out)


def dbt4(memos):
    """dBase IV memo file: a block starts with ff ff 08 00 and a length
    that counts the 8-byte header; the text ends in 0x1f. memos: (index,
    data, terminated)."""
    out = bytearray(b"\0" * 512)
    out[0:4] = struct.pack("<L", 1)
    out[20:22] = struct.pack("<H", 512)
    for index, data, terminated in memos:
        at = index * 512
        assert at >= len(out), index
        out += b"\0" * (at - len(out))
        body = data + (b"\x1f\x1f" if terminated else b"")
        out += b"\xff\xff\x08\x00" + struct.pack("<L", len(body) + 8) + body
        if len(out) % 512:
            out += b" " * (512 - len(out) % 512)
    out[0:4] = struct.pack("<L", len(out) // 512)
    return bytes(out)


def m10(n):
    return num(str(n), 10) if n is not None else b" " * 10


# ------------------------------------------------------------ the archive

def write_tables():
    # The registry office's staff list, dBase III, Windows ANSI.
    enc = "cp1252"
    people = [
        (b" ", c("Alice Lindqvist", 25, enc) + b"19870301" + c("Göteborg", 20, enc)
         + num("4500.00", 10) + b"T" + num("2", 2)),
        (b" ", c("Bob O'Brien", 25, enc) + b"19801112" + c("Dublin", 20, enc)
         + num("3200.50", 10) + b"F" + num("0", 2)),
        (b"*", c("Carl Lund", 25, enc) + b"19750101" + c("Oslo", 20, enc)
         + num("1000.00", 10) + b"T" + num("1", 2)),
        (b" ", c("Dörte Müller", 25, enc) + b"        " + c("Köln, NRW", 20, enc)
         + b" " * 10 + b"?" + b"  "),
        (b" ", c("José Núñez", 25, enc) + b"19991231" + c("São Paulo", 20, enc)
         + num("12000.75", 10) + b"y" + num("3", 2)),
        (b" ", c('Eve "Evie" Park', 25, enc) + b"20000229" + c("Seoul", 20, enc)
         + num("0.10", 10) + b"N" + b"**"),
    ]
    put("legacy/PEOPLE.DBF", dbf(0x03, [
        ("NAME", "C", 25, 0), ("BIRTHDATE", "D", 8, 0), ("CITY", "C", 20, 0),
        ("SALARY", "N", 10, 2), ("ACTIVE", "L", 1, 0), ("KIDS", "N", 2, 0)],
        people, lang=0x57))

    # The shop's order book, Visual FoxPro, with a memo file in upper case.
    memos = [
        (8, 1, "Deliver to the back door.".encode(enc)),
        (9, 1, "Lieferung für März, bitte\r\nzwei Kartons.".encode(enc)),
        (10, 0, b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"),
        (11, 2, b"\xd0\xcf\x11\xe0OLE2"),
        (12, 7, b"vendor blob \x00\x01\x02"),
        (13, 1, b"Paid in cash; see 'Ledger' tab."),
        (14, 1, b""),
    ]
    put("legacy/ORDERS.FPT", fpt(64, memos))
    dt = julian
    orders = [
        (1, "Acme", dt(2024, 1, 5), 34200123, 1250000, 0.075, b"T", 8, 11, b"\x00"),
        (2, "Bolt & Co", dt(2024, 1, 9), 0, 99999, 0.2, b"F", 0, 0, b"\x00"),
        (3, "Acme", dt(2024, 2, 1), 86399999, -5000, 1.0, b"T", 9, 13, b"\x00"),
        (4, "Cirrus", dt(2024, 2, 14), 43200000, 0, 1e-07, b"F", 10, 0, b"\x02"),
        (5, "Bolt & Co", dt(2024, 2, 29), 61200500, 123456789, 2.5e+20, b"T", 12, 0, b"\x00"),
        (6, "Delta", dt(2024, 3, 1), 1000, 777700, -0.0, b"T", 13, 0, b"\x00"),
        (7, "Acme", dt(2024, 3, 2), 3600000, 4321, 0.1 + 0.2, b"F", 14, 10, b"\x00"),
        (8, "Cirrus", dt(2024, 3, 3), 45296789, 30000000, 3.0, b"F", 0, 0, b"\x00"),
    ]
    rows = []
    for (oid, cust, day, ms, total, rate, paid, note, logo, nulls) in orders:
        rows.append((b"*" if oid == 6 else b" ",
                     i4(oid) + c(cust, 15) + t8(day, ms) + y8(total) + d8(rate)
                     + paid + ptr(note) + ptr(logo) + nulls))
    put("legacy/orders.dbf", dbf(0x30, [
        ("ID", "I", 4, 0), ("CUSTOMER", "C", 15, 0), ("ORDERED", "T", 8, 0),
        ("TOTAL", "Y", 8, 4), ("RATE", "B", 8, 0), ("PAID", "L", 1, 0),
        ("NOTE", "M", 4, 0), ("LOGO", "G", 4, 0), ("_NullFlags", "0", 1, 0)],
        rows, lang=0x03, backlink=263, date=(124, 3, 4)))

    # The help desk's tickets, Visual FoxPro with Varchar and autoincrement.
    tickets = [
        (1, b"Printer jam", dt(2024, 4, 1), 32400000, 4.5, b"open"),
        (2, b"VPN down", dt(2024, 4, 2), 0, 2.25, b"closed"),
        (3, b"", 0, 0, -1.5, b"waiting"),
        (4, b"New laptop", dt(1999, 12, 31), 86399000, 1e16, b""),
    ]
    rows = [(b" ", i4(t) + c(s, 20) + t8(d, ms) + d8(sc) + c(st, 8))
            for (t, s, d, ms, sc, st) in tickets]
    put("legacy/Tickets.DBF", dbf(0x32, [
        ("TICKET", "+", 4, 0), ("SUBJECT", "V", 20, 0), ("OPENED", "@", 8, 0),
        ("SCORE", "O", 8, 0), ("STATUS", "C", 8, 0)],
        rows, lang=0x03, backlink=263))

    # The caretaker's notes, dBase III with memo, DOS code page 437.
    enc = "cp437"
    long_note = ("Boiler service log\r\n" + "".join(
        "%02d: pressure %d.%d bar, all valves checked, café break\r\n"
        % (k, 1 + k % 2, k % 10) for k in range(1, 14))).encode(enc)
    assert len(long_note) > 512
    put("legacy/NOTES.DBT", dbt3([
        (1, "Ring the plumber.".encode(enc)),
        (2, long_note),
        (5, b"Roof: two tiles loose."),
        (6, "Last entry, no end marker é".encode(enc)),
    ], last_open=True))
    notes = [
        (b" ", c("Plumber", 20) + m10(1) + b"20230105"),
        (b" ", c("Boiler", 20, enc) + m10(2) + b"20230110"),
        (b" ", c("Empty", 20) + m10(None) + b"20230111"),
        (b" ", c("Roof", 20) + num("5", 10) + b"20230201"),
        (b"*", c("Old", 20) + m10(5) + b"20220101"),
        (b" ", c("Last", 20) + m10(6) + b"20230301"),
    ]
    put("legacy/notes.dbf", dbf(0x83, [
        ("TITLE", "C", 20, 0), ("BODY", "M", 10, 0), ("CREATED", "D", 8, 0)],
        notes, lang=0x01, date=(123, 3, 1)))

    # The stores' inventory, dBase IV with memo, code page 850.
    enc = "cp850"
    put("legacy/inventory.dbt", dbt4([
        (1, "Größe M, Farbe grün".encode(enc), True),
        (2, b"Spare part, see catalogue", True),
        (3, b"Written by another tool", False),
    ]))
    inv = [
        (b" ", c("A-100", 8) + c("Schraube Ø4", 20, enc) + num("250", 5)
         + num("0.15", 8) + m10(1)),
        (b" ", c("A-200", 8) + c("Mutter", 20, enc) + num("1200", 5)
         + num("0.05", 8) + m10(2)),
        (b" ", c("B-300", 8) + c("Kabel, 3m", 20, enc) + num("-4", 5)
         + num("12.5", 8) + "0000000000".encode()),
        (b" ", c("C-400", 8) + c("Lampe", 20, enc) + num("7", 5)
         + num("*****", 8) + m10(3)),
    ]
    put("legacy/inventory.dbf", dbf(0x8B, [
        ("SKU", "C", 8, 0), field("GRÖSSE", "C", 20, name_raw="GR\x99SSE".encode("latin-1")),
        ("QTY", "N", 5, 0), ("PRICE", "F", 8, 2), ("DESCR", "M", 10, 0)],
        inv, lang=0x02, date=(122, 11, 30)))

    # Customers in Danish, Russian (DOS and Windows) and Macintosh pages.
    enc = "cp865"
    kunder = [
        (b" ", c("Søren Ærø", 20, enc) + c("Ålesund", 15, enc) + b"19650704"),
        (b" ", c("Åse Bø", 20, enc) + c("Ærøskøbing", 15, enc) + b"19720229"),
    ]
    put("legacy/kunder.dbf", dbf(0x03, [
        ("NAVN", "C", 20, 0), ("BY", "C", 15, 0),
        field("FØDT", "D", 8, name_raw="FØDT".encode(enc))],
        kunder, lang=0x08))
    for name, enc, lang in [("klienty.dbf", "cp866", 0x26),
                            ("KLIENTY_W.DBF", "cp1251", 0xC9)]:
        rows = [
            (b" ", c("Иван Петров", 20, enc) + c("Москва", 15, enc) + num("1500", 6)),
            (b" ", c("Ольга Смирнова", 20, enc) + c("Санкт-Петербург", 15, enc) + num("-20", 6)),
            (b"*", c("Удалён", 20, enc) + c("Казань", 15, enc) + num("0", 6)),
        ]
        put("legacy/" + name, dbf(0x03, [
            field("ИМЯ", "C", 20, name_raw="ИМЯ".encode(enc)),
            ("GOROD", "C", 15, 0), ("BALANS", "N", 6, 0)], rows, lang=lang))
    enc = "mac_roman"
    put("legacy/menu.dbf", dbf(0x03, [("DISH", "C", 20, 0), ("PRICE", "N", 6, 2)], [
        (b" ", c("Crème brûlée", 20, enc) + num("6.50", 6)),
        (b" ", c("Apfelstrüdel", 20, enc) + num("5.25", 6)),
        (b" ", c("Café au lait", 20, enc) + num("3", 6)),
    ], lang=0x04))

    # An export with an unknown language driver: dbfread falls back to
    # ASCII, but the bytes are Windows ANSI.
    put("legacy/export.dbf", dbf(0x03, [("CITY", "C", 12, 0), ("CODE", "C", 4, 0)], [
        (b" ", c("Oslo", 12) + c("NO", 4)),
        (b" ", c("Malmö", 12, "cp1252") + c("SE", 4)),
        (b" ", c("Zürich".encode("cp1252") + b"\x81", 12) + c("CH", 4)),
    ], lang=0x99))

    # A table written by a modern tool in UTF-8 under driver 0 (ASCII).
    rows = [
        (b" ", c("naïve café", 16, "utf-8") + c("ok", 5)),
        (b" ", c("price €5", 16, "utf-8") + c("ok", 5)),
        (b" ", c(b"cut caf\xc3", 16) + c("end", 5)),
        (b" ", c(b"bad \xff byte", 16) + c("start", 5)),
        (b" ", c(b"half \xc3A", 16) + c("cont", 5)),
        (b" ", c(b"three \xe2\x82", 16) + c("eod", 5)),
    ]
    put("legacy/utf8.dbf", dbf(0x03, [("TEXT", "C", 16, 0), ("WHY", "C", 5, 0)],
                               rows, lang=0x00))

    # Memo files in both spellings: dbfread takes the .fpt first.
    put("legacy/both.dbf", dbf(0x30, [("N", "N", 3, 0), ("M", "M", 4, 0)], [
        (b" ", num("1", 3) + ptr(8)),
    ], backlink=263))
    put("legacy/both.fpt", fpt(64, [(8, 1, b"from the fpt")]))
    put("legacy/BOTH.DBT", dbt3([(1, b"from the dbt")]))

    # A FoxBASE+ table (0x03, no memo flag) whose memo file is a .dbt: the
    # library reads it as a dBase IV memo file.
    put("legacy/plain3.dbf", dbf(0x03, [("M", "M", 10, 0)], [
        (b" ", m10(1)),
    ]))
    put("legacy/plain3.dbt", dbt3([(1, b"dBase III text")])[:512 + 16])

    # Odd but readable files.
    put("legacy/empty.dbf", dbf(0x03, [("A", "C", 3, 0)], [], date=(0, 0, 0)))
    put("legacy/longchar.dbf", dbf(0x03, [("NOTE", "C", 300, 0), ("K", "N", 2, 0)], [
        (b" ", c("x" * 290 + "end", 300) + num("1", 2)),
    ]))
    put("legacy/names.dbf", dbf(0x03, [
        field("", "C", 3, name_raw=b"ELEVENCHARS"),
        field("", "C", 3, name_raw=b"AB\0XYZ\0\0\0\0\0"),
        field("", "N", 3, name_raw=b"lower_case"),
    ], [(b" ", b"abcdef 12")], date=(124, 13, 1)))
    put("legacy/flags.dbf", dbf(0x03, [("V", "C", 4, 0)], [
        (b" ", c("live", 4)), (b"X", c("odd", 4)), (b"*", c("gone", 4)),
        (b"\0", c("nul", 4)), (b" ", c("last", 4)),
    ], date=(99, 2, 29)))
    put("legacy/numbers.dbf", dbf(0x03, [("RAW", "C", 12, 0), ("N", "N", 12, 2),
                                         ("F", "F", 12, 3)], [
        (b" ", c(t, 12) + num(t, 12) + num(t, 12)) for t in [
            "12", "-3", "+7", " 0012", "1_000", "12.50", "1,5", "***",
            "", "1e3", "-0.0", ".5", "5.", "1.2.3", "1_0.5", "0.1",
            "2.5E-3", "-", "12 34"]
    ]))
    put("legacy/currency.dbf", dbf(0x30, [("WHAT", "C", 10, 0), ("AMT", "Y", 8, 4)], [
        (b" ", c(w, 10) + y8(v)) for w, v in [
            ("rent", 12000000), ("refund", -5), ("zero", 0), ("cent", 100),
            ("max", 2**63 - 1), ("min", -2**63), ("round", 10000), ("ten", 100000)]
    ], backlink=263))
    put("legacy/times.dbf", dbf(0x30, [("WHAT", "C", 10, 0), ("T", "T", 8, 0)], [
        (b" ", c(w, 10) + d) for w, d in [
            ("noon", t8(julian(2024, 6, 1), 43200000)),
            ("ms", t8(julian(2024, 6, 1), 1)),
            ("blank", b" " * 8),
            ("zeroday", t8(0, 2)),
            ("epoch", t8(julian(1970, 1, 1), 0)),
            ("first", t8(1721426, 0)),
            ("nextday", t8(julian(2024, 12, 31), 86400000 + 5)),
            ("week", t8(julian(2000, 1, 1), 7 * 86400000)),
        ]
    ], backlink=263))


def write_broken():
    put("legacy/broken/unknown_type.dbf", dbf(0x03, [
        ("CODE", "C", 4, 0), ("HEX", "X", 6, 0)], [
        (b" ", c("a", 4) + num("ff", 6)),
        (b" ", c("b", 4) + num("0x1F", 6)),
        (b" ", c("c", 4) + b" " * 6),
        (b" ", c("d", 4) + num("zz", 6)),
    ]))
    put("legacy/broken/bad_int.dbf", dbf(0x30, [("ID", "I", 2, 0)], [
        (b" ", b"\x01\x00")], backlink=263))
    put("legacy/broken/bad_logical.dbf", dbf(0x03, [("OK", "L", 3, 0)], [
        (b" ", b"YES")]))
    put("legacy/broken/short.dbf", b"\x03\x7c\x03\x0f\x01\x00\x00\x00\x41\x00")
    good = dbf(0x03, [("A", "C", 4, 0), ("B", "C", 4, 0)], [(b" ", b"abcdwxyz")])
    put("legacy/broken/cut_fields.dbf", good[:32 + 32 + 10])
    put("legacy/broken/no_terminator.dbf", good[:32 + 64])
    put("legacy/broken/no_eof_marker.dbf", good[:-1])
    put("legacy/broken/padded.dbf", dbf(0x03, [("A", "C", 3, 0)], [
        (b" ", b"one  "), (b" ", b"two  "), (b"*", b"del  "), (b" ", b"thr  "),
    ], recordlen=6))
    put("legacy/broken/bad_values.dbf", dbf(0x30, [
        ("D", "D", 8, 0), ("L", "L", 1, 0), ("N", "N", 6, 0), ("F", "F", 6, 0),
        ("M", "M", 10, 0), ("C", "C", 6, 0)], [
        (b" ", b"20240229" + b"T" + num("42", 6) + num("1.5", 6) + m10(None) + c("fine", 6)),
        (b" ", b"20241301" + b"x" + num("1.2.3", 6) + num("--", 6) + b"memo12    " + c("ok", 6)),
        (b" ", b"2024ab01" + b"?" + b"      " + num("*", 6) + b"\0" * 10 + c(b"caf\xe9", 6)),
        (b" ", b"00000000" + b" " + num("7", 6) + num("2e2", 6) + m10(8) + c(b"\x81x", 6)),
        (b" ", b" 2024 21" + b"t" + num("1_2", 6) + num("+.5", 6) + b"  0 0     " + c("", 6)),
    ], backlink=263))
    put("legacy/broken/bad_values.fpt", fpt(64, [(8, 1, b"a real memo")]))
    put("legacy/broken/missing_memo.dbf", dbf(0x83, [("T", "C", 5, 0), ("M", "M", 10, 0)], [
        (b" ", c("one", 5) + m10(1)),
        (b" ", c("two", 5) + m10(None)),
    ]))
    put("legacy/broken/vfp_double.dbf", dbf(0x30, [("X", "B", 8, 0)], [
        (b" ", d8(1.25))], backlink=263))
    put("legacy/broken/bad_memo.dbf", dbf(0x30, [("K", "C", 5, 0), ("M", "M", 4, 0)], [
        (b" ", c("ok", 5) + ptr(8)),
        (b" ", c("long", 5) + ptr(9)),
        (b" ", c("past", 5) + ptr(500)),
    ], backlink=263))
    memo = bytearray(fpt(64, [(8, 1, b"fine"), (9, 1, b"x" * 40)]))
    memo[9 * 64 + 4:9 * 64 + 8] = struct.pack(">L", 1000)  # longer than the file
    put("legacy/broken/bad_memo.fpt", bytes(memo[:9 * 64 + 48]))
    put("legacy/broken/tiny_fpt.dbf", dbf(0x30, [("M", "M", 4, 0)], [
        (b" ", ptr(0))], backlink=263))
    put("legacy/broken/tiny_fpt.fpt", b"\0\0\0\x09\0\0\0\x40")
    put("legacy/broken/bad_name.dbf", dbf(0x03, [
        field("", "C", 3, name_raw=b"N\xe4ME")], [(b" ", b"abc")], lang=0x00))
    put("legacy/broken/bad_time.dbf", dbf(0x30, [("W", "C", 6, 0), ("T", "T", 8, 0)], [
        (b" ", c("ok", 6) + t8(julian(2024, 1, 1), 0)),
        (b" ", c("early", 6) + t8(1721425, 0)),
        (b" ", c("bytes", 6) + b"\x01\x02\x03\x04\x05\x06\x07\x08"),
        (b" ", c("last", 6) + t8(julian(9999, 12, 31), 86399999)),
        (b" ", c("over", 6) + t8(julian(9999, 12, 31), 86400000)),
        (b" ", c("after", 6) + t8(julian(2024, 1, 2), 0)),
    ], backlink=263))
    put("legacy/broken/bad_auto.dbf", dbf(0x31, [("K", "+", 2, 0), ("S", "O", 4, 0)], [
        (b" ", b"\x01\x00" + b"\0\0\0\0")], backlink=263))


# ------------------------------------------------------------ the script

JOBS = []


def job(*parts):
    for p in parts:
        assert "\t" not in p and "\n" not in p, p
    JOBS.append("\t".join(parts))


def hx(b):
    return b.hex() if b else "-"


def write_jobs():
    L = "data/legacy/"
    B = "data/legacy/broken/"
    job("version")
    for v in [0x02, 0x03, 0x30, 0x31, 0x32, 0x43, 0x63, 0x83, 0x8B, 0xCB, 0xF5,
              0xE5, 0xFB, 0x00, 0x04, 0x7B, 0xFF]:
        job("dbversion", str(v))
    for d in [0x00, 0x01, 0x02, 0x03, 0x04, 0x08, 0x13, 0x26, 0x57, 0x64, 0x68,
              0x7D, 0x96, 0xC8, 0xC9, 0x99, 0xFF]:
        job("codepage", str(d))

    # dbfinfo, the library's example script, over the whole archive.
    job("dbfinfo", L + "PEOPLE.DBF", L + "orders.dbf", L + "Tickets.DBF",
        L + "notes.dbf", L + "inventory.dbf")
    job("dbfinfo", L + "kunder.dbf", L + "klienty.dbf", L + "KLIENTY_W.DBF",
        L + "menu.dbf", L + "empty.dbf", L + "names.dbf", L + "flags.dbf",
        B + "missing_memo.dbf")

    # Each table: what DBF() makes of the header, then the records.
    for path, opts in [
        ("PEOPLE.DBF", []), ("people.dbf", []), ("People.Dbf", ["lowernames=1"]),
        ("orders.dbf", []), ("Tickets.DBF", []), ("notes.dbf", []),
        ("inventory.dbf", []), ("inventory.dbf", ["lowernames=1"]),
        ("kunder.dbf", ["lowernames=1"]), ("klienty.dbf", []),
        ("KLIENTY_W.DBF", ["lowernames=1"]), ("menu.dbf", []),
        ("export.dbf", []), ("utf8.dbf", []), ("both.dbf", []),
        ("plain3.dbf", []), ("empty.dbf", []), ("longchar.dbf", []),
        ("names.dbf", []), ("names.dbf", ["lowernames=1"]), ("flags.dbf", []),
        ("numbers.dbf", []), ("currency.dbf", []), ("times.dbf", []),
        ("inv*.dbf", []), ("Ord?rs.DBF", []),
    ]:
        job("info", L + path, *opts)
    for path in ["PEOPLE.DBF", "orders.dbf", "Tickets.DBF", "notes.dbf",
                 "inventory.dbf", "names.dbf", "longchar.dbf", "empty.dbf"]:
        job("header", L + path)
    job("header", L + "kunder.dbf", "lowernames=1")
    job("header", B + "bad_values.dbf")

    for path, opts in [
        ("PEOPLE.DBF", []), ("PEOPLE.DBF", ["rec=dict"]), ("PEOPLE.DBF", ["rec=none"]),
        ("PEOPLE.DBF", ["lowernames=1"]), ("PEOPLE.DBF", ["raw=1"]),
        ("PEOPLE.DBF", ["encoding=latin-1"]), ("PEOPLE.DBF", ["encoding=ascii"]),
        ("PEOPLE.DBF", ["encoding=ascii", "char_decode_errors=replace"]),
        ("PEOPLE.DBF", ["encoding=ascii", "char_decode_errors=ignore"]),
        ("PEOPLE.DBF", ["encoding=ascii", "char_decode_errors=backslashreplace"]),
        ("orders.dbf", []), ("orders.dbf", ["raw=1"]), ("orders.dbf", ["load=1"]),
        ("Tickets.DBF", []), ("notes.dbf", []), ("notes.dbf", ["raw=1"]),
        ("inventory.dbf", []), ("kunder.dbf", []), ("kunder.dbf", ["encoding=cp850"]),
        ("klienty.dbf", []), ("KLIENTY_W.DBF", []), ("klienty.dbf", ["encoding=cp1251"]),
        ("klienty.dbf", ["encoding=cp1251", "char_decode_errors=strict"]),
        ("menu.dbf", []), ("menu.dbf", ["encoding=cp1252"]),
        ("export.dbf", []), ("export.dbf", ["encoding=cp1252"]),
        ("export.dbf", ["char_decode_errors=replace"]),
        ("export.dbf", ["encoding=cp1252", "char_decode_errors=replace"]),
        ("export.dbf", ["encoding=latin-1"]),
        ("utf8.dbf", []), ("utf8.dbf", ["encoding=utf-8"]),
        ("utf8.dbf", ["encoding=utf-8", "char_decode_errors=replace"]),
        ("utf8.dbf", ["encoding=utf-8", "char_decode_errors=ignore"]),
        ("utf8.dbf", ["encoding=utf-8", "char_decode_errors=backslashreplace"]),
        ("utf8.dbf", ["encoding=utf-8", "parser=lenient"]),
        ("both.dbf", []), ("plain3.dbf", []), ("empty.dbf", []),
        ("longchar.dbf", []), ("names.dbf", []), ("flags.dbf", []),
        ("numbers.dbf", []), ("numbers.dbf", ["parser=lenient"]),
        ("currency.dbf", []), ("times.dbf", []),
        ("people.dbf", ["ignorecase=0"]), ("PEOPLE.DBF", ["ignorecase=0"]),
        ("nothere.dbf", []), ("nothere.dbf", ["ignorecase=0"]),
        ("PEOPLE.DBF", ["parser=reverse"]), ("menu.dbf", ["parser=reverse"]),
        ("Tickets.DBF", ["parser=reverse"]), ("utf8.dbf", ["parser=reverse"]),
    ]:
        job("records", L + path, *opts)
    for path, opts in [
        ("PEOPLE.DBF", []), ("orders.dbf", []), ("orders.dbf", ["load=1"]),
        ("notes.dbf", []), ("klienty.dbf", []), ("flags.dbf", []),
        ("empty.dbf", []), ("PEOPLE.DBF", ["raw=1"]),
    ]:
        job("deleted", L + path, *opts)
    for path in ["PEOPLE.DBF", "orders.dbf", "empty.dbf"]:
        job("load", L + path)

    # The damaged files.
    for path, opts in [
        ("unknown_type.dbf", []), ("unknown_type.dbf", ["parser=hexx"]),
        ("unknown_type.dbf", ["parser=lenient"]),
        ("bad_int.dbf", []), ("bad_logical.dbf", []), ("short.dbf", []),
        ("cut_fields.dbf", []), ("no_terminator.dbf", []), ("no_eof_marker.dbf", []),
        ("padded.dbf", []), ("bad_values.dbf", []), ("bad_values.dbf", ["parser=lenient"]),
        ("bad_values.dbf", ["raw=1"]),
        ("missing_memo.dbf", []), ("missing_memo.dbf", ["ignore_missing_memofile=1"]),
        ("missing_memo.dbf", ["raw=1"]),
        ("vfp_double.dbf", []), ("vfp_double.dbf", ["ignore_missing_memofile=1"]),
        ("bad_memo.dbf", []), ("bad_memo.dbf", ["parser=lenient"]),
        ("tiny_fpt.dbf", []), ("tiny_fpt.dbf", ["raw=1"]),
        ("bad_name.dbf", []), ("bad_name.dbf", ["encoding=cp1252"]),
        ("bad_name.dbf", ["char_decode_errors=replace"]),
        ("bad_time.dbf", []), ("bad_time.dbf", ["parser=lenient"]),
        ("bad_auto.dbf", []), ("bad_auto.dbf", ["parser=lenient"]),
    ]:
        job("info", B + path, *opts)
        job("records", B + path, *opts)
    job("deleted", B + "padded.dbf")
    job("header", B + "no_terminator.dbf")
    job("header", B + "padded.dbf")

    # The memo files on their own.
    job("memo", L + "ORDERS.FPT", "48", "0,-1,8,9,10,11,12,13,14,7")
    job("memo", L + "NOTES.DBT", "131", "1,2,3,5,6,7,0")
    job("memo", L + "inventory.dbt", "139", "1,2,3,4,0")
    job("memo", L + "plain3.dbt", "3", "1")
    job("memo", L + "plain3.dbt", "131", "1")
    job("memo", B + "bad_memo.fpt", "48", "8,9")
    job("memo", B + "bad_memo.fpt", "48", "500")
    job("memo", B + "tiny_fpt.fpt", "48", "1")
    job("memo", L + "nothere.fpt", "48", "1")

    # Field parsing, one value at a time, as the library's own tests do.
    P = []

    def parse(ftype, data, *opts):
        P.append(("parse", ftype, hx(data)) + opts)

    for d in [b"\0", b"\xaa\xff", b""]:
        parse("0", d)
    for d in [b"test", b"test  \0\0", b"  lead", b"\0mid\0 ", b"", b"   ", b"tab\t"]:
        parse("C", d)
    parse("C", b"caf\xe9", "encoding=cp1252")
    parse("C", b"caf\xe9")
    parse("C", b"caf\xe9", "char_decode_errors=replace")
    parse("V", b"varchar  ")
    for d in [b"00000000", b"        ", b"19700101", b"NotIntgr", b"20240230",
              b"0000 000", b" 202 1 9", b"+1_00102", b"-0010101", b"2024010",
              b"20240101x", b"99991231", b"00010101"]:
        parse("D", d)
    for d in [b"1.5", b"  -2.25  ", b"***", b"", b"1e-07", b"12", b"*3.5*", b"abc",
              b"1_0.0_1", b"\t7\n", b"-.5e+2", b"1.e3", b"1e", b"0.30000000000000004"]:
        parse("F", d)
    for d in [b"\x01\x00\x00\x00", b"\xff\xff\xff\xff", b"\x00\x00\x00\x80",
              b"\x10\x27\x00\x00"]:
        parse("I", d)
        parse("+", d)
    parse("I", b"\x01\x00")
    for d in [b"T", b"t", b"Y", b"y", b"F", b"f", b"N", b"n", b"?", b" ", b"x", b"1",
              b"", b"TY"]:
        parse("L", d)
    for d in [b"1", b"  42  ", b"-17", b"1.5", b"1,5", b"*", b"", b"1_000", b"0012",
              b"+3", b"1e2", b"9.99", b"-0", b"bad", b"1,2,3", b"12.30"]:
        parse("N", d)
    for v in [1.5, -0.0, 1e100, 5e-324, 123456.789]:
        parse("O", struct.pack("<d", v))
    parse("O", b"\x00\x00")
    for d in [struct.pack("<LL", 2459581, 0), struct.pack("<LL", 2459581, 3723004),
              b" " * 8, struct.pack("<LL", 0, 5), struct.pack("<LL", 1721426, 1999),
              struct.pack("<LL", 1721425, 0), struct.pack("<LL", 5373484, 0),
              struct.pack("<LL", 5373485, 0), struct.pack("<LL", 0xFFFFFFFF, 0),
              struct.pack("<LL", 2147483647 + 1721425, 0),
              struct.pack("<LL", 2147483648 + 1721425, 0),
              struct.pack("<LL", 5373484, 86399999), struct.pack("<LL", 5373484, 86400000),
              struct.pack("<LL", 2460311, 0xFFFFFFFF)]:
        parse("T", d)
        parse("@", d)
    for v in [0, 1, -1, 10000, 123456789, 50000, -2**63]:
        parse("Y", struct.pack("<q", v))
    parse("B", struct.pack("<d", 2.5), "dbversion=48")
    parse("B", struct.pack("<d", 2.5), "dbversion=50")
    parse("B", b"         7", "dbversion=3")
    parse("B", b"\x00\x00", "dbversion=49")
    for t in ["M", "G", "P"]:
        for d in [b"\x07\x00\x00\x00", b"         5", b"          ", b"\0" * 10, b"abc"]:
            parse(t, d)
    parse("X", b"ff")
    parse("X", b"ff", "parser=hexx")
    parse("X", b"0x1F  ", "parser=hexx")
    parse("X", b"q", "parser=hexx")
    parse("X", b"q", "parser=lenient")
    parse("D", b"NotIntgr", "parser=lenient")
    parse("L", b"x", "parser=lenient")
    parse("C", b"caf\xe9", "parser=lenient")
    parse("I", b"\x01", "parser=lenient")
    parse("C", b"olleh 00", "parser=reverse")
    parse("C", b"tr\xc3\xa6 ", "parser=reverse")
    parse("C", b"tr\xe6", "parser=reverse")
    parse("V", b"abc", "parser=reverse")
    for p in P:
        job(*p)

    # Finding files whatever their case.
    for pat in ["data/legacy/people.dbf", "Straße.dbf", "a1_b2.DBF", "dir/ÆØÅ.fpt",
                "x-[1].dbf", "2024.123", ""]:
        job("ipat", pat or "-")
    for name, pat in [("PEOPLE.DBF", "people.dbf"), ("People.dbf", "PEOPLE.DBF"),
                      ("people.dbx", "people.dbf"), ("Strasse.dbf", "straße.dbf"),
                      ("STRASSE.DBF", "straße.dbf"), ("Straße.dbf", "STRASSE.DBF"),
                      ("notes.dbt", "*.DBT"), ("a.dbf", "?.dbf")]:
        job("ifnmatch", name, pat)
    for pat, ext in [("data/legacy/people.dbf", "-"), ("data/legacy/orders.dbf", ".fpt"),
                     ("data/legacy/orders.dbf", ".dbt"), ("data/legacy/NOTES.dbf", ".dbt"),
                     ("data/legacy/both.dbf", ".dbt"), ("data/legacy/nothere.dbf", "-"),
                     ("data/nowhere/people.dbf", "-"), ("data/legacy/tick*", "-"),
                     ("data/legacy/broken/BAD_MEMO.DBF", ".fpt")]:
        job("ifind", pat, ext)

    # The programs.
    O = "data/out/"
    job("invalid", B + "bad_values.dbf")
    job("invalid", L + "PEOPLE.DBF")
    job("reverse", L + "PEOPLE.DBF")
    job("csv", L + "PEOPLE.DBF", O + "people.csv")
    job("cat", O + "people.csv")
    job("csv", L + "orders.dbf", O + "orders.csv")
    job("cat", O + "orders.csv")
    job("csv", L + "notes.dbf", O + "notes.csv")
    job("cat", O + "notes.csv")
    job("csv", L + "export.dbf", O + "export.csv")
    job("cat", O + "export.csv")
    job("csv", L + "export.dbf", O + "export.csv", "encoding=cp1252")
    job("cat", O + "export.csv")
    job("json", L + "PEOPLE.DBF", O + "people.json")
    job("cat", O + "people.json")
    job("json", L + "orders.dbf", O + "orders.json", "lowernames=1")
    job("cat", O + "orders.json")
    job("json", L + "klienty.dbf", O + "klienty.json")
    job("cat", O + "klienty.json")
    job("json", L + "empty.dbf", O + "empty.json")
    job("cat", O + "empty.json")
    job("sql", O + "archive.sql", "-", "strict", L + "PEOPLE.DBF", L + "orders.dbf",
        L + "Tickets.DBF", L + "notes.dbf", L + "inventory.dbf", L + "kunder.dbf")
    job("cat", O + "archive.sql")
    job("sql", O + "export.sql", "-", "strict", L + "menu.dbf", L + "export.dbf")
    job("cat", O + "export.sql")
    job("sql", O + "export.sql", "cp1252", "strict", L + "menu.dbf", L + "export.dbf")
    job("cat", O + "export.sql")
    job("sql", O + "export2.sql", "-", "replace", L + "export.dbf", L + "utf8.dbf")
    job("cat", O + "export2.sql")
    job("ledger", L + "orders.dbf", O + "ledger.txt")
    job("cat", O + "ledger.txt")
    job("cat", O + "nothere.txt")


def main():
    if os.path.isdir(DATA):
        shutil.rmtree(DATA)
    write_tables()
    write_broken()
    write_jobs()
    with open(os.path.join(DATA, "jobs.tsv"), "w") as f:
        f.write("\n".join(JOBS) + "\n")
    with open(os.path.join(DATA, "files.txt"), "w") as f:
        f.write("\n".join(FILES) + "\n")
    print("%d files, %d jobs" % (len(FILES), len(JOBS)))


main()
