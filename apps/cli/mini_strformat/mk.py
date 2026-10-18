#!/usr/bin/env python3
"""Writes data/ for mini_strformat: an invoice's items, its layout, two
mail templates and the jobs."""
import os

os.makedirs("data", exist_ok=True)

ITEMS = """\
sku,item,qty,cents
A-100,Espresso beans 1 kg,2,2450
B-220,Burr grinder,1,18900
C-031,Paper filters (100),12,395
D-007,Descaler,3,1275
E-555,Milk jug 600 ml,1,2199
"""

# One format string per line: header, item line, rule, totals.
LAYOUT = """\
header\t{title:^48}
cols\t{:<6} {:<22} {:>4} {:>12}
row\t{sku:<6} {item:<22.22} {qty:>4} {total:>12}
rule\t{:-^48}
sum\t{label:>34} {amount:>13}
foot\tItems: {count}, units: {units:,}, VAT {vat_pct}% included
"""

MAIL_OK = """\
Hello $customer,

Thanks for order #${order}. Your total is $$${total}, paid by $method.
${count} items ship to $city on ${day}.

-- $shop
"""

MAIL_BAD = """\
Dear $customer,
your balance is $ 12.
"""

with open("data/items.csv", "w", encoding="utf-8") as f:
    f.write(ITEMS)
with open("data/layout.tsv", "w", encoding="utf-8") as f:
    f.write(LAYOUT)
with open("data/mail.tmpl", "w", encoding="utf-8") as f:
    f.write(MAIL_OK)
with open("data/bad.tmpl", "w", encoding="utf-8") as f:
    f.write(MAIL_BAD)

FORMATS = [
    # literal text and escapes
    "plain text", "{{literal}} braces }}{{", "a{}b{}c", "{0}{1}{0}", "{0} {}", "{} {0}",
    "{", "}", "x{0", "{0!", "{0!x}", "{0!r", "{0!rx}", "{0:{1}", "{:{:{}}}",
    "{2}", "{missing}", "{0[}", "{0.}", "{0[0]x}", "{name[0]x}",
    # positional and keyword values, conversions
    "{0}|{1}|{2}", "{name!r} {name!s} {city!a} {city!r}", "{quote!r}", "{quote!a}",
    "{empty!r}<", "{u}", "{u!r}", "{u.name} #{u.id} <{u.email}>", "{u.tags[1]}",
    "{u.tags}", "{u.missing}", "{cfg[host]}:{cfg[port]}", "{cfg[users][0]}",
    "{cfg[1]}", "{cfg[2]}", "{nums}", "{nums[4]}", "{nums[9]}", "{nums[x]}",
    "{u.tags[-1]}", "{nums:>9}", "{u:>9}", "{0.real}",
    # strings
    "[{name:20}]", "[{name:>20}]", "[{name:^20}]", "[{name:*^21}]", "[{name:.3}]",
    "[{name:>10.4}]", "[{city:~^9}]", "[{empty:-^4}]", "[{name:{w}.{p}}]",
    "[{name:{fill}{align}{w}}]", "[{1:05}]", "[{1:0>5}]",
    "{name:+}", "{name:,}", "{name:#}", "{name:=10}", "{name:z}", "{name:d}",
    "{name:.}", "{name:10.}", "{name:s}", "{name:ss}",
    # integers
    "[{n}] [{n:,}] [{n:_}] [{n:15,}] [{n:<15_}]", "[{neg:+}] [{n:+}] [{n: }] [{neg: }]",
    "[{neg:=8}] [{neg:08}] [{n:012,}] [{neg:0=+10,}]", "[{n:b}] [{n:#b}] [{n:_b}]",
    "[{n:o}] [{n:#o}] [{n:x}] [{n:#X}] [{n:#_x}] [{neg:#x}]", "[{n:d}] [{n:n}] [{zero:#x}]",
    "[{ch:c}] [{emoji:c}]", "{65:c}", "{0:c}", "{1:c}", "[{ch:^5c}]", "{n:,c}", "{n:+c}", "{n:#c}",
    "{n:.2}", "{n:.2d}", "{n:,_}", "{n:,x}", "{n:,b}", "{n:_d}", "{n:z}", "{n:q}",
    "{n:xx}", "{n:10000000000000000000}", "{n:  }", "[{big:,}]", "[{big:#x}]",
    "[{n:{w},}]", "{0:{1}}",
    # integers through the float types
    "[{n:f}] [{n:.2f}] [{neg:.0f}] [{n:#.0f}] [{n:,.2f}]", "[{n:e}] [{n:.2e}] [{n:E}] [{zero:e}]",
    "[{n:.0e}] [{n:#.0e}] [{neg:.3e}]", "[{n:%}] [{neg:.1%}] [{zero:%}] [{n:,.0%}]",
    "[{n:g}] [{n:.3g}] [{n:G}] [{neg:#g}] [{zero:g}] [{zero:#.3g}] [{p:.10g}]",
    "[{n:.10g}] [{r125:.2g}] [{r135:.2g}] [{r6:.6g}] [{r7:.6g}] [{r7:.7g}]",
    "[{n:>14.3e}] [{neg:010.1f}] [{n:_.2f}]",
]
JOBS = []
for f in FORMATS:
    JOBS.append("format\t%s\t%s" % (f.replace("\t", "\\t"), "s:ab\ti:-42\ts:Zoë"))
for t, kv in [
    ("$who likes $what", "who=tim\twhat=kung pao"),
    ("${who}s and $$5 and $$$who", "who=Ada"),
    ("$who $missing", "who=tim"),
    ("cost: $ 5", "who=tim"),
    ("tail $", ""),
    ("${unclosed", "unclosed=x"),
    ("$9lives", ""),
    ("$_ok ${_ok} $Ok", "_ok=1\tOk=2"),
    ("line one\nline $two $", "two=2"),
    ("café $naïve", "naïve=x"),
]:
    JOBS.append("template\t%s\t%s" % (t.replace("\n", "\\n"), kv))
JOBS.append("invoice\t@items.csv\t@layout.tsv\t19")
JOBS.append("invoice\t@items.csv\t@layout.tsv\t0")
JOBS.append("mail\t@mail.tmpl\tcustomer=Ada Lovelace\torder=10427\tmethod=card\tcity=London\tshop=Bean There")
JOBS.append("mail\t@bad.tmpl\tcustomer=Ada Lovelace")

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    for j in JOBS:
        f.write(j + "\n")
