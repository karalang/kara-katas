#!/usr/bin/env python3
"""Writes the inputs of mini_phonenumbers under data/:

- data/jobs.jsonl: one job a line, each a call or a few calls into
  phonenumbers' API (see oracle.py for what each kind does);
- data/contacts.csv: an address book, for the contacts tool;
- data/calls.txt: a call log, for the dialer tool.

The contacts start from the example numbers in the vendored metadata,
read with ast and never imported, and are written the ways people write
numbers. A seeded generator picks the variations.

Run: python3 -s -P -B mk.py"""
import ast
import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
META = os.path.join(HERE, "vendor", "phonenumbers", "data")


def region_examples(region):
    with open(os.path.join(META, "region_%s.py" % region), encoding="utf-8") as f:
        tree = ast.parse(f.read())
    call = tree.body[-1].value
    kw = {k.arg: k.value for k in call.keywords}
    out = {"cc": ast.literal_eval(kw["country_code"])}
    np = kw.get("national_prefix")
    out["np"] = ast.literal_eval(np) if np is not None else ""
    for name, v in kw.items():
        if isinstance(v, ast.Call) and v.func.id == "PhoneNumberDesc":
            d = {k.arg: k.value for k in v.keywords}
            if "example_number" in d:
                out[name] = ast.literal_eval(d["example_number"])
    return out


