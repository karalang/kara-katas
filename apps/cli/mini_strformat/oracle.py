#!/usr/bin/env python3
"""Python 3.13's str.format and string.Template over data/jobs.tsv: writes
expected.out's text to stdout. Run mk.py first."""
import csv
import os
import sys
from string import Template

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from env import keywords  # noqa: E402


def esc(s):
    out = []
    for ch in s:
        o = ord(ch)
        if ch == "\\":
            out.append("\\\\")
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\t":
            out.append("\\t")
        elif o < 32 or o == 0x7f:
            out.append("\\x%02x" % o)
        else:
            out.append(ch)
    return "".join(out)


def unesc(s):
    return s.replace("\\t", "\t").replace("\\n", "\n")


def error_text(e):
    if isinstance(e, KeyError):
        return "%s: %r" % (type(e).__name__, e.args[0])
    return "%s: %s" % (type(e).__name__, e)


def positional(fields):
    args = []
    for f in fields:
        if f.startswith("i:"):
            args.append(int(f[2:]))
        else:
            args.append(f[2:])
    return args


def pairs(fields):
    d = {}
    for f in fields:
        k, _, v = f.partition("=")
        d[k] = v
    return d


def money(cents):
    return "{:,}.{:02}".format(cents // 100, cents % 100)


def read(arg):
    with open("data/" + arg[1:], encoding="utf-8") as f:
        return f.read()


def invoice(items_arg, layout_arg, vat_pct):
    rows = list(csv.DictReader(read(items_arg).splitlines()))
    layout = {}
    for line in read(layout_arg).splitlines():
        k, _, v = line.partition("\t")
        layout[k] = v
    out = []
    out.append(layout["header"].format(title="INVOICE 10427"))
    out.append(layout["cols"].format("SKU", "Item", "Qty", "Total"))
    out.append(layout["rule"].format(""))
    total = 0
    units = 0
    for r in rows:
        qty = int(r["qty"])
        line_cents = qty * int(r["cents"])
        total += line_cents
        units += qty
        out.append(layout["row"].format(sku=r["sku"], item=r["item"], qty=qty, total=money(line_cents)))
    out.append(layout["rule"].format(""))
    vat = vat_pct * total * 2 // (100 + vat_pct)
    vat = (vat + 1) // 2  # half up on the exact cents
    out.append(layout["sum"].format(label="Net", amount=money(total - vat)))
    out.append(layout["sum"].format(label="VAT %d%%" % vat_pct, amount=money(vat)))
    out.append(layout["sum"].format(label="Total EUR", amount=money(total)))
    out.append(layout["foot"].format(count=len(rows), units=units, vat_pct=vat_pct))
    for line in out:
        print("  |" + esc(line))


def main():
    kw = keywords()
    with open("data/jobs.tsv", encoding="utf-8") as f:
        jobs = f.read().splitlines()
    for job in jobs:
        f = job.split("\t")
        print("== " + " | ".join(esc(x) for x in f))
        kind = f[0]
        if kind == "format":
            try:
                print("  " + esc(unesc(f[1]).format(*positional(f[2:]), **kw)))
            except Exception as e:
                print("  " + error_text(e))
        elif kind == "template":
            t = Template(unesc(f[1]))
            d = pairs(f[2:]) if len(f) > 2 and f[2] else {}
            print("  valid %s ids %s" % (t.is_valid(), ",".join(t.get_identifiers())))
            try:
                print("  " + esc(t.substitute(d)))
            except Exception as e:
                print("  " + error_text(e))
            try:
                print("  safe " + esc(t.safe_substitute(d)))
            except Exception as e:
                print("  safe " + error_text(e))
        elif kind == "invoice":
            invoice(f[1], f[2], int(f[3]))
        elif kind == "mail":
            d = pairs(f[2:])
            rows = list(csv.DictReader(read("@items.csv").splitlines()))
            cents = sum(int(r["qty"]) * int(r["cents"]) for r in rows)
            d["total"] = money(cents)
            d["count"] = str(len(rows))
            d["day"] = "Mon 20 Oct"
            t = Template(read(f[1]))
            try:
                for line in t.substitute(d).split("\n"):
                    print("  |" + esc(line))
            except Exception as e:
                print("  " + error_text(e))


main()
