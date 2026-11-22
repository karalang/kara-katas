# 2702. Minimum Operations to Make Numbers Non-positive

You are given a **0-indexed** integer array `nums` and two integers `x`
and `y`. In one operation, you must choose an index `i` such that
`0 <= i < nums.length` and perform the following:

- Decrement `nums[i]` by `x`.
- Decrement values by `y` at all indices except the `i`th one.

Return *the minimum number of operations to make all the integers in*
`nums` *less than or equal to zero.*

```
nums = [3,4,1,7,6], x = 4, y = 2  ->  3
nums = [1,2,1],     x = 2, y = 1  ->  1
```

**Constraints:** `1 <= nums.length <= 10^5`, `1 <= nums[i] <= 10^9`,
`1 <= y < x <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `nonpositive.kara` ★ | after t operations every number has lost t y, and x - y more each time it was chosen, so t suffices exactly when the numbers still above t y need at most t extra shares of x - y between them, each rounded up. That gets easier as t grows, so a binary search finds the least t, from 0 up to the largest number over y plus one; the count stops as soon as it passes t. O(n log(max / y)) |
| `nonpositive_sorted.kara` | the numbers sorted largest first, so a trial's count stops at the first number t y already clears, and the search bracketed tighter: at least the largest number over x and at most the largest over y, each rounded up. O(n log n + n log(max / y)) |
| `nonpositive_iter.kara` | the test is a closure, the numbers above t y `filter`ed, `map`ped to their shares and `sum`med against t, handed to a generic search for the first t any monotone test passes. O(n log(max / y)) |
| `nonpositive_gallop.kara` | trial counts double from 1 until one suffices, then a bisection between the last that failed and it; the test is a function of its own walking the numbers by index. O(n log(answer)) |
| `nonpositive_solution.kara` | a Rust solution as LeetCode's Rust users write it, `i32` numbers widened to `i64`, a capturing `check` closure, `for &v in nums.iter()` and a binary search on the count, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples; one number
of 1; one of `10^9` taken by a single x of `10^9`; then `10^5` numbers,
LeetCode's most, all `10^9` with x = `10^9` and y one less, all `10^9`
with x = 2 and y = 1, and falling from `10^9` by one with x = `10^9` and
y = 1; then the answers summed and a checksum for 2000 random cases of 1
to 8 numbers up to 100, and 200 of up to 1000 numbers up to `10^9`.
`nonpositive.py` mirrors the ★ arm and its output is byte-identical.

```
3
1
1
1
2
999990001
100000
2000 cases up to 100: operations sum to 12775, checksum 816863096
200 cases up to 1000000000: operations sum to 134282, checksum 975329200
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every choice of index tried, breadth first, from the numbers
as given, until some sequence of choices leaves every number at or below
zero, with no counting of shares. It checks 600 random cases of 1 to 4
numbers up to 10, y up to 4 and x up to 6 above it; 100 of up to 50
numbers up to 1000; and 40 of up to 2000 numbers up to `10^9` or `4 *
10^8`. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 4 numbers, the answer is the literal reading's |
| P2 | one number raised: the answer is no smaller |
| P3 | the numbers, x and y all multiplied by 2 to 5, within `10^9`: the same answer |
| P4 | a number of answer * y appended (at most `10^9`): the same answer |
| P5 | the answer lies between the largest number over x and over y, each rounded up, and its operations take at least the total |
| P6 | each arm agrees with at least three of the other four |

The differential prints `740 cases: checksum 850175211, 22200 checks
over 5 arms: 0 failures` under every lane in Verification. The checksum
folds the literal reading's answers, and a Python breadth-first search
over the same 600 small cases gives the same one. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Eleven edits to the differential, two or three to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run`. All eleven are
killed, each the same way under both backends. P3, the scaling, kills
only M11, the one edit that is wrong only at some scales. A twelfth, the
galloping arm's first trial count 2 rather than 1, is equivalent: when
the answer is 1 the bisection between 0 and 2 finds it.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the shares not rounded up | P1 293, P5 240, P6 381 |
| M2 | ★: the search's top the largest over y, not one more | P1 50, P5 62, P6 88 |
| M3 | sorted: the floor one above the largest over x | P1 408, P4 85, P5 107, P6 438 |
| M4 | sorted: sorted smallest first | P1 241, P5 345, P6 379 |
| M5 | iter: numbers above (t + 1) y counted | P1 195, P5 141, P6 253 |
| M6 | iter: a passing trial moves the top below it | P1 252, P2 53, P4 27, P5 233, P6 309 |
| M7 | gallop: the bisection stops two apart | P1 128, P5 21, P6 185 |
| M8 | gallop: shares of x, not x - y | P1 147, P5 123, P6 228 |
| M9 | solution: the check passes with one share to spare | P1 235, P5 155, P6 253 |
| M10 | solution: the numbers lose t y twice over | P1 350, P5 391, P6 490 |
| M11 | ★: a share rounded up only past a remainder of 2 | P1 165, P3 168, P5 90, P6 168 |

## Benchmarks

The bench draws 100 arrays of `10^4` numbers up to `10^9`, y up to 1000
and x up to `10^6` above it, all of them first, then answers each 5
times by the ★ arm in all five languages; each answer is a binary search
of about 20 trials over the array. Every implementation prints `100
arrays of 10000 numbers up to 1000000000, 5 rounds: operations sum to
1318606485, checksum 733609764`.

BENCHTAB

## Verification

All five arms print the same output as `nonpositive.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★, sorted and galloping arms checked clean as first written. The
iterator arm took one `karac fix`: the closure's `-> bool`, Rust's
spelling, dropped, since a Kāra closure's return type is inferred.

LeetCode's Rust template took one `karac fix` of 9 edits, among them:
`struct Solution {}` added, `Vec<i32>` respelled `Vec[i32]`, the `0i64` suffixes
dropped since an integer literal is `i64` by default, an `as i64` on a
number already `i64` dropped, the closure's `-> bool` dropped, and `for
&v in nums.iter()` became `for v in nums.iter()`, Kāra's spelling. The wrapper's `as i64` on the `i32` answer
was dropped too, since it widens by itself.
