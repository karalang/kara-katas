#!/usr/bin/env python3
"""Replays data/jobs.tsv (see mk.py) through the vendored dbfread and
prints what each job gives. Each job echoes as "> <job>"; its output
follows, two spaces in, and an exception prints as
"error <class>: <message>". The verbs:

  version, dbversion N, codepage N   the library's tables
  info PATH OPTS     DBF(PATH, **OPTS): repr, name, filename, memo file,
                     version, date, encoding, field names, record counts
  header PATH OPTS   the header and field structs
  records PATH OPTS  every record (deleted ARE skipped); the opts are the
  deleted PATH OPTS  DBF() keywords, plus rec= for the record factory and
                     parser= for a FieldParser subclass
  load PATH          load(), unload() and the with-block
  memo PATH V IDX    the memo file reader for dbversion V, at each index
  parse T HEX OPTS   FieldParser.parse() on one field of type T
  ipat / ifnmatch / ifind            the case-insensitive file helpers
  dbfinfo, invalid, reverse          the library's example scripts
  csv, json, sql, ledger             four programs that write data/out/
  cat PATH           a file under data/, each line after "  | "

Run: python3 -I -B oracle.py > expected.out"""
import collections
import csv
import datetime
import json
import os
import shutil
import sys
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
import dbfread  # noqa: E402
from dbfread import DBF, FieldParser, InvalidValue  # noqa: E402
from dbfread.codepages import guess_encoding  # noqa: E402
from dbfread.dbversions import get_dbversion_string  # noqa: E402
from dbfread.ifiles import ifind, ifnmatch, ipat  # noqa: E402
from dbfread.memo import open_memofile  # noqa: E402

os.chdir(HERE)


# The FieldParser subclasses the library's documentation and examples
# show: print_invalid_values.py, custom_field_type.py, and a parser for a
# vendor's own field type.
class LenientParser(FieldParser):
    def parse(self, field, data):
        try:
            return FieldParser.parse(self, field, data)
        except ValueError:
            return InvalidValue(data)


class ReverseParser(FieldParser):
    def parseC(self, field, data):
        # Return strings reversed.
        return data.rstrip(b' 0').decode()[::-1]


class HexParser(FieldParser):
    def parseX(self, field, data):
        """A vendor's 'X' field: a hexadecimal counter."""
        data = data.strip()
        return int(data, 16) if data else None


PARSERS = {"lenient": LenientParser, "reverse": ReverseParser, "hexx": HexParser}


def opts_of(parts):
    kw = {}
    rec = "ordered"
    for p in parts:
        k, v = p.split("=", 1)
        if k == "rec":
            rec = v
        elif k == "parser":
            kw["parserclass"] = PARSERS[v]
        elif k in ("lowernames", "ignorecase", "load", "raw", "ignore_missing_memofile"):
            kw[k] = v == "1"
        else:
            kw[k] = v
    if rec == "dict":
        kw["recfactory"] = dict
    elif rec == "none":
        kw["recfactory"] = None
    return kw


def err(e):
    cls = type(e)
    name = cls.__name__ if cls.__module__ == "builtins" else cls.__module__ + "." + cls.__name__
    return "error %s: %s" % (name, e)


def out(*words):
    print("  " + " ".join(str(w) for w in words))


def show_rec(r):
    out(repr(dict(r)) if isinstance(r, dict) else repr(r))


def records(table, which):
    rs = table.records if which == "records" else table.deleted
    first = True
    for r in rs:
        if first:
            out("type:", type(r).__name__)
            first = False
        show_rec(r)


# ------------------------------------------------------------ the programs

def dbfinfo(paths):
    # examples/dbfinfo.py
    def show(*words):
        print('  ' + ' '.join(str(word) for word in words))

    def show_field(field):
        print('    {} ({} {})'.format(field.name, field.type, field.length))

    for filename in paths:
        print(filename + ':')
        table = DBF(filename, ignore_missing_memofile=True)
        show('Name:', table.name)
        show('Memo File:', table.memofilename or '')
        show('DB Version:', table.dbversion)
        show('Records:', len(table))
        show('Deleted Records:', len(table.deleted))
        show('Last Updated:', table.date)
        show('Character Encoding:', table.encoding)
        show('Fields:')
        for field in table.fields:
            show_field(field)


def invalid(path):
    # examples/print_invalid_values.py
    table = DBF(path, parserclass=LenientParser)
    for i, record in enumerate(table):
        for name, value in record.items():
            if isinstance(value, InvalidValue):
                print('records[{}][{!r}] == {!r}'.format(i, name, value))


