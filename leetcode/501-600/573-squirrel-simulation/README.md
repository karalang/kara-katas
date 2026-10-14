# 573. Squirrel Simulation

You are given two integers `height` and `width` representing a garden of
size `height x width`. You are also given: an array `tree` where `tree =
[treer, treec]` is the position of the tree in the garden, an array
`squirrel` where `squirrel = [squirrelr, squirrelc]` is the position of
the squirrel in the garden, and an array `nuts` where `nuts[i] = [nutir,
nutic]` is the position of the i-th nut in the garden. The squirrel can
only take at most one nut at one time and can move in four directions:
up, down, left, and right, to the adjacent cell. Return the minimal
distance for the squirrel to collect all the nuts and put them under the
tree one by one. The distance is the number of moves.

```
height = 5, width = 7, tree = [2,2], squirrel = [4,4], nuts = [[3,0],[2,5]]  ->  12
height = 1, width = 3, tree = [0,1], squirrel = [0,0], nuts = [[0,2]]        ->  3
```

**Constraints:** `1 <= height, width <= 100`; `tree.length ==
2`; `squirrel.length == 2`; `1 <= nuts.length <= 5000`; `nuts[i].length
== 2`; `0 <= treer, squirrelr, nutir <= height`; `0 <= treec, squirrelc,
nutic <= width`.

## Approaches

Every arm is `fn min_distance(height: i64, width: i64, tree: Vec[i64],
squirrel: Vec[i64], nuts: Vec[Vec[i64]]) -> i64`. Every nut but the
first costs a round trip from the tree, so only the first nut is a
choice; the distances are Manhattan, since nothing in the garden blocks
the way.

| file | mechanism |
|---|---|
| `min_distance.kara` ★ | one pass: twice each nut's distance to the tree, less the largest saving from starting at a nut, its distance to the tree minus its distance to the squirrel; O(nuts) |
| `min_distance_first.kara` | each nut tried as the first and the whole walk added up again from scratch; O(nuts^2) |
| `min_distance_chain.kara` | the distance as a local closure, `far`, and the round trips and the best saving each one iterator chain, `map` then `sum` and `map` then `max` |
| `min_distance_sorted.kara` | each nut paired with what it costs extra as the first, the pairs sorted, the cheapest first and the rest round trips |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 11 lines: eight gardens at the edges (the two
examples, the squirrel on a nut, the squirrel at the tree, a nut at the
tree, a nut beyond the squirrel that beats the nearest nut, a tree
between the squirrel and the nuts so that every first nut is as good,
and one cell), a total and checksum over 300 random gardens of 1 to
10 by 1 to 10 with 1 to 8 nuts, and the problem's largest, 5,000 nuts on
100 by 100 at random, then all in the corner farthest from the tree.
`min_distance.py` mirrors the ★ arm and its output is byte-identical.

The chain arm does not build today; see Compiler findings. It is kept as
written. A copy outside this directory with `far` made a function, `fn
distance(a: Vec[i64], b: Vec[i64]) -> i64`, the only change, prints the
same output.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: every order of collecting the nuts tried,
the squirrel starting where it is and each later trip leaving from the
tree, and each leg's steps counted by walking the grid breadth first.
Each arm is held to the properties below on 1,000 random gardens of 1 to
6 by 1 to 6 with 1 to 5 nuts anywhere.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | at least the round trips less the longest distance from the tree to a nut, at most the round trips plus the squirrel's distance to the tree |
| P3 | turning the garden on its side changes nothing |
| P4 | the nuts in the other order change nothing |
| P5 | one more nut at the tree changes nothing |