def jobs():
    out = []

    def num(s, r, raw=False):
        out.append({"op": "num", "s": s, "r": r, "raw": raw})

    # the United States and its neighbours on +1
    num("(650) 253-0000", "US", True)
    num("+1 650-253-0000", "US", True)
    num("1-650-253-0000", "US", True)
    num("650.253.0000 ext. 123", "US", True)
    num("6502530000;ext=55", "US")
    num("tel:+1-650-253-0000;isub=12", "US")
    num("tel:253-0000;phone-context=+1-650", "US", True)
    num("tel:+1-650-253-0000;phone-context=example.com", "US")
    num("tel:253-0000;phone-context=", "US")
    num("tel:253-0000;phone-context=-example", "US")
    num("1-800-FLOWERS", "US", True)
    num("800 MY APPLE", "US", True)
    num("011 44 20 7031 3000", "US", True)
    num("+1 (201) 555-0123 x 42/x43", "US")
    num("201-555-0123 #", "US")
    num("201 555 0123 - 503#", "US")
    num("2015550123,,456", "US")
    num("(201) 555-0123;789", "US")
    num("201 555 0123 extensión 7", "US")
    num("201 555 0123 доб 8", "US")
    num("555-0123", "US", True)
    num("12", "US")
    num("1", "US")
    num("abc", "US")
    num("+", "US")
    num("+0 1234", "US")
    num("+999 123 456 789", "US")
    num("+1 123 456 7890", "US")
    num("12015550123", "US", True)
    num("011 1", "US")
    num("+44 1", None)
    num("+1 234567890123456789", None)
    num("+1 650 253 0000 " + "-" * 240, "US")
    num("＋１ ６５０ ２５３ ００００", "US", True)
    num("Call 650 253 0000 now!", "US")
    num("+1 613 555 0199", "CA")
    num("613 555 0199", "CA", True)
    num("+1 242 357 1234", None)
    num("+1 876 512 3456", None)
    num("+1 345 323 4567", None)
    num("+1 268 464 1234", None)
    num("+1 787 234 5678", None)
    num("+1 340 642 1234", None)
    num("+1 671 300 1234", None)
    num("300 1234", "GU", True)
    # Britain and the Crown dependencies
    num("020 7031 3000", "GB", True)
    num("+44 (0) 20 7031 3000", "GB", True)
    num("07400 123456", "GB", True)
    num("0800 123 4567", "GB")
    num("0044 20 7031 3000", "GB", True)
    num("+44 1481 256789", None)
    num("01624 756789", "IM", True)
    num("+441534 456789", None)
    num("456789", "JE", True)
    num("٠٢٠ ٧٠٣١ ٣٠٠٠", "GB")
    num("020 7031 3000", None)
    num("020 7031 3000", "ZZ")
    num("+44 20 7031 300", None)
    # the rest of Europe
    num("030 123456", "DE", True)
    num("+49 (0)30 1234 5678", "DE", True)
    num("0151 23456789", "DE", True)
    num("089 1234567", "DE")
    num("0180 2 123456", "DE")
    num("+49 30 12345678901234", None)
    num("01 23 45 67 89", "FR", True)
    num("+33 6 12 34 56 78", "FR")
    num("0033 1 23 45 67 89", "FR", True)
    num("02 1234 5678", "IT", True)
    num("+39 06 6981 2345", None)
    num("+39 312 345 6789", None)
    num("0039 02 12345678", "IT", True)
    num("+3900012345", None)
    num("912 34 56 78", "ES", True)
    num("+34 612 34 56 78", "ES")
    num("044 668 18 00", "CH", True)
    num("+41 79 123 45 67", "CH")
    num("00 41 44 668 18 00", "CH", True)
    num("020 123 4567", "NL", True)
    num("06 12345678", "NL")
    num("+31 (0)20 123 4567", "NL", True)
    num("8 (495) 123-45-67", "RU", True)
    num("+7 912 345-67-89", "RU")
    num("8 10 1 650 253 0000", "RU", True)
    num("+7 701 123 4567", None)
    num("+7 727 123 4567", None)
    # Asia and the Pacific
    num("(02) 9876 5432", "AU", True)
    num("0412 345 678", "AU")
    num("+61 1800 123 456", "AU")
    num("0011 1 650 253 0000", "AU", True)
    num("0014 44 20 7031 3000", "AU", True)
    num("+61 8 9162 1234", None)
    num("+61 8 9164 1234", None)
    num("09 123 4567", "NZ", True)
    num("021 123 4567", "NZ")
    num("0161 1 650 253 0000", "NZ", True)
    num("03-1234-5678", "JP", True)
    num("090-1234-5678", "JP", True)
    num("+81 3 1234 5678", "JP")
    num("0120-123-456", "JP")
    num("011 2345 6789", "IN", True)
    num("+91 98765 43210", "IN")
    num("098765 43210", "IN", True)
    num("1800 123 4567", "IN")
    num("6123 4567", "SG", True)
    num("+65 8123 4567", "SG")
    num("001 1 650 253 0000", "SG", True)
    num("+800 1234 5678", None)
    num("+800 1234 5678", "US", True)
    # the Americas
    num("011 15 2345-6789", "AR", True)
    num("+54 9 11 2345 6789", "AR", True)
    num("0351 15 412 3456", "AR", True)
    num("(011) 4567-8901", "AR", True)
    num("+54 11 4567-8901", None)
    num("0800 123 4567", "AR")
    num("(11) 96123-4567", "BR", True)
    num("0 15 11 96123 4567", "BR", True)
    num("+55 21 2345 6789", "BR")
    num("0xx21 2345 6789", "BR", True)
    num("0021 1 650 253 0000", "BR", True)
    num("55 1234 5678", "MX", True)
    num("+52 1 55 1234 5678", "MX", True)
    num("044 55 1234 5678", "MX", True)
    num("01 55 1234 5678", "MX", True)
    num("00 1 650 253 0000", "MX", True)

    def oocf(s, r, frm):
        out.append({"op": "oocf", "s": s, "r": r, "from": frm})

    everywhere = ["US", "CA", "GB", "DE", "AU", "RU", "BR", "MX", "SG", "JP", "NZ"]
    oocf("650 253 0000", "US", everywhere)
    oocf("020 7031 3000", "GB", everywhere)
    oocf("07400 123456", "GB", ["GB", "GG", "US", "DE"])
    oocf("030 123456", "DE", ["DE", "CH", "US", "AU"])
    oocf("0800 123 4567", "GB", ["GB", "US"])
    oocf("011 15 2345-6789", "AR", ["AR", "US", "BR"])
    oocf("(11) 96123-4567", "BR", ["BR", "AR", "US"])
    oocf("0 15 11 96123 4567", "BR", ["BR", "US"])
    oocf("55 1234 5678", "MX", ["MX", "US"])
    oocf("+800 1234 5678", None, ["US", "GB", "JP"])
    oocf("02 1234 5678", "IT", ["IT", "VA", "US"])
    oocf("8 (495) 123-45-67", "RU", ["RU", "KZ", "US"])
    oocf("+1 242 357 1234", None, ["US", "BS", "GB"])
    oocf("650.253.0000 ext. 123", "US", ["US", "GB"])
    oocf("+44 20 7031 3000 ext 22", None, ["GB", "US", "ZZ"])
    oocf("09 123 4567", "NZ", ["NZ", "AU", "US"])

    def alpha(s, r, frm):
        out.append({"op": "alpha", "s": s, "r": r, "from": frm})

    alpha("1-800-FLOWERS", "US", ["US", "GB", "AU", "DE"])
    alpha("800 MY APPLE", "US", ["US", "GB"])
    alpha("0800 BUY NOW", "GB", ["GB", "US"])
    alpha("+61 1300 TAXI CAB", None, ["AU", "NZ"])

    def carrier(s, r, cc):
        out.append({"op": "carrier", "s": s, "r": r, "cc": cc})

    carrier("(11) 96123-4567", "BR", "15")
    carrier("0 21 11 96123 4567", "BR", "15")
    carrier("+55 21 2345 6789", None, "")
    carrier("011 15 2345-6789", "AR", "15")
    carrier("650 253 0000", "US", "15")

    def match(a, b):
        out.append({"op": "match", "a": a, "b": b})

    match("+1 650 253 0000", "+1-650-253-0000")
    match("+1 650 253 0000", "650 253 0000")
    match("650 253 0000", "+1 650 253 0000")
    match("650 253 0000", "(650) 253-0000")
    match("+1 650 253 0000", "253 0000")
    match("+1 650 253 0000 ext 1", "+1 650 253 0000 ext 2")
    match("+1 650 253 0000 ext 1", "+1 650 253 0000")
    match("+44 20 7031 3000", "+1 20 7031 3000")
    match("+39 02 1234 5678", "+39 2 1234 5678")
    match("abc", "+1 650 253 0000")
    match("3 1234 5678", "+81 3 1234 5678")
    match("+800 1234 5678", "1234 5678")

    def trunc(s, r):
        out.append({"op": "trunc", "s": s, "r": r})

    trunc("+1 650 253 00001", None)
    trunc("+44 20 7031 30001234", None)
    trunc("+49 30 1234567890123", None)
    trunc("+1 123 456 78901", None)
    trunc("+33 1 23 45 67 89", None)

    def aytf(r, keys, remember=-1):
        out.append({"op": "aytf", "r": r, "keys": keys, "remember": remember})

    aytf("US", "6502530000", 4)
    aytf("US", "16502530000")
    aytf("US", "+16502530000", 7)
    aytf("US", "011442070313000")
    aytf("US", "650-253-0000", 5)
    aytf("US", "18002345678")
    aytf("CA", "+442070313000")
    aytf("GB", "02070313000", 3)
    aytf("GB", "07400123456")
    aytf("GB", "00498912345678")
    aytf("DE", "03012345678")
    aytf("DE", "015123456789")
    aytf("AR", "01123456789")
    aytf("AR", "0111523456789")
    aytf("AR", "+5491123456789")
    aytf("BR", "011961234567")
    aytf("BR", "0151196123456")
    aytf("JP", "0312345678")
    aytf("JP", "09012345678")
    aytf("AU", "0011442070313000")
    aytf("AU", "0298765432")
    aytf("MX", "5512345678")
    aytf("MX", "0445512345678")
    aytf("RU", "84951234567")
    aytf("RU", "+79123456789")
    aytf("IT", "0212345678")
    aytf("IN", "09876543210")
    aytf("SG", "61234567")
    aytf("NZ", "091234567")
    aytf("GG", "01481256789")
    aytf("ZZ", "+80012345678")
    aytf("ZZ", "6502530000")
    aytf("US", "*6502530000")
    aytf("US", "＋１６５０２５３００００")

    def region(r):
        out.append({"op": "region", "r": r})

    for r in ["US", "CA", "GB", "GG", "DE", "AR", "BR", "AU", "RU", "KZ", "VA", "ZZ", "AA"]:
        region(r)

    def example(r, t):
        out.append({"op": "example", "r": r, "t": t})

    for r, ts in [("US", [0, 1, 3, 7]), ("GB", [0, 1, 3, 4, 6, 8, 9]), ("DE", [0, 1, 5, 10]),
                  ("AR", [0, 1, 3]), ("BR", [0, 1, 5]), ("JP", [0, 1, 8]), ("IT", [0, 1, 10]),
                  ("AU", [0, 1, 5, 8]), ("IN", [0, 1, 4]), ("SG", [3, 9])]:
        for t in ts:
            example(r, t)
    return out


