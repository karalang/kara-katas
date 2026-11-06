# 370. Range Addition

Given an integer `length` and an array of `updates`, each `[start, end,
inc]`, start from an array of `length` zeros, add `inc` to every cell from
`start` to `end` inclusive for each update, and return the final array.

```
length = 5, updates = [[1,3,2],[2,4,3],[0,2,-2]]    -> [-2, 0, 3, 5, 3]
length = 10, updates = [[2,4,6],[5,6,8],[1,9,-4]]   -> [0, -4, 2, 2, 2, 4, 4, -4, -4, -4]
```

**Constraints:** `1 <= length <= 10^5`; `0 <= updates.length <= 10^4`;
`0 <= start <= end < length`; `-1000 <= inc <= 1000`.

## Approaches

The arms take the updates as a `Vec[(i64, i64, i64)]` and destructure each
one in the loop header.

| file | mechanism | time |
|---|---|---|
| `range_addition.kara` ★ | a difference array: `+inc` at `start`, `-inc` after `end`, then one running sum | O(n + k) |
| `range_addition_brute.kara` | add `inc` to every cell of every range | O(n k) |
| `range_addition_sweep.kara` | two events per update, sorted by position with `sort_by`, swept left to right | O(k log k + n) |
| `range_addition_fenwick.kara` | the difference array in a Fenwick tree: two point updates per range, a prefix sum per cell | O((k + n) log n) |
| `differential.kara` | the difference, sweep and Fenwick arms against the brute-force arm, 30,000 checks, five properties | — |

Every arm prints the same 10 lines: the two LeetCode examples, seven edge
cases (no updates, one cell, the whole array, updates that cancel, single
cells, nested ranges, large increments), and the cell count and a checksum
over 300 random arrays of up to 200 cells with up to 300 updates.
`range_addition.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms, with the brute-force arm
as the oracle. The test draws 2,000 random arrays of 1 to 40 cells with up
to 30 updates; half the cases keep `inc` in `[-5, 5]`, so that cells cancel
to zero often, and half use the full `[-1000, 1000]`.

| | property |
|---|---|
| P1 | each arm gives the oracle's array |
| P2 | the cells add up to the sum of `inc * (end - start + 1)` over the updates |
| P3 | reversing the order of the updates changes nothing |
| P4 | splitting every update in two at a random cell changes nothing |
| P5 | adding the negation of every update leaves all zeros |

It prints `2000 cases, 30000 checks, 0 failures` under `karac __mir-run`
(about 18 seconds), `karac run --interp`, LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`.

## Mutation testing

Nine edits to the copies inside `differential.kara`, each run under
`karac __mir-run`. All nine are killed.

| # | mutation | how |
|---|---|---|
| M1 | diff: the `-inc` lands on `end`, not after it | P1, P2 and P4, 5620 failures |
| M2 | diff: each cell takes the running sum before its own difference | P1 and P2, 3230 failures |
| M3 | sweep: events sorted by position descending | P1 and P2, 3832 failures |
| M4 | sweep: applies a cell's events only once the sweep has passed it | P1 and P2, 3230 failures |
| M5 | sweep: the closing event lands on `end`, not after it | P1, P2 and P4, 5620 failures |
| M6 | fenwick: an update climbs one index at a time instead of by the lowest set bit | P1 and P2, 3619 failures |
| M7 | fenwick: a prefix sum stops one cell short | P1 and P2, 3230 failures |
| M8 | oracle: `start..end`, leaving out the last cell | P1, 5751 failures |
| M9 | fenwick: the closing point update adds instead of subtracting | P1, P2 and P4, 5492 failures |

M3 survives P3 to P5: with the events in descending order the sweep never
meets one at its own cell and returns all zeros, which reversing, splitting
and cancelling all agree with.

## Verification

All four arms print the same output as `range_addition.py` under
`karac run --interp`, `karac __mir-run` (the v2 MIR interpreter), LLJIT,
`karac build` and `KARAC_AUTO_PAR=1 karac build`.

## Benchmarks

The bench program applies 10,000 random updates to each of 50 arrays of
100,000 cells, the problem's largest, with the ★ arm. The Kāra build and the
C, Rust, Go and Python mirrors all print `checksum 945052436`.

### Apple M5 Pro, 2026-11-06

30 runs each, 5 warmups, on the Apple M5 Pro, karac `0.8.0-dev.14606+g162ee7a0e`
(g162ee7a0e, the v2/MIR backend), measured 2026-11-06, with the Kāra binary built
`KARAC_AUTO_PAR=0`. This is the kata's first measurement; Python was not run.
The last column is Kāra's mean over that row's mean.

| implementation | mean | Kāra / this |
|---|---|---|
| c `clang -O3` | 21.0 ms ± 0.2 | 1.08× |
| rust `-O` | 21.3 ms ± 0.3 | 1.07× |
| rust `-O -C overflow-checks=on` (equal-safety) | 22.6 ms ± 0.2 | 1.01× |
| **kāra `karac build`, seq** | **22.7 ms ± 0.5** | **—** |
| go `go build` | 33.3 ms ± 0.7 | 0.68× |

Kāra is 1.07× `rustc -O`, 1.01× equal-safety Rust, 1.08× C and 0.68× Go.
The gaps were not investigated on this host.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 45.7 ms ± 1.3 | 32.8 KiB | 2.8 MiB |
| rust | 91.3 ms ± 1.9 | 455.6 KiB | 2.8 MiB |
| kāra | 113.1 ms ± 2.5 | 67.0 KiB | 2.8 MiB |
| go | — | 2450.5 KiB | 9.9 MiB |

`karac build` is 2.5× clang's cold compile and 1.2× rustc's. Kāra's
68,560-byte binary is 2.0× clang's and 6.8× smaller than rustc's. Raw numbers are in
[`bench/results.json`](bench/results.json). The sink matches across the Kāra,
Rust, C and Go builds (`checksum 945052436`).

## Compiler findings

None.
