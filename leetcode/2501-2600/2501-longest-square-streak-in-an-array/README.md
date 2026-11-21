# 2501. Longest Square Streak in an Array

You are given an integer array `nums`. A subsequence of `nums` is called
a **square streak** if:

- The length of the subsequence is at least `2`, and
- **after** sorting the subsequence, each element (except the first
  element) is the **square** of the previous number.

Return *the length of the **longest square streak** in* `nums`*, or
return* `-1` *if there is no **square streak**.*

A **subsequence** is an array that can be derived from another array by
deleting some or no elements without changing the order of the remaining
elements.

```
nums = [4,3,6,16,8,2]  ->  3
nums = [2,3,5,6,7]     ->  -1
```

**Constraints:** `2 <= nums.length <= 10^5`; `2 <= nums[i] <= 10^5`.

Sorting makes the order of the places irrelevant, and a streak cannot
use a value twice, since no value above 1 is its own square: a streak
is a chain of distinct values `v, v^2, v^4, ...`, all present. Each
value belongs to one chain at most, the one through its square root, so
the answer is the longest chain of present values, which is at most 5
long (`2, 4, 16, 256, 65536`) under the constraints. The approaches
differ in where a chain is started and how its length is kept.

## Approaches

| file | mechanism |
|---|---|
| `square.kara` ★ | the values in a `Set`; a chain is walked up through the squares from each value that is not a square of a present value. O(n) expected |
| `square_sort.kara` | the values sorted and deduplicated, then a `Map` from each value to the longest chain ending at it: one more than its square root's when that is present, else 1. O(n log n) |
| `square_table.kara` | the same chain lengths in a `Vec` over every value to `10^5`, filled upward. O(n + 10^5) |
| `square_rec.kara` | a recursion: the chain from `x` is 0 when `x` is absent, else one more than the chain from `x * x`; asked from every place, with no root skipped. O(n) expected, at most 5 deep |
| `square_iter.kara` | iterators: from every value in the `Set`, a `scan` of five squarings, `take_while` they are present, `count`ed, then the `max` |
| `square_solution.kara` | LeetCode's Rust template: `Vec<i32>` in, `i32` out; the values widened into a `HashSet<i64>`, and from every one a walk up through the squares; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's two examples and six
more; then 2000 random arrays of 2 to 40 values to 100, and 2000 drawn
from squares chains (a base 2 to 20 squared 0 to 3 times, kept to
`10^5`, or one time in four any value to `10^5`), each as a count of
those with no streak and a checksum; then the constraints' largest:
every value from 2 to `10^5`; `10^5` twos; `10^5` random values to
`10^5`; and `10^5` drawn from squares chains. `square.py` mirrors the ★
arm and its output is byte-identical, and the mirror was checked on 3000
random arrays of 2 to 10 values, most from a pool of chain members,
against a search over every subsequence, and the two agreed on every
array.

The iter arm's `scan` starts from `*v`. Written `scan(v, ...)`, with
`v` the `ref i64` that iterating the `Set` gives, `check` refuses it
with a bare E0200 "expected 'Option[(ref i64, _)]', found 'Option[(i64,
ref i64)]'": the state's type is taken from the seed as a `ref`, though
`let mut x = v` in the ★ arm copies the same `v` out to an `i64`, and
the message names neither the seed nor the `*v` that mends it. That
diagnostic gap is to be filed on the ledger once the kata rows' cap
allows.