# the contacts' regions, with how many each
CONTACT_REGIONS = [("US", 8), ("CA", 3), ("GB", 6), ("GG", 1), ("JE", 1), ("DE", 5), ("FR", 4),
                   ("IT", 4), ("ES", 3), ("CH", 2), ("NL", 3), ("AU", 4), ("NZ", 2), ("JP", 4),
                   ("IN", 4), ("SG", 3), ("RU", 3), ("KZ", 1), ("AR", 3), ("BR", 4), ("MX", 3),
                   ("JM", 1), ("BS", 1)]
FIRST = ["Ada", "Bruno", "Chen", "Dalia", "Emeka", "Freya", "Goran", "Hana", "Ines", "Jonas",
         "Kiri", "Lars", "Mei", "Nadia", "Omar", "Priya", "Quinn", "Rosa", "Sven", "Tomas",
         "Uma", "Vera", "Wim", "Xavier", "Yuki", "Zara"]
LAST = ["Abara", "Brandt", "Costa", "Dubois", "Engel", "Fischer", "Gallo", "Hughes", "Ivanova",
        "Jensen", "Kato", "Lopez", "Moreau", "Nakamura", "Okafor", "Patel", "Quiroga", "Rossi",
        "Sato", "Tanaka", "Ueda", "Varga", "Weber", "Young"]
