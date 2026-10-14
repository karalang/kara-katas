# 594. Longest Harmonious Subsequence

We define a harmonious array as an array where the difference between
its maximum value and its minimum value is exactly `1`. Given an integer
array `nums`, return the length of its longest harmonious subsequence
among all its possible subsequences.

```
nums = [1,3,2,2,5,2,3,7]  ->  5    ([3,2,2,2,3])
nums = [1,2,3,4]          ->  2
nums = [1,1,1,1]          ->  0
```

**Constraints:** `1 <= nums.length <= 2 * 10^4`; `-10^9 <= nums[i] <=
10^9`.

## Approaches

Every arm is `fn find_lhs(nums: Vec[i64]) -> i64`. The parameter is
bare, so the array is borrowed; the sorted arm sorts a copy. A
subsequence keeps its order, but its minimum and maximum do not depend
on order, so the longest harmonious one is every copy of two values a
step apart.

| file | mechanism |
|---|---|
| `find_lhs.kara` ★ | count each value in a `Map[i64, i64]`, then for every value v with v + 1 also counted take count[v] + count[v + 1]; O(n) expected |
| `find_lhs_sorted.kara` | sort a copy, so equal values stand in runs, and pair each run with the run before it when their values are a step apart; O(n log n) |
| `find_lhs_onepass.kara` | one pass: count each value as it arrives and take the pairs it belongs to, (x - 1, x) and (x, x + 1), as candidates; the last time a pair is looked at its counts are final; O(n) expected |
| `find_lhs_ordered.kara` | count in a `SortedMap[i64, i64]` and pair neighbouring keys in its ordered walk when they are a step apart; O(n log n) |
| `differential.kara` | the four arms against the definition, five properties |

The ★ arm walks its `Map`, whose order is random from run to run, but it
takes only a maximum from the walk, so its output does not depend on the
order. Every arm prints the same 13 lines: the three examples above,
seven cases at the edges (one value; two values a step apart; two values
two apart; values at both ends of the constraints; negative values; a
pair that is not the most common values; a later pair beating an earlier
one), two arrays of 20,000 values, the problem's longest (values from
0 to 49, and distinct values two apart), and a total and checksum over
300 random arrays. `find_lhs.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which is the problem's sentence: every subsequence, one for each set of
positions, whose maximum and minimum differ by exactly 1, and the
longest of them, or 0. Each of 1,000 random arrays has 1 to 10 values
from a range of 1 to 5 starting at -3 to 3, so that most hold a pair a
step apart; 613 have an answer above 0.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the array reversed, or turned round to start at a random place, gives the same answer |
| P3 | every value moved by the same amount, up to 10^9 either way, gives the same answer |
| P4 | every value negated gives the same answer |
| P5 | the array twice over gives twice the answer |

It prints `1000 cases (613 with an answer above 0), 4 arms,
20000 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each value paired with itself | P1 840 |
| M2 | ★: only the larger of the two counts | P1 613 |
| M3 | sorted: the first run paired with an empty run of 0s before it | P1 49, P3 49, P4 95 |
| M4 | sorted: the copy not sorted | P1 542, P2 479, P4 415, P5 515 |
| M5 | onepass: only the value above looked at | P1 254, P2 467, P4 537, P5 231 |
| M6 | onepass: the latest candidate kept, not the best | P1 80, P2 173, P4 116, P5 6 |
| M7 | ordered: any two neighbouring keys paired | P1 94 |
| M8 | ordered: every key compared with the first | P1 176, P4 301 |
| E1 | ★: each value paired with the one below | 0 |
| E2 | sorted: a run before it tested by position | 0 |
| E3 | onepass: the sum written the other way round | 0 |
| E4 | ordered: a step of at most 1 | 0 |

