# 1168. Optimize Water Distribution in a Village

There are `n` houses in a village. We want to supply water for all the
houses by building wells and laying pipes.

For each house `i`, we can either build a well inside it directly with
cost `wells[i - 1]` (note the `-1` due to 0-indexing), or pipe in water
from another well to it. The costs to lay pipes between houses are given
by the array `pipes` where each `pipes[j] = [house1j, house2j, costj]`
represents the cost to connect `house1j` and `house2j` together using a
pipe. Connections are bidirectional, and there could be multiple valid
connections between the same two houses with different costs.

Return the minimum total cost to supply water to all houses.

```
n = 3, wells = [1,2,2], pipes = [[1,2,1],[2,3,1]]   ->  3
n = 2, wells = [1,1],   pipes = [[1,2,1],[1,2,2]]   ->  2
n = 2, wells = [1,1],   pipes = [[1,2,1]]           ->  2
```

**Constraints:** `2 <= n <= 10^4`; `wells.length == n`; `0 <= wells[i] <=
10^5`; `1 <= pipes.length <= 10^4`; `pipes[j].length == 3`; `1 <= house1j,
house2j <= n`; `0 <= costj <= 10^5`; `house1j != house2j`.

The arms are `fn min_cost_to_supply_water(n: i64, wells: Vec[i64], pipes:
Vec[Vec[i64]]) -> i64`.

## Approaches

A well is a pipe from a source, a house 0 that has water, to its house, so
the cheapest supply is a minimum spanning tree over houses 0 to `n`; the
arms differ in how the tree is found.

| file | mechanism |
|---|---|
| `water_distribution.kara` ★ | Kruskal: every well and pipe sorted by cost as a `(cost, a, b)` tuple, each joined in turn unless its ends are already joined, the joins kept in a union-find by size with path halving. O((n + m) log(n + m)) |
| `water_distribution_prim.kara` | Prim: the tree grown from the source, a `PriorityQueue` of `(cost, house)` pairs holding every pipe that leaves it; a popped pipe to a house already in the tree is skipped. O((n + m) log(n + m)) |
| `water_distribution_boruvka.kara` | Borůvka: each round every group of joined houses takes its cheapest pipe out, ties broken by the pipe's place in the list, until one group is left; each round at least halves the groups. O((n + m) log n) |
| `water_distribution_folded.kara` | the wells folded into the groups, with no source: every house starts as a group that digs its own well, and a pipe, taken in order of cost, is laid when it costs less than the dearer of the two groups' cheapest wells, the joined group keeping the cheaper. O(n + m log m) |
| `water_distribution_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `i32` costs, `usize` houses, Kruskal over a `Vec<(i32, usize, usize)>` sorted with `sort_unstable`, a recursive `find(&mut Vec<usize>, usize)` nested in the method), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's examples (3, 2, 2); every
well cheaper than any pipe (15); one cheap well and a cheap ring of pipes
(6); a free well and a free pipe (3); two villages apart, each with its
own well (23). Then 300 random villages of 2 to 30 houses and 1 to 2n
pipes, half with costs of 0 to 10 so that costs tie (`300 random
villages: total 25282993, checksum 456866380`), and two of 10^4 houses
and 10^4 pipes, the constraints' most: random (103137658) and a ring of
pipes cheaper than every well (109998). `water_distribution.py` mirrors
the ★ arm and its output is byte-identical; with `lit` it reads the
statement literally for the villages of up to 5 houses and 6 pipes,
trying every set of wells and pipes, and gives the same output.

The Mend loop: every arm takes one fix in its harness, `let mut pipes =
[]` to `Vec.new()`, since a `let` without a type gives an empty literal
nothing to take its element type from. The ★ arm also takes `(ra, rb) =
(rb, ra)` to `ra, rb = rb, ra`, a parenthesized tuple being a value and
not a place, and the Prim arm `!` to `not`. The Rust arm takes four
rounds (30, 2, 1 and 14 edits): the generics to brackets, `::` to `.`,
`&mut` to `mut ref` and `&pipes` to `ref pipes`, and the `&` of the
closure and loop patterns dropped; then the nested `fn find` moved out
of the method; then `struct Solution {}`; then `usize` to `i64` in every
type and cast, since Kāra writes indices as `i64`, the `mut` marker on
the recursive call's argument, `sort_unstable` to `sort`, `ans`
annotated `i32`, and the adapter's `as i64` dropped as a widening Kāra
does by itself. Its output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every set of wells to dig and every set of pipes to lay tried,
and the cheapest that brings water to every house, from a well in it or
through laid pipes from one, kept. It checks 1200 villages in four kinds
of 300: 2 to 4 houses and 1 to 5 pipes costing 0 to 5, so that costs
tie; 2 to 5 houses and 1 to 6 pipes costing 0 to 10^5; 6 to 30 houses
and 1 to 3n pipes costing 0 to 10; and 6 to 60 houses and 1 to 3n pipes
costing 0 to 10^5. Every random choice the properties make is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the cost is the literal one, for the villages of up to 5 houses and 6 pipes |
| P2 | every well and pipe k times as dear costs k times as much |
| P3 | the pipes in another order, some with their ends swapped, cost the same |
| P4 | the houses renamed, their wells and pipes with them, cost the same |
| P5 | a dearer copy of every pipe beside it changes nothing |
| P6 | no way of supplying costs less: neither every well dug nor a drawn mix, the houses taken in a drawn order, each laying a drawn pipe to a house already supplied or digging its well |

All 33,000 checks pass on every arm: `1200 villages: checksum 140849934,
33000 checks over 5 arms: 0 failures`, in 11 s under `karac __mir-run`.
A Python reading of the same draws, with the mirror against the literal
reading, gives the same checksum.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`,
each failing the same way under both. All fifteen are caught.

