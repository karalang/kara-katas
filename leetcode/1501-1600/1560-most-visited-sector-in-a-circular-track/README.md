# 1560. Most Visited Sector in a Circular Track

Given an integer `n` and an integer array `rounds`: a circular track has
`n` sectors labeled `1` to `n`, and a marathon is held on it in `m`
rounds. The `i`th round starts at sector `rounds[i - 1]` and ends at
sector `rounds[i]`, running in ascending order of sector numbers
(`n` is followed by `1`). Return the most visited sectors sorted in
ascending order.

```
n = 4, rounds = [1,3,1,2]           ->  [1,2]
n = 2, rounds = [2,1,2,1,2,1,2,1,2] ->  [2]
n = 7, rounds = [1,3,5,7]           ->  [1,2,3,4,5,6,7]
```

**Constraints:** `2 <= n <= 100`; `1 <= m <= 100`;
`rounds.length == m + 1`; `1 <= rounds[i] <= n`;
`rounds[i] != rounds[i + 1]`.

## Approaches

The legs join up, so the run is one walk from the first sector to the
last: whole laps, which visit every sector alike, and then the stretch
from the first sector on to the last, which is visited once more.

| file | mechanism |
|---|---|
| `sectors.kara` ★ | the sectors from the first on to the last: `(start..=end).collect()`, or `(1..=end).chain(start..=n).collect()` when the run wraps past `n`. O(n) |
| `sectors_walk.kara` | the run walked sector by sector: a count per sector in a `Vec`, the start counted once, each leg from `windows(2)` stepped round until it arrives, and the sectors with the largest count kept by a `filter`. O(n m) |
| `sectors_diff.kara` | a difference array: each leg adds 1 over the sectors it arrives at, one range or two when it passes `n`, through a helper taking `mut ref Vec[i64]`; a running sum gives every count. O(n + m) |
| `sectors_solution.kara` | LeetCode's Rust template (`most_visited(n: i32, rounds: Vec<i32>) -> Vec<i32>`, the ★ arm pushing the sectors by two loops when the run wraps), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples, then
`n = 2` with `[1, 2]`, `n = 5` with `[3, 1]` and `[5, 1]`, `n = 3` with
a run that comes back to its start, and `n = 10` with a run that ends one
short of its start; then the count of sectors and a checksum for 3000
random tracks of up to 8 sectors and 8 legs, 300 of up to 100 and 100,
and 30 of up to 1000 sectors and 100 legs. `sectors.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the marathon written out as the list of sectors it passes,
counted in a `Map`, and the sectors counted most, sorted. It checks 3000
tracks of 2 to 8 sectors run for 1 to 6 legs, every random choice drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is nonempty, ascending, names sectors of the track, and holds the sector the run ends at |
| P3 | every sector moved on by the same turn moves the answer on |
| P4 | a lap put after the run (to another sector and back) leaves the answer |
| P5 | the answer holds as many sectors as lie from the first on to the last |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 18988817, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the run read as ending one leg early | P1 3000, P2 1662, P4 1876, P5 3000, P6 3000 |
| M2 | ★: a run ending where it began read as wrapping | P1 732, P2 732, P5 732, P6 732 |
| M3 | ★: the wrapped pieces in the wrong order | P1 1159, P2 1159, P3 1107, P6 1159 |
| M4 | walk: the start not counted | P1 3000, P5 3000, P6 3000 |
| M5 | walk: each leg's last sector not counted | P1 2624, P2 2195, P4 1450, P5 2525, P6 2624 |
| M6 | walk: sector `n` never kept | P1 1859, P2 700, P3 2475, P5 1859, P6 1859 |
| M7 | diff: a wrapping leg adds nothing before `n` | P1 1237, P2 418, P3 1663, P4 326, P5 1229, P6 1237 |
| M8 | diff: every leg counts its own start | P1 2313, P2 1554, P3 2205, P4 1685, P5 2146, P6 2313 |
| M9 | template: sector `n` left out of the wrapped piece | P1 1159, P3 1750, P5 1159, P6 1159 |
| M10 | template: the run read as starting at its second sector | P1 3000, P5 3000, P6 3000 |

## Benchmarks

The bench builds 20000 tracks of 2 to 100 sectors run for 1 to 100 legs
once, and asks each 100 times by the ★ arm, in all five languages. Every
call returns a fresh vector of about 26 sectors: Rust collects the same
range or chain, C mallocs the exact size and fills it, Go appends to a
nil slice, and Python joins two `range` lists. Every implementation
prints `100 passes over 20000 tracks: 51799000 sectors, checksum
342941437`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.150 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.163 s |
| Rust (`rustc -O`) | 0.165 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.250 s |
| Kāra (`karac build`) | 0.258 s |
| Go | 0.563 s |
| Python | 1.6 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.27 s and 0.29 s on one run).

Kāra is 1.53x Rust under overflow checks by median. Traced with
callgrind: Kāra runs 2.06 G instructions to Rust's 0.75 G, and 26% of
Kāra's are `karac_realloc_or_panic` and `memcpy`, because the chain's
`collect` grows its vector by doubling where Rust's sizes it once from
the two ranges' exact lengths. The same function with the wrapped case as
a `collect` and an `extend` ran 0.235 s, and with `Vec.with_capacity` of
the exact size and push loops 0.228 s, against Rust's 0.172 s in the same
batch of five. Filed as B-2026-11-14-15 (perf); the ★ arm keeps the
`chain`, the natural way to write it.

## Verification

All four arms print the same output as `sectors.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`.

## Writing it

The ★, walk and difference arms were written in Kāra and checked as
written. The bench read each track as `let (n, rounds) = tracks[t];`,
which is refused (a tuple holding a `Vec` cannot be moved out of an
index); one round of `karac fix` made it `ref tracks[t]`, as the refusal
says it will.

The Rust template took 5 changed lines, then 1 added, over two rounds of
`karac fix`: the `Vec<..>` types to `Vec[..]`, `Vec::new()` to
`Vec.new()`, the wrapper's `|&r|` and `|&s|` to `|r|` and `|s|`, and
`Solution::` to `Solution.`; then `struct Solution {}` added. The
template's `*rounds.last().unwrap()` checks as written. It checks and
agrees with no hand edit.
