# 1449. Form Largest Integer With Digits That Add up to Target

Given an array of integers `cost` and an integer `target`, return the
maximum integer you can paint under the following rules: the cost of
painting a digit `(i + 1)` is given by `cost[i]` (0-indexed); the total
cost used must be equal to `target`; the integer does not have `0`
digits. Since the answer may be very large, return it as a string. If
there is no way to paint any integer given the condition, return `"0"`.

```
cost = [4,3,2,5,6,7,2,5,5], target = 9              ->  "7772"
cost = [7,6,5,5,5,6,8,7,8], target = 12             ->  "85"
cost = [2,4,6,2,4,6,4,4,4], target = 5              ->  "0"
cost = [6,10,15,40,40,40,40,40,40], target = 47     ->  "32211"
```

**Constraints:** `cost.length == 9`, `1 <= cost[i], target <= 5000`.

Each arm is `fn largest_number(cost: Vec[i32], target: i32) -> String`.

## Approaches

A larger number has more digits, and of two with as many, the one with
more of the largest digit, then of the next; so the answer is the most
digits the target buys, written from 9 down.

| file | mechanism |
|---|---|
| `largest_number.kara` ★ | the most digits each cost from 0 to target buys exactly, -1 when it buys none; then the digits taken from 9 down, each while what is left still buys one digit fewer. O(9 · target) |
| `largest_number_counts.kara` | for each cost from 0 to target, the best answer it buys exactly, kept as an `Option[Vec[i64]]` of how many of each digit, `let .. else` passing over a cost that buys none; more digits win, then more of the larger digits. O(81 · target) |
| `largest_number_memo.kara` | top down: the most digits a cost buys exactly, by recursion with a memo; then each place takes the largest digit that leaves a cost buying one digit fewer, the search left by `break`. O(9 · target) |
| `largest_number_table.kara` | a table by digits, row i the most digits from 1 to i buy for each cost exactly, each digit as often as wanted; then back from row 9, a digit taken while the cost without it buys one fewer, and the row dropped when not. O(9 · target) |
| `largest_number_solution.kara` | a Rust solution as LeetCode's Rust users write it (`let t = target as usize`, `vec![i32::MIN; t + 1]`, each digit's cost through `as usize`, the answer pushed as `(b'1' + d as u8) as char`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's four examples and three
more, every cost 1, every cost 5000, and only the digit 1 cheap (`7772
85 0 32211 99999 9 1111111`); the constraints' most, a target of 5000
with every cost 1 and with costs drawn from 1 to 50 (`target 5000: 5000
and 713 digits, checksum 680209296`); and 2000 random cases, costs from
1 to 1 to 30, or a third of them 1 to 1 to 5000, and a target from 1 to
200 (`2000 random cases: 96511 digits, checksum 863104868`).
`largest_number.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac __mir-run`, `karac run`,
`karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, counts and memo arms check clean as first written.
The table arm wrote its row and cost as `let (mut i, mut t) = (9,
target);`, which `karac check` refuses, saying `mut` goes before the
whole pattern in Kāra, and `karac fix` writes `let mut (i, t) = (9,
target);`, 3 fixes by its count. The Rust solution takes one round of 13
fixes by `karac fix`'s count: `struct Solution;` to `struct Solution
{}`, `Vec<i32>` to `Vec[i32]`, `target as usize` and `cost[d] as usize`
to `as i64`, `vec![i32::MIN; t + 1]` to `Vec.filled(t + 1, i32.MIN)`,
`i32::MIN` to `i32.MIN`, `&&` to `and`, `String::new()` to
`String.new()`, and `Solution::` to `Solution.`. Every arm's output
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every number whose digits cost the target exactly, each
written with its digits from the largest down, so every way to buy them
is met once, and the largest of them, while the target is at most 12.
LeetCode's examples, the three edge cases above, the constraints' most
two ways, and 1994 random cases drawn as the harness draws them, a third
of them with a target from 1 to 12, for the literal reading.

Two of its lines are refused and fixed. P2 adds up the digits' costs by
`got.bytes().map(..)`, and P5 collects the digits by
`got.bytes().collect()`: a `String`'s `bytes()` is a `Slice[u8]` in
Kāra, not an iterator, so both are refused, and `karac fix` writes
`got.bytes().iter()` in each, with the cast in `cost[(b - b'1') as i64]`
dropped as unneeded, 3 fixes. P2 first ran over every answer and stopped
at its first `"0"`, `b'0' - b'1'` overflowing a `u8`; it now skips an
answer of `"0"`.

| | property |
|---|---|
| P1 | the statement read literally, while the target is at most 12 |
| P2 | the digits cost the target exactly, unless the answer is 0 |
| P3 | every cost and the target doubled give the same number |
| P4 | a target the cost of a 9 more gives at least a 9 in front of the answer |
| P5 | the digits from 1 to 9, never rising, and no more of them than the target buys of the cheapest |
| P6 | the ★ arm's answer |

All 46,695 checks pass on every arm: `2003 cases: checksum 592128365,
46695 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by a memo of the
best string for each cost left for the targets up to 200 and the ★ arm's
mirror for the three of 5000, gives the same checksum.

The fixed cases are a typed list of tuples written as Rust writes them,
`[([4, 3, 2, 5, 6, 7, 2, 5, 5].to_vec(), 9), ..].to_vec()` into a
`Vec[(Vec[i32], i64)]`. Check refused each tuple, its `.to_vec()` list
taking the default `i64` where the slot names `i32`: the slot's type
reached a `[..].to_vec()` at a `let` of its own but not one inside a
tuple. That was B-2026-11-26-78, fixed at a648c7a471.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: each cost's count taken from the last digit tried, not the most | P1 159, P6 3340 |
| M2 | ★: the digits taken from 1 up, not from 9 down | P1 200, P4 300, P5 297, P6 2788 |
| M3 | counts: fewer digits held the better answer | P1 264, P4 525, P6 1097 |
| M4 | counts: fewer of the larger digits held the better answer | P1 182, P4 230, P6 552 |
| M5 | memo: each place given the smallest digit that fits, not the largest | P1 200, P4 300, P5 297, P6 697 |
| M6 | memo: a digit never bought with exactly the cost left | P1 410, P6 1298 |
| M7 | table: each digit written as its mirror, 1 for 9 | P1 381, P2 1074, P4 365, P5 294, P6 1192 |
| M8 | table: the target's own column never filled | P1 410, P6 1298 |
| M9 | solution: each digit taken at most once | P1 322, P2 1158, P4 1208, P6 1198 |
| M10 | solution: each digit written as its mirror, 1 for 9 | P1 381, P2 1074, P4 365, P5 294, P6 1192 |

## Benchmarks

The bench answers 5000 cases with the constraints' most target, 5000,
each with nine costs drawn from 1 to 50, by the ★ arm, folding each
answer's digits to a checksum. Every implementation prints `5000 targets
of 5000: checksum 251245596`.

BENCHTAB

Measured by hand, Kāra takes 0.40 to 0.44 s against Rust's 0.35 to 0.37
s (0.41 to 0.45 s with overflow checks on), C's 0.24 to 0.27 s and Go's
0.67 s; Python takes 33 s.
