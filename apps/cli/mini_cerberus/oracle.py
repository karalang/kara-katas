# Runs data/jobs.tsv through Cerberus 1.3.8 (the cerberus/ package next to
# this file, unchanged) and prints what it did. mini_cerberus.kara must
# print the same bytes.
#
# The schemas and documents are JSON. AppValidator adds the coercers,
# default setters and checks the schemas name, the way an application
# subclasses Validator.
import datetime
import json
import os
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import cerberus  # noqa: E402
from cerberus import SchemaError, Validator, rules_set_registry, schema_registry  # noqa: E402

warnings.simplefilter("ignore")

OUT = []


def emit(s):
    OUT.append(s)


def read(rel):
    with open(os.path.join(HERE, "data", rel), encoding="utf-8") as f:
        return f.read()


def load(rel):
    return json.loads(read(rel))


class AppValidator(Validator):
    # coercers
    def _normalize_coerce_int(self, value):
        return int(value)

    def _normalize_coerce_float(self, value):
        return float(value)

    def _normalize_coerce_strip(self, value):
        return value.strip()

    def _normalize_coerce_lower(self, value):
        return value.lower()

    def _normalize_coerce_split(self, value):
        return [x.strip() for x in value.split(",")]

    def _normalize_coerce_yesno(self, value):
        return {"yes": True, "y": True, "true": True, "1": True,
                "no": False, "n": False, "false": False, "0": False}[value.lower()]

    def _normalize_coerce_date(self, value):
        y, m, d = value.split("-")
        return datetime.date(int(y), int(m), int(d))

    def _normalize_coerce_snake(self, value):
        out = ""
        for i, c in enumerate(value):
            if c.isupper() and i > 0:
                out += "_"
            out += c.lower()
        return out.replace("-", "_").replace(" ", "_")

    # default setters
    def _normalize_default_setter_slug(self, document):
        return document["title"].lower().replace(" ", "-")

    def _normalize_default_setter_owner(self, document):
        return document["author"] + "@example.com"

    def _normalize_default_setter_author(self, document):
        return document["owner"].split("@")[0]

    def _normalize_default_setter_count(self, document):
        return len(document["items"])

    # checks
    def _check_with_even(self, field, value):
        if isinstance(value, int) and value % 2:
            self._error(field, "must be an even number")

    def _check_with_luhn(self, field, value):
        if not isinstance(value, str):
            return
        digits = [int(c) for c in value if c.isdigit()]
        total = 0
        for i, d in enumerate(reversed(digits)):
            if i % 2:
                d *= 2
                if d > 9:
                    d -= 9
            total += d
        if total % 10:
            self._error(field, "card number fails the Luhn check")

    def _check_with_port(self, field, value):
        if isinstance(value, int) and value < 1024 and value not in (80, 443):
            self._error(field, "privileged port %d" % value)

    def _check_with_sorted(self, field, value):
        if isinstance(value, list) and value != sorted(value):
            self._error(field, "items are not sorted")


OPTIONS = ("allow_unknown", "require_all", "purge_unknown", "purge_readonly", "ignore_none_values")


def make(schema, opts):
    kw = {}
    for o in opts:
        if o in OPTIONS:
            kw[o] = True
        elif o.startswith("allow_unknown="):
            kw["allow_unknown"] = json.loads(o.split("=", 1)[1])
    return AppValidator(schema, **kw)


def err(e):
    return "%s: %s" % (type(e).__name__, e)


def docs_of(rel):
    return [line for line in read(rel).splitlines() if line.strip()]


def run(kind, args):
    schema_rel, docs_rel, opts = args[0], args[1], args[2:]
    try:
        v = make(load(schema_rel), opts)
    except SchemaError as e:
        emit("  " + err(e))
        return
    update = "update" in opts
    normalize = "no_normalize" not in opts
    for line in docs_of(docs_rel):
        emit("> " + line)
        doc = json.loads(line)
        if kind == "validate":
            ok = v.validate(doc, update=update, normalize=normalize)
            emit("  valid" if ok else "  invalid")
            if not ok:
                emit("  errors: %r" % (v.errors,))
            emit("  document: %r" % (v.document,))
        elif kind == "validated":
            emit("  result: %r" % (v.validated(doc, update=update, normalize=normalize),))
        else:
            emit("  result: %r" % (v.normalized(doc),))
            if v._errors:
                emit("  errors: %r" % (v.errors,))


def schemas_job(rel):
    for line in docs_of(rel):
        emit("> " + line)
        try:
            AppValidator(json.loads(line))
            emit("  ok")
        except SchemaError as e:
            emit("  " + err(e))


def main():
    for line in read("jobs.tsv").splitlines():
        job = line.split("\t")
        emit("== " + " ".join(job))
        k = job[0]
        if k == "schema_registry":
            schema_registry.add(job[1], load(job[2]))
        elif k == "rules_set_registry":
            rules_set_registry.add(job[1], load(job[2]))
        elif k == "schemas":
            schemas_job(job[1])
        else:
            run(k, job[1:])
    sys.stdout.write("\n".join(OUT) + "\n")


main()
