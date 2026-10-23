"""Run data/jobs.jsonl against the vendored rapidfuzz 3.14.6 and print what
mini_rapidfuzz must print.

RAPIDFUZZ_IMPLEMENTATION=python selects the library's pure-Python
implementation, the one the port follows; the compiled extension is not
vendored.

Run: python3 -I -B oracle.py > expected.out
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
os.environ["RAPIDFUZZ_IMPLEMENTATION"] = "python"
os.chdir(HERE)

import rapidfuzz  # noqa: E402
from rapidfuzz import distance, fuzz, process, utils  # noqa: E402

assert rapidfuzz.__version__ == "3.14.6"
assert fuzz.ratio.__module__ == "rapidfuzz.fuzz_py"
assert process.extract.__module__ == "rapidfuzz.process_py"

FUZZ = ["ratio", "partial_ratio", "token_sort_ratio", "token_set_ratio",
        "token_ratio", "partial_token_sort_ratio", "partial_token_set_ratio",
        "partial_token_ratio", "WRatio", "QRatio"]
FNS = ["distance", "similarity", "normalized_distance", "normalized_similarity"]


def kwargs(opts):
    kw = {}
    for k, v in opts.items():
        if k == "processor":
            kw[k] = utils.default_process if v == "default" else None
        elif k == "weights":
            kw[k] = tuple(v) if v is not None else None
        elif k == "scorer":
            mod, name = v.split(".")
            kw[k] = getattr(fuzz if mod == "fuzz" else getattr(distance, mod), name)
        elif k == "scorer_kwargs":
            kw[k] = kwargs(v)
        else:
            kw[k] = v
    return kw


def show(name, thunk):
    try:
        v = thunk()
    except Exception as e:
        print("  %s: error %s: %s" % (name, type(e).__name__, e))
        return
    print("  %s: %r" % (name, v))


def run_job(job):
    op = job[0]
    opts = job[-1] if isinstance(job[-1], dict) else {}
    kw = kwargs(opts)
    if op == "fuzz":
        names = FUZZ if job[1] == "all" else job[1]
        for n in names:
            show(n, lambda: getattr(fuzz, n)(job[2], job[3], **kw))
    elif op == "align":
        show("alignment", lambda: fuzz.partial_ratio_alignment(job[1], job[2], **kw))
    elif op == "process":
        show("default_process", lambda: utils.default_process(job[1]))
    elif op == "metric":
        mod = getattr(distance, job[1])
        for n in FNS:
            show(n, lambda: getattr(mod, n)(job[2], job[3], **kw))
    elif op == "ops":
        mod = getattr(distance, job[1])
        a, b = job[2], job[3]
        try:
            ops = mod.editops(a, b, **kw)
        except Exception as e:
            print("  editops: error %s: %s" % (type(e).__name__, e))
            return
        if "processor" in kw and kw["processor"] is not None:
            a, b = kw["processor"](a), kw["processor"](b)
        codes = mod.opcodes(job[2], job[3], **kw)
        print("  editops: %r" % ops)
        print("  opcodes: %r" % codes)
        print("  editops.apply: %r" % ops.apply(a, b))
        print("  opcodes.apply: %r" % codes.apply(a, b))
        print("  matching_blocks: %r" % ops.as_matching_blocks())
        print("  opcodes.matching_blocks: %r" % codes.as_matching_blocks())
        inv = ops.inverse()
        print("  inverse: %r" % inv)
        print("  inverse.apply: %r" % inv.apply(b, a))
        print("  as_editops: %r" % (codes.as_editops() == ops))
    elif op in ("extract", "extractOne", "extract_iter"):
        fn = getattr(process, op)
        if op == "extract_iter":
            show(op, lambda: list(fn(job[1], job[2], **kw)))
        else:
            show(op, lambda: fn(job[1], job[2], **kw))


def read_lines(path):
    with open(path, encoding="utf-8") as f:
        return [ln for ln in f.read().split("\n") if ln]


def dedupe(path):
    """Group vendor names that are the same company written differently."""
    heads = []
    members = []
    for name in read_lines(path):
        best = process.extractOne(name, heads, scorer=fuzz.WRatio,
                                  processor=utils.default_process, score_cutoff=88)
        if best is None:
            heads.append(name)
            members.append([(name, None)])
        else:
            members[best[2]].append((name, best[1]))
    for group in members:
        print("  %s" % group[0][0])
        for name, score in group[1:]:
            print("    = %s (%r)" % (name, score))
    print("  %d names, %d vendors" % (sum(len(g) for g in members), len(heads)))


def suggest(cmd_path, typo_path):
    """`git`-style "did you mean": edit distance first, then Jaro-Winkler."""
    commands = read_lines(cmd_path)
    for typo in read_lines(typo_path):
        near = process.extract(typo, commands, scorer=distance.Levenshtein.distance,
                               score_cutoff=2, limit=3)
        if near:
            print("  %s: did you mean %s?" % (typo, ", ".join(
                "%s (%d)" % (c, d) for c, d, _ in near)))
            continue
        jw = process.extractOne(typo, commands, scorer=distance.JaroWinkler.similarity,
                                score_cutoff=0.8)
        if jw is None:
            print("  %s: unknown command" % typo)
        else:
            print("  %s: maybe %s (%r)" % (typo, jw[0], jw[1]))


def reconcile(cat_path, ord_path):
    """Match free-text order lines to the catalog, as a store's import does."""
    catalog = {}
    for ln in read_lines(cat_path):
        sku, name = ln.split("\t")
        catalog[sku] = name
    matched = 0
    for ln in read_lines(ord_path):
        order, item = ln.split("\t")
        best = process.extract(item, catalog, scorer=fuzz.WRatio,
                               processor=utils.default_process, limit=2, score_cutoff=70)
        if not best:
            print("  %s %r: no match" % (order, item))
            continue
        matched += 1
        name, score, sku = best[0]
        print("  %s %r -> %s %s (%r)" % (order, item, sku, name, score))
        for name, score, sku in best[1:]:
            print("      also %s %s (%r)" % (sku, name, score))
    print("  %d of %d orders matched" % (matched, len(read_lines(ord_path))))


def main():
    with open(os.path.join("data", "jobs.jsonl"), encoding="utf-8") as f:
        lines = [ln for ln in f.read().split("\n") if ln]
    for line in lines:
        if line.startswith("#"):
            print(line)
            continue
        print("> " + line)
        if line.startswith("!"):
            parts = line[1:].split(" ")
            if parts[0] == "dedupe":
                dedupe(parts[1])
            elif parts[0] == "suggest":
                suggest(parts[1], parts[2])
            elif parts[0] == "reconcile":
                reconcile(parts[1], parts[2])
            continue
        run_job(json.loads(line))


main()