def reverse(path):
    # examples/custom_field_type.py
    for record in DBF(path, parserclass=ReverseParser):
        print(record['NAME'])


def to_csv(path, dest, kw):
    """Exports a table as CSV, a header row of field names and a row a
    record, as the library's print_csv.py example does."""
    table = DBF(path, **kw)
    with open(dest, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(table.field_names)
        n = 0
        for record in table:
            writer.writerow(list(record.values()))
            n += 1
    out("wrote", dest, "(%d rows)" % n)


def to_json(path, dest, kw):
    """Exports a table as a JSON array of objects; dates, timestamps,
    currency and binary memos become strings."""
    table = DBF(path, **kw)
    rows = list(table)
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False, default=str)
        f.write("\n")
    out("wrote", dest, "(%d records)" % len(rows))


# Column types from the library's dbf2sqlite script, plus the ones it
# leaves to TEXT that a SQL database can hold better.
TYPEMAP = {
    'F': 'FLOAT', 'L': 'BOOLEAN', 'I': 'INTEGER', 'C': 'TEXT', 'N': 'REAL',
    'M': 'TEXT', 'D': 'DATE', 'T': 'DATETIME', '0': 'INTEGER',
    'Y': 'NUMERIC', '+': 'INTEGER', '@': 'DATETIME', 'O': 'FLOAT',
    'V': 'TEXT', 'G': 'BLOB', 'P': 'BLOB',
}


def sql_literal(v):
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, (int, float, Decimal)):
        return str(v)
    if isinstance(v, bytes):
        return "X'" + v.hex().upper() + "'"
    if isinstance(v, (datetime.date, datetime.datetime)):
        return "'" + str(v) + "'"
    return "'" + v.replace("'", "''") + "'"


