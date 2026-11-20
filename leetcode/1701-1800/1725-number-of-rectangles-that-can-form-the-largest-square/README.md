# 1725. Number Of Rectangles That Can Form The Largest Square

You are given an array `rectangles` where `rectangles[i] = [li, wi]`
represents the `ith` rectangle of length `li` and width `wi`.

You can cut the `ith` rectangle to form a square with a side length of
`k` if both `k <= li` and `k <= wi`. For example, if you have a
rectangle `[4,6]`, you can cut it to get a square with a side length of
at most `4`.

Let `maxLen` be the side length of the **largest** square you can obtain
from any of the given rectangles.

Return *the **number** of rectangles that can make a square with a side
length of* `maxLen`.

```
rectangles = [[5,8],[3,9],[5,12],[16,5]]   ->  3    (squares of 5, 3, 5, 5)
rectangles = [[2,3],[3,7],[4,3],[3,7]]     ->  3
```

**Constraints:** `1 <= rectangles.length <= 1000`;
`1 <= li, wi <= 10^9`; `li != wi`.

## Approaches

| file | mechanism |
|---|---|
| `rectangles.kara` ★ | the largest square of a rectangle has its shorter side; one pass keeps the largest such side so far and how many rectangles give it, a larger side starting the count again at one. O(n) |
| `rectangles_fold.kara` | the same pass as a `fold` over the shorter sides, its state the pair (largest side, how many). O(n) |
| `rectangles_sorted.kara` | the shorter sides collected and sorted, and the run of sides equal to the last counted from the end. O(n log n) |
| `rectangles_solution.kara` | a Rust solution as LeetCode's Rust users write it, the sides collected with `r[0].min(r[1])`, `*sides.iter().max().unwrap()`, and `filter(\|&&s\| s == max_len).count() as i32`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 7 lines: LeetCode's two examples, one
rectangle, and a thousand squares alike; then the answers summed and a
checksum for 3000 random problems of up to 8 rectangles with sides up
to 6, 300 of up to 1000 with sides up to 20, and 300 of up to 1000 with
sides up to `10^9`. The random rectangles may be squares, which the
constraints leave out; every arm answers them the same. `rectangles.py`
mirrors the ★ arm and its output is byte-identical.

```
3
3
1
1000
3000 problems of up to 8 rectangles with sides up to 6: answers sum to 3925, checksum 270913013
300 problems of up to 1000 rectangles with sides up to 20: answers sum to 685, checksum 285558923
300 problems of up to 1000 rectangles with sides up to 1000000000: answers sum to 300, checksum 810107245
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: each rectangle's largest square found by growing a side one
at a time while the next still fits both `k <= li` and `k <= wi`,
`maxLen` the largest of those, and the rectangles that can make a square
of `maxLen` counted. It checks 3000 random problems of 1 to 7 rectangles
with sides of 1 to 5. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the rectangles in reverse order give the same answer |
| P3 | every rectangle turned, its length and width swapped, gives the same answer |
| P4 | a square one larger than any rectangle's largest square added makes the answer 1 |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 902988923, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, `min` of each rectangle and the count of the
largest, gives the same checksum. On a failure it prints the first ten
and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

A first M4 found a compiler bug. It made the fold's first branch
`(side, count + 1)`, a count that carries on past a larger side, and the
two backends disagreed: the interpreter failed 1639 checks of P1, and
the compiled program 3000, answering 0 where the interpreter answered 3.
The fold's state is `(i64, i32)`, its seed's first `0` taking the
default, while the branch gives `(side, count + 1)`, an `(i32, i32)`;
`karac check` passes it, the interpreter's values carry no width, and
the compiled fold reads the pair at the wrong width. The kata's own fold
gives `(side, 1)` there, and every lane agrees on it. Since kara `93fd9b2078` (B-2026-11-20-48) the closure is typed as the slot's tuple, its branches are built at the slot's widths, and the first M4 gives the same answers on every lane. It was
replaced by `(side, 2)`.

M3 and M5 both leave the count at one, M3 by starting it again at an
equal side and M5 by not adding one there, and M7 and M8 both count the
rectangles equal to the smallest side, from the two ends; each pair
fails the very same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a larger side adds to the count instead of starting it again | P1 1639, P2 1935, P4 3000, P5 1639 |
| M2 | ★: a rectangle's longer side taken | P1 1606, P4 1647, P5 1606 |
| M3 | ★: an equal side starts the count again | P1 837, P5 837 |
| M4 | fold: a larger side starts the count at two | P1 3000, P4 3000, P5 3000 |
| M5 | fold: an equal side not counted | P1 837, P5 837 |
| M6 | sorted: the sides not sorted | P1 839, P2 843, P5 839 |
| M7 | sorted: the run counted is the one equal to the first side | P1 2412, P4 3000, P5 2412 |
| M8 | sorted: the run counted from the front | P1 2412, P4 3000, P5 2412 |
| M9 | solution: the smallest side taken as `max_len` | P1 1437, P4 1523, P5 1437 |
| M10 | solution: the sides not equal to `max_len` counted | P1 2575, P4 2593, P5 2575 |

## Benchmarks

The bench draws 1000 random problems of 1000 rectangles, LeetCode's
largest, with sides up to 20 so that many rectangles share the largest
square, all of them first, then answers each 50 times by the ★ arm in
all five languages. Every implementation prints `1000 problems of 1000
rectangles, 50 rounds: answers sum to 155450, checksum 401554012`. The
work is a compare or two a rectangle, so the bench mostly measures
walking the rectangles: Kāra, Rust and Go hold them as a list of
two-element lists, as LeetCode passes them, and C as one flat array of
pairs, which is less to walk. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.088 s |
| Go | 0.124 s |
| Kāra (`karac build`) | 0.170 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.182 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.184 s |
| Rust (`rustc -O`) | 0.193 s |
| Python | 3.2 s |

The sequential Kāra build is 6% faster than Rust and level with Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.088 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.170 s and 0.190 s on one
run).

## Verification

All four arms print the same output as `rectangles.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ and sorted arms checked clean as first written.

The fold arm was written `fold((0, 0), |(best, count), side| ...)` and
then `let (_, count) = ...; count` as the `i32` answer. `count` comes
from the second literal of the seed, which met only `count + 1` and the
`1` beside a side, so it took `i64`, the literal's default, and `karac
check` named the narrowing at the return. Its fix reached back through
the `fold` and the tuple pattern to the seed and wrote `(0, 0i32)`.

LeetCode's Rust template took one `karac fix` of 7 edits:
`struct Solution {}` added, `Vec<Vec<i32>>` and `Vec<i32>` written
`Vec[Vec[i32]]` and `Vec[i32]`, and `|&&s|` written `|s|`.
`r[0].min(r[1])`, `*sides.iter().max().unwrap()` and
`.count() as i32` carried over as written.

The differential checked clean as first written. `arm_name` in it
indexes a list of string literals for a `Str`, as #1662's does
(B-2026-11-19-131).
