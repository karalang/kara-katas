"""Writes data/jobs.txt: the workbooks the port builds, one call a line.

A book starts with `book <file> <options>` and ends with `close`. Every line
between is `<target> <method> <args...>`, target `wb` for the Workbook or
`s<n>` for the n-th worksheet add_worksheet() returned. Arguments are typed
tokens, so the oracle and the port rebuild the same Python values:

  N None   T True   F False   i<int>   f<float repr>   s<text, %XX escaped>
  d<datetime>   D<date>   t<time>   x<days>,<seconds>,<microseconds> (timedelta)
  @<k> the k-th add_format() of the book   @u the default URL format
  L<n> a list of the next n tokens   M<n> a dict of the next n key/value pairs
  C<n> the next n string tokens joined   R<count>:<c> c repeated count times

Run: python3 -s -P -B mk.py"""
import datetime as dt
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
SAFE = set(chr(c) for c in range(0x21, 0x7F)) - set('%"\\{}~')


class Fmt:
    def __init__(self, k):
        self.k = k


URL = Fmt("u")


def pct(s):
    out = []
    for c in s:
        if c in SAFE:
            out.append(c)
        else:
            out.append("".join("%%%02X" % b for b in c.encode("utf-8")))
    return "".join(out)


def enc(v):
    if v is None:
        return ["N"]
    if v is True:
        return ["T"]
    if v is False:
        return ["F"]
    if isinstance(v, Fmt):
        return ["@%s" % v.k]
    if isinstance(v, int):
        return ["i%d" % v]
    if isinstance(v, float):
        return ["f" + repr(v)]
    if isinstance(v, str):
        if len(v) <= 200:
            return ["s" + pct(v)]
        # A long string goes as a concatenation, runs of one character as
        # R<count>:<character>.
        parts = []
        i = 0
        while i < len(v):
            j = i
            while j < len(v) and v[j] == v[i]:
                j += 1
            if j - i >= 20:
                parts.append("R%d:%s" % (j - i, pct(v[i])))
                i = j
            else:
                k = i
                while k < len(v) and not (k + 20 <= len(v) and v[k:k + 20] == v[k] * 20):
                    k += 1
                parts.append("s" + pct(v[i:k]))
                i = k
        return ["C%d" % len(parts)] + parts
    if isinstance(v, dt.datetime):
        return ["d" + v.strftime("%Y-%m-%dT%H:%M:%S.%f")]
    if isinstance(v, dt.date):
        return ["D" + v.strftime("%Y-%m-%d")]
    if isinstance(v, dt.time):
        return ["t" + v.strftime("%H:%M:%S.%f")]
    if isinstance(v, dt.timedelta):
        return ["x%d,%d,%d" % (v.days, v.seconds, v.microseconds)]
    if isinstance(v, dict):
        out = ["M%d" % len(v)]
        for k, x in v.items():
            out += enc(k) + enc(x)
        return out
    if isinstance(v, (list, tuple)):
        out = ["L%d" % len(v)]
        for x in v:
            out += enc(x)
        return out
    raise TypeError(repr(v))


class Book:
    def __init__(self, lines, name, options=None):
        self.lines = lines
        self.nfmt = 0
        self.nsheet = 0
        lines.append(" ".join(["book", pct(name)] + enc(options or {})))

    def call(self, target, method, *args):
        toks = [target, method]
        for a in args:
            toks += enc(a)
        self.lines.append(" ".join(toks))

    def fmt(self, props):
        self.call("wb", "add_format", props)
        self.nfmt += 1
        return Fmt(self.nfmt - 1)

    def sheet(self, *args):
        self.call("wb", "add_worksheet", *args)
        self.nsheet += 1
        return Sheet(self, "s%d" % (self.nsheet - 1))

    def bad_sheet(self, *args):
        # A name add_worksheet() refuses: no worksheet comes back.
        self.call("wb", "add_worksheet", *args)

    def wb(self, method, *args):
        self.call("wb", method, *args)

    def close(self):
        self.lines.append("close")


class Sheet:
    def __init__(self, book, target):
        self.book = book
        self.target = target

    def __getattr__(self, method):
        return lambda *args: self.book.call(self.target, method, *args)


def cell(r, c):
    s = ""
    c += 1
    while c:
        m = c % 26 or 26
        s = chr(64 + m) + s
        c = (c - 1) // 26
    return "%s%d" % (s, r + 1)


REGIONS = ["North", "South", "East", "West"]
REPS = {
    "North": ["Avery Brooks", "Mina Okafor", "Lars Nyberg"],
    "South": ["Rosa Delgado", "Tomás Ruiz", "Priya Nair"],
    "East": ["Hannah Cho", "Owen Fitzgerald", "Zainab Hassan"],
    "West": ["Diego Alvarez", "Kaia Sato", "Ben O'Connor"],
}
PRODUCTS = [
    ("Desk lamp", 34.5), ("Office chair", 189.0), ("Monitor arm", 72.25),
    ("Standing desk", 449.99), ("Keyboard", 58.0), ("Webcam", 64.75),
    ("Headset", 89.9), ("Cable tray", 19.95),
]


