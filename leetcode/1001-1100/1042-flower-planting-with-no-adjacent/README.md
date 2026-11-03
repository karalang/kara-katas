# 1042. Flower Planting With No Adjacent

You have `n` gardens, labeled from `1` to `n`, and an array `paths`
where `paths[i] = [xi, yi]` describes a bidirectional path between
garden `xi` and garden `yi`. In each garden, you want to plant one of
four types of flowers.

All gardens have **at most 3** paths coming into or leaving it.

Your task is to choose a flower type for each garden such that, for any
two gardens connected by a path, they have different types of flowers.

Return **any** such choice as an array `answer`, where `answer[i]` is
the type of flower planted in the `(i+1)th` garden. The flower types
are denoted `1`, `2`, `3`, or `4`. It is guaranteed an answer exists.

```
n = 3, paths = [[1,2],[2,3],[3,1]]                     ->  [1,2,3]
n = 4, paths = [[1,2],[3,4]]                           ->  [1,2,1,2]
n = 4, paths = [[1,2],[2,3],[3,4],[4,1],[1,3],[2,4]]   ->  [1,2,3,4]
```

**Constraints:** `1 <= n <= 10^4`; `0 <= paths.length <= 2 * 10^4`;
`paths[i].length == 2`; `1 <= xi, yi <= n`; `xi != yi`; every garden
has at most 3 paths coming into or leaving it.

## Approaches

Any valid answer is accepted, so every arm here gives the same one: the
smallest in dictionary order. A garden has at most three neighbors, so
they take at most three of the four types and one is always free.
Planting the gardens in order, each with the smallest type its planted
neighbors have not taken, never gets stuck, and each type it picks is
the smallest the garden can have: every smaller one is taken by a
neighbor planted before it.

| file | mechanism |
|---|---|
| `garden_no_adj.kara` ★ | the greedy: each garden's neighbors in a `Vec[Vec[i64]]`, the types they took in a `[bool; 5]`, the first free one found by a `while` loop. O(n + paths) |
| `garden_no_adj_mask.kara` | the taken types as the bits of one integer, bit 0 for an unplanted neighbor; the free type is the trailing zeros of the complement. O(n + paths) |
| `garden_no_adj_sorted.kara` | no neighbor lists: each path written as (later, earlier), the paths sorted, and one sweep over the gardens reading the paths that end at each one. O(n + paths log paths) |
| `garden_no_adj_slots.kara` | the problem's bound in the type: a `Garden` struct holds its paths in an `Array[i64, 3]` and finds its own free type through a `ref self` method. O(n + paths) |
| `garden_no_adj_iter.kara` | one line a garden: `(1..5).find(..)` over the types, `all(..)` over the neighbors. O(n + paths) |
| `differential.kara` | the five arms against counting through every planting, five properties |

