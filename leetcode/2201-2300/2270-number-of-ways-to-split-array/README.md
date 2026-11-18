# 2270. Number of Ways to Split Array

You are given a **0-indexed** integer array `nums` of length `n`.

`nums` contains a **valid split** at index `i` if the following are
true:

- The sum of the first `i + 1` elements is **greater than or equal to**
  the sum of the last `n - i - 1` elements.
- There is **at least one** element to the right of `i`. That is,
  `0 <= i < n - 1`.

Return *the number of **valid splits** in* `nums`.

```
nums = [10,4,-8,7]  ->  2
nums = [2,3,1,0]    ->  2
```

**Constraints:** `2 <= nums.length <= 10^5`; `-10^5 <= nums[i] <= 10^5`.

The right part's sum is the total less the left's, so one pass that
grows the left sum tests every split. The sums reach 10^10, past an
`i32`. O(n).

## Approaches

| file | mechanism |
|---|---|
| `split.kara` ★ | the total by `sum`, then the left sum grown a value at a time and tested against `total - left` |
| `split_prefix.kara` | a table of prefix sums one longer than the array; the split after `i` compares `prefix[i + 1]` with `prefix[n] - prefix[i + 1]` |
| `split_two.kara` | two running sums, the right starting as the whole array; each value moves from right to left over `nums[..n - 1]`, with no total |
| `split_struct.kara` | `struct Cut` of the sums on either side; `shift` (`mut ref self`) moves a value across and `valid` compares |
| `split_iter.kara` | one chain: `take(n - 1)`, the left sums by `scan` as Kāra's `Some((next_state, item))`, `filter` where twice the left reaches the total, `count` |
| `split_solution.kara` | LeetCode's Rust template: `Vec<i32>` in, `i32` out; the total by `map(\|&x\| x as i64).sum()` into an `i64`, the left `0i64` grown by `nums[i] as i64`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and five
more (two values rising, 0; a tie, 1; all negative, 2; rising, 1; a
large value at each end, 3), each with its count; then 2000 random
arrays of 2 to 40 values within 1, 10, 1000 or 10^5 of 0, with a
checksum; then three of the constraints' longest, 10^5 values: random
within 10^5 (50026), all 10^5 (50000), and -10^5 and 10^5 alternating
(49999). `split.py` mirrors the ★ arm and its output is byte-identical.

