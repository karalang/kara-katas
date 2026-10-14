# 605. Can Place Flowers

A flowerbed is a row of plots, `1` for a plot with a flower and `0` for
an empty one, and no two flowers may stand in plots side by side. Given
the flowerbed and an integer `n`, return whether `n` new flowers can be
planted in it without breaking that rule.

```
flowerbed = [1, 0, 0, 0, 1], n = 1  ->  true
flowerbed = [1, 0, 0, 0, 1], n = 2  ->  false
```

**Constraints:** the flowerbed has 1 to 2 * 10^4 plots, each `0` or
`1`, with no two flowers side by side; `0 <= n <=` the number of plots.

## Approaches

Every arm is `fn can_place_flowers(flowerbed: Vec[i64], n: i64) ->
bool`.

| file | mechanism |
|---|---|
| `can_place_flowers.kara` ★ | from the left, a new flower in every empty plot whose neighbours are empty, an edge counting as empty, written into a copy of the bed so the next plot sees it; planting as early as possible never costs a later plot, so the count is the most that fit; O(n) |
| `can_place_flowers_gaps.kara` | a stretch of z empty plots between two flowers takes (z - 1) / 2 new ones, and a stretch at an edge is counted as if one more empty plot lay beyond the edge; O(n) |
| `can_place_flowers_dp.kara` | the most new flowers so far with the last plot empty and with it holding a flower; an old flower must follow an empty plot, and an empty plot stays empty or takes a new flower after an empty one; O(n) |
| `can_place_flowers_skip.kara` | a walk that steps two past a flower, plants in an empty plot whose right neighbour is empty and steps two, and otherwise steps three, stopping as soon as `n` are planted; O(n) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 13 lines: the two examples above; nine more
(one plot, empty or not, and with `n = 0`; two and three empty plots;
empty stretches at the edges; a stretch of four between flowers; flowers
every other plot, with `n` of 1 and of 0); 20,000 empty plots, the
problem's largest, with `n` of 10,000 and 10,001; and a total and
checksum of the largest `n` each of 300 random beds of 1 to 40 plots
takes, found by asking for `n + 1` until the answer is `false`.
`can_place_flowers.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: every set of plots tried, by the bits of a
mask, counting when each plot in it is empty and no two flowers, old or
new, stand side by side; the bed takes `n` when some such set has `n`
plots. Each of 1,000 random cases is a bed of 1 to 12 plots, flowers
never side by side, with a second bed of 1 to 6; 186 of them take no new
flower at all.

| | property |
|---|---|
| P1 | for every `n` from 0 to two past the bed's size, the answer is the definition's |
| P2 | a bed that takes `n` takes `n - 1` |
| P3 | the bed read backwards takes the same largest `n` |
| P4 | an empty plot, a flower and an empty plot between the two beds keep them apart, so the joined bed takes the sum of their largest `n` |
| P5 | a new flower in a plot that could take one leaves one or two fewer, since only it and its two neighbours change |

It prints `1000 cases (186 taking no more), 4 arms, 20000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a new flower not written into the copy | P1 554, P5 146 |
| M2 | ★: the last plot never planted | P1 328, P3 316, P4 328, P5 166 |
| M3 | gaps: a stretch between flowers counted as one at an edge | P1 467, P3 401, P4 422, P5 126 |
| M4 | gaps: the left edge not counted as empty | P1 290, P3 316, P4 302, P5 146 |
| M5 | dp: a new flower allowed after a new one | P1 554, P5 161 |
| M6 | dp: an old flower allowed after a new one | P1 467, P3 401, P4 422, P5 115 |
| M7 | skip: two plots stepped before a flower, not three | P1 249, P4 258 |
| M8 | skip: one plot stepped after a flower, not two | P1 285, P3 317, P4 294, P5 221 |
| E1 | gaps: a stretch of none clamped to zero | 0 |
| E2 | ★: the right neighbour read from the original | 0 |
| E3 | dp: the impossible case held as -7 | 0 |
| E4 | skip: stopping only once more than `n` are planted | 0 |

Two pairs of mutants make the same mistake in different arms. M1 and
M5 let new flowers stand side by side, so both count every empty plot
with no old flower beside it; M3 and M6 let a new flower stand just left
of an old one. Each pair fails the same number of cases under P1, P3 and
P4, and differs under P5 only because P5 picks its plot afresh for each
arm. M1 and M5's count reads the same backwards and adds up across the
joint of P4, so only P1 sees them on most cases, and P5 when both
neighbours of the new flower could have taken one too, so that the count
falls by three. P2 kills nothing: every arm compares a count with `n`,
the skip arm's early stop included, so no arm can take `n` and refuse a
smaller number. E1 is safe because `(zeros - 1) / 2` is -1 / 2 only for
a stretch of none, which truncates to 0; E2 because the walk writes only
the plot it stands on, so the one to its right still holds what the
original holds; E3 because the counts that can happen are never
negative; and E4 because the walk ends with the same `planted >= n`
test.

## Verification

Every arm prints the same output as `can_place_flowers.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes every arm, the differential and the bench program. All at kara
`929c8e578f`.

The frozen legacy backends agree on the arms: every arm prints the same
output under `karac run --interp`, `karac run` and `karac build`, and
under `KARAC_AUTO_PAR=1 karac build`, though `karac build` warns that
the harness moves `empty` and uses it again, where v2 borrows it. The
differential is refused at type checking by `karac run --interp` and
`karac build`: legacy types the elements of `other.iter()` as `i64`, so
the `*plot` that reads one is an error. The bench program is refused by
`karac build`, which reads passing `beds[..]` to the borrowing parameter
as a move out of an index (E_INDEX_MOVE_NON_COPY). Legacy is frozen, so
these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 100 beds of 20,000 plots, the
problem's largest, each with flowers about one plot in 2 to 6, never
side by side, once, and then 50 times over asks of each whether it takes
an `n` from 0 to 7,999. Every implementation prints `100 beds,
50 rounds: 2959 fit, checksum 576262675`, the Kāra program under `karac
__mir-run` included (43 s).

Each implementation copies the bed on every call, as the ★ arm clones
it: a `Vec` in Rust, a slice in Go, a list in Python, and in C a
`malloc`'d buffer. Spot timings on a shared 4-core container, three runs
each (two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.41 to 0.46 s |
| Rust (`rustc -O`) | 0.42 to 0.47 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.41 to 0.48 s |
| Go | 0.53 to 0.55 s |
| Python | 8.50 to 8.64 s |
| Kāra (`karac build --mir`) | 0.42 to 0.52 s |

So `bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. A copy outside this directory that passes
`beds[..].clone()` instead, which legacy builds, runs in 0.40 to 0.52 s
under the legacy `karac build` and 0.50 to 0.57 s under `karac build
--mir`, three runs each; the ranges overlap. Under `karac
__mir-llvm-run` the program prints the same line in 1.96 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

The Kāra row is level with Rust's and C's, and Go's is a little slower.
Every call copies 20,000 eight-byte plots and walks them once, which C,
Rust and Kāra all do in about the same time; that the copy and the walk
over memory decide it is a reading of the programs, not profiled.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
