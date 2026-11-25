# 1388. Pizza With 3n Slices

There is a pizza with `3n` slices of varying size, you and your friends
will take slices of pizza as follows:

You will pick any pizza slice. Your friend Alice will pick the next
slice in the anti-clockwise direction of your pick. Your friend Bob will
pick the next slice in the clockwise direction of your pick. Repeat
until there are no more slices of pizzas.

Given an integer array `slices` that represent the sizes of the pizza
slices in a clockwise direction, return the maximum possible sum of
slice sizes that you can pick.

```
slices = [1,2,3,4,5,6]  ->  10
slices = [8,9,8,6,1,1]  ->  16
```

**Constraints:** `3 * n == slices.length`, `1 <= slices.length <= 500`,
and `1 <= slices[i] <= 1000`.

Each arm is `fn max_size_slices(slices: Vec[i32]) -> i32`. The slices
you end with are exactly the sets of n slices no two of which sit side
by side around the circle, and every such set can be had by some order
of picks; every arm answers that question rather than playing the game,
which the differential plays.

## Approaches

| file | mechanism |
|---|---|
| `max_size_slices.kara` ★ | the better of two straight runs, without the last slice and without the first, since the circle cannot have both; in each, `best[i][j]` is the most from at most j slices, no two adjacent, among the first i, taking slice i over `best[i - 2][j - 1]` or leaving it. O(n^2) |
| `max_size_slices_greedy.kara` | a greedy that can take back what it took: the largest slice taken, and in its place one slice worth its two neighbours less itself, the neighbours gone, so that taking it later trades the first slice for both. The circle kept as a linked list in two `Vec`s, the slices in a max-first `PriorityQueue`, stale entries skipped. O(n log n) |
| `max_size_slices_memo.kara` | the same two runs by a recursive function, slice i left or taken with the next skipped, kept in a memo `Vec` passed `mut ref`. O(n^2) |
| `max_size_slices_rolling.kara` | the ★ arm's table kept as its last two rows, swapped by moving the `Vec`s. O(n^2) time, O(n) space |
| `max_size_slices_solution.kara` | a Rust solution as LeetCode's Rust users write it (a nested `fn calc` over `&[i32]`, a `vec![vec![0; n + 1]; m + 2]` table filled from the back with `(0..m).rev()` and `1..=n`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples, three
slices, six of one size, and one large slice beside two that together
are larger (`10 16 4 14 11`); the constraints' most, 498 slices up to
1000, and 498 of size 1000 (`498 slices: 130297, and 166000 when all are
1000`); and 2000 random pizzas of 3 to 60 slices, half of up to 1000 and
half of up to 3, so that sizes tie (`2000 random pizzas: 8253581 in all,
checksum 4792579`). `max_size_slices.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, memo and rolling arms check clean as first
written. The greedy arm's `let mut total = 0;`, added to with each `i32`
slice and returned as the `i32` answer, keeps its literal's `i64`, which
the return refuses; `karac fix` writes `let mut total: i32 = 0;`. The
Rust solution takes one round of 13 fixes by `karac fix`'s count, from 6
errors: `struct Solution;` to `struct Solution {}`, `Vec<i32>` to
`Vec[i32]`, `&[i32]` to `Slice[i32]`, the nested `fn calc` moved above
the `impl`, since Kāra has no nested items, its `usize` to `i64`,
`vec![vec![0; n + 1]; m + 2]` to `Vec.filled(m + 2, Vec.filled(n + 1,
0i32))`, and the `&` dropped from `&slices[..len - 1]` and
`&slices[1..]`; `(0..m).rev()`, `1..=n` and the open-ended ranges stay.
Its output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the game played every way, you taking any slice that is left,
Alice the next one anticlockwise and Bob the next one clockwise around
what is left, until nothing is, and the best total kept. LeetCode's two
examples and 2000 pizzas of 3 to 12 slices, half of up to 990, leaving
room inside the constraints for P4, and half of up to 3, so that sizes
tie, each with a turn for P2. Every case is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the pizza turned: the same |
| P3 | the pizza flipped over: the same |
| P4 | every slice 5 larger: 5 more for each of your n slices |
| P5 | at least the largest slice, at most the n largest together |
| P6 | the ★ arm's answer |

All 60,060 checks pass on every arm: `2002 pizzas: checksum 63587709,
60060 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, playing every
game, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a slice taken beside the last one taken | P1 615, P2 133, P6 2460 |
| M2 | ★: the first of the two lines kept whole, so the first and the last slice both count | P1 89, P2 171, P6 356 |
| M3 | greedy: a taken slice left worth 0, so taking it back gains nothing | P1 84, P2 25, P3 46, P6 84 |
| M4 | greedy: the slice clockwise of a taken one left in play | P1 361, P2 52, P3 446, P6 361 |
| M5 | memo: a slice taken beside the last one taken | P1 615, P2 133, P6 615 |
| M6 | memo: a line's last slice never taken | P1 646, P2 877, P3 864, P5 127, P6 646 |
| M7 | rolling: a slice taken beside the last one taken | P1 615, P2 133, P6 615 |
| M8 | rolling: the row two back never moved on | P1 1508, P4 1508, P6 1508 |
| M9 | solution: a slice taken without counting it | P1 1468, P4 1483, P5 1249, P6 1468 |
| M10 | solution: only the line without the last slice | P1 514, P2 765, P3 1024, P5 127, P6 514 |

P1 and P6 kill all ten, P2 eight, P3 four, P5 three and P4 two. M1, M5
and M7 make one mistake in three arms, letting two neighbouring slices
both count, and fail exactly alike. A pizza turned round (P2) moves
which slices fall at the two ends of each line, so every edit that
mistreats the ends or the neighbours fails it; only M8 and M9, which
count the wrong number of slices rather than the wrong slices, pass it,
and only they fail P4, since 5 more for each slice comes out wrong when
the number taken is not n. M9, taking more than n, passes the n largest
together (P5); M6 and M10, never taking one end, can miss the largest
slice.

The greedy arm's first M4, which dropped the `v != value[i]` test on
what the queue gives back, survived, and it is an equivalent mutant: the
only slice whose worth changes is the one just popped, so the queue
never holds an old worth of a slice still in play, and the test never
fires. The arm keeps the test, as the usual guard of a lazily updated
queue, and M4 now leaves the clockwise neighbour in play.

## Benchmarks

The bench draws 498 slices, the constraints' most, of up to 1000, once.
Then 1000 rounds, each giving one slice a new size and asking the ★ arm
for the most you can get, all drawn from the checksum so far. Every
implementation prints `1000 rounds over 498 slices: checksum 4842454`.
The work is two tables of 498 by 167, a round. Rust and Go build them as
vectors of rows, as Kāra does; C as one flat `calloc`.

BENCHTAB
