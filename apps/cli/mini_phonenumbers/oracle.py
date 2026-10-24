#!/usr/bin/env python3
"""Runs data/jobs.jsonl and the two tools through the real phonenumbers
8.13.52 and prints what mini_phonenumbers.kara must print.

vendor/phonenumbers holds the library's core modules unchanged and the
metadata of the regions the jobs reach. The package's own __init__.py
pulls in the geocoder, the carrier and time zone data and the matcher,
and data/__init__.py imports the alternate formats, none of which the
jobs use, so this script builds the two packages itself: it takes the
calling code table from data/__init__.py with ast and registers a loader
for every region, which loads the vendored ones and records the rest. It
fails at the end if a job asked for metadata that is not vendored.

Run from this directory: python3 -I -B oracle.py > expected.out"""
import ast
import importlib
import json
import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.join(HERE, "vendor", "phonenumbers")

pkg = types.ModuleType("phonenumbers")
pkg.__path__ = [V]
sys.modules["phonenumbers"] = pkg
data = types.ModuleType("phonenumbers.data")
data.__path__ = [os.path.join(V, "data")]
data.__package__ = "phonenumbers.data"
with open(os.path.join(V, "data", "__init__.py"), encoding="utf-8") as f:
    for node in ast.parse(f.read()).body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in ("_COUNTRY_CODE_TO_REGION_CODE", "_AVAILABLE_REGION_CODES",
                        "_AVAILABLE_NONGEO_COUNTRY_CODES"):
                setattr(data, name, ast.literal_eval(node.value))
sys.modules["phonenumbers.data"] = data
pkg.data = data

from phonenumbers.phonemetadata import PhoneMetadata  # noqa: E402

VENDORED = set(n[len("region_"):-3] for n in os.listdir(os.path.join(V, "data"))
               if n.startswith("region_") and n.endswith(".py"))
MISSING = []


def loader(code):
    code = str(code)
    if code in VENDORED:
        importlib.import_module("phonenumbers.data.region_" + code)
    else:
        MISSING.append(code)


for r in data._AVAILABLE_REGION_CODES:
    PhoneMetadata.register_region_loader(r, loader)
for c in data._AVAILABLE_NONGEO_COUNTRY_CODES:
    PhoneMetadata.register_nongeo_region_loader(c, loader)

import phonenumbers.phonenumberutil as pu  # noqa: E402
from phonenumbers.phonenumberutil import (PhoneNumberFormat, PhoneNumberType, MatchType,  # noqa: E402
                                          ValidationResult, NumberParseException)
from phonenumbers.asyoutypeformatter import AsYouTypeFormatter  # noqa: E402
from phonenumbers.phonenumber import PhoneNumber  # noqa: E402

TYPE_NAMES = PhoneNumberType.to_string


def q(s):
    return "None" if s is None else "'%s'" % s


def parse(s, r, raw=False):
    try:
        return pu.parse(s, r, keep_raw_input=raw), None
    except NumberParseException as e:
        return None, str(e)


def describe(n, r, raw):
    print("  e164 %s | intl %s | national %s | rfc3966 %s" % (
        pu.format_number(n, PhoneNumberFormat.E164),
        pu.format_number(n, PhoneNumberFormat.INTERNATIONAL),
        pu.format_number(n, PhoneNumberFormat.NATIONAL),
        pu.format_number(n, PhoneNumberFormat.RFC3966)))
    t = pu.number_type(n)
    print("  type %s, valid %s, region %s, possible %s, geographical %s" % (
        TYPE_NAMES(t), pu.is_valid_number(n), pu.region_code_for_number(n),
        ValidationResult.to_string(pu.is_possible_number_with_reason(n)),
        pu.is_number_geographical(n)))
    line = "  area code %d, ndc %d, dialable from abroad %s" % (
        pu.length_of_geographical_area_code(n), pu.length_of_national_destination_code(n),
        pu.can_be_internationally_dialled(n))
    if r is not None:
        line += ", valid for %s %s" % (r, pu.is_valid_number_for_region(n, r))
    print(line)
    if raw:
        print("  original %s" % pu.format_in_original_format(n, r))


