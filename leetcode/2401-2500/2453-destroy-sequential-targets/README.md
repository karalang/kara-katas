# 2453. Destroy Sequential Targets

You are given a **0-indexed** array `nums` consisting of positive
integers, representing targets on a number line. You are also given an
integer `space`.

You have a machine which can destroy targets. **Seeding** the machine
with some `nums[i]` allows it to destroy all targets with values that
can be represented as `nums[i] + c * space`, where `c` is any
non-negative integer. You want to destroy the **maximum** number of
targets in `nums`.

Return *the **minimum value** of* `nums[i]` *you can seed the machine
with to destroy the maximum number of targets.*

```
nums = [3,7,8,1,1,5], space = 2  ->  1
nums = [1,3,5,2,4,6], space = 2  ->  1
nums = [6,2,5], space = 100      ->  2
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^9`;
`1 <= space <= 10^9`.

A seed destroys the targets at or above it whose distance from it is a
multiple of `space`, which are the targets above it with the same
remainder modulo `space`. The least value of a remainder class destroys
the whole class, and no seed destroys more than its class, so the
answer is the least value of a largest class, the least such value when
classes tie.

## Approaches

| file | mechanism |
|---|---|
| `targets.kara` ★ | a `Map` counts each remainder class, and a second pass over the values keeps the least value of a largest class. O(n) |
| `targets_naive.kara` | the statement read directly: every value tried as the seed and the targets it destroys counted, those at or above it a multiple of `space` away; the most kept, the least seed on a tie. O(n^2) |
| `targets_sort.kara` | sorting: the values as `(remainder, value)` pairs sorted, so each class is a run whose first value is its least; the longest run wins, and on a tie the run with the least first value. O(n log n) |
| `targets_least.kara` | one pass: a `Map` from each remainder to its class's size and least value, updated by `match` on `get` as each value arrives; then the classes compared by size, and by least value on a tie. O(n) |
| `targets_iter.kara` | iterators: the class sizes counted by `fold` into a `Map`, the largest found by `map` and `max`, and the answer the `min` of the values whose class is that size, picked out by `filter`. O(n) |
| `targets_solution.kara` | LeetCode's Rust template: a `HashMap` filled by `*count.entry(n % space).or_insert(0) += 1` over `&nums`, then the values walked again, each count read by `count[&(n % space)]`, the answer started at `i32::MAX`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's three examples; one
value; space 1, one class; a space larger than every gap, each value
its own class; two classes of three
tied, the answer the lesser of their least values; then 2000 random values up to `10^9` against spaces 1, 7,
1000 and `10^9`, and 2000 values up to 50 against space 3; and 3000
random arrays of 1 to 8 values up to 20, space 1 to 6, as a checksum.
`targets.py` mirrors the ★ arm and its output is byte-identical, and
the mirror was checked on 50000 random arrays of up to 9 values up to
30, space up to 12, against every seed's targets counted directly. The
random arrays stop at 2000 values, not the constraints' `10^5`, because
the naive arm is quadratic; the bench takes `10^5`.

`check` first reports 13 errors on the template, and `karac fix`
carries it in one call, reporting 17 edits: `use
std::collections::HashMap;` deleted, since `Map` is in the prelude; the
angle brackets of `Vec<i32>` and `HashMap<i32, i32>` made square;
`HashMap::new` and `i32::MAX` written with `.`; the `&` of each `for &n`
pattern dropped and each `&nums` written `ref nums`; the `&` of the
index `count[&(..)]` dropped; `||` and `&&` written `or` and `and`;
`struct Solution;` given its braces; and, once the template parses,
both `HashMap` names written `Map`. `*count.entry(..).or_insert(0) +=
1`, the parenthesised index and `i32.MAX` stand as Kāra. The values fit
an `i32`, as LeetCode's signature has them; the other arms take `i64`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each value tried as the seed, the machine stepped from it by
`space` up to the largest value, and at each step every value standing
there counted as destroyed; the most destroyed kept, the least seed on
a tie. No remainder is taken. It checks 300 random arrays of 1 to 10
values up to 60, space 1 to 8; then 30 of up to 30 values up to `5 *
10^8`, space `10^8` to `5 * 10^8`, so the walk stays short; then 30 of
up to 30 values up to 10, space 1 to 3, full of repeats. All 360 are
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the values in reverse order: the same answer |
| P3 | every value raised by `space`: the answer plus `space` |
| P4 | every value and `space` doubled: the answer doubled |
| P5 | the answer put in once more: the same answer |
| P6 | each arm agrees with at least three of the other five |