TYPES = ["fixed_line", "mobile", "mobile", "toll_free"]


def group(digits, rng):
    sep = rng.choice([" ", " ", "-", ".", ""])
    out = []
    k = 0
    while k < len(digits):
        n = rng.choice([2, 3, 3, 4, 4])
        out.append(digits[k:k + n])
        k += n
    if len(out) > 2 and rng.random() < 0.25:
        out[0] = "(" + out[0] + ")"
    return sep.join(out)


def contacts(rng):
    lines = ["name,country,phone"]
    seen = set()
    for region, count in CONTACT_REGIONS:
        ex = region_examples(region)
        for _ in range(count):
            while True:
                name = rng.choice(FIRST) + " " + rng.choice(LAST)
                if name not in seen:
                    seen.add(name)
                    break
            kinds = [t for t in TYPES if t in ex]
            nsn = ex[rng.choice(kinds)]
            # change the last two digits
            nsn = nsn[:-2] + "%02d" % rng.randrange(100)
            roll = rng.random()
            if roll < 0.06:
                nsn = nsn[:-1]
            elif roll < 0.1:
                nsn = nsn + str(rng.randrange(10))
            style = rng.random()
            if style < 0.35:
                phone = "+%d %s" % (ex["cc"], group(nsn, rng))
            elif style < 0.8:
                phone = ex["np"] + group(nsn, rng)
            elif style < 0.9:
                phone = "00%d%s" % (ex["cc"], nsn)
            else:
                phone = "%s%s ext %d" % (ex["np"], group(nsn, rng), rng.randrange(10, 999))
            country = region if rng.random() < 0.9 else rng.choice(["US", "GB", ""])
            lines.append("%s,%s,%s" % (name, country, phone))
    # duplicates of earlier contacts, written another way
    for k in range(6):
        name, country, phone = lines[1 + rng.randrange(len(lines) - 1)].split(",")
        digits = "".join(c for c in phone if c.isdigit() or c == "+")
        lines.append("%s (work),%s,%s" % (name, country, digits))
    body = lines[1:]
    rng.shuffle(body)
    return "\n".join([lines[0]] + body) + "\n"


def calls(rng, contact_text):
    phones = []
    for line in contact_text.splitlines()[1:]:
        name, country, phone = line.split(",")
        phones.append((country, phone))
    homes = ["US", "GB", "DE", "BR", "MX", "AU", "JP"]
    lines = []
    for k in range(40):
        home = rng.choice(homes)
        country, phone = rng.choice(phones)
        minutes = rng.randrange(1, 60)
        lines.append("%s %d %s %s" % (home, minutes, country or "-", phone))
    lines.append("US 5 US 1-800-FLOWERS")
    lines.append("GB 3 GB 0800 123 4567")
    lines.append("DE 12 DE 0900 1234567")
    lines.append("JP 7 - +800 1234 5678")
    return "\n".join(lines) + "\n"


def main():
    rng = random.Random(20261024)
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "jobs.jsonl"), "w", encoding="utf-8") as f:
        for job in jobs():
            f.write(json.dumps(job, ensure_ascii=False) + "\n")
    text = contacts(rng)
    with open(os.path.join(DATA, "contacts.csv"), "w", encoding="utf-8") as f:
        f.write(text)
    with open(os.path.join(DATA, "calls.txt"), "w", encoding="utf-8") as f:
        f.write(calls(rng, text))


main()