`check` first reports 8 errors on the template, all Rust's spellings:
the `use std::collections::HashSet;` line, `struct Solution;`,
`Vec<i32>` and `HashSet<i64>` in angle brackets, the `&` patterns in
`|&x|` and `for &x`, the `&set` borrow, and the `&` in
`contains(&cur)`. `karac fix` carries it in one call, reporting 14
edits: the `use` line goes, since `Set` is in the prelude, and
`HashSet` becomes `Set`; `struct Solution {}`; the brackets; the `&`
patterns and the argument's `&` dropped; `for x in ref set`; `let mut
ans = -1` and `let mut len = 0` given `: i32`, which their `-1` and `0`
would otherwise not be beside the `i32` return; and the wrapper's
lossless `as i64` dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every subsequence of two or more places is gathered, sorted,
and kept when each value is the square of the one before; the answer
is the longest kept, -1 if none. No square root is taken. It checks 300
random arrays of 2 to 10 values, to 20 or drawn from squares chains of
a base 2 to 10; then 20 of two values, and 40 of 10, from the same
chains. All 360 are drawn before any arm answers, and 117 of them have
a streak.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | -1, or from 2 to the smaller of `n` and 5 |
| P3 | the values in the other order: the same answer |
| P4 | every value written twice: the same answer |
| P5 | the squares chain of the least value, up to `10^5`, added: the greater of the answer and that chain's length when it is 2 or more, else the same answer |
| P6 | each arm agrees with at least three of the other five |

P5 holds because the least value is the bottom of its chain, so the
added values form a chain of exactly their own length, which reaches as
high as the bound allows; any other streak meets none of them.

The differential prints `360 cases, 117 with a streak: checksum
846559183, 12960 checks over 6 arms: 0 failures` under every lane in
Verification; the checksum of the literal answers was checked against a
Python reading that builds the same cases and runs the same search. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a lone value a streak of 1 | P1 243, P2 243, P6 243 |
| M3 | ★: each value cubed | P1 125, P5 342, P6 125 |
| M6 | ★: a square never a start | P1 66, P5 117, P6 66 |
| M7 | sort: the values left unsorted | P1 55, P3 85, P4 55, P6 55 |
| M9 | sort: a missing root worth 1 | P1 242, P5 105, P6 242 |
| M10 | sort: the last value never asked | P1 7, P5 202, P6 7 |
| M12 | table: the table filled downward | P1 117, P5 342, P6 117 |
| M14 | table: a non-square begun at 0 | P1 50, P5 222, P6 50 |
| M16 | table: a streak of 2 refused | P1 93, P5 27, P6 93 |
| M19 | rec: the walk to the cube | P1 121, P5 342, P6 121 |
| M20 | rec: the first value only | P1 95, P3 44, P5 263, P6 95 |
| M21 | rec: values past 1000 absent | P1 45, P5 315, P6 45 |
| M22 | iter: two squarings only | P1 24, P5 315, P6 24 |
| M25 | iter: squares counted past a gap | P1 52, P6 52 |
| M26 | iter: squarings kept past 1000 | P1 198, P2 54, P5 99, P6 198 |
| M28 | solution: the walk stopped at 100 | P1 61, P5 342, P6 61 |
| M29 | solution: the walk counted from 1 | P1 360, P2 1, P5 321, P6 360 |

P1 and P6 kill all seventeen, P5 fourteen, P2 three, P3 two, and P4
one.

None of the first thirty-one edits survived, but three were replaced so
that the kept ones could all fail differently: the rec and iter arms'
least taken and the template's answer begun at 0 failed exactly as
other edits did, and the arms' other edits left no set of seventeen
with distinct failures. They became the rec arm's values past 1000
absent (M21), the iter arm's squarings kept past 1000 (M26), and the
template's walk stopped at 100 (M28).

Fourteen are not kept, and none survives. Seven fail exactly as the
table arm's table filled downward (M12), which answers -1 for every
array: the ★ arm's walk one short and shortest kept (M2, M5), the sort
arm's square not extended (M8), the table arm's root's entry not
extended and only the first value marked (M13, M15), the rec arm's
square never asked (M18), and the iter arm's value itself skipped
(M24). Three fail as the template's walk counted from 1 (M29), every
streak one longer and every lone value a streak: the ★ arm's length
begun at 1 (M4), the rec arm's absent value worth 1 (M17), and the iter
arm's count one more (M23). The template's lone value a streak (M27)
fails as the ★ arm's (M1), its walk to the cube (M30) as the rec arm's
(M19), and its walk stopped at two (M31) as the iter arm's two
squarings only (M22). The sort arm's answer one more (M11) fails in a
way of its own, but its arm already holds its kept edits.

## Verification

Every arm prints the same output as `square.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.3 to 4.5 s, but for the table arm, which fills its table of `10^5` entries on every ask and takes 73 s, and the differential 25.5 s; under `karac __mir-llvm-asan` the arms take 0.7 to 1.5 s, the table arm 18.8 s, and the differential 7.0 s; and under `karac run` the differential takes 0.7 s.

## Benchmarks

The bench builds 20 arrays of `10^5` values drawn from squares chains
once from its own generator, then makes 32 passes. Each pass, for every
array, sets the value at place `check % 10^5` to `(check + p) % 99999 +
2`, asks, and puts it back, folding the answer plus 1 plus the pass into
the checksum. The bench uses the ★ arm in all five languages, each
building a fresh hash set of the values on every ask: Kāra's `Set`,
Rust's `HashSet`, Go's map, Python's `set`, and in C an open-addressed
table of `2^18` slots probed linearly. Every implementation prints `32
passes over 20 arrays of 10^5: checksum 475404371`.

BENCHTAB
