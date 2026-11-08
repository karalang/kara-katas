# 2008. Maximum Earnings From Taxi

There are `n` points on a road, labelled `1` to `n`, that a taxi drives in
the direction from `1` to `n`. The passengers are `rides`, where
`rides[i] = [start, end, tip]` asks for a ride from `start` to `end` and
offers a tip. A ride earns `end - start + tip` dollars. The taxi carries at
most one passenger at a time, and may drop one off and pick up another at
the same point. Return the most the driver can earn.

```
n = 5,  rides = [[2,5,4],[1,5,1]]                                     ->  7
n = 20, rides = [[1,6,1],[3,10,2],[10,12,3],[11,12,2],[12,15,2],[13,18,1]]  ->  20
```

**Constraints:** `1 <= n <= 10^5`; `1 <= rides.length <= 3 * 10^4`;
`1 <= start < end <= n`; `1 <= tip <= 10^5`.

The harness also draws tips of 0, which the constraints leave out; every
arm reads them the same way, and they make a ride that only breaks even on
distance worth comparing with the empty road.

## Approaches

| file | mechanism |
|---|---|
| `taxi.kara` ★ | `best[p]`, the most earned on reaching point `p`: the best at `p - 1`, or a ride ending at `p` on top of the best at its start; the rides grouped by where they end in a `Vec[Vec[..]]`. O(n + m) |
| `taxi_sorted.kara` | the rides sorted by end, `best[i]` the most from the first `i`; ride `i` unused, or added to the best of those ending by its start, found by binary search. O(m log m) |
| `taxi_memo.kara` | top down over the rides sorted by start: skip ride `i`, or take it and go on from the first ride starting at or after its end (`partition_point`); each suffix's best kept in a `Vec[Option[i64]]`. O(m log m) |
| `taxi_heap.kara` | the rides sorted by start; a `PriorityQueue` of (end, earnings) holds the trips under way, each settled into the best so far once its end is passed. O(m log m) |
| `taxi_map.kara` | the rides sorted by end; a `SortedMap` from each end reached to the best by then, the best at a ride's start the last entry at or before it (`range_inclusive`, `next_back`). O(m log m) |
| `taxi_solution.kara` | LeetCode's Rust template (a unit struct, `impl Solution`, a `mut rides: Vec<Vec<i32>>` parameter, `sort_unstable_by_key`, `usize` points, a `&` reference), carried by `karac fix` to a clean check |
| `differential.kara` | all six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: the answers for LeetCode's two examples
and four more; then the sum and a checksum of the answers for 3000 roads of
2 to 16 points with 1 to 8 rides, and for 6 roads of 1000 or 100000 points
with 30000 rides each. `taxi.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every set of rides, kept when no two overlap (one may start where
another ends), the best total. It checks 1500 problems of 1 to 10 rides on
roads of 2 to 20 points. Every random choice of a problem (the rides, a
shuffle, a shift, a ride to append) is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the rides shuffled leave the answer |
| P3 | the road lengthened at its start, every point moved along by the same amount, leaves the answer |
| P4 | the road driven the other way, point `p` turned into `n + 1 - p`, leaves the answer |
| P5 | one more ride never lowers the answer, and raises it by at most what that ride earns |
| P6 | each arm agrees with at least three of the other five |

The differential prints `1500 problems: checksum 107715863, 54000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Fifteen are kept, two or
three to each arm. All thirty are killed, each fails the same way under
both backends, none by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the best never carried to the next point | P1 914, P4 667, P5 69, P6 914 |
| M2 | ★: point 2 never reached | P1 385, P3 385, P4 371, P6 385 |
| M3 | ★: a ride never starting where another ends | P1 626, P6 626 |
| M4 | sorted: a ride always taken | P1 482, P2 367, P4 427, P5 231, P6 482 |
| M5 | sorted: the rides sorted by start | P1 186, P2 126, P4 234, P5 46, P6 186 |
| M6 | memo: a ride never skipped | P1 669, P4 515, P5 137, P6 669 |
| M7 | memo: only the taken branch remembered | P1 76, P4 49, P5 12, P6 76 |
| M8 | memo: the last ride never taken | P1 942, P4 703, P5 68, P6 942 |
| M9 | heap: the last trip settled, not the best | P1 43, P4 75, P5 14, P6 43 |
| M10 | heap: the trips still under way never settled | P1 1500, P4 690, P5 84, P6 1500 |
| M11 | map: the best stored at the ride's start | P1 1085, P2 302, P4 568, P5 61, P6 1085 |
| M12 | map: the best never raised | P1 1500, P6 1500 |
| M13 | map: the rides never sorted | P1 669, P2 533, P4 773, P6 669 |
| M14 | Rust: the best never carried back a point | P1 899, P3 906, P4 667, P5 75, P6 899 |
| M15 | Rust: rides matched one point late | P1 1295, P3 692, P4 725, P5 218, P6 1295 |