def regional_sales(lines, rng):
    b = Book(lines, "regional_sales.xlsx")
    b.wb("set_properties", {
        "title": "Regional sales, Q3 2026",
        "subject": "Quarterly revenue by region & rep",
        "author": "Finance <reporting@example.com>",
        "manager": "Dana Whitfield",
        "company": "Northwind Office Supply",
        "category": "Sales",
        "keywords": "sales, quarterly, regions",
        "comments": "Generated by the monthly close job.\nFigures are unaudited.",
        "status": "Draft",
        "hyperlink_base": "https://intranet.example.com/finance/",
        "created": dt.datetime(2026, 10, 1, 9, 30, 0),
    })
    title = b.fmt({"bold": True, "font_size": 16, "font_color": "#1F4E78"})
    head = b.fmt({"bold": True, "bg_color": "#DDEBF7", "border": 1, "align": "center",
                  "valign": "vcenter", "text_wrap": True})
    date = b.fmt({"num_format": "yyyy-mm-dd"})
    money = b.fmt({"num_format": "$#,##0.00"})
    pct_f = b.fmt({"num_format": "0.0%"})
    ints = b.fmt({"num_format": "#,##0"})
    total = b.fmt({"bold": True, "num_format": "$#,##0.00", "top": 6, "top_color": "#1F4E78"})
    total_lbl = b.fmt({"bold": True, "top": 6, "top_color": "#1F4E78"})
    money2 = b.fmt({"num_format": "$#,##0.00"})  # same key as money: one cell format
    sales = b.sheet("Sales")
    summary = b.sheet("Summary")
    lookup = b.sheet("Lookup")
    sales.merge_range("A1:H1", "Regional sales, July to September 2026", title)
    sales.set_row(0, 24)
    sales.write_row(2, 0, ["Date", "Region", "Rep", "Product", "Units", "Unit price",
                           "Revenue", "Discount"], head)
    sales.set_row(2, 30.5)
    start = dt.date(2026, 7, 1)
    rows = []
    for i in range(200):
        d = start + dt.timedelta(days=rng.randrange(92))
        reg = rng.choice(REGIONS)
        rep = rng.choice(REPS[reg])
        prod, price = rng.choice(PRODUCTS)
        units = rng.randrange(1, 40)
        disc = rng.choice([0.0, 0.0, 0.05, 0.1, 0.125])
        rows.append((d, reg, rep, prod, units, price, disc))
    rows.sort(key=lambda r: (r[0], r[1], r[2]))
    tot = 0.0
    for i, (d, reg, rep, prod, units, price, disc) in enumerate(rows):
        r = 3 + i
        sales.write_datetime(r, 0, d, date)
        sales.write_string(r, 1, reg)
        sales.write(r, 2, rep)
        sales.write(r, 3, prod)
        sales.write_number(r, 4, units, ints)
        sales.write_number(r, 5, price, money)
        rev = units * price * (1 - disc)
        tot += rev
        sales.write_formula(r, 6, "=E%d*F%d*(1-H%d)" % (r + 1, r + 1, r + 1), money2, rev)
        sales.write_number(r, 7, disc, pct_f)
    last = 3 + len(rows)
    sales.write(last, 0, "Total", total_lbl)
    sales.write_formula(last, 4, "=SUM(E4:E%d)" % last, total, sum(r[4] for r in rows))
    sales.write_formula(last, 6, "=SUM(G4:G%d)" % last, total, tot)
    sales.set_column("A:A", 11)
    sales.set_column(1, 1, 8.43)
    sales.set_column("C:D", 16)
    sales.set_column(4, 5, 10, None)
    sales.set_column("G:G", 13.5)
    sales.set_column("H:H", 9)
    sales.freeze_panes(3, 0)
    sales.autofilter(2, 0, last - 1, 7)
    sales.filter_column_list(1, ["East", "West"])
    sales.filter_column_list("Z", ["x"])
    sales.set_landscape()
    sales.set_paper(9)
    sales.fit_to_pages(1, 0)
    sales.repeat_rows(2)
    sales.set_header('&C&"Calibri,Bold"Regional Sales&RPage &P of &N')
    sales.set_footer("&L&D&R&F", {"margin": 0.4})
    sales.set_margins(0.5, 0.5, 0.9, 0.9)
    sales.print_area(0, 0, last, 7)
    sales.set_h_pagebreaks([60, 120, 0, 60])
    sales.center_horizontally()
    # Summary: one row per region, formulas with their cached values.
    summary.write_row("A1", ["Region", "Orders", "Units", "Revenue", "Share"], head)
    by = {}
    for (d, reg, rep, prod, units, price, disc) in rows:
        o, u, v = by.get(reg, (0, 0, 0.0))
        by[reg] = (o + 1, u + units, v + units * price * (1 - disc))
    for i, reg in enumerate(REGIONS):
        r = i + 1
        o, u, v = by[reg]
        summary.write(r, 0, reg)
        summary.write_formula(r, 1, '=COUNTIF(Sales!B4:B%d,A%d)' % (last, r + 1), None, o)
        summary.write_formula(r, 2, '=SUMIF(Sales!B4:B%d,A%d,Sales!E4:E%d)' % (last, r + 1, last), ints, u)
        summary.write_formula(r, 3, '=SUMIF(Sales!B4:B%d,A%d,Sales!G4:G%d)' % (last, r + 1, last), money, v)
        summary.write_formula(r, 4, "=D%d/Sales!$G$%d" % (r + 1, last + 1), pct_f, v / tot)
    summary.set_column(0, 0, 12)
    summary.set_column(1, 4, 12.75)
    summary.set_tab_color("#70AD47")
    summary.set_zoom(120)
    summary.set_selection("B2:D5")
    summary.write_boolean(6, 0, True)
    summary.write_boolean(6, 1, 0)
    summary.write(7, 0, False)
    summary.activate()
    lookup.write_column(0, 0, [p for p, _ in PRODUCTS])
    lookup.write_column("B1", [x for _, x in PRODUCTS], money)
    lookup.hide()
    b.wb("define_name", "SalesTotal", "=Sales!$G$%d" % (last + 1))
    b.wb("define_name", "Summary!Regions", "=Summary!$A$2:$A$5")
    b.wb("define_name", "Prices", "=Lookup!$B$1:$B$8")
    b.wb("define_name", "1stQuarter", "=Sales!$A$1")
    b.wb("define_name", "AB12", "=Sales!$A$1")
    b.wb("define_name", "R1C1", "=Sales!$A$1")
    b.wb("define_name", "Nowhere!Total", "=Nowhere!$A$1")
    b.wb("set_size", 1200, 800)
    b.wb("set_tab_ratio", 45.5)
    b.close()


