# 1467. Probability of a Two Boxes Having The Same Number of Distinct Balls

Given `2n` balls of `k` distinct colors. You will be given an integer
array `balls` of size `k` where `balls[i]` is the number of balls of
color `i`. All the balls will be shuffled uniformly at random, then we
will distribute the first `n` balls to the first box and the remaining
`n` balls to the other box. Please note that the two boxes are
considered different. For example, if we have two balls of colors `a`
and `b`, and two boxes `[]` and `()`, then the distribution `[a] (b)` is
considered different than the distribution `[b] (a)`. Return the
probability that the two boxes have the same number of distinct balls.
Answers within `10^-5` of the actual value will be accepted as correct.

```
balls = [1,1]       ->  1.00000
balls = [2,1,1]     ->  0.66667
balls = [1,2,1,2]   ->  0.60000
```

**Constraints:** `1 <= balls.length <= 8`, `1 <= balls[i] <= 6`, and
`sum(balls)` is even.

The arms are `fn get_probability(balls: Vec[i32]) -> f64`. Each counts
the good shuffles exactly in `i64` and divides once at the end, so all
five give the same `f64` to the last bit, and the harness prints it
whole.

## Approaches

| file | mechanism |
|---|---|
| `get_probability.kara` ★ | a shuffle is fixed by which places of the first half each ball takes, so the balls of one colour split j to the first box in C(n, j) ways: a depth-first search over how many of each colour go into the first box, each choice weighted by its C(n, j), counting the splits that fill the first box and leave the two boxes as many colours each, over all C(total, total / 2). O(7^8) at worst, pruned by the first box's room |
| `get_probability_table.kara` | a Pascal triangle in a `Vec[Vec[i64]]`, and a table over the colours of the shuffles by the first box's count and the two boxes' difference in colours, each colour moving every entry by a split. O(k · total^2 · 6) |
| `get_probability_memo.kara` | the same search, keyed by colour, the first box's room and the difference in colours, memoized in a `Map[(i64, i64, i64), i64]` passed down as `mut ref`, with C(n, k) by the recursion C(n - 1, k - 1) · n / k |
| `get_probability_halves.kara` | meet in the middle: each half of the colours' splits tallied in a `Map[(i64, i64), i64]` by `*next.entry(..).or_insert(0) += ..`, and each left split matched with the right splits that fill the first box and even the colours |
| `get_probability_solution.kara` | a Rust solution as LeetCode's Rust users write it (a Pascal triangle of `f64` in `vec![vec![0.0; 49]; 49]`, a nested `fn dfs` taking `&[i32]` and `&Vec<Vec<f64>>` with `usize` indices, every split tried), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples and three
more, one colour of two balls, two colours that cannot split evenly, and
the constraints' most, 8 colours of 6 balls (`1.0 0.6666666666666666 0.6
1.0 0.0 0.8557108876701283`); and 300 random sets of 1 to 8 colours of 1
to 6 balls, their probabilities summed and the millionths of each folded
into a checksum (`300 random sets: sum 138.8788730741624, checksum
37803317`). `get_probability.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, table, memo and halves arms check clean as first
written. The memo arm as first written took C(n, k) by Pascal's two-term
recursion with no memo of its own, which makes about 3 x 10^13 calls for
C(48, 24) and stops at the interpreter's step limit; it is my error, and
the arm now takes the one-term recursion. The Rust solution takes one
round of 21 fixes by `karac fix`'s count: `struct Solution;` to `struct
Solution {}`, `Vec<..>` to `Vec[..]`, the nested `fn dfs` moved above
the `impl`, since Kāra has no nested items, `&[i32]` to `Slice[i32]` and
`&Vec<Vec<f64>>` to `ref Vec[Vec[f64]]`, `usize` to `i64` and the `as
usize` index casts dropped, `&&` to `and`, `vec![vec![0.0; 49]; 49]` to
`Vec.filled(49, Vec.filled(49, 0.0))`, the `&` on the call's arguments
dropped, and `Solution::get_probability` to `Solution.get_probability`.
Every arm's output then matches on its first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the balls told apart, so every set of half of them is as
likely a first box as any other, each such set tried by a bit mask, and
the share of them that leaves the two boxes as many colours each, while
there are at most 12 balls. LeetCode's examples, the edge cases above
with eight colours of one ball and a colour of six beside one of two,
and 1995 random sets: 1500 of 1 to 6 colours of 1 to 3 balls, and 495 of
1 to 8 colours of 1 to 6.

| | property |
|---|---|
| P1 | the statement read literally, while there are at most 12 balls |
| P2 | the colours reversed give the same answer |
| P3 | the colours shuffled give the same answer |
| P4 | the answer is a whole number of the C(total, total / 2) equally likely splits |
| P5 | the answer lies from 0 to 1, and is 1 for a single colour or for colours of one ball each |
| P6 | the ★ arm's answer |

All 58,130 checks pass on every arm: `2003 cases: checksum 708842662,
58130 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, building a table
with `math.comb`, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a colour with one ball in the first box not counted there | P1 1422, P5 272, P6 7256 |
| M2 | ★: a split that leaves the first box short counted | P1 1156, P5 372, P6 6192 |
| M3 | table: a split colour counted as one more in the first box | P1 1541, P5 240, P6 1933 |
| M4 | table: n choose j taken as n - 1 choose j - 1 | P1 1213, P5 1592, P6 1605 |
| M5 | memo: every answer filed as if the colours were even | P1 909, P2 1187, P3 1132, P6 1301 |
| M6 | memo: a split counted however the colours fall | P1 1125, P6 1517 |
| M7 | halves: the right half matched to the same difference, not the opposite | P1 1099, P2 554, P3 771, P5 69, P6 1489 |
| M8 | halves: each split counted once, not by its shuffles | P1 1384, P5 240, P6 1776 |
| M9 | solution: n choose j taken as n - 1 choose j - 1 | P1 1213, P5 1592, P6 1605 |
| M10 | solution: a split counted however many balls each box holds | P1 1156, P4 1, P5 750, P6 1548 |

## Benchmarks

The bench draws 100 sets of 8 colours of 1 to 6 balls with an even
count, once; then makes 2 passes, each moving one colour of every set,
chosen from the checksum so far, by two balls, so the count stays even
and no answer carries over, answering it with the ★ arm and folding the
billionths of the answer into the checksum. Every implementation makes
the same search. Every implementation prints `2 passes over 100 sets of
8 colours: checksum 112328304`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.26 s against Rust's 0.23 s (0.25 s with overflow checks
on), C's 0.21 s and Go's 0.31 s; Python takes 10.2 s.
