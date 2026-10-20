# 811. Subdomain Visit Count

A website domain such as `discuss.leetcode.com` has parts separated by
dots. A visit to it is also a visit to each domain it ends in, here
`leetcode.com` and `com`. A count-paired domain is a count, a space and
a domain: `9001 discuss.leetcode.com` says the domain was visited 9001
times. Given a list of count-paired domains, return the count-paired
domains of every domain they visit, each with its total, in any order.

```
["9001 discuss.leetcode.com"]
  ->  ["9001 leetcode.com", "9001 discuss.leetcode.com", "9001 com"]
["900 google.mail.com", "50 yahoo.com", "1 intel.mail.com", "5 wiki.org"]
  ->  ["901 mail.com", "50 yahoo.com", "900 google.mail.com", "5 wiki.org",
       "5 org", "1 intel.mail.com", "951 com"]
```

**Constraints:** `1 <= cpdomains.length <= 100` and `1 <=
cpdomains[i].length <= 100`. Each entry is `count d1.d2.d3` or `count
d1.d2`, with a count from 1 to 10^4 and parts of lowercase letters.

## Approaches

Every entry adds its count to its whole domain and to each domain after
one of its dots. The four arms differ in how they find those domains and
where they keep the totals.

| file | mechanism |
|---|---|
| `subdomain_visits.kara` ★ | a `Map` from domain to total: count the whole domain, cut it after its first dot, count again, until no dot is left. O(L) for L the entries' length |
| `subdomain_visits_sorted.kara` | the parts split out and the domains built from the right, `c`, `b.c`, `a.b.c`, into a `SortedMap`. O(L log D) for D the distinct domains |
| `subdomain_visits_merge.kara` | no map: every (domain, count) pair listed, the pairs sorted by domain, each run of one domain added up. O(P log P) for P the pairs |
| `subdomain_visits_iter.kara` | one chain: `flat_map` each entry to its pairs, `fold` them into a `Map`, `map` the totals to lines |
| `differential.kara` | the four arms against the counts taken straight from the statement, four properties |

The answer may come in any order, and the ★ and iterator arms return it
in the `Map`'s order, which is random per process. The harness sorts
each answer before printing it, so every arm prints the same 8 lines:
LeetCode's two examples; `[1 a.b.c, 2 b.c, 3 d.c]`, where `b.c` is both
an entry and a subdomain of another; one entry twice; two domains under
one top part; `a.com` and `com.a`, the same parts in the other order;
LeetCode's largest, 100 entries with counts up to 10000, as a count of
domains and a checksum; and 300 random rounds of 1 to 10 entries.
`subdomain_visits.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement
itself: a domain's visits are the counts of every entry whose domain is
that domain or ends in a dot and that domain, and the domains are each
entry's domain and every part of it after a dot. Its 1,600 cases have 1
to 8 entries of 2 or 3 parts and come in four kinds of 400: parts from 3
names, so that domains repeat and share their ends; parts from 8 names,
so that most domains are distinct; one domain repeated, so that counts
add up; and parts `b` and `ab` only, names that end in one another, so
that a test on characters rather than on parts would miscount.

| | property |
|---|---|
| P1 | every line is a positive count, a space and a domain |
| P2 | the domains are exactly the ones the statement names, each once |
| P3 | each count is the statement's count for its domain |
| P4 | the counts add up to each entry's count times its number of parts |

It prints `1600 cases (11260 lines), 25600 checks over 4 arms: 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one character too many cut after each dot | P1 1491, P2 1600, P3 1600 |
| M2 | ★: a count set, not added | P3 1208, P4 1208 |
| M3 | ★: the space kept in the domain | P2 1600, P3 1600 |
| M4 | sorted: the whole domain left out | P2 1600, P3 422, P4 1600 |
| M5 | sorted: each entry counted once, not by its count | P3 1600, P4 1600 |
| M6 | sorted: parts joined the wrong way round | P2 1459, P3 1514 |
| M7 | merge: the whole domain left out | P2 1600, P3 422, P4 1600 |
| M8 | merge: runs split on count, not domain | P2 1550, P3 1560 |
| M9 | merge: the pairs not sorted | P2 1208, P3 1208 |
| M10 | iter: parts joined without dots | P2 1600, P3 1600 |
| M11 | iter: the whole domain left out | P2 1600, P3 422, P4 1600 |
| M12 | iter: a count set, not added | P3 1208, P4 1208 |

