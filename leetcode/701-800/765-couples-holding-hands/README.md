# 765. Couples Holding Hands

`row` seats people numbered 0 to 2n - 1 in 2n seats, and seats 2i and 2i
+ 1 form a couch. The couples are (0, 1), (2, 3), and so on. A swap
makes any two people change seats. Return the fewest swaps after which
every couple shares a couch.

```
[0, 2, 1, 3]  ->  1
[3, 2, 0, 1]  ->  0
```

**Constraints:** `row.length` is even, from 4 to 60; `row` holds each of
0 to `row.length` - 1 once.

## Approaches

Treat each couple as a node and each couch as an edge joining the two
couples on it. Every couple has two members, so every node has two edges
and the graph splits into cycles; a cycle of k couches takes exactly k -
1 swaps, so the answer is the number of couches less the number of
cycles. The arms count that in four ways.

| file | mechanism |
|---|---|
| `couples_holding_hands.kara` ★ | greedy: on each couch in turn, swap the first person's partner into the second seat, with a table of where everyone sits; each swap seats one couple for good; O(n) |
| `couples_holding_hands_unionfind.kara` | union-find over the couples, joining the two on each couch; the answer is the couples less the groups |
| `couples_holding_hands_graph.kara` | the couch graph built as adjacency lists and its cycles counted by a recursive depth-first search |
| `couples_holding_hands_chains.kara` | no graph built: from each couch not yet seen, walk from neighbour to partner to neighbour until the walk returns, and charge each cycle its length less one |
| `differential.kara` | the four arms against the definition, four properties |

The ★ arm takes `row` as `own Vec[i64]`, since its swaps rearrange it;
the others borrow it. Every arm prints the same 8 lines: the two
LeetCode examples; a couple already seated, each way round; three
couples needing two swaps; four with one couple seated and three in a
cycle; five in one cycle; then 300 random rows of up to 60 seats, with
their swaps' total and a checksum. `couples_holding_hands.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which searches ever deeper, over swaps of any two people at all, for the
fewest that seat every couple. 1,500 random rows of up to 8 seats are
checked against it, and 300 of up to 60 against the other properties.

| | property |
|---|---|
| P1 | the answer is the definition's (the 1,500 short rows) |
| P2 | renumbering the couples, and exchanging the numbers of some couples' two members, changes nothing |
| P3 | the row read backwards has the same answer |
| P4 | one swap of two random seats changes the answer by at most 1 |

It prints `1800 rows (5715 swaps), 4 arms, 27600 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error; the total is the ★ arm's.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every couch swapped, seated or not | P1 1500 |
| M2 | ★: the moved person's seat never updated | P1 165, P3 198, P4 105 |
| M3 | ★: the moved person never put in the partner's old seat | P1 998, P4 198 |
| M4 | union-find: a union counted but never made | P1 998, P4 198 |
| M5 | union-find: find stopping one step up | P1 165, P3 198, P4 105 |
| M6 | union-find: every couple started in one group | P1 998 |
| M7 | graph: each link made one way only | P1 62 |
| M8 | graph: seats grouped into couches by seat mod n | P1 676 |
| M9 | graph: no search started from the first couch | P1 596, P3 199 |
| M10 | chains: each cycle charged half its length | P1 484 |
| M11 | chains: a walk following the same person's partner | P1 88, P3 214 |
| M12 | chains: only the starting couch marked done | P1 998, P4 690 |
| E1 | ★: the partner's new seat never recorded | 0 |
| E2 | ★: the last couch never checked | 0 |
| E3 | union-find: the second occupant's couple found through their partner | 0 |

P1 kills all twelve, and P2 none: every arm treats all couples and both
members alike, so renumbering them cannot change what any edit does.
M1, M6, M7, M8 and M10 are seen by P1 alone; M1 and M6, for two, answer
the number of couches and 0 whatever the row, which reversing it or one
more swap cannot expose. P3 sees the edits whose error depends on where
in the row a walk or a group starts, M2, M5, M9 and M11, and P4 those
whose answer can jump by two or more after one swap. Two first choices
survived and were replaced, rightly: skipping the first couch in the ★
arm, since the greedy count does not depend on the order of the couches
and the first couch is seated once the rest are; and stopping a chain
only at its starting seat, since a walk always returns to its first
couch on the seat it set out from. E1 never records the partner's new
seat, but no one looks it up again, since the one person who would is
already beside them; E2 never checks the last couch, which holds the one
couple left once every other couch is fixed; E3 finds the second
occupant's couple through their partner, who belongs to it too.

## Verification

Every arm prints the same output as `couples_holding_hands.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`8a2af7d554`, whose last compiler change is `60d9973e03`. The runtime
archives were built after the last runtime change, `176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept the ★, union-find and chain arms and
the bench: each arm prints the same output under the legacy interpreter,
`karac run`, `karac build` and an auto-par build. They refuse the graph
arm and the differential at a `*` over an element of `iter()`
(`seen[*next]`), which legacy gives by value where v2 gives references.
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages, on
1,000,000 random rows of 60 seats, the most LeetCode allows, shuffling a
fresh row for each, adding up the swaps and a checksum. Every
implementation prints `1000000 rows of 60 seats: 27315702 swaps in all,
checksum 182483749`, the Kāra program under `karac __mir-run` included
(in 107 s). C keeps the row in a fixed array, where the others allocate
one for each row.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.41 to 0.52 s |
| Rust (`rustc -O`) | 0.48 to 0.61 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.42 to 0.52 s |
| Go | 0.83 to 0.91 s |
| Python | 20.4 to 21.8 s |
| Kāra (`karac build --mir`) | 0.59 to 0.66 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
3.6 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 0.63 s,
against C's 0.44, Rust's 0.50 (0.49 under overflow checks) and Go's
0.87. Under valgrind's cachegrind v2 runs 6.4 billion instructions, Rust
3.2 billion and C 1.9 billion. The legacy build of the same program ran
0.48 to 0.55 s, a median of 0.51 s in the interleaved runs, so v2 takes
1.2 times as long as legacy, inside M2's limit of twice legacy; new
katas' benches are outside M2's frozen set in any case. The comparison
with C and Rust waits until after M4.

## Compiler findings

None new.