STATUS = ["In stock", "Low", "Reorder", "Discontinued"]
ITEMS = [
    ("Copy paper A4", "Paper"), ("Copy paper Letter", "Paper"), ("Sticky notes", "Paper"),
    ("Ballpoint pens", "Writing"), ("Gel pens", "Writing"), ("Highlighters", "Writing"),
    ("Stapler", "Desk"), ("Staples 26/6", "Desk"), ("Tape dispenser", "Desk"),
    ("Toner HP 26A", "Print"), ("Toner Brother TN-760", "Print"), ("Ink cartridge #63", "Print"),
    ("USB-C cable", "Tech"), ("HDMI cable 2 m", "Tech"), ("Mouse pads", "Tech"),
    ("Whiteboard markers", "Writing"), ("Binder clips", "Desk"), ("Envelopes C5", "Paper"),
]


def inventory(lines, rng):
    b = Book(lines, "inventory.xlsx", {"default_format_properties": {"font_name": "Arial", "font_size": 10}})
    b.wb("set_properties", {"title": "Stock count", "author": "Warehouse",
                            "created": dt.datetime(2026, 10, 20, 17, 5, 44)})
    unlocked = b.fmt({"locked": False, "bg_color": "#FFF2CC"})
    hidden = b.fmt({"hidden": True})
    money = b.fmt({"num_format": "#,##0.00"})
    qty = b.fmt({"num_format": "0"})
    gen = b.fmt({"num_format": "General", "italic": True})
    head = b.fmt({"bold": True, "font_color": "white", "bg_color": "navy", "pattern": 1})
    stock = b.sheet("Stock")
    data = []
    for i, (item, cat) in enumerate(ITEMS):
        q = rng.randrange(0, 400)
        cost = round(rng.uniform(0.5, 120.0), 2)
        data.append(["SKU-%04d" % (1000 + i * 7), item, cat, q, cost, None, rng.choice(STATUS)])
    n = len(data)
    stock.add_table(0, 0, n + 1, 6, {
        "name": "Stock",
        "style": "Table Style Medium 2",
        "total_row": True,
        "data": data,
        "columns": [
            {"header": "SKU", "total_string": "Totals"},
            {"header": "Item"},
            {"header": "Category", "total_function": "count"},
            {"header": "Qty", "format": qty, "total_function": "sum",
             "total_value": sum(r[3] for r in data)},
            {"header": "Unit cost", "format": money, "total_function": "average"},
            {"header": "Value", "format": money, "formula": "=[@Qty]*[@[Unit cost]]",
             "total_function": "sum"},
            {"header": "Status", "total_function": "COUNTIF([Status],\"Reorder\")"},
        ],
    })
    stock.data_validation(1, 6, n, 6, {"validate": "list", "source": STATUS,
                                       "input_title": "Status", "input_message": "Pick one"})
    stock.data_validation("D2:D%d" % (n + 1), {"validate": "integer", "criteria": "between",
                                               "minimum": 0, "maximum": 10000,
                                               "error_title": "Quantity",
                                               "error_message": "A whole number from 0 to 10,000",
                                               "error_type": "warning"})
    stock.data_validation(1, 4, n, 4, {"validate": "decimal", "criteria": ">", "value": 0.01})
    stock.data_validation(1, 0, n, 0, {"validate": "length", "criteria": "==", "value": 8,
                                       "ignore_blank": False, "show_error": False})
    stock.data_validation(1, 1, n, 1, {"validate": "custom", "value": "=LEN(B2)<40",
                                       "dropdown": False})
    stock.data_validation("I1", {"validate": "any", "input_title": "Note",
                                 "input_message": "Free text & comments <optional>"})
    stock.data_validation("I2", {"validate": "any"})
    stock.data_validation("I3", {"validate": "list", "source": "=$K$1:$K$4",
                                 "error_type": "information"})
    stock.data_validation("I4", {"validate": "whole", "criteria": "not between", "value": 5,
                                 "maximum": "=$K$5"})
    stock.data_validation("I5", {"validate": "whole", "value": 5})
    stock.data_validation("I6", {"validate": "whole", "criteria": "~", "value": 5})
    stock.data_validation("I7", {"validate": "colour", "criteria": "=", "value": 5})
    stock.data_validation("I8", {"validate": "whole", "criteria": "=", "value": 5, "prompt": "x"})
    stock.data_validation("I9", {"validate": "whole", "criteria": "between", "value": 1})
    stock.data_validation("I10", {"validate": "list", "source": ["a" * 100, "b" * 100, "c" * 60]})
    stock.data_validation("I11", {"validate": "any", "input_title": "T" * 33})
    stock.data_validation("I12", {"validate": "time", "criteria": "<=", "value": "0.5",
                                  "error_type": "panic"})
    stock.write("I1", None, unlocked)
    stock.write_blank("I2", "ignored", unlocked)
    stock.write_blank("I3", None)
    stock.write("K1", "In stock")
    stock.write("K2", "Low", hidden)
    stock.write("K3", "Reorder", gen)
    stock.write("K4", "Discontinued")
    stock.write("K5", 500)
    stock.set_column("I:I", 18, unlocked)
    stock.set_column("K:K", None, None, {"hidden": True})
    stock.set_column("L:N", 8, None, {"level": 1, "hidden": True})
    stock.set_column("O:O", 0.5)
    stock.set_column(15, 15, 0, None, {"hidden": True})
    stock.protect("not-a-real-password", {"format_columns": True, "sort": True,
                                          "autofilter": True, "select_locked_cells": False,
                                          "objects": True, "bogus": True})
    stock.unprotect_range("I1:I20")
    stock.unprotect_range("=$K$1:$K$5", "Lists", "also-not-real")
    stock.hide_gridlines(2)
    # A second table of reorder lines with no header row and no filter.
    orders = b.sheet("Reorders")
    reorder = [[r[0], max(0, 250 - r[3])] for r in data if r[6] == "Reorder"]
    orders.add_table(1, 1, len(reorder), 2, {"header_row": False, "banded_columns": True,
                                             "banded_rows": False, "first_column": True,
                                             "style": None, "data": reorder})
    orders.add_table("E1:F3", {"name": "Draft table", "data": [[1, 2]]})
    orders.add_table("E5:F7", {"name": "AB12"})
    orders.add_table("E9:F9", {})
    orders.add_table("E11:F13", {"columns": [{"header": "Same"}, {"header": "SAME"}]})
    orders.add_table("E15:F17", {"autofit": True})
    orders.add_table("E19:F21", {"name": "R2C3"})
    orders.add_table("H1:I4", {"name": "Notes", "columns": [{"header": "Week #1 [draft]"},
                                                             {"header": "Who's next",
                                                              "total_function": "max"}],
                               "total_row": True, "autofilter": False})
    orders.merge_range("H3:I3", "clash")
    orders.merge_range("K1:L1", "Merged")
    orders.merge_range("L1:M2", "clash again")
    orders.merge_range("K5:K5", "single")
    orders.set_row(5, None, hidden, {"level": 2})
    orders.set_row(6, 0)
    orders.set_row(7, 15, None, {"hidden": True, "level": 1, "collapsed": True})
    orders.outline_settings(True, False, True, True)
    orders.autofit()
    orders.set_column("B:B", 30)
    b.close()


