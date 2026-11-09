# 2021. Brightest Position on Street

A perfectly straight street is a number line. `lights[i] = [position,
range]` is a street lamp that lights the closed stretch `[position - range,
position + range]`. The brightness of a position is the number of lamps
that light it. Return the brightest position; if there are several, the
smallest of them.

```
lights = [[-3,2],[1,2],[3,3]]  ->  -1
lights = [[1,0],[0,1]]          ->  1
lights = [[1,2]]                ->  -1
```

**Constraints:** `1 <= lights.length <= 10^5`; `-10^8 <= position <=
10^8`; `0 <= range <= 10^8`.

Moving left from a lit position keeps every lamp lighting it until one of
their left ends is passed, so the answer is always some lamp's left end.

## Approaches

| file | mechanism |
|---|---|
| `brightest.kara` ★ | each lamp two events, `(position - range, 1)` and `(position + range + 1, -1)`, sorted; a sweep applies every event at a position before reading the brightness there, and the first position to beat the best wins. O(n log n) |
| `brightest_map.kara` | a `SortedMap` from each position to its change in brightness, built through `entry().or_insert(0)`; a walk in key order. O(n log n) |
| `brightest_brute.kara` | every left end tried, each lamp checked for whether it lights it, the brightest kept, leftmost on a tie. O(n^2) |
| `brightest_heap.kara` | the lamps sorted by their left ends and a `PriorityQueue` of the right ends of the lit ones; at each left end the lamps that ended before it leave the queue, and its size is the brightness. O(n log n) |
| `brightest_search.kara` | the left ends and the right ends sorted apart; at each left end, the lamps started at or before it less those ended before it, each count by `partition_point`, the best carried by a `fold`. O(n log n) |
| `brightest_solution.kara` | LeetCode's Rust template (`use std::collections::BTreeMap`, a unit struct, `impl Solution`, `Vec<Vec<i32>>`, `*diff.entry(..).or_insert(0) += 1`, `let (mut cur, mut best, mut ans) = (0, 0, 0i64)`, `for (&x, &d) in diff.iter()`, a `&Vec` wrapper), carried by `karac fix` to a clean check |
| `differential.kara` | all six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's three
examples and five more; then the sum and a checksum of the answers for
3000 streets of 1 to 12 lamps within 1 to 20 of 0 with ranges up to 0 to
7, and for 5 streets of 2000 lamps, from positions and ranges up to 10^8
to lamps of range 0. `brightest.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every position from the leftmost lit one to the rightmost, the
lamps lighting it counted, the first of the brightest kept. It checks 1500
problems of 1 to 10 lamps at positions within 1 to 20 of 0 with ranges up
to 0 to 7. Every random choice of a problem (the lamps, a distance to move
them) is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the lamps listed in reverse order leave the answer |
| P3 | every lamp moved by the same distance moves the answer by it |
| P4 | every lamp listed twice leaves the answer |
| P5 | a lamp of range 0 added at the answer leaves the answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `1500 problems: checksum 781643493, 54000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Sixteen are kept, two or
three to each arm. All thirty are killed, each fails the same way under
both backends, none by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the light gone at the end itself | P1 762, P3 256, P6 762 |
| M2 | ★: the light starting one place late | P1 1355, P3 256, P6 1355 |
| M3 | ★: the events never sorted | P1 982, P2 1271, P6 982 |
| M4 | map: a change replacing the one there | P1 326, P2 433, P4 284, P6 326 |
| M5 | map: the brightness read before the change | P1 1500, P5 172, P6 1500 |
| M6 | map: a range read as twice as wide | P1 906, P6 906 |
| M7 | brute: a lamp covering only up to before its end | P1 633, P3 142, P6 633 |
| M8 | brute: a tie never moving left | P1 386, P2 575, P6 386 |
| M9 | brute: the lamp itself not counted | P1 68, P3 209, P4 68, P6 68 |
| M10 | heap: a lamp ending at the start let go | P1 427, P4 100, P6 427 |
| M11 | heap: the spans sorted by their ends | P1 520, P2 152, P4 21, P5 36, P6 520 |
| M12 | heap: the new lamp counted before it is pushed | P1 1383, P3 1499, P6 1383 |
| M13 | search: the starts counted strictly before | P1 643, P3 517, P6 643 |
| M14 | search: the ends never sorted | P1 498, P2 620, P4 480, P5 285, P6 498 |
| M15 | Rust: the range ignored | P1 942, P6 942 |
| M16 | Rust: the first position always the answer | P1 1053, P3 7, P6 1053 |

