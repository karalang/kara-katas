# 1217. Minimum Cost to Move Chips to The Same Position

We have `n` chips, where the position of the `i`th chip is
`position[i]`.

We need to move all the chips to the same position. In one step, we can
change the position of the `i`th chip from `position[i]` to:

- `position[i] + 2` or `position[i] - 2` with `cost = 0`.
- `position[i] + 1` or `position[i] - 1` with `cost = 1`.

Return the minimum cost needed to move all the chips to the same
position.

```
position = [1,2,3]            ->  1    the chip at 2 moves to 1 or 3
position = [2,2,2,3,3]        ->  2
position = [1,1000000000]     ->  1
```

**Constraints:** `1 <= position.length <= 100`; `1 <= position[i] <=
10^9`.

The arms are `fn min_cost_to_move_chips(position: Vec[i64]) -> i64`. The
two Rust arms keep the method LeetCode gives Rust users, on `Vec<i32>`,
inside `impl Solution`, and a one-line `min_cost_to_move_chips` narrows
the positions and calls it.

## Approaches

A move of two is free, so every chip reaches any position of its own
parity for nothing, and only a change of parity costs 1: all chips meet
at an odd position or an even one, and the cheaper pays one for each
chip of the other parity.

| file | mechanism |
|---|---|
| `minimum_cost_to_move_chips_to_the_same_position.kara` ★ | the odd and the even chips counted in one loop, and the lesser count the answer. O(n) |
| `minimum_cost_to_move_chips_to_the_same_position_targets.kara` | every chip's position tried as the meeting place, each chip paying its distance modulo 2, and the cheapest place kept; some chip's position is always among the best, since only the place's parity matters. O(n^2) |
| `minimum_cost_to_move_chips_to_the_same_position_lowbit.kara` | the odd chips counted as the sum of every position's lowest bit, by an iterator's `map` and `sum`, and the even ones as the rest |
| `minimum_cost_to_move_chips_to_the_same_position_halves.kara` | the positions sorted by parity with `sort_by_key`, the even ones first, and the cut where the first odd one stands found by a binary search; the smaller side moves. O(n log n) |
| `minimum_cost_to_move_chips_to_the_same_position_filter.kara` | a Rust solution as LeetCode's Rust users write it (the even chips counted by `position.iter().filter(\|&&p\| p % 2 == 0).count()`, the odd ones as the rest, and `even.min(odd) as i32`), carried to Kāra by `karac fix` |
| `minimum_cost_to_move_chips_to_the_same_position_fold.kara` | another Rust solution (both counts in one pass, `fold((0, 0), \|(o, e), &p\| ..)` with `p & 1` telling odd from even, and `std::cmp::min(odd, even)`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six more properties |

Every arm prints the same 12 lines: LeetCode's three examples; one chip
(`0`); three chips at one place (`0`); `[1, 2]` (`1`); three even chips
and three odd ones (`3`); 1000 random small cases, 1 to 10 chips at
positions up to 1 to 10 (`1000 small cases: costs total 1638, checksum
169294616`); and four at the constraints' top, 100 chips: random
positions up to 10^9 (`44`), all at 10^9 (`0`), the positions 1 to 100
(`50`), and 99 odd chips with one at 10^9 (`1`).
`minimum_cost_to_move_chips_to_the_same_position.py` mirrors the ★ arm,
and its output is byte-identical. Every arm gives the same output under
`karac run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, targets, lowbit and halves arms check clean as
written. The filter arm takes one round of 5 fixes (among them `struct
Solution;` to `struct Solution {}`, `Vec<i32>` to `Vec[i32]`, and
`|&&p|` to `|p|`), and the fold arm one round of 8 (among them `|(o, e),
&p|` to `|(o, e), p|`, the fold's start `(0, 0)` to `(0i32, 0i32)`, so
the counts are the `i32` the method returns, and `std::cmp::min` to
`min`). In both, the wrapper's own `as i64` on the `i32` answer is
dropped as a widening Kāra makes by itself. Both outputs match.

## Gaps

None found.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every place from the least position to the greatest tried as
the meeting place, and every chip moved there as cheaply as it can be,
found by a search over the positions around them in which a step of one
costs 1 and a step of two nothing (a 0-1 breadth-first search). 2000
random cases: 1 to 12 chips at positions up to 1 to 9; 1438 of them cost
something.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the chips in reverse order give the same |
| P3 | every chip two further gives the same |
| P4 | every chip one further gives the same |
| P5 | a chip added where one stands costs the same or one more |
| P6 | no more than half the chips pay |
| P7 | the ★ arm's answer |

All 84,000 checks pass on every arm: `2000 cases: checksum 344401722,
84000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. A Python reading of
the same cases, each chip's cheapest path by Dijkstra's algorithm with
`heapq`, gives the same checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All
twelve are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the dearer side paid | P1 1744, P6 1744, P7 8720 |
| S2 | ★: parity read modulo 3 | P1 937, P3 983, P4 1153, P7 4685 |
| T1 | targets: a chip pays for its moves of two | P1 1320, P5 47, P6 390, P7 1320 |
| T2 | targets: the last place kept rather than the cheapest | P1 390, P2 623, P5 413, P6 390, P7 390 |
| L1 | lowbit: the second bit taken for the lowest | P1 900, P4 1065, P7 900 |
| L2 | lowbit: the odd chips always pay | P1 1171, P4 1744, P6 1171, P7 1171 |
| H1 | halves: the chips never sorted by parity | P1 1012, P2 1188, P4 1170, P5 329, P7 1012 |
| H2 | halves: the search looks for the first even chip | P1 1438, P7 1438 |
| F1 | filter: one chip too few counted odd | P1 829, P4 1744, P6 115, P7 829 |
| F2 | filter: the even chips always pay | P1 573, P4 1744, P6 573, P7 573 |
| D1 | fold: an odd chip counted on both sides | P1 1171, P4 1744, P6 1171, P7 1171 |
| D2 | fold: the odd count begun at one | P1 573, P4 1744, P6 236, P7 573 |

A mutation of the ★ arm fails P7 on all six arms, the ★ arm against the
other five. Of the 2000 cases, 1438 cost something, and 256 have as many
odd chips as even ones, 1171 more odd and 573 more even (counted by a
Python reading of the cases). S1 pays the dearer side and fails the 1744
where the two counts differ. L2 always moves the odd chips, and D1,
counting an odd chip on both sides, makes the even count every chip, so
the lesser is again the odd: the two fail alike, in the 1171 with more
odd chips. F2 always moves the even chips, and D2, its odd count begun
at one, moves them whenever there are more even, and the two fail the
573. H2's search, looking for the first even chip among the even ones
sorted first, ends at one end or the other, so it answers 0 and fails
every one of the 1438 that cost something. P4, every chip one further,
swaps the two parities; it catches every edit that treats them
differently, and P3, every chip two further, only S2, which reads the
parity modulo 3.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (the odd and the even chips counted, the lesser count the cost) on
20000 sets of 100 chips, the constraints' most, at positions up to 10^9,
drawn once; then 20 rounds over the sets, every answer folded into a
checksum. Every program prints `20 rounds over 20000 sets of 100 chips:
checksum 921447271`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.227 to 0.273 s | 0.248 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.229 to 0.269 s | 0.245 s |
| Rust (`rustc -O`) | 0.038 to 0.057 s | 0.041 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.224 to 0.268 s | 0.241 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.229 to 0.262 s | 0.242 s |
| C (`clang -O3`) | 0.038 to 0.051 s | 0.043 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.027 to 0.046 s | 0.031 s |
| Go | 0.280 to 0.337 s | 0.292 s |
| Python | 3.126 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (0.241 s
against 0.245 s), and the two ranges overlap. Kāra takes about 5.7x C's
time (0.245 s against 0.043 s); Kāra is about 16% ahead of Go (0.245 s
against 0.292 s). Python takes about 13x Kāra's time. No profile was
taken.