Every arm prints the same 18 lines: the answers for ten gardens,
LeetCode's three examples among them, with one plot alone, a star, a
path written backwards, two triangles and a spare plot, a cube, the
Petersen graph and two plots each joined to the same three others; for every garden
of 1 to 6 plots with at most three paths at each plot, the number of
them, how many need all four types and a checksum of the answers; the
same for 300 random gardens of 1 to 50 plots; and one of 10000 plots,
with how many plots take each type. `garden_no_adj.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: it counts through every planting in dictionary order,
`1` to `4` at each garden with the first garden the most significant,
and stops at the first under which the two ends of every path differ.
That needs no reasoning about the greedy, and it is the smallest valid
answer by construction. It checks 3143 gardens: every garden of 1 to 5
plots with at most three paths at each plot (843), 2000 random ones of
2 to 8 plots and 300 of 9 to 60. The 2843 of at most 8 plots are
counted through.

| | property |
|---|---|
| P1 | the answer is the first valid planting counted through, on at most 8 plots |
| P2 | the answer is valid: every type is 1 to 4 and the two ends of every path differ |
| P3 | every type smaller than a garden's is taken by a neighbor with a smaller number, so no garden could take a smaller one |
| P4 | the paths in another order, each written either way round, change nothing |
| P5 | the first `k` gardens alone, with only the paths among them, give the first `k` types of the answer |
| P6 | each arm agrees with at least two of the other four |

The differential prints `3143 gardens (2843 counted through): checksum
533566591, 92790 checks over 5 arms: 0 failures` under `karac
__mir-run` (9 s), `karac __mir-llvm-run` and `karac __mir-llvm-asan`
with no error, and the same line under `karac run` and from a `karac
build` binary. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with a 120 s limit.
Fifteen are kept, three to each arm. All fifteen are killed, each fails
the same way under both backends, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each path recorded at one end only | P1 2038, P2 2318, P4 2232, P6 2318 |
| M2 | ★: the neighbors' types never marked taken | P1 2535, P2 2830, P6 2830 |
| M3 | ★: every type shifted one along, `flower % 4 + 1` | P1 2843, P2 2830, P3 3143, P6 3143 |
| M4 | mask: bit 0 not set for an unplanted neighbor | P1 2843, P2 3143, P5 1878, P6 3143 |
| M5 | mask: the count of taken bits for the free one | P1 889, P2 1083, P3 1132, P6 1132 |
| M6 | mask: `^=` for `\|=` | P1 2414, P2 2709, P5 1738, P6 2709 |
| M7 | sorted: the paths not sorted | P1 1302, P2 1581, P4 1664, P5 521, P6 1581 |
| M8 | sorted: the last garden removed instead of the padding | P1 2843, P2 3143, P3 1773, P6 3143 |
| M9 | sorted: the last garden left unplanted | P1 2843, P2 3143, P5 2466, P6 3143 |
| M10 | slots: the first slot ignored | P1 2233, P2 2525, P4 1202, P5 285, P6 2525 |
| M11 | slots: all three slots read, empty ones as garden 1 | P1 2465, P3 2765, P5 337, P6 2765 |
| M12 | slots: the gardens planted last to first | P1 2371, P3 2666, P5 1778, P6 2666 |
| M13 | iter: three types, falling back to 1 | P1 39, P2 77, P6 77 |
| M14 | iter: the largest free type | P1 2843, P3 3143, P6 3143 |
| M15 | iter: the last garden left unplanted when `n` is odd | P1 1629, P2 1781, P5 1374, P6 1781 |

P1 and P6 kill all fifteen, P2 twelve, P5 eight, P3 six and P4 three.
P2 misses the three edits that still plant validly (M11, M12, M14): an
empty slot reads garden 1, so M11 only adds constraints, and the other
two are other greedies. P3 sees all three, on gardens of any size. P4
sees only the edits whose answer depends on how the paths are listed:
M1 keeps each path at the end it was written from, M7 reads the paths
in the order given, and M10 forgets whichever neighbor came first. P5
sees the edits whose answer for a garden depends on the gardens after
it: M4 and M6 read an unplanted later neighbor, M12 plants last to
first, M9 and M15 leave a last garden unplanted, and M7, M10 and M11
change with the paths that a later garden brings. M5 and M6 are bit slips: M5 counts what is taken, which
passes while the neighbors hold 1, 2 and so on in order, and M6's xor
clears a type two neighbors share. M13 shows only where a garden needs
the fourth type, 39 of the 2843 counted through.

Fifteen other edits were set aside. One is equivalent: the slots arm
returning type 4 without looking, since a garden with at most three
neighbors always finds 4 free when 1 to 3 are taken. Nine fail exactly
as a kept one does: the ★ arm planting last to first (as M12); the
mask arm reading the type for its bit (as M2) and wrapping type 4 to
0 (as M13); the sorted arm leaving each path as written (as M1),
sorting by the earlier garden or reading the garden itself for its
neighbor (both as M2); the slots arm putting every path in slot 0 (as
M2) or linking each path at one end (as M1); and the iterator arm
recording each path at one end (as M1). Five fail in ways of their
own: the ★ arm stepping once past a taken type or sending a path from
`x` back to `x`, the mask arm leaving the first garden unplanted, and
the iterator arm's `==` for `!=` and `any` for `all`, both of which
panic on an `unwrap` of `None` under both backends.

## Verification

Every arm prints the same output as `garden_no_adj.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with
no error. `karac run` and a `karac build` binary print the same output
for every arm and the differential. `karac check --output=json` reports
nothing on any file. The runs used a release build of kara
`27f59a0e9c`, and were repeated on `ea418f4a5e`, which has the fix
below (it landed at `25a40f3d26`). Under `karac __mir-run` the arms take 1.4 s (★, mask,
sorted) to 1.8 s (slots) and 3.2 s (iter).

The arms went through the Mend loop clean but for one `!` for `not`,
which `karac fix` rewrote. Probing the Rust-shaped ways to write the
problem turned up one gap, fixed in kara (B-2026-11-03-27):
`for &(x, y) in paths.iter()`, `.filter(|&x| ..)`, `f(&v)` and
`let r = &v;` each drew only "Expected pattern (or parameter pattern,
or expression), found `&`", with no fix, and in the `for` the failure
cascaded into a second error about statements outside `main`. Each is
now one diagnostic with a machine-applicable fix: a pattern and an
argument drop the `&` (an argument's `&mut x` becomes the call-site
marker `mut x`), and a borrow becomes `ref v` or `mut ref v`.

## Benchmarks

The bench builds 10 random gardens of 10000 plots (the problem's most)
once in all five languages, each from 40000 tries at a path, which
gives 13000 to 13500 paths a garden. Then it plants every garden 100
times with the ★ arm, adding up the types of each answer and folding
each sum into a checksum. Every implementation prints `10 gardens of
10000 plots, 100 rounds: types sum to 18162300, checksum 639009401`.
Doubling the rounds doubles C's time (1.42 to 1.47 s against 0.70 s),
so no compiler hoists the planting out of the round loop. Each
implementation keeps the ★ arm's neighbor lists, one growable array a
garden, built afresh on every call: `Vec[Vec[i64]]` in Kāra,
`Vec<Vec<i64>>` in Rust, a slice of slices in Go and a `realloc`ed
array a garden in C. Building those lists is most of the work.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.685 to 0.746 s | 0.704 s |
| Rust (`rustc -O`) | 0.749 to 0.842 s | 0.784 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.772 to 0.838 s | 0.791 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.779 to 0.862 s | 0.801 s |
| Kāra (`karac build`) | 0.785 to 0.854 s | 0.821 s |
| Go | 1.757 to 1.954 s | 1.880 s |
| Python | 8 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(0.84 s real, 0.83 s user on one run) and runs as fast as the
sequential one.

Kāra took 1.01 times Rust's median time under overflow checks. Go
spends the difference, by inference rather than profiling, on
allocating and collecting the 100000 small neighbor slices a round.