P1 and P6 kill all sixteen, P3 seven, P2 five, P4 five and P5 three. P3
moves every lamp and expects the answer to move with it; it sees an edit
that ties the answer to a fixed place or to the lamps' order rather than
their positions: an end or a start off by one (M1, M2, M7), a lamp not
counting itself (M9), a lamp counted before it is lit (M12), starts
counted strictly before (M13), the first position always the answer
(M16). P2 reverses the list of lamps, which only an edit that reads
the list's order sees: events or ends never sorted (M3, M14), a change in
the map replacing another lamp's (M4), a tie not moving left when a later
lamp is further left (M8), spans sorted by their ends (M11). P4 lists
every lamp twice, which doubles every brightness; it sees the edits whose
count is not proportional to the lamps: a replaced change (M4), the lamp
itself not counted (M9), a lamp ending at the start let go (M10), and the
two sorting edits (M11, M14). P5 adds a lamp of range 0 at the answer,
which a correct arm keeps as the answer; it sees a brightness read before
its change (M5) and the two sorting edits.

The other fourteen fail as a kept one does, or with counts of their own.
The map arm's light taken off at its end and the search arm's ends counted
through the start fail as M1. The ★ arm's tie taking the later position
and the search arm's tie taking the later start and its starts walked
from the right fail alike (P1 640). With counts of their own: the ★
arm's answer one place right (P1 1500, P5 734), the map arm's best never
raised (P1 1315, P5 811), the brute arm's right ends tried (P1 624) and
left end one place early (P1 1333, P3 175, P5 87), the heap arm's answer
at the span's end (P1 975, P5 26) and queue largest first (P1 490), and
the Rust arm's end read as the start (P1 778), light starting a place
early (P1 1354) and gone a place late (P1 440).

Four drafts were replaced. Three survived, two of them equivalent: the
★ arm reading each event on its own (the events sort the `-1`s at a
position before the `+1`s, so no partial count there passes the full
one), and the brute arm's answer starting at the first lamp (any lamp
lights its own left end, so the first is always replaced). The third, the
heap arm letting go of only one ended lamp per start, is not equivalent
(the queue keeps lamps that no longer light the start), but in these small
problems the stale lamps never changed an answer. The fourth, the Rust arm
keeping only the last change, `cur = d` in place of `cur += d`, did not
check: assigning the `ref i32` that `diff.iter()` yields to `cur`, an
`i64` since its tuple's literal took the default, is refused with E0509
("a view ... is stored in an escaping closure, a `shared` value or a
channel"), though `cur` is a plain local. `let mut cur: i64 = 0` is
refused the same way; an `i32` binding checks. That refusal is ledger row
B-2026-11-08-67.

## Verification

Every arm prints the same output as `brightest.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them. Under `karac __mir-run` the arms take 0.4 s to 15.7 s (brute) and
the differential 3.7 s.

The five arms were written in Kāra. The search arm's `fold`, whose closure
returns `(here, x)` with `x` the `ref i64` that `starts.iter()` yields, was
refused: the closure's type kept the reference inside the tuple and failed
against the `(i64, i64)` the fold carries, though the tuple literal's own
check had accepted it. Fixed in kara 8da94b7d90 for this kata: a closure's
tail tuple now reads a borrowed scalar part as its value, as a bare `x`
tail already did.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` alone, in three rounds (23, 2 and 4 edits). The
first carries the `Vec<..>` and `BTreeMap<..>` types, the `::` paths, the
unit struct, the `&lights` loop, the `mut` inside the tuple pattern, the
`(&x, &d)` pattern, the `&Vec` parameter and the `|&(p, r)|` closure, and
drops the `use`; the second renames `BTreeMap` to `SortedMap`; the third
drops the `0i64` suffix the default already gives, turns the wrapper's
`vec![..]` into a list literal, drops its `ref`, and drops an `as i64` on
an `i32`, a widening Kāra does by itself.

## Benchmarks

The bench builds 100 streets of 10000 lamps once in all five languages,
the lamps within 10^6, 10^7 or 10^8 of 0 with ranges up to 10^3, 10^5 or
10^6, and runs the ★ arm on each for 5 rounds: 500 calls, each building and
sorting 20000 events. Every implementation prints `500 calls: sum
-9096236005, checksum 303489337`. Every language builds and sorts the
events per call, as the Kāra program does.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `6a852dc7b7` on LLVM 22:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 0.454 to 0.566 s | 0.465 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.458 to 0.648 s | 0.485 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.492 to 0.543 s | 0.505 s |
| Kāra (`karac build`) | 0.497 to 0.561 s | 0.518 s |
| C (`clang -O3`) | 1.517 to 1.582 s | 1.563 s |
| Go | 1.983 to 2.268 s | 2.075 s |
| Python | 6.2 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.510 s) is not above its real time (0.518 s).

The sequential Kāra program is 1.04x Rust under overflow checks and 0.32x
C. When this kata was written it was 2.46x (kara 64bba595f2) Rust: Kāra
sent a Vec of pairs to the runtime's generic merge sort, which called the
comparison through a pointer, where Rust monomorphizes its stable sort.
That was B-2026-11-08-85, fixed by kara d308599fbb: a plain `sort()` of
non-integer elements now runs an emitted merge sort with the comparison in
line.