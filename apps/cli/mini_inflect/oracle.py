# Runs data/jobs.jsonl through inflect itself (the copy in inflect/,
# unchanged) and prints what mini_inflect prints. inflect imports two
# packages that are stood in for here: typeguard, whose @typechecked
# only checks argument types (every call in the jobs passes the right
# ones), and more_itertools, for its windowed_complete.
import csv
import json
import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
DATA = os.path.join(HERE, "data")

_tg = types.ModuleType("typeguard")
_tg.typechecked = lambda f: f
_mi = types.ModuleType("more_itertools")


def windowed_complete(iterable, n):
    seq = tuple(iterable)
    for i in range(len(seq) - n + 1):
        yield seq[:i], seq[i:i + n], seq[i + n:]


_mi.windowed_complete = windowed_complete
sys.modules["typeguard"] = _tg
sys.modules["more_itertools"] = _mi

import inflect  # noqa: E402

METHODS = [
    "plural", "plural_noun", "plural_verb", "plural_adj", "singular_noun", "compare",
    "compare_nouns", "compare_verbs", "compare_adjs", "a", "an", "no", "present_participle",
    "ordinal", "number_to_words", "join", "classical", "num", "gender", "defnoun", "defverb",
    "defadj", "defa", "defan", "inflect",
]


def failure(e):
    return f"! {type(e).__name__}: {e}"


def call_text(fn, args, kw):
    parts = [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kw.items()]
    return f"{fn}({', '.join(parts)})"


def op_call(p, op):
    fn, args, kw = op["fn"], op.get("args", []), op.get("kw", {})
    assert fn in METHODS
    try:
        r = getattr(p, fn)(*args, **kw)
    except Exception as e:
        print(f"{call_text(fn, args, kw)} {failure(e)}")
        return
    print(f"{call_text(fn, args, kw)} -> {r!r}")


def lines_of(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


# A repository digest: each repository's open items, counted the way a
# chat bot or a release note writes them. Counts under ten are words.
def op_digest(p, op):
    with open(os.path.join(DATA, op["file"]), encoding="utf-8") as f:
        repos = json.load(f)
    for repo in repos:
        parts = []
        for kind, n in repo["open"]:
            count = p.number_to_words(n) if n < 10 else str(n)
            if n == 0:
                parts.append(p.no(kind, 0))
            else:
                parts.append(f"{count} {p.plural(kind, n)}")
        verb = p.plural_verb("is", repo["owners"])
        owners = p.join(repo["maintainers"]) if repo["maintainers"] else "nobody"
        print(f"{repo['name']}: {p.join(parts)} open; {owners} {verb} on call")
        if repo.get("stale"):
            stale = repo["stale"]
            print(f"  {p.no('stale branch', stale)} {p.plural_verb('was', stale)} found; "
                  f"{p.a(repo['oldest'])} is the oldest")


# A cheque writer: the amount in words, the cents as a fraction.
def op_cheques(p, op):
    with open(os.path.join(DATA, op["file"]), encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    for payee, amount, currency, unit_one, unit_many in rows[1:]:
        whole, _, cents = amount.partition(".")
        cents = (cents + "00")[:2]
        words = p.number_to_words(whole, andword="", comma="")
        unit = unit_one if whole == "1" else unit_many
        line = f"{words} {unit} and {cents}/100"
        print(f"{payee:<24} {currency} {amount:>12}  {line[0].upper()}{line[1:]}")
        grouped = p.number_to_words(whole, group=3)
        print(f"{'':<24} {'':<3} {'':>12}  read back: {grouped}")


# A leaderboard: ranks as ordinals, numerals in the table and words in
# the announcement, ties sharing a rank.
def op_leaderboard(p, op):
    with open(os.path.join(DATA, op["file"]), encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    rows.sort(key=lambda r: -int(r["points"]))
    rank = 0
    last = None
    for i, r in enumerate(rows):
        pts = int(r["points"])
        if pts != last:
            rank = i + 1
            last = pts
        print(f"{p.ordinal(rank):>5} {r['player']:<12} {pts:>6} {p.plural('point', pts)}")
    winners = [r["player"] for r in rows if int(r["points"]) == int(rows[0]["points"])]
    print(f"{p.join(winners)} {p.plural_verb('takes', len(winners))} "
          f"{p.ordinal(p.number_to_words(1))} place; "
          f"the field had {p.number_to_words(len(rows))} {p.plural('player', len(rows))}, "
          f"the last in {p.ordinal(p.number_to_words(rank))} place")


def snake(name):
    out = []
    for i, c in enumerate(name):
        if c.isupper() and i > 0 and (not name[i - 1].isupper() or (i + 1 < len(name) and name[i + 1].islower())):
            out.append("_")
        out.append(c.lower())
    return "".join(out)


# ORM table names: a model class gives its table (the last word made
# plural) and its verbose names; a table name maps back to a model.
def op_tables(p, op):
    for line in lines_of(op["file"]):
        if not line or line.startswith("#"):
            continue
        kind, name = line.split(" ", 1)
        if kind == "model":
            words = snake(name).split("_")
            words[-1] = p.plural_noun(words[-1])
            verbose = " ".join(snake(name).split("_"))
            print(f"model {name}: table {'_'.join(words)}, verbose {verbose!r}, "
                  f"plural {p.plural_noun(verbose)!r}, {p.a(verbose)}")
        else:
            words = name.split("_")
            single = p.singular_noun(words[-1])
            if single is False:
                print(f"table {name}: already singular, model {''.join(w.capitalize() for w in words)}")
            else:
                words[-1] = single
                print(f"table {name}: model {''.join(w.capitalize() for w in words)}")


# A stock report: each line is a count and an item, as a warehouse
# export writes them.
def op_inventory(p, op):
    total = 0
    for line in lines_of(op["file"]):
        if not line:
            continue
        qty, item = line.split(" ", 1)
        n = int(qty)
        total += n
        if n == 1:
            print(f"  {p.a(item)} in stock")
        else:
            print(f"  {p.no(item, n)} in stock")
    print(f"  {p.number_to_words(total)} {p.plural('item', total)} in all")


# Notification templates written with inflect's own call syntax; the
# count for each message is set with num() and not shown.
def op_notify(p, op):
    for line in lines_of(op["file"]):
        if not line:
            continue
        count, template = line.split("\t", 1)
        p.num(int(count), show=False)
        try:
            print(p.inflect(template))
        except Exception as e:
            print(failure(e))
        p.num()


# A dry-run plan: what a deploy tool is about to do, as present
# participles.
def op_dryrun(p, op):
    for line in lines_of(op["file"]):
        if not line:
            continue
        verb, n, thing = line.split(" ", 2)
        n = int(n)
        print(f"{p.present_participle(verb).capitalize()} {p.no(thing, n)}")


PROGRAMS = {
    "digest": op_digest, "cheques": op_cheques, "leaderboard": op_leaderboard,
    "tables": op_tables, "inventory": op_inventory, "notify": op_notify, "dryrun": op_dryrun,
}


def main():
    for line in lines_of("jobs.jsonl"):
        if not line:
            continue
        job = json.loads(line)
        print(f"== {job['name']}")
        p = inflect.engine()
        for op in job["ops"]:
            if op["op"] == "call":
                op_call(p, op)
            else:
                PROGRAMS[op["op"]](p, op)


main()