def job_num(j):
    n, err = parse(j["s"], j["r"], j["raw"])
    head = "parse %s %s:" % (q(j["s"]), j["r"])
    if err is not None:
        print(head, err)
        return
    print(head, str(n))
    describe(n, j["r"], j["raw"])


def job_oocf(j):
    n, err = parse(j["s"], j["r"])
    print("dial %s %s:" % (q(j["s"]), j["r"]), err if err is not None else pu.format_number(n, PhoneNumberFormat.E164))
    if err is not None:
        return
    for frm in j["from"]:
        print("  from %s: %s | mobile %s | %s" % (
            frm, pu.format_out_of_country_calling_number(n, frm),
            q(pu.format_number_for_mobile_dialing(n, frm, True)),
            q(pu.format_number_for_mobile_dialing(n, frm, False))))


def job_alpha(j):
    print("alpha %s %s: alpha %s, converted %s" % (
        q(j["s"]), j["r"], pu.is_alpha_number(j["s"]), q(pu.convert_alpha_characters_in_number(j["s"]))))
    n, err = parse(j["s"], j["r"], True)
    if err is not None:
        print(" ", err)
        return
    for frm in j["from"]:
        print("  from %s: %s" % (frm, pu.format_out_of_country_keeping_alpha_chars(n, frm)))


def job_carrier(j):
    n, err = parse(j["s"], j["r"], True)
    head = "carrier %s %s %s:" % (q(j["s"]), j["r"], q(j["cc"]))
    if err is not None:
        print(head, err)
        return
    print(head, "%s | preferred %s" % (
        pu.format_national_number_with_carrier_code(n, j["cc"]),
        pu.format_national_number_with_preferred_carrier_code(n, j["cc"])))


def job_match(j):
    print("match %s %s: %s" % (q(j["a"]), q(j["b"]), MatchType.to_string(pu.is_number_match(j["a"], j["b"]))))


def job_trunc(j):
    n, err = parse(j["s"], j["r"])
    head = "truncate %s:" % q(j["s"])
    if err is not None:
        print(head, err)
        return
    before = pu.format_number(n, PhoneNumberFormat.E164)
    ok = pu.truncate_too_long_number(n)
    print(head, "%s -> %s %s" % (before, ok, pu.format_number(n, PhoneNumberFormat.E164)))


def job_aytf(j):
    f = AsYouTypeFormatter(j["r"])
    outs = []
    for k, c in enumerate(j["keys"]):
        outs.append(f.input_digit(c, k == j["remember"]))
    print("type %s %s: %s" % (j["r"], q(j["keys"]), " | ".join(outs)))
    if j["remember"] >= 0:
        print("  remembered position %d" % f.get_remembered_position())
    f.clear()
    again = [f.input_digit(c) for c in j["keys"][:4]]
    print("  after clear: %s" % " | ".join(again))


def job_region(j):
    r = j["r"]
    cc = pu.country_code_for_region(r)
    types_ = sorted(TYPE_NAMES(t) for t in pu.supported_types_for_region(r))
    print("region %s: code %d, national prefix %s / %s, nanpa %s, portable %s" % (
        r, cc, q(pu.ndd_prefix_for_region(r, True)), q(pu.ndd_prefix_for_region(r, False)),
        pu.is_nanpa_country(r), pu.is_mobile_number_portable_region(r)))
    print("  types %s" % ", ".join(types_))
    print("  sharing %d: %s" % (cc, " ".join(pu.region_codes_for_country_code(cc))))


def job_example(j):
    n = pu.example_number_for_type(j["r"], j["t"])
    head = "example %s %s:" % (j["r"], TYPE_NAMES(j["t"]))
    if n is None:
        print(head, None)
        return
    print(head, "%s, which is %s" % (pu.format_number(n, PhoneNumberFormat.INTERNATIONAL),
                                     TYPE_NAMES(pu.number_type(n))))


JOBS = {"num": job_num, "oocf": job_oocf, "alpha": job_alpha, "carrier": job_carrier,
        "match": job_match, "trunc": job_trunc, "aytf": job_aytf, "region": job_region,
        "example": job_example}