The iter arm was first written as Rust's `scan`, `|left, x| { *left +=
x; Some(*left) }`. `karac check` explains that Kāra's `scan` takes the
state by value and returns `Some((next_state, item))`, and `karac fix`
rewrites the closure as `|left, x| { let left = left + x; Some((left,
left)) }`.

`karac fix` carries the template in one round, reporting 11 edits:
`Vec<i32>` and `Vec<i64>` to `Vec[i32]` and `Vec[i64]`, the patterns
`|&x|` to `|x|` twice, `0i64` to `0` and `nums[i] as i64` to `nums[i]`,
both lossless since `left` is an `i64` either way, `struct Solution;`
to `struct Solution {}`, `Solution::` to `Solution.`, and the adapter's
`as i64` dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every place to cut, the left part and the right part
each summed afresh by a loop, and the cut counted when the left is no
smaller. No running sum and no total. It checks 300 random arrays of 2
to 12 values within 1, 3, 10 or 10^5 of 0; then 30 of one value
repeated; then 30 that rise or fall by a step. All 360 are drawn before
any arm answers.

| | property |
|---|---|
| P1 | the count is the literal reading's |
| P2 | the array reversed and every value negated: the same count |
| P3 | every value times 3: the same count |
| P4 | at least 0 and at most the number of cuts, `n - 1` |
| P5 | a 0 put at the end: the count, plus one when the whole sum is not negative |
| P6 | each arm agrees with at least three of the other five |

P2 holds because a cut in the turned array has the old right part,
negated, on its left, so `-right >= -left` is the old test. P5 holds
because the 0 leaves every old cut's sums as they were and adds one
cut, the whole array against nothing.

The differential prints `360 cases: checksum 966354574, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
compares `sum(nums[:cut])` with `sum(nums[cut:])`. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a tie not counted | P1 96, P5 32, P6 96 |
| M3 | ★: the first value never added | P1 220, P2 279, P5 63, P6 220 |
| M5 | ★: the total without the last value | P1 186, P2 242, P5 186, P6 186 |
| M7 | prefix: the sums never accumulated | P1 283, P2 306, P5 148, P6 283 |
| M8 | prefix: the cut one early | P1 266, P2 328, P5 78, P6 266 |
| M10 | prefix: the last cut missed | P1 166, P2 231, P5 78, P6 166 |
| M12 | two: the right never shrinks | P1 263, P2 303, P5 202, P6 263 |
| M15 | two: the right started at 0 | P1 262, P2 303, P6 262 |
| M16 | two: the left counted twice | P1 184, P2 260, P6 184 |
| M17 | struct: a left short by one valid | P1 57, P3 57, P5 21, P6 57 |
| M20 | struct: the value one ahead | P1 230, P2 198, P5 63, P6 230 |
| M21 | struct: the cut after the last value | P1 158, P2 328, P4 31, P6 158 |
| M24 | iter: the state never moved | P1 286, P2 285, P5 269, P6 286 |
| M25 | iter: the total halved | P1 26, P2 57, P3 26, P6 26 |
| M26 | iter: the scan from 1 | P1 117, P3 117, P5 36, P6 117 |
| M29 | solution: each cut counted twice | P1 333, P4 181, P5 158, P6 333 |
| M31 | solution: the values taken off | P1 324, P2 320, P5 328, P6 324 |

P1 and P6 kill all seventeen, P2 thirteen, P5 thirteen, P3 three, and
P4 two. P2 catches every edit that treats the two ends differently,
which is most of them: only a tie not counted, a left short by one,
twice the count and a scan from 1 pass it. P3 catches the three edits
that add a constant beside the sums, a left short by one, the scan from
1 and the total halved, whose rounding the tripled values move. P4
catches the counts out of range: a cut after the last value and each
cut counted twice. A tie not counted is wrong in only 96 cases, where
some cut balances exactly.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Twelve fail as a kept one does: the ★ arm's cut
after the last value and the iter arm's every value taken (M2, M22) as
the struct arm's (M21); the ★ arm's and the iter arm's left against the
whole and the struct arm's right never shrinking (M4, M23, M19) as the
two arm's right never shrinking (M12); the ★ and two arms' value one
ahead (M6, M13) as the struct arm's (M20); the prefix arm's last value
left out of the right (M9) as the ★ arm's total without it (M5); the
two arm's and the template's tie not counted (M14, M28) as the ★ arm's
(M1); the struct arm's right started at 0 (M18) as the two arm's
(M15); and the template's first value never added (M30) as the ★ arm's
(M3). Two fail in ways of their own and are left out because their
arms keep enough: the prefix arm's left no larger (M11) and the
template's total without the first value (M27).

Two edits of the first draft were replaced. The two arm's tie not
counted, `if left >= right {`, matched the literal reading's line too,
so its anchor took the line before it. The iter arm's state made the
value, `Some((x, left))`, was refused by the type checker, since `x`
is a `ref i64` from `iter()` where the state is an `i64`; it is now the
state never moved, M24.

## Verification

Every arm prints the same output as `split.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the differential takes 0.4 s, the ★ arm 0.5 s,
the two arm 0.6 s, the prefix and struct arms 0.6 s, the template 1.1
s, and the iter arm 1.2 s.

## Benchmarks

The bench answers 100 arrays of the constraints' longest, 10^5 values
from -10^5 to 10^5, with the ★ arm in all five languages. Every
implementation prints `100 arrays of 10^5: checksum 880717614`. Each
builds its array a value at a time from the same generator.

BENCHTAB
