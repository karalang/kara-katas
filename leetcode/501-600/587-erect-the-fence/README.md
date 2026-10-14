# 587. Erect the Fence

You are given an array `trees` where `trees[i] = [x_i, y_i]` represents
the location of a tree in the garden. Fence the entire garden using the
minimum length of rope, as it is expensive. The garden is well-fenced
only if all the trees are enclosed. Return the coordinates of trees that
are exactly located on the fence perimeter. You may return the answer in
any order.

```
trees = [[1,1],[2,2],[2,0],[2,4],[3,3],[4,2]]  ->  [[1,1],[2,0],[4,2],[3,3],[2,4]]
trees = [[1,2],[2,2],[4,2]]                    ->  [[4,2],[2,2],[1,2]]
```

**Constraints:** `1 <= trees.length <= 3000`; `trees[i].length ==
2`; `0 <= x_i, y_i <= 100`; all the given positions are unique.

## Approaches

Every arm is `fn outer_trees(trees: Vec[(i64, i64)]) ->
Vec[(i64, i64)]`, a tree being its two coordinates. The answer may come
in any order, so the harness sorts it before printing.

| file | mechanism |
|---|---|
| `outer_trees.kara` ★ | the monotone chain: the trees sorted, swept left to right for the lower side and back for the upper, a tree dropped when keeping it would make a clockwise turn, trees in a line kept; then the two sides' trees sorted with repeats removed; O(n log n) |
| `outer_trees_wrap.kara` | gift wrapping: from the leftmost tree, the rope goes each time to the tree that leaves all others on one side, the farthest of them on a tie, and every tree on that stretch is marked; O(n * c), c the corners |
| `outer_trees_graham.kara` | the Graham scan: the trees sorted by angle around the lowest with `sort_by`, the last angle's trees turned round, and a stack that drops clockwise turns; O(n log n) |
| `outer_trees_corners.kara` | the monotone chain keeping only the corners, then every tree tested against each side between two corners; O(n log n + n * c) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 16 lines: nine gardens at the edges (the two
examples, one tree, two, trees in an upright and in a slanting line, a
3 by 3 square, a triangle with trees along its sides and one inside, and
one tree well inside three), a count and checksum over 300 random
gardens of 1 to 30 trees on an 11 by 11 grid, and the problem's largest:
3,000 trees at random on the 101 by 101 grid, all 3,000 of a 50 by
60 grid, and the 2,965 inside a diamond, whose fence is the 152 trees on
its edge. `outer_trees.py` mirrors the ★ arm and its output is
byte-identical.

The gift wrap's tie rule, the farthest of several trees in a line, is
what keeps it from looping. Its first version kept whichever of them it
found first, and on a garden with a straight side it could step
backwards along that side and never come back to its start; the
differential's first run hung on such a garden, and the rule was added
before anything else was measured.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: a straight stretch of rope runs between
two trees when no tree is on each side of the line through them, and
every tree lying on such a stretch is on the fence; a single tree is its
own fence. Each arm's answer, sorted, is held to the properties below on
1,000 random gardens of 1 to 12 trees on grids of 3 by 3 to 6 by
6, small enough that many trees fall in a line.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | no tree twice, only trees of the garden, and the first and last tree in sorted order on the fence |
| P3 | the trees in reverse order give the same answer |
| P4 | the garden turned a quarter round gives the answer turned |
| P5 | fencing the answer again gives the answer |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac
__mir-llvm-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: trees in a line dropped from the lower side | P1 344, P4 354 |
| M2 | ★: the trees on both sides not kept once | P1 1000, P2 1000, P4 769, P5 1000 |
| M3 | wrap: every tree beside a stretch and within its span counted | P1 420 |
| M4 | wrap: four trees all taken as the fence | P1 10 |
| M5 | graham: the last angle's trees not turned round | P1 189, P4 274 |
| M6 | graham: trees in a line dropped | P1 444, P4 274 |
| M7 | corners: the side back to the first corner not tested | P1 237, P4 334 |
| M8 | corners: a tree on the inner side of a side counted | P1 420 |
| E1 | ★: the turn measured from the newest tree | 0 |
| E2 | wrap: the rope started at the rightmost tree | 0 |
| E3 | graham: the pivot the rightmost of the lowest | 0 |
| E4 | corners: a side's ends not tested, only its line | 0 |

