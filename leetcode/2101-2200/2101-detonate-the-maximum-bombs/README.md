# 2101. Detonate the Maximum Bombs

You are given a list of bombs. The range of a bomb is defined as the
area where its effect can be felt. This area is in the shape of a circle
with the center as the location of the bomb.

The bombs are represented by a 0-indexed 2D integer array `bombs` where
`bombs[i] = [xi, yi, ri]`. `xi` and `yi` denote the X-coordinate and
Y-coordinate of the location of the `i`th bomb, whereas `ri` denotes the
radius of its range.

You may choose to detonate a single bomb. When a bomb is detonated, it
will detonate all bombs that lie in its range. These bombs will further
detonate the bombs that lie in their ranges.

Given the list of bombs, return the maximum number of bombs that can be
detonated if you are allowed to detonate only one bomb.

```
bombs = [[2,1,3],[6,1,4]]                               ->  2
bombs = [[1,1,5],[10,10,5]]                             ->  1
bombs = [[1,2,3],[2,3,1],[3,4,2],[4,5,3],[5,6,4]]       ->  5
```

**Constraints:** `1 <= bombs.length <= 100`; `bombs[i].length == 3`;
`1 <= xi, yi, ri <= 10^5`.

Bomb `i` sets off bomb `j` when `j` lies within `i`'s radius, which
says nothing of `j`'s radius, so the reach is one-way: the first example
sets off both bombs from the second, whose radius 4 reaches the first,
and only one from the first, whose radius 3 does not. The bombs and the
reach between them are a directed graph, and the answer is the most
bombs any one bomb reaches in it. Every arm compares the distance
squared, so no root is taken; at the constraints' largest the square is
2 * 10^10, past `i32`.

## Approaches

| file | mechanism |
|---|---|
| `detonate.kara` ★ | adjacency lists, a `Vec[Vec[i64]]` built from every pair, then a breadth-first search from each bomb with a `VecDeque` and a `Vec[bool]` of the bombs seen. O(n^3) for n <= 100 |
| `detonate_dfs.kara` | a recursive depth-first search, `spread(bombs, i, mut gone)`, testing the reach afresh at each step with no lists built; the starts' counts folded with `map` and `max` |
| `detonate_closure.kara` | Warshall's transitive closure: a `Vec[Vec[bool]]` of direct reach (each bomb reaching itself) built with nested `map` and `collect`, the triple loop adding every route through each bomb `k`, and the largest row's count of `true`. O(n^3) |
| `detonate_struct.kara` | a `struct Bomb` of its place and radius with a `sets_off` method, the field a `Vec[Bomb]`, and a depth-first search from each bomb with a `Vec` as an explicit stack |
| `detonate_bits.kara` | reach sets as bits: with at most 100 bombs each set fits in one `u128`; each round ors into every set the sets of the bombs it holds, until a round changes nothing, and the largest `count_ones` is the answer |
| `detonate_solution.kara` | LeetCode's Rust template (`bombs: Vec<Vec<i32>>`, the squares cast to `i64`, adjacency lists from `vec![vec![]; n]`, a depth-first search with a `Vec` stack and a `HashSet` whose `insert` says whether the bomb is new), carried by `karac fix` in four rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's three examples and four
more (one bomb alone; a bomb exactly on another's rim, which does not
reach back; two bombs out of each other's reach; a line whose first four
bombs chain only forward, to a last one that reaches all), each
field with its answer; then the total of the answers for 3000 random
fields of 1 to 12 bombs (on a 20 by 20 square with radii of 1 to 8, or
spread up to 10^5 with radii up to 10^5) and a checksum of them; then the
constraints' largest, 100 bombs each: a line whose gaps shrink, so each
bomb reaches only the next and the first sets off all; a line whose gaps
grow, so each reaches only the one before and the last does; a grid too
far apart for any bomb to reach another; and the four corners of the
square with the largest radius. `detonate.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: from each bomb, every bomb within range of one already gone
off is set off too, sweeping all pairs again until a sweep adds nothing.
It checks 300 random fields of 1 to 10 bombs on a 20 by 20 square with
radii of 1 to 8; then 20 fields of 1 to 10 bombs along one line, 1 to 5
apart with radii of 1 to 5, so that chains are long and often one-way;
then 20 fields of 1 to 10 bombs spread up to 10^5 with radii up to 10^5.
All 340 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is 1 to n, and at least what any one bomb reaches directly, itself included |
| P3 | the bombs listed in reverse: the same answer |
| P4 | the field turned a quarter, `(x, y)` to `(y, 100001 - x)`: the same answer |
| P5 | every radius halved, rounded up: an answer no larger |
| P6 | each arm agrees with at least three of the other five |

The turned and halved fields stay within the constraints. The
differential prints `340 fields: checksum 275354610, 12240 checks over 6
arms: 0 failures` under every lane in Verification; the checksum of the
literal answers was checked against a Python reading of the same fields
with a depth-first search. On a failure it prints the first ten and
then the count by property.

## Mutation testing

Thirty edits to the differential, five or six to each arm, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a bomb on the rim left out | P1 27, P2 14, P6 27 |
| M2 | ★: only the first bomb started from | P1 159, P2 153, P3 150, P6 159 |
| M3 | ★: the bombs outside the radius set off | P1 281, P2 5, P5 4, P6 281 |
| M4 | dfs: only the across gap measured | P1 227, P4 173, P6 227 |
| M5 | dfs: the last start's count taken | P1 167, P2 162, P3 150, P6 167 |
| M6 | dfs: the chain not followed past the first bomb | P1 59, P6 59 |
| M7 | closure: the bomb routed through in the middle loop | P1 2, P3 3, P6 2 |
| M8 | closure: only routes through the first bomb | P1 54, P3 11, P6 54 |
| M9 | closure: the bombs beyond the radius set off | P1 282, P2 6, P5 3, P6 282 |
| M10 | struct: the radius read from y | P1 272, P2 20, P4 52, P6 272 |
| M11 | struct: the reach read the wrong way | P1 78, P2 41, P6 78 |
| M12 | struct: the vertical gap counted twice | P1 202, P2 14, P4 214, P6 202 |
| M13 | bits: one round only | P1 7, P3 14, P6 7 |
| M14 | bits: sets met rather than joined | P1 227, P2 224, P3 9, P5 52, P6 227 |
| M15 | bits: the bomb a bit to the side | P1 276, P6 276 |
| M16 | solution: the adapter's answer one less | P1 340, P2 281, P6 340 |
| M17 | solution: x measured against y | P1 194, P2 33, P4 262, P6 194 |

P1 and P6 kill all seventeen, P2 eleven, P3 six, P4 four and P5 three.
P2 misses the edits whose answers still lie between the largest direct
reach and n (M4, M6, M7, M8, M13, M15). P3 sees the edits that depend on which bomb comes
first: a single start (M2, M8), the last start's count (M5), and two
whose result depends on the order the bombs are visited in, Warshall's
loops with the routed-through bomb in the middle (M7) and the reach
sets grown in one round (M13); and the sets met (M14), whose result
depends on that order too. P4 sees the edits that treat x and y differently
(M4, M10, M12, M17). P5 sees the edits under which a smaller radius can
reach more: the bombs outside the radius set off (M3, M9) and the sets
met (M14).

M7 is the classic slip in Warshall's algorithm, the loop over the bomb
routed through moved inside the loop over the start. It fails only 2 of
the 340 fields: a route through a bomb numbered lower than one that
joins it later is missed, which few small fields need.

Of the thirty, thirteen were not kept, and none survives. Three fail as
a kept one: the ★ arm's and the Rust arm's other bomb's radius as M11;
the struct arm's last start's chain as M5. Five fail the same way as
each other and were left out together: the ★ arm's reach taken both
ways and the bits arm's sets read across (P1 37, P6 37); and a bomb not
counting itself in the closure and bits arms and the Rust arm's start
never marked as gone (P1 155, P2 138, P6 155). Four are killed with
checks of their own but were left out because their arm keeps its
share: the ★ arm's count started at one, the dfs arm's own count left
out and its gaps added unsquared, and the closure arm's fewest taken.
One crashes and is not kept: the Rust arm's squares taken in `i32`,
which the wide fields overflow, and Kāra's overflow check stops.

## Verification

Every arm prints the same output as `detonate.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 0.6 s to 2.0 s, and the
differential 1.7 s (timed while other work shared the machine).

