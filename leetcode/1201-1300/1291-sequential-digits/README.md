# 1291. Sequential Digits

An integer has *sequential digits* if and only if each digit in the
number is one more than the previous digit.

Return a **sorted** list of all the integers in the range `[low, high]`
inclusive that have sequential digits.

```
low = 100,  high = 300    ->  [123,234]
low = 1000, high = 13000  ->  [1234,2345,3456,4567,5678,6789,12345]
```

**Constraints:** `10 <= low <= high <= 10^9`.

The arms are `fn sequential_digits(low: i64, high: i64) -> Vec[i64]`.

## Approaches

There are only 36 numbers with sequential digits, one for each length
from 2 to 9 and each first digit that leaves room for it, so every arm is
constant time; they differ in how they reach the 36.

| file | mechanism |
|---|---|
| `sequential_digits.kara` ★ | made by length, then first digit, which is increasing order, each built digit by digit, those in the range kept |
| `sequential_digits_queue.kara` | a breadth-first walk in a `VecDeque` from the digits 1 to 9, each number followed by itself with the next digit written after it while its last digit is below 9; the queue yields them in increasing order, so the walk stops at the first past `high` |
| `sequential_digits_window.kara` | every window of the string `"123456789"` from the length of `low` to the length of `high`, each read with `i64.parse` |
| `sequential_digits_dfs.kara` | depth first from each first digit, a digit at a time while the number stays within `high`; the order is by first digit, not by size, so the found numbers are sorted at the end |
| `sequential_digits_step.kara` | without digits: the next number of a length is the last plus `11...1` (`1234 + 1111 = 2345`), and each length starts from `12...k` |
| `sequential_digits_solution.kara` | a Rust solution as LeetCode's Rust users write it (slices `s[i..i + len]` of `"123456789"` from the length of `low` to the length of `high`, each `.parse()`d to an `i32`), carried to Kāra by `karac fix` |
| `sequential_digits_windows.kara` | a second Rust solution as LeetCode's Rust users write it (`windows(len)` over the digits 1 to 9 collected from `1..=9`, each window folded to a number with `fold(0, \|acc, &d\| acc * 10 + d)` and kept when `(low..=high).contains(&n)`), carried to Kāra by `karac fix` |
| `differential.kara` | the seven arms against the statement read literally, five more properties |

Every arm prints the same 9 lines: LeetCode's two examples, the whole
range `[10, 10^9]`, ranges with none, with exactly one at either end, and
the top of the range; then 20000 random ranges, a third anywhere up to
`10^9` and two thirds from a random power of ten over a random number of
digits (`20000 random ranges: 63015 numbers, checksum 685057337`).
`sequential_digits.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`.

The Mend loop: the ★, window, depth-first and step arms checked clean as
first written. The queue arm was first written with a `Deque`, which
Kāra calls `VecDeque`: `E0100` and `E0104` asked "did you mean
`VecDeque`?" and `karac fix` made both changes (2 fixes). The two Rust
arms each take one round, 9 fixes and 13 by `karac fix`'s count:
`Vec<i32>` to `Vec[i32]`, `vec![]` and `Vec::new()` to `Vec.new()`,
`struct Solution;` to `struct Solution {}`, `::` to `.`, `&&` to `and`,
`s[i..i + len].parse().unwrap()` to `i32.parse(s[i..i + len]).unwrap()`,
and in the windows arm the closure's `&d` pattern to `d`, `contains(&n)`
to `contains(n)`, the fold's seed `0` to `0i32`, since a bare literal
would settle to `i64` before it meets the `i32` digits, and `let mut ans
= Vec::new();` to `let mut ans: Vec[i32] = Vec.new();`. Both Rust arms'
outputs match on the first run. No gap was met.

The windows arm is the slowest under `karac __mir-run`, about 6 to 8 s
against about 1 s for the others; compiled, all seven take the same 0.4 s.
Its `windows` is not the cost: the same arm over `digits[s..s + len]`
slices takes as long. No profile was taken.

## Differential

`differential.kara` holds copies of the seven arms and the statement read
literally: every number found is in the range and has sequential digits,
each digit checked against the one after it from the last digit back, and
the numbers are strictly increasing; on a range of at most 3000 numbers,
every number in it is checked, so none is missing. 1500 ranges in three
kinds, 500 each: within 1500 either side of a number with sequential
digits, drawn by its first digit and length, so that P1 reads every
number in it; from a random power of ten over a random number of digits;
and anywhere up to `10^9`. Every range and every split point is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the range split at a random point: the two answers, one after the other |
| P3 | the whole range `[10, 10^9]`'s answer, cut to this range |
| P4 | each number found is the answer for itself alone, and the numbers between two found ones have none |
| P5 | the range from `low + 1`: the answer without `low` |
| P6 | the ★ arm's answer |

All 62,643 checks pass on every arm: `1500 ranges: checksum 229939641,
62643 checks over 7 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum.

## Mutation testing

Fourteen edits to the differential, two to each arm, each run under both
`karac __mir-llvm-run` and `karac __mir-run`. Every one is killed, fails
the same way under both backends and not by a crash. Twelve are kept, at
least one to each arm, so that no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no numbers of 9 digits | P1 12, P6 822 |
| M2 | ★: `low` itself left out | P1 5, P2 6, P3 9, P4 802, P5 4, P6 54 |
| M3 | queue: `high` itself left out | P1 5, P2 9, P3 5, P4 802, P6 5 |
| M5 | window: the last window of each length skipped | P1 400, P6 662 |
| M6 | window: the shortest length one too long | P1 531, P2 227, P3 370, P4 519, P6 675 |
| M7 | depth first: the found numbers not sorted | P1 437, P2 302, P4 389, P5 6, P6 437 |
| M8 | depth first: no number starting with 1 | P1 328, P6 576 |
| M9 | step: each length's first number built with the wrong last digit | P1 790, P6 790 |
| M10 | step: the step one `1` short | P1 657, P6 657 |
| M11 | solution: the length of `high` left out | P1 482, P2 183, P3 606, P4 451, P6 743 |
| M13 | windows: no two-digit numbers | P1 273, P6 305 |
| M14 | windows: each digit folded one too high | P1 643, P6 661 |

The two left out fail exactly as a kept one does: the queue arm growing
no number past a last digit of 8 drops the numbers ending in 9, as M5
does, and the solution arm skipping the window from 1 drops the numbers
starting with 1, as M8 does.

P1 and P6 kill all twelve, P2 and P4 five each, P3 four and P5 two. An
arm that leaves out the same numbers everywhere passes P2, P3 and P5,
which compare an arm with itself, so only P1 and P6 see the missing
numbers; P1 sees them on the narrow ranges it reads in full, which is why
M1, a whole length gone, fails P1 only 12 times. P4 catches the edits at
the ends of a range: a range of one number is all ends.

## Benchmarks

The bench builds 10^5 ranges from a random power of ten over a random
number of digits once, from its own generator, then makes 20 passes; each
moves every range's `low` up by the checksum so far modulo 1000, so no
answer carries over, answers it with the ★ arm and folds the count, the
pass and every number found into the checksum. Each answer is a fresh
growable array in Kāra, Rust, Go and Python, and a fresh `malloc` of 36
slots in C. Every implementation prints `20 passes over 10^5 ranges:
checksum 956878873`.

BENCHTAB