M3 and M8 make the same mistake in two arms, counting a tree that is on
the inner side of a stretch and within the box it spans, and give the
same answers; P5 does not see them, since fencing their answer again
counts the same trees again. M1, M5, M6 and M7 lose trees from one part
of the fence, the lower side, the side the scan closes on, or the
closing side, and turning the garden a quarter round moves that part, so
P4 sees each. M2 keeps both ends of the chain twice, and every tree
twice when all are in a line, so it fails P2 on every case. M4 is killed
only by the ten gardens of four trees with one inside the other three.
P3 sees none of the mutants: every arm sorts the trees, or in the gift
wrap picks each stretch by a rule that does not depend on their order.

The four survivors are safe for reasons that have to be argued, not
tested. E1 turns the three trees round in order, which leaves the sign
of the cross product as it was. E2 starts the rope at the largest tree,
which is a corner as much as the smallest is. E3 takes the rightmost of
the lowest trees as the pivot; the trees left of it on its row then
share the last angle, and are turned round to come farthest first, as
the fence meets them. E4 tests only that a tree is on a side's line: a
tree on that line beyond a corner would be outside the fence, and every
tree is inside it. The first version of M3 dropped the gift wrap's test
that a tree lies between the stretch's ends and survived for that same
reason, so it was replaced.

## Verification

The four arms print the same output as `outer_trees.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and run
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes on every arm, the differential and the bench program.

The frozen legacy backends refuse the ★, Graham and corners arms, the
differential and the bench program under `karac run --interp`, `karac
run` and `karac build`, at type checking: each reads a tree out of
`iter()` as `*p` or `*t`, and legacy gives the element as a
`(i64, i64)` where v2 gives a reference ("unary '*' requires 'ref T' ...
found '(i64, i64)'"). The gift wrap arm reads its trees by index; `karac
run --interp` prints the same output for it, and `karac run` and `karac
build` stop it at module verification on the harness's `show` call
("Call parameter type does not match function signature"). Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 50 gardens once, each of
1,000 to 3,000 trees (the problem's most) at distinct random places on
the 101 by 101 grid; then 300 times over every garden is fenced. Every
implementation prints `50 gardens, 300 rounds: 1134900 on the fence,
checksum 5712530`, the Kāra program under `karac __mir-run` included
(272 s).

Each call copies the trees, sorts them, builds the fence in a second
array, sorts that and removes repeats, as the Kāra arm does: `to_vec`,
`sort` and `dedup` in Rust, `slices.Clone`, `slices.SortFunc` and
`slices.Compact` in Go, `sorted` and a list in Python, and `qsort` with
a comparison function in C. Spot timings on a shared 4-core container,
three runs each (two for Python; `bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 4.29 to 4.46 s |
| Rust (`rustc -O`) | 1.36 to 1.53 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.52 to 1.63 s |
| Go | 4.47 to 5.06 s |
| Python | 26.5 s |
| Kāra (`karac build --mir`) | 3.55 to 3.83 s |

The legacy `karac build` refuses this program on the same `*p`. So
`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`f6052c659c`. Under `karac __mir-llvm-run` the program prints the same
line in 14.6 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

The Kāra row is about 2.5 times Rust's and ahead of C's and Go's. C and
Go sort through a comparison function called for every pair, where
Rust's `sort` on tuples compares inline, which suggests the two sorts
are much of each call's work; how much of Kāra's time they take is not
measured.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