P2 holds because the answer depends on the values and not their order.
P3 holds because raising every value by `space` keeps every class and
moves each value up by the same amount, and P4 because doubling both
doubles each distance and the step alike. P5 holds because the answer's
class grows by one and is then the only largest. The second group keeps
its values and spaces at `5 * 10^8` or below so that P3 and P4 stay
within the constraints' `10^9`.

The differential prints `360 cases: checksum 733806165, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and walks the same steps. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the greatest on a tie | P1 318, P6 318 |
| M2 | ★: the last of a largest class kept | P1 213, P2 301, P6 213 |
| M6 | ★: a class two larger needed to win | P1 125, P2 30, P3 108, P5 38, P6 125 |
| M7 | naive: the seed itself never destroyed | P1 120, P3 113, P6 120 |
| M8 | naive: one beyond each step destroyed | P1 64, P4 64, P6 64 |
| M11 | naive: the targets below the seed | P1 247, P6 247 |
| M12 | sort: never sorted | P1 170, P2 190, P5 20, P6 170 |
| M15 | sort: the last of the longest runs | P1 80, P6 80 |
| M16 | sort: a value skipped after each run | P1 128, P6 128 |
| M18 | least: the last value kept | P1 149, P2 232, P6 149 |
| M19 | least: two classes merged | P1 68, P4 68, P6 68 |
| M21 | least: each class's least started at 0 | P1 360, P3 360, P6 360 |
| M22 | iter: the smallest class | P1 193, P5 212, P6 193 |
| M24 | iter: classes one short admitted | P1 52, P6 52 |
| M26 | iter: the first of the largest class | P1 227, P2 301, P6 227 |
| M29 | solution: odd values counted twice | P1 62, P3 37, P4 62, P6 62 |
| M31 | solution: space one larger | P1 127, P4 140, P6 127 |

P1 and P6 kill all seventeen, P2 five, P3 and P4 four each, and P5
three.

Fourteen are not kept. Five fail exactly as a kept one: the sort arm's
run's greatest and the least arm's greatest kept (M14, M17) as the
naive arm's targets below the seed (M11), all three answering the
greatest value of a largest class; the iter arm's greatest of the
largest class and the template's greatest on a tie (M23, M28) as the ★
arm's (M1); and the template's last of a largest class kept (M27) as
the ★ arm's (M2). Nine fail apart from every kept one and were left out
because those arms keep their share already: the ★ arm's most started
at 1, first value never tried and each class weighed by its values (M3,
M4, M5); the naive arm's odd seeds one ahead and first target never
counted (M9, M10); the sort arm's runs of equal values (M13); the least
arm's greatest on a tie (M20), which takes the greatest of the tied
classes' least values rather than the greatest value; the iter arm's
first value's class taken as the largest (M25); and the template's
counts halved (M30).

## Verification

Every arm prints the same output as `targets.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.2 to 0.3 s, but for the naive
arm, which counts every pair of 2000 values on five of its lines: it
takes 3.5 s there, 1.1 s under `karac __mir-llvm-asan` and 0.3 s under
`karac run`. The differential takes 0.7 s under `karac __mir-run`, 0.6 s
under `karac __mir-llvm-asan` and 0.5 s under `karac run`.

## Benchmarks

The bench builds 10 arrays of `10^5` values up to `10^9`, the
constraints' largest, once from its own generator. It then makes 50
passes; each sets one value of every array to one more than the
checksum so far, so no answer carries over, then answers every array
with a space from 1 to `10^5` that changes with the pass and the array,
folding the answer plus the pass into the checksum. The bench uses the
★ arm, a count of each class and a second pass for the least value of
a largest, in all five languages. Every implementation prints `50
passes over 10 arrays of 10^5 values: checksum 13328410`. The count is
the language's own hash map: `Map` in Kāra, `HashMap` in Rust, `map` in
Go and `dict` in Python; C has none, and uses an open-addressing table
of `2^18` slots, cleared for every answer.

BENCHTAB
