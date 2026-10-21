# 817. Linked List Components

Given the head of a linked list of distinct values and an array `nums`
holding some of those values, return the number of connected components
in `nums`: two values are connected when they sit next to each other in
the list.

```
head = [0, 1, 2, 3], nums = [0, 1, 3]         ->  2     [0, 1] and [3]
head = [0, 1, 2, 3, 4], nums = [0, 3, 1, 4]   ->  2     [0, 1] and [3, 4]
```

**Constraints:** the list has `n` nodes, `1 <= n <= 10^4`, its values
are distinct and `0 <= Node.val < n`; `1 <= nums.length <= n`, and the
values of `nums` are distinct and in the list.

## Approaches

A component is a run of adjacent nodes whose values are all in `nums`,
so counting components is counting runs, by their first or last node.

| file | mechanism |
|---|---|
| `linked_list_components.kara` ★ | put `nums` in a set and count the nodes in it whose next node is missing or not in it, the last node of each run. O(n + m) |
| `linked_list_components_starts.kara` | count the first node of each run instead, carrying along whether the node before was in the set. O(n + m) |
| `linked_list_components_marks.kara` | the values are 0 to n - 1, so a table of n flags indexed by value stands in for the set, after one walk to find n; then the ★ arm's count. O(n + m) with no hashing |
| `linked_list_components_iter.kara` | read the values into a vector, map each to whether it is in the set, and count with a `filter` over the positions where a run of marks ends |
| `differential.kara` | the four arms against a search of the graph of neighbours in `nums`, four properties |

Every arm prints the same 10 lines: LeetCode's two examples; one node; a
run across the head; a list with its values out of order; three single
nodes; every node in `nums`; LeetCode's largest, 10,000 nodes in a
random order, with `nums` a random half of them and every other node
from the head; and 300 random rounds of 1 to 30 nodes, with a total and
a checksum. `linked_list_components.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms, sharing the ★ arm's
`ListNode`, and the statement itself: link two values of `nums` when
they sit next to each other in the list, and count the groups of linked
values by search. Its 1,600 cases have 1 to 30 nodes in a random order
and come in four kinds of 400: each value in `nums` one time in two; one
time in five; four times in five; and every value, or a single one. The
most components any case has is 10.

| | property |
|---|---|
| P1 | the statement's count |
| P2 | the same for the list reversed |
| P3 | with the count for the values not in `nums`, one run more than the places where the list crosses between the two |
| P4 | the same with every value renamed, in the list and in `nums` |

It prints `1600 cases (at most 10 components), 25600 checks over 4 arms:
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the tail never ends a component | P1 848, P2 845, P3 1600, P4 848 |
| M2 | ★: every node in nums counted as an end | P1 1052, P2 1052, P3 1485, P4 1052 |
| M3 | ★: the ends of the runs outside nums counted | P1 1503, P2 1487, P3 1493, P4 1503 |
| M4 | starts: the last node's mark never carried | P1 1052, P2 1052, P3 1485, P4 1052 |
| M5 | starts: the walk starts as if inside a component | P1 845, P2 848, P3 1600, P4 845 |
| M6 | starts: a component counted where a run ends, not where it starts | P1 848, P2 845, P3 1600, P4 848 |
| M7 | marks: the tail never ends a component | P1 848, P2 845, P3 1600, P4 848 |
| M8 | marks: the first number never marked | P1 1125, P2 1125, P3 1181, P4 1125 |
| M9 | marks: an end counted where the next node is marked | P1 1385, P2 1398, P3 1435, P4 1385 |
| M10 | iter: the last position never an end | P1 848, P2 845, P3 1600, P4 848 |
| M11 | iter: a run that ends at the head never counted | P1 303, P2 297, P3 559, P4 303 |
| M12 | iter: the marks inverted | P1 1103, P2 1103, P3 310, P4 1103 |

Every property kills every edit. M1, M6, M7 and M10 all lose the run at
the tail, so they fail on the same cases, and M5 loses the run at the
head, the same cases with the list reversed, so its P1 and P2 counts
swap. P3 sees each of these on all 1,600 cases: the tail ends a run
either of `nums` or of the values outside it, so one of the two counts
always comes up short. M12 counts the runs outside `nums`, which P3
cannot tell apart from the right answer except where every value is in
`nums` and there is no run outside to count. M2 and M4 count every node
in `nums`, and fail wherever a component holds two nodes or more.

## Verification

Every arm prints the same output as `linked_list_components.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` is at kara
`d0ad6409f5`, whose last compiler change is `c120cafada`; the release
build that runs `check` and `__mir-run` is at `f6f2efb14`, one parser
change behind it. The runtime archives were built after the last runtime
change in that tree, `45d6c491fc`.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`), the legacy JIT
(`karac run`) and `karac build` refuse every arm, the differential and
the bench program: legacy types the item of `nums.iter()` over a
`Vec[i64]` as an `i64` rather than a reference and so refuses its `*`.
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 lists of
10,000 nodes, LeetCode's largest, hold the values 0 to 9,999 in a random
order, each with `nums` a random set of 1 to 9,999 of them, all drawn
once. Each of 8,000 rounds swaps one number of the next list's `nums`
for a value outside it and counts the components, so a round builds a
set of up to 10,000 numbers and walks 10,000 nodes. C has no hash set,
so its mirror carries an open-addressing table with a short integer mix
for a hash; Kāra's `Set` and Rust's `HashSet` hash with SipHash-1-3, and
Go uses its built-in map. Rust's list is `Option<Box<ListNode>>`,
LeetCode's Rust signature. Every implementation prints `8000 rounds of
10000 nodes: total 12909396, checksum 910808805`, the Kāra program under
`karac __mir-run` included, in 205 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.45 to 1.57 s |
| Rust (`rustc -O`) | 2.12 to 2.23 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.08 to 2.41 s |
| Go | 2.47 to 2.59 s |
| Python | 6.54 to 6.87 s |
| Kāra (`karac build --mir`) | 3.21 to 3.36 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 26.4 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 3.27 s,
against C's 1.50, Rust's 2.17 (2.17 under overflow checks) and Go's
2.49. Under valgrind's cachegrind v2 runs 31.9 billion instructions and
10.0 billion data references, Rust 20.2 billion and 2.0 billion, and C
3.8 billion. Most of v2's time is the set: `karac_hash_word`, the
SipHash of one number, is 44% of its instructions, and
`karac_mir_map_find_hv`, the lookup, another 25%, with 1.7 billion
writes of its own, nearly half of all v2's data writes, in what is a
read of the table. `karac.main`, which holds the walk, is 11%. Built for
`x86-64-v3`, the target `karac build` uses, C (`clang -O3
-march=x86-64-v3`) takes 1.51 to 1.57 s and Rust with overflow checks
(`-C target-cpu=x86-64-v3`) 2.11 to 2.20 s, against v2's 3.22 to 3.38 s
in the same five interleaved runs. Legacy refuses the bench program (see
Verification), so there is no legacy timing to set v2 against. The
comparison with C and Rust waits until after M4.

## Compiler findings

Nothing new in v2: every arm, the differential and the bench passed
`karac check` and every v2 lane as first written. The writes inside the
set's lookup, measured above, are a lead for the v2 runtime's map, not
filed, as the comparison with C and Rust waits until after M4. The
runtime archives measured predate kara `7fad5e51e7`, which changes that
map to remember its last index and slot, so a later archive may differ.
