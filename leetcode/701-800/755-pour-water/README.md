# 755. Pour Water

A landscape is a row of columns of ground, `heights[i]` units tall.
`volume` units of water fall one at a time onto column `k`. Each unit
first tries to move left: if, rolling left over ground that never rises,
it would end lower than it started, it does, settling at the nearest of
the lowest columns it can reach. Otherwise it tries the right the same
way, and otherwise it stays on `k`. A unit that has settled counts as
ground for the next. Return the heights of ground and water at the end.

```
heights = [2, 1, 1, 2, 1, 2, 2], volume = 4, k = 3
                                ->  [2, 2, 2, 3, 2, 2, 2]
heights = [1, 2, 3, 4], volume = 2, k = 2  ->  [2, 3, 3, 4]
heights = [3, 1, 3], volume = 5, k = 1     ->  [4, 4, 4]
```

**Constraints:** 1 to 100 columns, each 0 to 99 tall; 0 <= volume <=
2000; k is a column.

## Approaches

With at most 2,000 units and 100 columns, simulating each unit is cheap;
the arms differ in how a unit finds where it settles.

| file | mechanism |
|---|---|
| `pour_water.kara` ★ | walk left while the next column is no higher, keeping the first column lower than the best so far; settle there if it beats k, else walk right the same way; O(V x n) |
| `pour_water_recur.kara` | `roll` follows a unit by recursion and returns the lowest column it passes, the nearest among equals; left if that ends lower than k, else right, else k |
| `pour_water_iter.kara` | `take_while` and `count` measure the run over which the ground never rises, and a `fold` keeps its first lowest column |
| `pour_water_land.kara` | a `Land` struct with methods: `settle_side` returns `Option` of where a unit settles on one side, and `drop_at` adds the unit |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 11 lines: the three LeetCode examples; one
column; no water; a flat landscape; a slope down to the right with k at
the top, and its mirror; water poured on a peak between two dips; a
valley; and 200 random landscapes of up to 100 columns and 2,000 units,
with the total height at the end and a checksum. `pour_water.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which places each unit in two passes per side: first how far the unit
can roll, then the lowest height within that run and the column at that
height nearest k. 4,000 random landscapes are checked, of 1 to
25 columns no taller than 0 to 5, so that level ground, equal heights
and walls are common, with up to 39 units each (77,991 in all).

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | it has as many columns as the landscape, and its total is the landscape's plus the volume |
| P3 | pouring in two parts, a random number of units and then the rest, ends the same as pouring all at once |
| P4 | one unit fewer leaves the same heights but for one column, exactly one lower |

It prints `4000 landscapes (77991 units poured), 4 arms, 63584 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a column as low as the best so far taken, not only a lower one | P1 3066 |
| M2 | ★: no rolling across level ground | P1 3158 |
| M3 | ★: the right side tried first | P1 2188 |
| M4 | recursion: the farther of two equal columns taken | P1 2068 |
| M5 | recursion: no rolling across level ground | P1 3158 |
| M6 | recursion: the right roll taken when it ends level with k | P1 1421 |
| M7 | iterator: the run measured against k, not the previous column | P1 604 |
| M8 | iterator: the farther of two equal columns taken | P1 3066 |
| M9 | iterator: the run cut one column short of the whole width | P1 639 |
| M10 | landscape: the farther of two equal columns taken | P1 3066 |
| M11 | landscape: a drop with nowhere to go put on column 0 | P1 2897 |
| M12 | landscape: the run measured against k, not the previous column | P1 604 |
| E1 | ★: the side given up when its best is lower than k | 0 |
| E2 | recursion: the end tested as next > len - 1 | 0 |
| E3 | iterator: one more step offered to the run | 0 |

P1 kills all twelve; the other three properties kill none. They are laws
that any consistent pouring rule obeys, whichever column it picks: water
is conserved, pouring in parts is pouring at once, and each unit lands
somewhere. Every edit here changes which column a unit picks,
consistently, so only the definition sees it. E1 gives up on the left
side when its best is lower than k rather than when it moved, which is
the same, since it moves only to a lower column; E2 tests the right end
as next > len - 1; E3 offers the iterator's run one more step than the
landscape is wide, which `take_while` never takes.

## Verification

Every arm prints the same output as `pour_water.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`b84c5d937f`, whose last compiler change is `56a4cad109`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse every program here at type checking,
at a `*` over a vector's `iter()` (`*x` in the harness, the differential
and the bench), since legacy gives those by value where v2 gives
references. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. For each of
6,000 random landscapes of 100 columns, each 0 to 99 tall, it pours
2,000 units at a random column, adding up the heights at the end and a
checksum. Every implementation prints `6000 landscapes of 100 columns,
2000 drops each: 41697115 units in all, checksum 687211143`, the Kāra
program under `karac __mir-run` included (in 97 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.23 to 0.29 s |
| Rust (`rustc -O`) | 0.32 to 0.39 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.25 to 0.35 s |
| Go | 0.30 to 0.48 s |
| Python | 17.4 to 17.6 s |
| Kāra (`karac build --mir`) | 0.47 to 0.71 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 3.7 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 0.59 s,
against C's 0.25, Rust's 0.34 (0.31 under overflow checks) and Go's
0.39. The legacy backends refuse the program; a copy for legacy alone,
with `*x` written `x` in the final sum, ran 0.28 to 0.33 s, a median of
0.32 s in the interleaved runs, so v2 takes about 1.8 times legacy's
time (2.1 times in an earlier quick run, 0.60 s against 0.29 s), close
to M2's limit of twice legacy. Most of the gap is the ★ arm's `for d in
[-1, 1]`: under `karac build --mir` that literal is a new heap `Vec`
every drop, 12,042,010 allocations in all against 42,010 with
`Array[-1, 1]` (valgrind), and with `Array[-1, 1]` the same program runs
0.44 to 0.51 s, about 1.5 times legacy. That is B-2026-10-18-52, filed
from kata 752 (below). Under valgrind's cachegrind v2 runs 8.6 billion
instructions against C's 3.7 billion and Rust's 4.7 billion. The legacy
copy is a measurement only and is not in the kata, and new katas'
benches are outside M2's frozen set in any case. The comparison with C
and Rust waits until after M4.

## Compiler findings

B-2026-10-18-52 (kara ledger, open, filed from kata 752): a bare list
literal that is only walked, here `for d in [-1, 1]`, heap-allocates a
`Vec` each time under `karac build --mir`, where legacy keeps it on the
stack. It costs this bench some 12 million allocations and most of its
gap to legacy. Nothing in the kata works around it.