M1, M2 and M7 give answers that depend only on how many of each value
there are and how the values are spaced, which no property but
P1 changes; M2 is wrong exactly on the 613 arrays with a pair. M3 counts
a run of 1s as if 0s stood before it, so it can go wrong only where 1 is
the smallest value, which a shift or a negation moves: P3 and P4 see it
as often as P1 does, or more. M8 compares every key with the smallest
one only, and negating the array changes which value that is, so P4 sees
it more often than P1. M4, M5 and M6 depend on the order the values come
in, which is what P2 changes; negating turns M5's look above into a look
below, and the array twice over gives M5 and M6 a second look at every
pair once its counts are final, so P4 and P5 see them as well. P3 sees
only M3, the one mutant that treats some value apart from the others.

M5 was first written as `if let Some(below) = None`, to switch the look
below off. `karac check` passed it and `karac __mir-run` stopped with
invalid MIR, which is kara B-2026-10-14-31, filed from this kata (see
Compiler findings); it was rewritten to look above twice. E1 is safe
because every pair is met from its other end; E2 because a run stands
before the current one exactly when the current one does not start at
0; E3 trivially; and E4 because the keys of the ordered walk are
distinct and increasing, so a step is never below 1.

## Verification

Every arm prints the same output as `find_lhs.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes every arm, the differential and the bench program. `karac check`
and `karac __mir-run` at kara `2b8e2b9f00`, the compiled MIR backend at
`555c29b44e`.

The frozen legacy backends agree too: every arm prints the same output
under `karac run --interp`, `karac run` and `karac build`, and under
`KARAC_AUTO_PAR=1 karac build`, and the differential prints its line
under `karac run --interp` and `karac build`. Only the bench program is
refused, by `karac build` at type checking: it passes `arrays[..]` to
the borrowing parameter, which legacy reads as a move out of an index
(E_INDEX_MOVE_NON_COPY). Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 100 arrays of 20,000 values,
the problem's longest, once, each from a random range of 1 to
5,000 values somewhere between -10^9 and 10^9, and then 20 times over
solves every one. Every implementation prints `100 arrays, 20 rounds:
total 176800, checksum 481481270`, the Kāra program under `karac
__mir-run` included (85 s).

Each implementation counts into a fresh hash table on every call: a
`HashMap` with its default hasher in Rust, which is SipHash-1-3 under a
random key, the hash Kāra's `Map` uses; Go's built-in map; a dict in
Python; and in C, which has no map, an open-addressing table written by
hand, hashed with the splitmix64 finalizer and allocated per call. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.56 to 0.59 s |
| Rust (`rustc -O`) | 0.90 to 1.02 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.80 to 0.87 s |
| Go | 1.08 to 1.10 s |
| Python | 4.97 to 5.48 s |
| Kāra (`karac build --mir`) | 1.88 to 2.04 s |

So `bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`555c29b44e`. A copy outside this directory that passes
`arrays[..].clone()` instead, which legacy builds, runs in 2.04 to
2.20 s under the legacy `karac build` and 1.90 to 1.93 s under `karac
build --mir`, three runs each, so v2 is level with legacy here. Under
`karac __mir-llvm-run` the program prints the same line in 19.6 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

The Kāra row is about 2 times Rust's. In callgrind profiles of both at
2 rounds, building the arrays included, the Kāra program runs
1.92 billion instructions to Rust's 0.73 billion. 44% of Kāra's is
`karac_hash_word`, SipHash-1-3 of one key, called out of line
9.1 million times at about 93 instructions a call, and 33% is
`karac_mir_map_find`, 8.5 million calls: the counting line `count[x] =
count.get(x).unwrap_or(0) + 1` looks each value up twice, once to read
and once to store, where Rust's `entry` looks it up once and inlines the
hash. That this is where the gap comes from is read from the profiles;
it is not measured by changing the program.

## Compiler findings

**kara B-2026-10-14-31** (new, open; found by this kata's mutation
testing, low severity). `if let Some(b) = None { ... }`, the payload's
type left to inference, passes `karac check`, and then `karac __mir-run`
stops with "invalid MIR: ... binary operands of different types i64 and
()" and `karac __mir-llvm-run` panics in its codegen. A `None` bound by
`let` first is refused by check, and a `match` on a bare `None` runs, so
only the `if let` lets the unresolved type through. The kata's own arms
do not write this; the mutant M5 did.

The legacy failure above is not filed because legacy is frozen.
