# Runs data/jobs.txt through the vendored pyspellchecker 0.8.1 (vendor/,
# the four Python files of the package without its language dictionaries)
# and prints what each command returns; that is expected.out. Run as:
# python3 -I -B oracle.py > expected.out, from this directory.
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
from spellchecker import SpellChecker  # noqa: E402
from spellchecker.info import __version__  # noqa: E402

assert __version__ == "0.8.1"


def fnv(s):
    h = 2166136261
    for b in s.encode("utf-8"):
        h = ((h ^ b) * 16777619) & 0xFFFFFFFF
    return f"{h:08x}"


def wset(s):
    if s is None:
        return "None"
    xs = sorted(s)
    return "{" + ", ".join(xs) + "}"


def opts(args):
    d = {}
    for a in args:
        k, _, v = a.partition("=")
        d[k] = v
    return d


def run(lines):
    checkers = {}
    name = None
    sc = None
    for line in lines:
        if line.startswith("#"):
            print(line)
            continue
        op, _, rest = line.partition(" ")
        args = rest.split()
        label = f"{name} {op}"
        if op == "new":
            o = opts(args[1:])
            name = args[0]
            sc = SpellChecker(language=None, distance=int(o["distance"]), case_sensitive=o["case"] == "1")
            checkers[name] = sc
            print(f"{name}: new checker, distance {sc.distance}, case-sensitive {o['case'] == '1'}")
        elif op == "open":
            name = args[0]
            sc = SpellChecker(language=None, local_dictionary=args[1])
            checkers[name] = sc
            wf = sc.word_frequency
            print(f"{name}: opened {args[1]}, {wf.unique_words} words")
        elif op == "use":
            name = args[0]
            sc = checkers[name]
            print(f"{name}: in use")
        elif op == "load_text_file":
            sc.word_frequency.load_text_file(args[0])
            print(f"{label}: {sc.word_frequency.total_words} words")
        elif op == "load_text":
            sc.word_frequency.load_text(rest)
            print(f"{label}: {sc.word_frequency.total_words} words")
        elif op == "load_words":
            sc.word_frequency.load_words(args)
            print(f"{label}: {sc.word_frequency.total_words} words")
        elif op == "add":
            sc.word_frequency.add(args[0], int(args[1]))
            print(f"{label} {args[0]}: {sc[args[0]]}")
        elif op == "pop":
            print(f"{label} {args[0]}: {sc.word_frequency.pop(args[0])}")
        elif op == "remove":
            sc.word_frequency.remove(args[0])
            print(f"{label} {args[0]}: {sc.word_frequency.unique_words} words")
        elif op == "remove_words":
            sc.word_frequency.remove_words(args)
            print(f"{label}: {sc.word_frequency.unique_words} words")
        elif op == "remove_threshold":
            sc.word_frequency.remove_by_threshold(int(args[0]))
            print(f"{label} {args[0]}: {sc.word_frequency.unique_words} words")
        elif op == "stats":
            wf = sc.word_frequency
            top = sorted(wf.items(), key=lambda kv: (-kv[1], kv[0]))[:6]
            tops = ", ".join(f"{k} {v}" for k, v in top)
            print(
                f"{label}: {wf.total_words} total, {wf.unique_words} unique, longest {wf.longest_word_length}, "
                f"letters [{''.join(sorted(wf.letters))}]; top {tops}"
            )
        elif op == "freq":
            print(f"{label} {args[0]}: {sc[args[0]]}")
        elif op == "contains":
            print(f"{label} {args[0]}: {args[0] in sc}")
        elif op == "split":
            toks = list(sc.split_words(rest))
            print(f"{label}: {len(toks)} [{'|'.join(toks)}]")
        elif op == "known":
            print(f"{label}: {wset(sc.known(args))}")
        elif op == "unknown":
            print(f"{label}: {wset(sc.unknown(args))}")
        elif op == "candidates":
            print(f"{label} {args[0]}: {wset(sc.candidates(args[0]))}")
        elif op == "correction":
            print(f"{label} {args[0]}: {sc.correction(args[0])}")
        elif op == "ed1":
            e = sorted(sc.edit_distance_1(args[0]))
            print(f"{label} {args[0]}: {len(e)} edits, first {' '.join(e[:6])}, last {' '.join(e[-3:])}; fnv {fnv(' '.join(e))}")
        elif op == "ed2":
            e = sc.edit_distance_2(args[0])
            k = sc.known(e)
            print(f"{label} {args[0]}: {len(e)} edits, {len(k)} known: {wset(k)}")
        elif op == "distance":
            sc.distance = int(args[0])
            print(f"{label} {args[0]}: {sc.distance}")
        elif op == "check":
            toks = list(sc.split_words(rest))
            bad = sorted(sc.unknown(toks))
            parts = []
            corr = {}
            for w in bad:
                c = sc.candidates(w)
                n = 0 if c is None else len(c)
                corr[w] = sc.correction(w)
                parts.append(f"{w} -> {corr[w]} ({n})")
            fixed = []
            for t in toks:
                fx = corr.get(t.lower())
                fixed.append(t if fx is None else fx)
            print(f"{label}: {len(toks)} words, {len(bad)} unknown: {'; '.join(parts)}; fnv {fnv(' '.join(fixed))}")
        elif op == "export":
            sc.export(args[0], gzipped=False)
            with open(args[0], encoding="utf-8") as f:
                data = f.read()
            print(f"{label} {args[0]}: {len(data)} bytes, starts [{data[:60]}]; fnv {fnv(data)}")
        else:
            raise SystemExit(f"unknown op {op}")


with open("data/jobs.txt", encoding="utf-8", newline="\n") as f:
    run(f.read().split("\n")[:-1])
for p in ("data/docs.json", "data/names.json"):
    if os.path.exists(p):
        os.remove(p)