P3 kills all twelve, and P2 all but the three that only change counts
(M2, M5, M12). P4 sees an edit only when counts are lost or changed: an
edit that renames a domain (M1, M3, M6, M10) or splits it over two lines
(M8, M9) keeps the sum. P1 sees only M1, whose cut can run past the end
of a part and leave an empty domain. M2, M9 and M12 fail the same 1,208
cases, the ones where some domain is counted twice: setting a count
keeps only its last addition, and an unsorted list splits its runs. The
three edits that leave the whole domain out fail P2 in all 1,600 cases
but P3 in only 422: the lines that remain are counted right unless one
entry's domain is also the end of another's, as `b.c` is of `a.b.c`, and
then that line misses its own entry.

## Verification

Every arm prints the same output as `subdomain_visits.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` is at kara
`d0ad6409f5`, whose last compiler change is `c120cafada`; the release
build that runs `check` and `__mir-run` is at `f6f2efb14`, one parser
change behind it. The runtime archives were built after the last runtime
change, `45d6c491fc`.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`) prints the same
output for the ★ and sort-and-merge arms, and the legacy JIT (`karac
run`) and `karac build` panic in codegen on both
(`src/codegen/method_call.rs:3350`). Legacy refuses the rest: the
sorted-map arm and the differential for `split(" ").collect()`, which it
wants written with an `.iter()` in between; the iterator arm for
`split_once`, which its `String` lacks; the differential under its
interpreter for `ref e.1`, a borrow of a tuple field; and the bench
program, reading `subdomain_visits(lists[k])` as moving a `Vec` out of
an index (`E_INDEX_MOVE_NON_COPY`). Legacy is frozen, so all of this is
noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages: a hash map from
domain to total (Rust's `HashMap` and Kāra's `Map` both SipHash under a
random key, Go's map and Python's dict, and in C an open-addressing
table with FNV-1a). 64 lists of 100 entries of 2 or 3 parts are made
once. Each of 100,000 rounds writes a new count into one entry of the
next list and counts that list's visits, and the answer's lines, in
whatever order they come, are folded into a sum. Every implementation
prints `100000 rounds of 100 entries: 7570322 lines, checksum
948227224`, the Kāra program under `karac __mir-run` included, in 167 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.94 to 2.26 s |
| Rust (`rustc -O`) | 3.02 to 3.26 s |
| Rust (`rustc -O -C overflow-checks=on`) | 3.00 to 3.50 s |
| Go | 3.70 to 4.50 s |
| Python | 11.18 to 11.88 s |
| Kāra (`karac build --mir`) | 4.14 to 4.60 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 34.8 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 4.34 s,
against C's 2.04, Rust's 3.03 (3.10 under overflow checks) and Go's
3.98. Under valgrind's cachegrind v2 runs 44.1 billion instructions,
Rust 28.6 billion and C 19.8 billion. A callgrind profile of 10,000
rounds puts 26% of v2's instructions under `karac_mir_str_find`, the
`find(" ")` and `find(".")` that cut each entry: with a string pattern
the runtime runs a substring search, where the Rust mirror finds a
`char` and C calls `strchr`. Kāra's `find` takes a `char` too, and the
bench written with `find(' ')` and `find('.')` prints the same line in
3.81 billion instructions at 10,000 rounds rather than 4.40 billion,
against Rust's 2.87 billion and C's 1.99 billion; `find` is then 15% of
v2's instructions, formatting the answer's lines 19% and hashing the
keys 14%. The arms keep the string patterns, the spelling the Python
mirror shares, and the bench keeps the ★ arm as it is. Built for
`x86-64-v3`, the target `karac build` uses, C (`clang -O3
-march=x86-64-v3`) takes 1.93 to 2.23 s and Rust (`rustc -O -C
overflow-checks=on -C target-cpu=x86-64-v3`) 3.08 to 3.28 s, so the
instruction set does not explain the gap here. Legacy refuses the bench
program (see Verification), so there is no legacy timing to set v2
against. The comparison with C and Rust waits until after M4.

## Compiler findings

The iterator arm was first written with a `flat_map` closure that
returns the entry's pairs as a `Vec`. `flat_map` takes a closure that
returns an iterator (`U: Iterator`, docs/library/iterators.md), so the
arm calls `.into_iter()` on the `Vec`, as the spec asks. But `karac
check` says so poorly: five errors for the one missing call, the first
listing all 29 `Iterator` implementors and suggesting nothing. That is
filed as B-2026-10-20-33. Probing `IntoIterator` from there found that
the trait is not the spec's: the prelude's has an `IntoIter` type and no
`into_iter` method, so an impl written as design.md gives it is refused,
a `C: IntoIterator` bound cannot call `.into_iter()`, and `v.extend(x)`
on a type of one's own passes `karac check` and is then refused by the
MIR builder. That is B-2026-10-20-32. Neither needed a change to the
kata: `Vec.into_iter()` is a method of `Vec` itself.

Every arm, the differential and the bench otherwise passed `karac check`
and every v2 lane as first written.