def to_sql(dest, encoding, errors, paths):
    """Migrates tables to one SQL script, as dbf2sqlite does with its
    schema dump: a CREATE TABLE and an INSERT a record, each table in a
    transaction. A decode error stops the run before anything is written."""
    lines = []
    for path in paths:
        try:
            table = DBF(path, lowernames=True,
                        encoding=None if encoding == "-" else encoding,
                        char_decode_errors=errors)
            rows = list(table)
        except UnicodeDecodeError as e:
            out(err(e))
            out("Please use --encoding or --char-decode-errors.")
            return
        lines.append("-- %s: %s, %d rows, %d deleted records skipped"
                     % (path, table.dbversion, len(rows), len(table.deleted)))
        lines.append("BEGIN;")
        lines.append('DROP TABLE IF EXISTS "%s";' % table.name)
        defs = ", ".join('"%s" %s' % (f.name, TYPEMAP.get(f.type, "TEXT"))
                         for f in table.fields)
        lines.append('CREATE TABLE "%s" (%s);' % (table.name, defs))
        for r in rows:
            lines.append('INSERT INTO "%s" VALUES (%s);'
                         % (table.name, ", ".join(sql_literal(v) for v in r.values())))
        lines.append("COMMIT;")
    with open(dest, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    out("wrote", dest, "(%d tables)" % len(paths))


def ledger(path, dest):
    """The shop's month-end report from its order book: orders, totals,
    what is still unpaid and the last order date, a line a customer."""
    table = DBF(path)
    by = {}
    for r in table:
        e = by.setdefault(r["CUSTOMER"], [0, Decimal(0), Decimal(0), None])
        e[0] += 1
        e[1] += r["TOTAL"]
        if not r["PAID"]:
            e[2] += r["TOTAL"]
        if e[3] is None or r["ORDERED"] > e[3]:
            e[3] = r["ORDERED"]
    lines = ["%-12s %6s %16s %14s  %s" % ("customer", "orders", "total", "unpaid", "last order")]
    grand = Decimal(0)
    for name in sorted(by):
        n, total, unpaid, last = by[name]
        grand += total
        lines.append("%-12s %6d %16s %14s  %s" % (name, n, total, unpaid,
                                                   last.strftime("%Y-%m-%d %H:%M")))
    lines.append("%-12s %6d %16s" % ("all", sum(e[0] for e in by.values()), grand))
    with open(dest, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    out("wrote", dest)


def cat(path):
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError as e:
        out(err(e))
        return
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    out(path, "(%d lines)" % len(lines))
    # Text mode reads with universal newlines, so no "\r" survives.
    for ln in lines:
        print("  | " + ln)


# ------------------------------------------------------------ the jobs

class MockHeader(object):
    dbversion = 0x02


class MockDBF(object):
    def __init__(self):
        self.header = MockHeader()
        self.encoding = 'ascii'
        self.char_decode_errors = 'strict'


class MockField(object):
    def __init__(self, type=''):
        self.type = type


def run(parts):
    verb, args = parts[0], parts[1:]
    if verb == "version":
        out(dbfread.__version__)
        out(repr(dbfread.version_info))
    elif verb == "dbversion":
        out(get_dbversion_string(int(args[0])))
    elif verb == "codepage":
        try:
            out(guess_encoding(int(args[0])))
        except LookupError as e:
            out(err(e))
    elif verb == "info":
        t = DBF(args[0], **opts_of(args[1:]))
        out("repr:", repr(t))
        out("name:", repr(t.name))
        out("filename:", repr(t.filename))
        out("memofilename:", repr(t.memofilename))
        out("dbversion:", t.dbversion)
        out("date:", repr(t.date))
        out("encoding:", t.encoding)
        out("field_names:", repr(t.field_names))
        out("loaded:", t.loaded)
        out("len:", len(t), "deleted:", len(t.deleted))
    elif verb == "header":
        t = DBF(args[0], **opts_of(args[1:]))
        out(repr(t.header))
        for f in t.fields:
            out(repr(f))
    elif verb in ("records", "deleted"):
        t = DBF(args[0], **opts_of(args[1:]))
        records(t, verb)
    elif verb == "load":
        t = DBF(args[0])
        out(repr(t), t.loaded, type(t.records).__name__, len(t))
        t.load()
        out(repr(t), t.loaded, type(t.records).__name__, len(t.records), len(t.deleted))
        out("iterated:", sum(1 for _ in t))
        t.load()
        t.unload()
        out(repr(t), t.loaded, type(t.deleted).__name__, len(t.deleted))
        with DBF(args[0], load=True) as t2:
            out("in with:", repr(t2), len(t2))
        out("after with:", repr(t2), t2.loaded)
    elif verb == "memo":
        for i in args[2].split(","):
            try:
                with open_memofile(args[0], int(args[1])) as m:
                    v = m[int(i)]
                out(i, type(v).__name__, repr(v))
            except Exception as e:
                out(i, err(e))
    elif verb == "parse":
        kw = dict(p.split("=", 1) for p in args[2:])
        db = MockDBF()
        db.header.dbversion = int(kw.get("dbversion", "2"))
        db.encoding = kw.get("encoding", "ascii")
        db.char_decode_errors = kw.get("char_decode_errors", "strict")
        cls = PARSERS[kw["parser"]] if "parser" in kw else FieldParser
        data = b"" if args[1] == "-" else bytes.fromhex(args[1])
        v = cls(db).parse(MockField(args[0]), data)
        out(type(v).__name__, repr(v))
    elif verb == "ipat":
        out(repr(ipat("" if args[0] == "-" else args[0])))
    elif verb == "ifnmatch":
        out(ifnmatch(args[0], args[1]))
    elif verb == "ifind":
        out(repr(ifind(args[0], ext=None if args[1] == "-" else args[1])))
    elif verb == "dbfinfo":
        dbfinfo(args)
    elif verb == "invalid":
        invalid(args[0])
    elif verb == "reverse":
        reverse(args[0])
    elif verb == "csv":
        to_csv(args[0], args[1], opts_of(args[2:]))
    elif verb == "json":
        to_json(args[0], args[1], opts_of(args[2:]))
    elif verb == "sql":
        to_sql(args[0], args[1], args[2], args[3:])
    elif verb == "ledger":
        ledger(args[0], args[1])
    elif verb == "cat":
        cat(args[0])
    else:
        raise SystemExit("unknown verb " + verb)


def main():
    out_dir = os.path.join(HERE, "data", "out")
    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    with open(os.path.join(HERE, "data", "jobs.tsv"), encoding="utf-8") as f:
        jobs = [ln for ln in f.read().split("\n") if ln]
    nerr = 0
    for line in jobs:
        parts = line.split("\t")
        print("> " + " ".join(parts))
        sys.stdout.flush()
        try:
            run(parts)
        except Exception as e:
            sys.stdout.flush()
            print("  " + err(e))
            nerr += 1
    print("%d jobs, %d ended in an error" % (len(jobs), nerr))


main()