| # | mutation | failures by property |
|---|---|---|
| K1 | ★: a pipe laid between houses already joined | P1 229, P5 514 |
| K2 | ★: the pipes left unsorted | P1 509, P6 496 |
| K3 | ★: one pipe or well short | P1 574 |
| P1 | prim: a house reached twice counted twice | P1 154, P4 68, P5 475 |
| P2 | prim: every pipe one way only | P1 288, P3 868, P4 97, P5 569, P6 95 |
| P3 | prim: the dearest pipe out taken first | P1 598, P5 1188, P6 1155 |
| B1 | boruvka: each group's dearest pipe out taken | P1 598, P5 1188, P6 1155 |
| B2 | boruvka: every well one dearer | P1 600, P2 1200, P6 215 |
| B3 | boruvka: each join counted as two | P1 119, P3 46, P4 14 |
| F1 | folded: a pipe laid only when cheaper than the cheaper well | P1 281, P6 57 |
| F2 | folded: the joined group keeping the dearer well | P1 162, P3 150, P5 40, P6 255 |
| F3 | folded: the pipes left unsorted | P1 136, P3 590, P6 16 |
| X1 | solution: a laid pipe never joins its ends | P1 600, P5 1200, P6 1189 |
| X2 | solution: each well put in the house before | P1 411, P4 930, P6 161 |
| X3 | solution: the dearest pipes first | P1 598, P5 1188, P6 1155 |

P1 catches all fifteen, P6 eleven, P5 eight, P3 and P4 four each, and P2
one. K3, which stops one join short, is seen by P1 alone: the answer it
gives is short by the dearest join every time, which every other
property reproduces. P2 sees only B2, the one edit that adds a fixed
amount, which does not scale with the costs. P5 sees, among others, the
edits that pay for a pipe they should skip (K1, P1, X1), since each
dearer copy is one more such pipe. The three edits that build the
largest tree instead (P3, B1, X3) fail alike, on the same villages.

## Benchmarks

`bench/` times the ★ arm against Kruskal in C (edges sorted with
`qsort`), Rust (a `Vec` of tuples, `sort`), Go (`sort.Slice`) and Python
(`sort`), each with the same union-find. 16 villages of 10^4 houses and
10^4 pipes, the constraints' most, are built once; each of 40 rounds
gives one pipe of every village a new cost and supplies the village.
Every program prints `40 rounds over 16 villages of 10^4 houses: total
65717795495, checksum 75303402`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `1bdebaaa70`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.623 to 0.719 s | 0.657 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.631 to 0.693 s | 0.658 s |
| Rust (`rustc -O`) | 0.561 to 0.806 s | 0.597 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.570 to 0.670 s | 0.604 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.555 to 0.646 s | 0.582 s |
| C (`clang -O3 -march=x86-64-v3`) | 1.674 to 1.828 s | 1.706 s |
| C (`clang -O3`) | 1.667 to 1.877 s | 1.732 s |
| Go | 2.225 to 2.584 s | 2.311 s |
| Python | 7.8 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; a plain `karac build` gives the same binary, so the
two Kāra rows are one program timed twice. Kāra takes about 1.09x
overflow-checked Rust's time, the equal-safety comparison. C takes about
2.6x Kāra's and Go about 3.5x: each supply sorts 2 x 10^4 edges, and
`qsort` and `sort.Slice` call their comparison through a pointer or a
closure for every compare, where Rust's and Kāra's sorts compare the
tuples inline. That the sort is where the gap lies is read from the
programs, not profiled. Python takes about 12x.