def timesheet(lines, rng):
    b = Book(lines, "timesheet.xlsx", {"default_date_format": "dd/mm/yyyy hh:mm",
                                       "strings_to_numbers": True})
    b.wb("set_properties", {"author": "Payroll", "company": "",
                            "created": dt.datetime(2026, 10, 23, 23, 59, 59)})
    dur = b.fmt({"num_format": "[h]:mm"})
    tm = b.fmt({"num_format": "hh:mm"})
    day = b.fmt({"num_format": 14})
    bold = b.fmt({"bold": 1})
    week = b.sheet("Week 43")
    summ = b.sheet()
    hidden = b.sheet("HR only")
    week.write_row(0, 0, ["Employee", "Day", "In", "Out", "Hours", "Note"], bold)
    names = ["Avery Brooks", "Mina Okafor", "Lars Nyberg", "Rosa Delgado", "Tomás Ruiz"]
    r = 1
    for d in range(5):
        dd = dt.date(2026, 10, 19) + dt.timedelta(days=d)
        for nm in names:
            tin = dt.datetime.combine(dd, dt.time(8, rng.randrange(0, 60), rng.randrange(0, 60)))
            span = dt.timedelta(hours=rng.randrange(6, 10), minutes=rng.randrange(0, 60),
                                seconds=rng.randrange(0, 60), microseconds=rng.randrange(0, 10) * 100000)
            tout = tin + span
            week.write(r, 0, nm)
            week.write_datetime(r, 1, dd, day)
            week.write_datetime(r, 2, tin)
            week.write(r, 3, tout, None)
            week.write_datetime(r, 4, span, dur)
            if rng.random() < 0.2:
                week.write(r, 5, rng.choice(["8.5", "1_000", " 42 ", "nan", "-inf", "1e3",
                                             "12abc", "", "0x1F", "+.5", "1__0", "Infinity",
                                             "-0", "3.", ".", "1e", "2_5.7_5"]))
            r += 1
    week.write(r, 0, dt.time(12, 30), tm)
    week.write(r, 1, dt.time(23, 59, 59, 999999))
    week.write(r + 1, 0, dt.datetime(1900, 1, 1))
    week.write(r + 1, 1, dt.datetime(1900, 2, 28, 12))
    week.write(r + 1, 2, dt.datetime(1900, 3, 1))
    week.write(r + 1, 3, dt.date(1899, 12, 31))
    week.write(r + 1, 4, dt.datetime(2026, 10, 24, 6, 7, 8, 90))
    week.write(r + 1, 5, dt.timedelta(days=-1, seconds=3600))
    week.write(r + 2, 0, "=SUM(E2:E%d)" % r)
    week.write(r + 2, 1, "{=SUM(E2:E6*1)}")
    week.write(r + 2, 2, "https://example.com/time?week=43&team=ops")
    week.write(r + 2, 3, "mailto:payroll@example.com")
    week.write(r + 2, 4, "ftp://files.example.com/drop")
    week.write(r + 2, 5, "internal:'HR only'!A1")
    week.set_column(0, 0, 16)
    week.set_column(1, 5, 12)
    week.set_default_row(18)
    week.set_row(r + 2, 21)
    week.freeze_panes(1, 1)
    week.set_selection(3, 3, 3, 3)
    week.set_top_left_cell(10, 0)
    # Links: escapes, anchors, external files, limits, and a link overwritten
    # by a number afterwards.
    summ.write_url(0, 0, "https://example.com/report [Q3] {final}.pdf")
    summ.write_url(1, 0, "https://example.com/a%20b.pdf", None, "Already escaped")
    summ.write_url(2, 0, "https://example.com/docs#Section 2", None, None, "See section 2")
    summ.write_url(3, 0, "internal:Week 43!A1", None, "Back to the week")
    summ.write_url(4, 0, "internal:'Week 43'!B2")
    summ.write_url(5, 0, "external:c:/reports/timesheet.xlsx#Sheet1!A1")
    summ.write_url(6, 0, "external:\\\\NETWORK\\share\\hours.xlsx", None, "Share")
    summ.write_url(7, 0, "external:./archive/2025.xlsx")
    summ.write_url(8, 0, "mailto:hr@example.com?subject=Hours", bold, "Mail HR")
    summ.write_url(9, 0, "https://example.com/" + "x" * 2100)
    summ.write_url(10, 0, "https://example.com/count")
    summ.write_number(10, 0, 7)
    summ.write_url(11, 0, "https://example.com/after-the-number", None, "after")
    summ.write_url(12, 0, "internal:Sheet2!C3", None, "Self", "Tip with \"quotes\"")
    summ.write("A15", "https://example.com/plain-string")
    summ.write_string("A16", "https://example.com/written-as-string")
    summ.set_column("A:A", 40)
    hidden.write(0, 0, "Salary bands")
    hidden.very_hidden()
    summ.activate()
    summ.set_first_sheet()
    week.select()
    b.wb("set_calc_mode", "manual")
    b.close()


