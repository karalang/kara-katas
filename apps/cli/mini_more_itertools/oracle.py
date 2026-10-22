#!/usr/bin/env python3
"""Runs data/jobs.tsv through more-itertools and prints expected.out.

Each job prints "== " and its fields joined by " | ", then two spaces and
the Python repr of the result (a list for an iterator, the scalar for a
reduction, True/False for a predicate, or the raised error's message).
"""
import sys

sys.path.insert(0, "vendor")
import more_itertools as mi


def ints(s):
    if s == "" or s == "-":
        return []
    return [int(x) for x in s.split(",")]


def lists(s):
    return [ints(p) for p in s.split(";")]


def offsets(code):
    out = []
    i = 0
    while i < len(code):
        if code[i] == "m":
            out.append(-int(code[i + 1]))
            i += 2
        else:
            out.append(int(code[i]))
            i += 1
    return out


def rl_pairs(s):
    out = []
    i = 0
    while i < len(s):
        out.append((s[i], int(s[i + 1])))
        i += 2
    return out


def run(f):
    k = f[0]
    if k == "chunked":
        return repr(list(mi.chunked(ints(f[1]), int(f[2]), strict=f[3] == "1")))
    if k == "chunked_even":
        return repr(list(mi.chunked_even(ints(f[1]), int(f[2]))))
    if k == "distribute":
        return repr([list(c) for c in mi.distribute(int(f[1]), ints(f[2]))])
    if k == "divide":
        return repr([list(c) for c in mi.divide(int(f[1]), ints(f[2]))])
    if k == "sliced":
        return repr([list(c) for c in mi.sliced(ints(f[1]), int(f[2]))])
    if k == "split_at":
        return repr(
            list(
                mi.split_at(
                    ints(f[1]),
                    lambda x: x == 0,
                    maxsplit=int(f[2]),
                    keep_separator=f[3] == "1",
                )
            )
        )
    if k == "split_before":
        return repr(list(mi.split_before(ints(f[1]), lambda x: x == int(f[2]))))
    if k == "split_after":
        return repr(list(mi.split_after(ints(f[1]), lambda x: x == int(f[2]))))
    if k == "split_when":
        ms = 2 if f[2] == "gt2" else -1
        return repr(list(mi.split_when(ints(f[1]), lambda a, b: a > b, maxsplit=ms)))
    if k == "split_into":
        return repr(list(mi.split_into(ints(f[1]), ints(f[2]))))
    if k == "grouper":
        return repr(list(mi.grouper(ints(f[1]), int(f[2]), incomplete=f[3], fillvalue=0)))
    if k == "partition":
        a, b = mi.partition(lambda x: x % 2 == 0, ints(f[1]))
        return repr([list(a), list(b)])
    if k == "bucket":
        b = mi.bucket(ints(f[1]), key=lambda x: x % 3)
        return repr([(key, list(b[key])) for key in sorted(b)])
    if k == "windowed":
        return repr(list(mi.windowed(ints(f[1]), int(f[2]), fillvalue=0, step=int(f[3]))))
    if k == "substrings":
        return repr(list(mi.substrings(f[1])))
    if k == "substrings_indexes":
        return repr(list(mi.substrings_indexes(f[1])))
    if k == "stagger":
        return repr(list(mi.stagger(ints(f[1]), offsets=offsets(f[2]), longest=f[3] == "1", fillvalue=0)))
    if k == "windowed_complete":
        return repr(list(mi.windowed_complete(ints(f[1]), int(f[2]))))
    if k == "triplewise":
        return repr(list(mi.triplewise(ints(f[1]))))
    if k == "sliding_window":
        return repr(list(mi.sliding_window(ints(f[1]), int(f[2]))))
    if k == "subslices":
        return repr(list(mi.subslices(f[1])))
    if k == "count_cycle":
        return repr(list(mi.count_cycle(ints(f[1]), int(f[2]))))
    if k == "intersperse":
        return repr(list(mi.intersperse(int(f[1]), ints(f[2]), n=int(f[3]))))
    if k == "padded":
        return repr(list(mi.padded(ints(f[1]), int(f[2]), n=int(f[3]), next_multiple=f[4] == "1")))
    if k == "repeat_each":
        return repr(list(mi.repeat_each(ints(f[1]), int(f[2]))))
    if k == "repeat_last":
        return repr(list(mi.take(int(f[2]), mi.repeat_last(ints(f[1])))))
    if k == "ncycles":
        return repr(list(mi.ncycles(ints(f[1]), int(f[2]))))
    if k == "mark_ends":
        return repr(list(mi.mark_ends(ints(f[1]))))
    if k == "padnone":
        return repr(list(mi.take(int(f[2]), mi.padnone(ints(f[1])))))
    if k == "collapse":
        return repr(list(mi.collapse(eval(f[1]))))
    if k == "flatten":
        return repr(list(mi.flatten(lists(f[1]))))
    if k == "interleave":
        return repr(list(mi.interleave(*lists(f[1]))))
    if k == "interleave_longest":
        return repr(list(mi.interleave_longest(*lists(f[1]))))
    if k == "interleave_evenly":
        return repr(list(mi.interleave_evenly(lists(f[1]))))
    if k == "roundrobin":
        return repr(list(mi.roundrobin(*lists(f[1]))))
    if k == "zip_offset":
        return repr(list(mi.zip_offset(*lists(f[1]), offsets=ints(f[2]), longest=f[3] == "1", fillvalue=0)))
    if k == "dotproduct":
        return repr(mi.dotproduct(ints(f[1]), ints(f[2])))
    if k == "convolve":
        return repr(list(mi.convolve(ints(f[1]), ints(f[2]))))
    if k == "sort_together":
        return repr(mi.sort_together(lists(f[1]), key_list=(int(f[2]),)))
    if k == "transpose":
        return repr(list(mi.transpose(lists(f[1]))))
    if k == "unzip":
        return repr([list(x) for x in mi.unzip([tuple(p) for p in lists(f[1])])])
    if k == "reshape":
        return repr(list(mi.reshape([tuple(p) for p in lists(f[1])], int(f[2]))))
    if k == "ilen":
        return repr(mi.ilen(iter(ints(f[1]))))
    if k == "take":
        return repr(mi.take(int(f[1]), ints(f[2])))
    if k == "first":
        return repr(mi.first(ints(f[1]), int(f[2])))
    if k == "last":
        return repr(mi.last(ints(f[1]), int(f[2])))
    if k == "nth":
        return repr(mi.nth(ints(f[1]), int(f[2]), int(f[3])))
    if k == "nth_or_last":
        try:
            return repr(mi.nth_or_last(ints(f[1]), int(f[2])))
        except ValueError as e:
            return str(e)
    if k == "only":
        try:
            return repr(mi.only(ints(f[1]), int(f[2])))
        except ValueError as e:
            return str(e)
    if k == "one":
        try:
            return repr(mi.one(ints(f[1])))
        except ValueError as e:
            return str(e)
    if k == "all_equal":
        return repr(mi.all_equal(ints(f[1])))
    if k == "all_unique":
        return repr(mi.all_unique(ints(f[1])))
    if k == "first_true":
        return repr(mi.first_true(ints(f[1]), default=-1, pred=lambda x: x % 2 == 1))
    if k == "quantify":
        return repr(mi.quantify(ints(f[1]), pred=lambda x: x % 2 == 0))
    if k == "is_sorted":
        return repr(mi.is_sorted(ints(f[1]), strict=f[2] == "1"))
    if k == "minmax":
        return repr(mi.minmax(ints(f[1])))
    if k == "iequals":
        return repr(mi.iequals(*lists(f[1])))
    if k == "map_reduce":
        d = mi.map_reduce(ints(f[1]), keyfunc=lambda x: x % 3, reducefunc=sum)
        return repr(sorted(d.items()))
    if k == "exactly_n":
        return repr(mi.exactly_n(ints(f[1]), int(f[2]), lambda x: x != 0))
    if k == "run_length_encode":
        return repr(list(mi.run_length.encode(f[1])))
    if k == "run_length_decode":
        return repr(list(mi.run_length.decode(rl_pairs(f[1]))))
    if k == "consecutive_groups":
        return repr([list(g) for g in mi.consecutive_groups(ints(f[1]))])
    if k == "locate":
        return repr(list(mi.locate(ints(f[1]))))
    if k == "rlocate":
        return repr(list(mi.rlocate(ints(f[1]))))
    if k == "replace":
        cnt = None if f[4] == "-1" else int(f[4])
        return repr(list(mi.replace(ints(f[1]), lambda x: x == int(f[2]), ints(f[3]), count=cnt)))
    if k == "longest_common_prefix":
        return repr(list(mi.longest_common_prefix(f[1].split(";"))))
    if k == "argminmax":
        xs = ints(f[1])
        return repr((mi.argmin(xs), mi.argmax(xs)))
    if k == "running_max":
        return repr(list(mi.running_max(ints(f[1]))))
    if k == "running_min":
        return repr(list(mi.running_min(ints(f[1]))))
    if k == "unique_everseen":
        return repr(list(mi.unique_everseen(ints(f[1]))))
    if k == "unique_justseen":
        return repr(list(mi.unique_justseen(ints(f[1]))))
    if k == "unique_in_window":
        return repr(list(mi.unique_in_window(ints(f[1]), int(f[2]))))
    if k == "duplicates_everseen":
        return repr(list(mi.duplicates_everseen(ints(f[1]))))
    if k == "duplicates_justseen":
        return repr(list(mi.duplicates_justseen(ints(f[1]))))
    if k == "classify_unique":
        return repr(list(mi.classify_unique(f[1])))
    if k == "powerset":
        return repr(list(mi.powerset(ints(f[1]))))
    if k == "partitions":
        return repr([["".join(p) for p in part] for part in mi.partitions(f[1])])
    if k == "set_partitions":
        kk = None if f[2] == "-1" else int(f[2])
        return repr([["".join(p) for p in part] for part in mi.set_partitions(f[1], kk)])
    if k == "circular_shifts":
        return repr(list(mi.circular_shifts(ints(f[1]), int(f[2]))))
    if k == "distinct_permutations":
        r = None if f[2] == "-1" else int(f[2])
        return repr(list(mi.distinct_permutations(ints(f[1]), r)))
    if k == "distinct_combinations":
        return repr(list(mi.distinct_combinations(ints(f[1]), int(f[2]))))
    if k == "nth_product":
        return repr(mi.nth_product(int(f[1]), *lists(f[2])))
    if k == "nth_combination":
        return repr(mi.nth_combination(ints(f[1]), int(f[2]), int(f[3])))
    if k == "nth_permutation":
        return repr(mi.nth_permutation(ints(f[1]), int(f[2]), int(f[3])))
    if k == "gray_product":
        return repr(list(mi.gray_product(*lists(f[1]))))
    if k == "partial_product":
        return repr(list(mi.partial_product(*lists(f[1]))))
    if k == "sum_of_squares":
        return repr(mi.sum_of_squares(ints(f[1])))
    if k == "polynomial_eval":
        return repr(mi.polynomial_eval(ints(f[1]), int(f[2])))
    if k == "polynomial_from_roots":
        return repr(mi.polynomial_from_roots(ints(f[1])))
    if k == "polynomial_derivative":
        return repr(mi.polynomial_derivative(ints(f[1])))
    if k == "matmul":
        return repr(list(mi.matmul(lists(f[1]), lists(f[2]))))
    if k == "factor":
        return repr(list(mi.factor(int(f[1]))))
    if k == "is_prime":
        return repr(mi.is_prime(int(f[1])))
    if k == "sieve":
        return repr(list(mi.sieve(int(f[1]))))
    if k == "totient":
        return repr(mi.totient(int(f[1])))
    if k == "multinomial":
        return repr(mi.multinomial(*ints(f[1])))
    raise SystemExit("unknown job: " + k)


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().splitlines():
        f = line.split("\t")
        out.append("== " + " | ".join(f))
        out.append("  " + run(f))
sys.stdout.write("\n".join(out) + "\n")