P1 and P6 kill all fifteen, P4 thirteen, P5 eleven, P2 four and P3 three.
P4 is the strongest property after the literal reading: driving the road
the other way swaps which rides start early and which end late, so an edit
that treats one end of a ride, or one end of the road, apart from the other
shows there. It misses only the edits that stay consistent under the
mirror: a ride that may not start where another ends (M3) is still refused
after it, and a map whose best never rises (M12) answers the best single
ride either way. P2 sees only the edits that let the input's order through:
a heap or map arm that never sorts (M13), a sort on the wrong key (M5),
an entry stored where a later ride reads it out of order (M11), and the
sorted arm taking every ride whatever came before (M4). P3 sees the edits
pinned to a point's number rather than to the rides, which a shift moves
past: point 2 skipped (M2), the walk starting one point off (M14, M15). M9
is the faintest, 43 problems in 1500: settling the last trip to end rather
than the best differs only when two trips end before one ride starts and
the later one earned less.

The other fifteen fail as a kept one does, or with counts of their own
that add nothing. The tips dropped fails alike in the ★, sorted and Rust
arms (P1 and P6 only: a problem without its tips is still a problem every
property holds for). A ride refused when it starts where another ends fails
alike in all five arms that have such a comparison (M3's 626). The heap arm
queuing each ride on its own earnings and the map arm reading the first
entry rather than the last both answer the best single ride, and fail
alike. The ★ arm's answer read one point early, the sorted arm's last best
never read, the memo arm's next ride allowed to overlap, the heap arm's
rides unsorted, and the Rust arm's rides unsorted and answer read from
point 2 fail with counts of their own. One draft was replaced twice: the
memo arm with its rides unsorted recursed past the stack, and its skip
passing over two rides ran off the end of the rides, both crashes.

## Verification

Every arm prints the same output as `taxi.py` under `karac __mir-run` (the
v2 MIR interpreter), `karac __mir-llvm-run`, and `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer) with no error. `karac run` and a
`karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 0.91 s (★) to 2.8 s (memo) and the
differential 2.1 s.

The ★, sorted and memo arms were written in Kāra and checked clean. Two
arms were first written with Rust's spellings, and `karac fix` carries
each in one round: the heap arm's `BinaryHeap[Reverse[(i64, i64)]]`
becomes a `PriorityQueue[(i64, i64)]`, which already pops the smallest
first, and every `Reverse(..)` it was built or matched with is unwrapped
(six edits); the map arm's `best.range(0..=start)` becomes
`best.range_inclusive(0, start)` (one edit). Before kara cdb6382000 the
first was an unknown type `Reverse` with a did-you-mean of `Release`, and
the second an arity error with no fix.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` alone, in five rounds (16, 3, 2, 2 and 2 edits).
The first round carries the struct, the `Vec<..>` types, `vec![..]`, the
`&&`, the `&` reference and the `::` path, and turns
`sort_unstable_by_key` into `sort_by_key`. Rust's `mut rides:
Vec<Vec<i32>>` parameter, which owns the vector and sorts it in place, now
becomes `rides: own Vec[Vec[i32]]` with `let mut rides = rides;` at the
top of the body; before cdb6382000 it was a parse error with no fix. The
later rounds settle the `usize` points: `let n = n as usize;` becomes `as
i64` (kata 2003's fix), and the casts in `let (end, tip) = (r[1] as usize,
r[2] as i64);` become `as i64`, which the tuple `let` did not get before.

## Benchmarks

The bench builds 80 roads of 10000 points with 5000 rides each, rides up to
100 points long with tips up to 1000, once in all five languages, and runs
the ★ arm on each for 25 rounds, the road's empty tail shortened by the
round: 2000 calls, each grouping 5000 rides over about 10000 points. Every
implementation prints `2000 calls: sum 706147825, checksum 256814380`.
Every language allocates the per-point ride lists and the best array per
call, as the Kāra program does; the C mirror grows each list by doubling.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| Go | 0.553 to 0.638 s | 0.601 s |
| Kāra (`karac build`) | 0.658 to 0.709 s | 0.665 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.661 to 0.737 s | 0.673 s |
| C (`clang -O3`) | 0.658 to 0.703 s | 0.677 s |
| Rust (`rustc -O`) | 0.684 to 0.740 s | 0.695 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.673 to 0.749 s | 0.701 s |
| Python | 6.5 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.659 s) is not above its real time (0.665 s).

The sequential Kāra program is 0.96x Rust under overflow checks and 0.99x
C.