The ★ arm was first written with `use std.collections.VecDeque;`,
Rust's path in Kāra's dots. `karac fix` turned the `use` into `import`,
and the import then failed with "unknown module `std.collections`":
Kāra's collections are in the prelude, and no such module exists. The
`::` spelling already had a fix that deletes the line; the dotted one,
written as `use` or as `import`, now gets the same. Fixed in kara
81aca4606b, test `tests/kata_2101_dotted_std_use_fix.rs`. The arm has no
import.

`karac fix` carries the template in four rounds of 17, 1, 4 and 2 edits:
Rust's spellings (`use std::collections::HashSet;` deleted, `Vec<..>` to
brackets, `&&` to `and`, `Solution::` and `HashSet::` to `.`, the `&v`
pattern dropped and `&graph[u]` and the adapter's `&Vec` to `ref`, `struct Solution;` to `struct
Solution {}`); then `HashSet` to `Set`; then `vec![]` to `Vec.new()`,
`vec![s]` to `[s]`, `ans` given `: i32` so its `max` with an `i32`
types, and the adapter's `as i64` dropped as a cast `i32` widens
without; then `vec![Vec.new(); n]` to `Vec.filled(n, Vec.new())`, and
the adapter's `ref` parameter to a bare one.

## Benchmarks

The bench asks 2000 fields of 100 bombs, the constraints' largest count,
on a 1000 by 1000 square with radii of 1 to 150, with the ★ arm in all
five languages: adjacency lists from every pair, then a breadth-first
search from each bomb (`VecDeque` in Kāra and Rust, a fixed array in C,
a slice in Go, `deque` in Python). Every implementation prints `2000
fields: 53166 bombs in all, checksum 854557197`.

BENCHTAB