Since the chain arm does not build, the differential does not either:
`karac check` and the MIR backends stop at its copy of that arm. The
copy outside this directory with the workaround in that place prints
`1000 cases, 4 arms, 20000 checks, 0 failures` under `karac __mir-run`
and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the workaround copy of the differential, two to each arm
that change its answers and one to each that does not, each run under
`karac __mir-llvm-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the saving taken the wrong way round | P1 500, P2 106, P5 363 |
| M2 | ★: diagonal steps allowed | P1 592, P2 329 |
| M3 | first: the other nuts fetched one way only | P1 737, P2 584, P5 185 |
| M4 | first: the nuts before the first left out | P1 711, P2 666, P4 473, P5 583 |
| M5 | chain: the smallest saving taken | P1 532, P5 363 |
| M6 | chain: round trips measured from the squirrel | P1 700, P2 553, P5 828 |
| M7 | sorted: the pairs reversed, not sorted | P1 316, P4 388, P5 547 |
| M8 | sorted: the first nut's round trip added as well | P1 914, P2 564, P4 263 |
| E1 | ★: the best saving started at -1000000 | 0 |
| E2 | first: the best walk started at 10^9 | 0 |
| E3 | chain: the subtraction written the other way round | 0 |
| E4 | sorted: sorted by the extra cost alone | 0 |

P3 sees none of the mutants: every one, M2's diagonal steps included,
treats rows and columns alike, so turning the garden changes no answer,
right or wrong. P4 sees the two mutants whose answer depends on where a
nut sits in the list: M4 leaves out the nuts before the first, and
M7 takes whichever nut ends up first after reversing. P5's nut at the
tree is never the best first one and costs nothing to fetch, so it
catches a mutant that would choose it, M1 and M5 by taking the worst
saving, or that counts it wrongly. E1 and E2 are safe because no saving
here is below -20 and no walk above 10^9, and E4 because a tie in the
extra cost gives the same walk whichever nut goes first.

## Verification

The ★, first and sorted arms print the same output as `min_distance.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak. `karac check` passes on those three and the bench program; it
refuses the chain arm and the differential, and so do both MIR backends
(B-2026-10-14-23). The workaround copy of the chain arm prints the same
output under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

The frozen legacy backends: `karac run --interp` runs the ★ arm, but the
two lines from random gardens come out different, and the other nine
match; the cause is not measured. `karac run` and `karac build` fail on
the ★ arm in code generation, at the harness's calls to `show`, whose
first argument is a string literal for a `Str` parameter ("Call
parameter type does not match function signature"). The first and sorted
arms, the differential and the bench program stop at type checking: each
reads a nut as `nuts[i]`, and legacy takes that as a move out of the
index (E_INDEX_MOVE_NON_COPY) where v2 borrows it. The chain arm stops
at its closure, as on every backend. Legacy is frozen, so these are
noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 cases once on a 100 by
100 garden, each with a tree, a squirrel and 5,000 nuts (the problem's
most) at random; then 2,000 times over every case is answered. Every
implementation prints `20 cases of 5000 nuts, 2000 rounds:
26301176000 steps, checksum 597283043`, the Kāra program under `karac
__mir-run` included (718 s).

Every implementation keeps each nut as its own pair, as LeetCode gives
them and the Kāra arm takes them: a `Vec<i64>` in Rust, a slice in Go, a
`malloc`'d pair in C and a list in Python. Spot timings on a shared
4-core container, three runs each (two for Python; `bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.40 to 0.55 s |
| Rust (`rustc -O`) | 0.53 to 0.55 s |
| Rust (`rustc -O -C overflow-checks=on`) | 3.14 to 3.42 s |
| Go | 0.63 to 0.87 s |
| Python | 68.6 s |
| Kāra (`karac build --mir`) | 1.48 to 1.67 s |

The legacy `karac build` refuses this program, since it moves `trees[p]`
out of the index where v2 borrows it. So `bench.sh` builds the Kāra
program with `karac build --mir`, the v2 compiled backend; that edit is
by hand, on top of the `scripts/new-bench.sh` output. The `--mir` row is
timed at kara `680733538b`. Under `karac __mir-llvm-run` the program
prints the same line in 5.5 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

The Kāra row is about three times Rust's and C's, and about half of
Rust's with overflow checks on. Where the gap to `rustc -O` comes from
is not measured; the bench does little but add, subtract and take
absolute values, so the overflow checks are the first suspect, as they
were on kata 567, but that is not measured here.

## Compiler findings

One filed: **B-2026-10-14-23**. A closure that passes a captured binding
that is not `Copy` to a closure-valued local's `ref` parameter is judged
once-callable, so the chain arm's `nuts.iter().map(|n| far(n,
tree)).sum()`, with `let far = |a: ref Vec[i64], b: ref Vec[i64]| ...`,
is refused by `karac check` and both MIR backends ("cannot pass
once-callable closure ... because it consumes captured binding 'tree'").
`far` borrows `tree`, so nothing is consumed. The arm keeps its closure;
the copy outside this directory makes `far` a function, which builds and
prints the same output. The legacy failures above are not filed because
legacy is frozen.