def edge_cases(lines, rng):
    b = Book(lines, "edge_cases.xlsx", {"nan_inf_to_errors": True, "use_future_functions": True,
                                        "strings_to_urls": False, "max_url_length": 100})
    b.wb("set_properties", {"title": "Edge cases", "created": dt.datetime(2026, 1, 2, 3, 4, 5)})
    b.bad_sheet("Sheet[1]")
    b.bad_sheet("x" * 32)
    b.bad_sheet("'Quoted")
    b.bad_sheet("What?")
    s = b.sheet("Q1 Results")
    b.bad_sheet("q1 results")
    t = b.sheet("O'Brien")
    u = b.sheet()
    v = b.sheet("x" * 31)
    f_diag = b.fmt({"diag_type": 3, "diag_color": "red", "left": 2, "right": 13, "bottom": 7,
                    "bottom_color": "automatic", "left_color": "#00ff00"})
    f_font = b.fmt({"underline": 33, "font_strikeout": True, "font_script": 1, "italic": 1,
                    "font_outline": 1, "font_shadow": 1, "font_name": "Courier New",
                    "font_family": 3, "font_charset": 1, "font_color": "automatic"})
    f_font2 = b.fmt({"underline": 2, "font_script": 2, "font_condense": 1, "font_extend": 1,
                     "font_size": 9.5, "font_color": "#FF0000"})
    f_align = b.fmt({"indent": 2, "align": "right", "valign": "top", "rotation": -45,
                     "shrink": True, "reading_order": 2})
    f_align2 = b.fmt({"align": "justify_distributed", "rotation": 270, "text_wrap": True,
                      "shrink": True})
    f_align3 = b.fmt({"center_across": True, "valign": "vjustify", "rotation": 120})
    f_fill = b.fmt({"pattern": 18})
    f_fill2 = b.fmt({"pattern": 1, "bg_color": "yellow", "fg_color": "#C0C0C0"})
    f_fill3 = b.fmt({"fg_color": "lime"})
    f_fill4 = b.fmt({"pattern": 5, "bg_color": "automatic"})
    f_num = b.fmt({"num_format": "0"})
    f_num2 = b.fmt({"num_format": 4, "quote_prefix": True})
    f_num3 = b.fmt({"num_format": "0.000;[Red]-0.000", "align": "fill"})
    f_num4 = b.fmt({"num_format": 0.0, "valign": "vdistributed", "align": "centre"})
    f_theme = b.fmt({"theme": -1, "font_name": "Calibri"})
    f_idx = b.fmt({"color_indexed": 10, "bold": True})
    f_dup = b.fmt({"diag_type": 3, "diag_color": "red", "left": 2, "right": 13, "bottom": 7,
                   "bottom_color": "automatic", "left_color": "#00ff00"})
    for i, f in enumerate([f_diag, f_font, f_font2, f_align, f_align2, f_align3, f_fill, f_fill2,
                           f_fill3, f_fill4, f_num, f_num2, f_num3, f_num4, f_theme, f_idx, f_dup]):
        s.write(i, 0, "fmt %d" % i, f)
        s.write(i, 1, i * 1.25 - 3, f)
    s.write(0, 3, "Tab\there & <tags> \"q\" 'a'")
    s.write(1, 3, "  padded  ")
    s.write(2, 3, "line one\nline two")
    s.write(3, 3, "ctl\x01\x07\x1fend")
    s.write(4, 3, "literal _x0041_ and _x00e9_")
    s.write(5, 3, "\ufffe\uffff marks")
    s.write(6, 3, "trailing\n")
    s.write(7, 3, "\u00a0nbsp")
    s.write(8, 3, "Ünïcödé ✓ 漢字 😀")
    s.write(9, 3, "q" * 32800)
    s.write(10, 3, "=ignored formula? no: strings_to_formulas is on")
    s.write(11, 3, "https://not-a-link.example.com")
    s.write_number(0, 5, float("nan"))
    s.write_number(1, 5, float("inf"))
    s.write_number(2, 5, -float("inf"))
    s.write_number(3, 5, 1e300)
    s.write_number(4, 5, -2.5e-7)
    s.write_number(5, 5, 123456789012345678)
    s.write_number(6, 5, 0.1 + 0.2)
    s.write_number(7, 5, 1 / 3)
    s.write_number(8, 5, -0.0)
    s.write_number(9, 5, 2 ** 53 + 1)
    s.write_number(10, 5, 1e16)
    s.write_number(11, 5, 123456.0)
    s.write_number(12, 5, 9.999999999999999e15)
    s.write_number(13, 5, 0.0001)
    s.write_number(14, 5, 0.00001234)
    s.write_number(15, 5, True)
    s.write_formula(0, 7, "=A1&\"!\"", None, "fmt 0!")
    s.write_formula(1, 7, "=1/0", None, "#DIV/0!")
    s.write_formula(2, 7, "=B1>0", None, True)
    s.write_formula(3, 7, "=B2*2", None, 3.5)
    s.write_formula(4, 7, "")
    s.write_formula(5, 7, "=STDEV.S(B1:B10)+CONCAT(D1,D2)+BETA_DIST(1,2,3,TRUE)")
    s.write_formula(6, 7, "=_xlfn.STDEV.S(B1:B10)")
    s.write_formula(7, 7, "=LEN(MINGLE(D1))")
    s.write_formula(8, 7, "=COTH(1)+ACOTH(2)+COT(3)+T.DIST.2T(1,2)+F.DIST.RT(1,2,3)")
    s.write_formula(9, 7, "=IFS(B1>0,\"pos\",TRUE,\"neg\")", None, "pos")
    s.write_formula(10, 7, "=SORT(B1:B5)")
    s.write_dynamic_array_formula("I1:I5", "=UNIQUE(A1:A5)", None, 0)
    s.write_array_formula("J1:J3", "{=B1:B3*2}", f_num, 0)
    s.write_array_formula(4, 9, 4, 9, "=TREND(B1:B3)", None, "n/a")
    s.write_array_formula(8, 11, 6, 9, "{=MMULT(B1:B2,B1:B2)}")
    s.write_formula(1048576, 0, "=1")
    s.write(0, 16384, 1)
    s.write(-1, 0, 1)
    s.write_string(1048575, 16383, "corner")
    s.write_boolean(0, 20000, True)
    s.write_rich_string(20, 0, "plain ", f_idx, "red bold", " then ", f_font2, "small", f_align)
    s.write_rich_string(21, 0, f_font, "only formatted ", "then plain")
    s.write_rich_string(22, 0, "a", f_idx, f_font, "b")
    s.write_rich_string(23, 0, "a", f_idx, "", "b")
    s.write_rich_string(24, 0, "a", f_idx)
    s.write_rich_string(25, 0, " lead", f_theme, "x ")
    s.write_rich_string(26, 0, "link look ", URL, "here")
    s.merge_range("D30:F31", "Merged & centred", f_align3)
    s.merge_range("E31:G32", "overlap")
    s.add_table("D29:F33", {})
    s.merge_range(40, 0, 40, 0, "single")
    s.set_column(25, 23, 3.75)
    s.set_column(30, 30, None, f_fill2)
    s.set_column(16383, 16384, 4)
    s.set_row(1048576, 30)
    s.set_row(30, 45.25, f_fill3, {"level": 9, "collapsed": True})
    s.set_row(31, None, None, {"level": -2})
    s.set_zoom(5)
    s.set_print_scale(500)
    s.set_print_scale(75)
    s.set_start_page(3)
    s.print_across()
    s.print_black_and_white()
    s.set_portrait()
    s.set_paper(0)
    s.center_vertically()
    s.print_row_col_headers()
    s.hide_gridlines(0)
    s.hide_row_col_headers()
    s.hide_zero()
    s.right_to_left()
    s.set_page_view()
    s.set_header("&L&G")
    s.set_header("h" * 256)
    s.set_header("&CEdge cases", 0.5)
    s.set_footer("&CPage &P", {"align_with_margins": False, "scale_with_doc": False})
    s.repeat_columns("A:B")
    s.repeat_rows(0, 1)
    s.print_area("A1:H40")
    s.set_v_pagebreaks([5, 2, 9, 2])
    s.autofilter("A1:B17")
    s.filter_column_list("B", ["Blanks", "1.25", "-3", "x"])
    s.filter_column_list(0, ["blanks"])
    s.set_selection("C3:A1")
    s.freeze_panes("B3", 5, 1)
    s.set_tab_color("red")
    s.protect()
    t.write(0, 0, "Apostrophe sheet")
    t.print_area(0, 0, 1048575, 2)
    t.print_area(3, 0, 4, 16383)
    t.print_area(0, 0, 1048575, 16383)
    t.repeat_columns(1)
    t.autofilter("B1:A1")
    t.set_zoom(400)
    t.set_page_view(2)
    t.freeze_panes(0, 2)
    u.write_formula("A1", "=SEQUENCE(3)", None, 1)
    u.write(1, 1, "{=SUM(A1:A3)}", None, 6)
    u.write_row(3, 0, ["x", None, 5, "", True, "=A1", dt.date(2026, 10, 24)])
    u.write_column(5, 0, ["a", "b" * 32768, "c"])
    u.set_landscape()
    u.set_page_view(1)
    u.set_zoom(85)
    v.write(0, 0, "Long-named sheet")
    v.set_tab_color("#ABCDEF")
    v.fit_to_pages(2, 3)
    b.wb("define_name", "=Interest_Rate", "=0.05")
    b.wb("define_name", "'Q1 Results'!Totals", "='Q1 Results'!$B$1:$B$17")
    b.wb("define_name", "O'Brien!Local", "=O'Brien!$A$1")
    b.wb("define_name", "Rates.2026", "={0.05,0.06}")
    b.wb("define_name", "\\Path", "=1")
    b.wb("define_name", "Ünits", "=Sheet3!$A$1")
    b.wb("define_name", "Bad name", "=1")
    b.wb("define_name", "r", "=1")
    b.wb("define_name", "aaa1", "=1")
    b.wb("define_name", "abcd1", "=1")
    b.wb("read_only_recommended")
    b.wb("set_tab_ratio", 101)
    b.wb("set_calc_mode", "auto_except_tables", 191029)
    b.close()