def contacts_tool():
    print("== contacts")
    with open(os.path.join(HERE, "data", "contacts.csv"), encoding="utf-8") as f:
        rows = [line.rstrip("\n").split(",") for line in f][1:]
    kept = []
    by_region = {}
    by_type = {}
    bad = 0
    for name, country, phone in rows:
        n, err = parse(phone, country or None, True)
        if err is not None:
            print("%s: %s (%s)" % (name, phone, err))
            bad += 1
            continue
        if not pu.is_valid_number(n):
            reason = ValidationResult.to_string(pu.is_possible_number_with_reason(n))
            print("%s: %s is not valid (%s, %s)" % (name, phone, reason,
                                                    pu.format_number(n, PhoneNumberFormat.E164)))
            bad += 1
            continue
        region = pu.region_code_for_number(n)
        t = TYPE_NAMES(pu.number_type(n))
        print("%s: %s (%s %s) %s" % (name, pu.format_number(n, PhoneNumberFormat.E164), region, t,
                                     pu.format_in_original_format(n, country or "US")))
        by_region[region] = by_region.get(region, 0) + 1
        by_type[t] = by_type.get(t, 0) + 1
        kept.append((name, n))
    for a in range(len(kept)):
        for b in range(a + 1, len(kept)):
            m = pu.is_number_match(kept[a][1], kept[b][1])
            if m != MatchType.NO_MATCH:
                print("same number: %s and %s (%s)" % (kept[a][0], kept[b][0], MatchType.to_string(m)))
    print("valid %d, rejected %d" % (len(kept), bad))
    print("by region: %s" % ", ".join("%s %d" % (k, by_region[k]) for k in sorted(by_region)))
    print("by type: %s" % ", ".join("%s %d" % (k, by_type[k]) for k in sorted(by_type)))


# cents a minute
def rate(home_cc, n, t):
    if t in ("TOLL_FREE",):
        return 0
    if t == "PREMIUM_RATE":
        return 150
    if n.country_code == home_cc:
        return 3 if t == "MOBILE" else 1
    if n.country_code == 1 and home_cc == 1:
        return 2
    return 9 if n.country_code in (1, 44, 49, 33, 39, 34, 41, 31) else 24


def calls_tool():
    print("== calls")
    total = 0
    minutes_total = 0
    per_home = {}
    with open(os.path.join(HERE, "data", "calls.txt"), encoding="utf-8") as f:
        for line in f:
            home, minutes, country, phone = line.rstrip("\n").split(" ", 3)
            minutes = int(minutes)
            n, err = parse(phone, home if country == "-" else country)
            if err is not None:
                print("%s %s: %s" % (home, phone, err))
                continue
            if not pu.is_valid_number(n):
                print("%s %s: not a valid number" % (home, phone))
                continue
            t = TYPE_NAMES(pu.number_type(n))
            dial = pu.format_number_for_mobile_dialing(n, home, True)
            if dial == "":
                print("%s %s: %s cannot be dialled from %s" % (home, phone, t, home))
                continue
            cents = rate(pu.country_code_for_region(home), n, t) * minutes
            total += cents
            minutes_total += minutes
            per_home[home] = per_home.get(home, 0) + cents
            print("%s %s: dial %s, %s, %d min, %d.%02d" % (
                home, phone, dial, t, minutes,
                cents // 100, cents % 100))
    print("%d minutes, %d.%02d" % (minutes_total, total // 100, total % 100))
    print("by caller: %s" % ", ".join("%s %d.%02d" % (k, per_home[k] // 100, per_home[k] % 100)
                                      for k in sorted(per_home)))


def main():
    with open(os.path.join(HERE, "data", "jobs.jsonl"), encoding="utf-8") as f:
        for line in f:
            j = json.loads(line)
            JOBS[j["op"]](j)
    contacts_tool()
    calls_tool()
    if MISSING:
        raise SystemExit("metadata not vendored: %s" % " ".join(sorted(set(MISSING))))


main()
