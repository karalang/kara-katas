# Runs data/jobs.tsv through inflection 0.5.1 (the files in inflection/,
# unchanged) and prints what each operation returns. Run mk.py first.
import importlib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inflection  # noqa: E402


def unesc(s):
    out, i = [], 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            out.append({"t": "\t", "n": "\n", "\\": "\\"}[s[i + 1]])
            i += 2
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def number(a):
    kind, text = a[0], a[2:]
    if kind == "i":
        return int(text)
    if kind == "f":
        return float(text)
    if kind == "b":
        return text == "True"
    return text


def err(e):
    if isinstance(e, re.error):
        return f"re.error: {e}"
    return f"{type(e).__name__}: {e}"


def scaffold(spec):
    name, *fields = spec.split()
    table = inflection.tableize(name)
    out = [
        f"model {name}",
        f"table {table}",
        f"singular {inflection.underscore(name)}",
        f"route /{inflection.dasherize(table)}",
        f"controller {inflection.camelize(table)}Controller",
        f"human {inflection.humanize(inflection.underscore(name))}",
        f"heading {inflection.titleize(inflection.pluralize(name))}",
    ]
    for f in fields:
        col, typ = f.split(":")
        line = f"column {col} {typ} label={inflection.humanize(col)!r} header={inflection.titleize(col)!r}"
        if col.endswith("_ids"):
            assoc = inflection.pluralize(col[:-4])
            line += f" has_many={assoc} class={inflection.camelize(inflection.singularize(assoc))}"
        elif col.endswith("_id"):
            assoc = col[:-3]
            line += f" belongs_to={assoc} class={inflection.camelize(assoc)} inverse={inflection.tableize(name)}"
        out.append(line)
    return out


def run(f):
    op, args = f[0], f[1:]
    if op == "reset":
        print("-- reset")
        importlib.reload(inflection)
        return
    print("-- " + op + "".join(" " + repr(a) for a in args))
    try:
        if op == "pluralize":
            r = inflection.pluralize(args[0])
        elif op == "singularize":
            r = inflection.singularize(args[0])
        elif op == "roundtrip":
            r = (inflection.singularize(inflection.pluralize(args[0])),
                 inflection.pluralize(inflection.singularize(args[0])))
        elif op == "camelize":
            if len(args) == 1:
                r = inflection.camelize(args[0])
            elif args[1] == "lower":
                r = inflection.camelize(args[0], False)
            else:
                r = inflection.camelize(inflection.underscore(args[0]))
        elif op == "underscore":
            r = inflection.underscore(args[0])
        elif op == "dasherize":
            r = inflection.dasherize(args[0])
        elif op == "tableize":
            r = inflection.tableize(args[0])
        elif op == "humanize":
            r = inflection.humanize(args[0])
        elif op == "titleize":
            r = inflection.titleize(args[0])
        elif op == "capitalize":
            r = args[0].capitalize()
        elif op == "transliterate":
            r = inflection.transliterate(args[0])
        elif op == "parameterize":
            r = inflection.parameterize(*args)
        elif op == "ordinal":
            r = inflection.ordinal(number(args[0]))
        elif op == "ordinalize":
            r = inflection.ordinalize(number(args[0]))
        elif op == "irregular":
            inflection._irregular(args[0], args[1])
            r = None
        elif op == "uncountable":
            inflection.UNCOUNTABLES.add(args[0])
            r = None
        elif op == "plural":
            inflection.PLURALS.insert(0, (args[0], args[1]))
            r = None
        elif op == "singular":
            inflection.SINGULARS.insert(0, (args[0], args[1]))
            r = None
        elif op == "scaffold":
            for line in scaffold(args[0]):
                print("   " + line)
            return
        else:
            raise SystemExit("unknown op " + op)
    except (re.error, IndexError, ValueError) as e:
        print("   error: " + err(e))
        return
    print("   ok" if r is None else f"   {r!r}")


with open("data/jobs.tsv", encoding="utf-8") as fh:
    for line in fh:
        line = line.rstrip("\n")
        if line.startswith("== "):
            print(line)
            continue
        run([unesc(x) for x in line.split("\t")])