def broken(lines, rng):
    b = Book(lines, "broken.xlsx")
    s = b.sheet("One")
    t = b.sheet("Two")
    s.add_table("A1:B3", {"name": "Orders"})
    t.add_table("A1:B3", {"name": "orders"})
    b.close()
    b = Book(lines, "empty.xlsx", {"strings_to_formulas": False})
    b.wb("set_properties", {"created": dt.datetime(2026, 10, 24, 0, 0, 0)})
    b.close()


ACCOUNTS = [
    ("1000", "Cash"), ("1100", "Accounts receivable"), ("1200", "Inventory"),
    ("2000", "Accounts payable"), ("2100", "Accrued expenses"), ("3000", "Owner's equity"),
    ("4000", "Sales revenue"), ("4100", "Service revenue"), ("5000", "Cost of goods sold"),
    ("6000", "Rent"), ("6100", "Salaries"), ("6200", "Utilities"), ("6300", "Software"),
    ("6400", "Travel"), ("6500", "Office supplies"),
]
MEMOS = ["Invoice", "Payment", "Refund", "Accrual", "Reversal", "Transfer", "Adjustment",
         "Depreciation", "Payroll run", "Card settlement"]


def ledger(lines, rng):
    b = Book(lines, "ledger.xlsx", {"strings_to_numbers": False})
    b.wb("set_properties", {"title": "General ledger, FY2026", "author": "Accounting",
                            "keywords": "ledger, journal", "created": dt.datetime(2026, 10, 24, 6, 0, 0)})
    head = b.fmt({"bold": True, "bottom": 2})
    date = b.fmt({"num_format": "dd mmm yyyy"})
    money = b.fmt({"num_format": "#,##0.00;[Red](#,##0.00)"})
    g = b.sheet("Journal")
    g.write_row(0, 0, ["Date", "Entry", "Account", "Name", "Memo", "Debit", "Credit", "Balance"], head)
    bal = 0.0
    day = dt.date(2025, 11, 1)
    for i in range(1500):
        if rng.random() < 0.15:
            day += dt.timedelta(days=1)
        code, name = rng.choice(ACCOUNTS)
        amt = round(rng.uniform(1, 25000), 2)
        if rng.random() < 0.05:
            amt = float(rng.randrange(1, 200) * 100)
        debit = rng.random() < 0.5
        bal = bal + amt if debit else bal - amt
        r = i + 1
        g.write_datetime(r, 0, day, date)
        g.write_row(r, 1, [100000 + i, code, name, "%s %s" % (rng.choice(MEMOS), rng.randrange(1, 60))])
        g.write_row(r, 5, [amt, None, bal] if debit else [None, amt, bal], money)
    g.freeze_panes(1, 0)
    g.autofilter(0, 0, 1500, 7)
    g.autofit()
    g.set_column("E:E", 10)
    t = b.sheet("Trial balance")
    t.write_row(0, 0, ["Account", "Name", "Net"], head)
    for i, (code, name) in enumerate(ACCOUNTS):
        t.write_string(i + 1, 0, code)
        t.write_string(i + 1, 1, name)
        t.write_formula(i + 1, 2, '=SUMIF(Journal!C:C,A%d,Journal!F:F)-SUMIF(Journal!C:C,A%d,Journal!G:G)'
                        % (i + 2, i + 2), money)
    t.autofit()
    b.close()


def main():
    rng = random.Random(20261024)
    lines = []
    regional_sales(lines, rng)
    inventory(lines, rng)
    timesheet(lines, rng)
    edge_cases(lines, rng)
    broken(lines, rng)
    ledger(lines, rng)
    with open(os.path.join(HERE, "data", "jobs.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("%d lines, %d bytes" % (len(lines), sum(len(x) + 1 for x in lines)))


main()
